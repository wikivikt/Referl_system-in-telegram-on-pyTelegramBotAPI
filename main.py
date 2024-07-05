#Импортируем библиотеки для работы с BotAPI и базами данных 

import telebot 
import sqlite3


bot = telebot.TeleBot("") #Подключаем API бота
nick_bot = ''

#Обрабатываем команду start
@bot.message_handler(commands = ['start'])
def start(message):
        start_com = message.text #Берем текст, который был написан при вызове команды или переходе по ссылке
        user_id = message.from_user.id #В переменную user_id помещаем id пользователя
        bot.send_message(message.chat.id, 'Привет, сейчас я тебя зарегестрирую и дам тебе твою реферальную ссылку') #Отправляем сообщение и реферальную ссылку
        bot.send_message(message.chat.id, f'http://t.me/{nick_bot}?start={message.from_user.id}') 
        #Проверяем способ входа пользователя
        if start_com == '/start':
            refer_id = 'None'
        else:
            refer_id = str(start_com[7:]) #Оставляем только id пользователя, который отправил ссылку
            #Отправляем пользователю, что по его ссылке кто-то перешел, использую try или except на случай если отправитель ссылки уже не пользуется ботом и удалил его
            try:     
                bot.send_message(refer_id, 'По твоей ссылке перешел новый пользователь!')
            except:
                pass
        #Регестрируем пользователя или проверяем его на наличие в БД
        try:
            #Cоздаем БД и добавляем данные пользователя
            conn = sqlite3.connect('Referalka.sql')
            cur = conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS Referalka (id int primary key, Referal int)')
            cur.execute('INSERT INTO Referalka (id, Referal) VALUES (?, ?)', (user_id, refer_id))
            cur.execute('SELECT id FROM Referalka')
            conn.commit()
            cur.close()
        except:
              bot.send_message(message.chat.id, 'Ты уже зарегестрирован')

#Обрабатываем команду number_of_referrals, с помощью которой можно узнать сколько человек перешло по его ссылке 
@bot.message_handler(commands = ['number_of_referrals'])
def get(message):
        user_id = message.from_user.id
        refer_id = int(user_id)
        #Подключаемся к БД
        conn = sqlite3.connect('Referalka.sql')
        cur = conn.cursor()
        cur.execute('SELECT Referal FROM Referalka WHERE Referal = (?)', (refer_id,)) #Выбираем нужные данные
        conn.commit()
        quantity = cur.fetchall() #Извлекаем данные из БД, нам они выводятся ввиде списка
        cur.close()
        quantity = int(len(quantity)) #Получаем количество значений списка и это количество равняется количеству перешедших
        bot.send_message(message.chat.id, f'По вашей ссылке перешло {quantity} человек')
    
   

#Зацикливаем программу
bot.infinity_polling()

'''
Код написан 05.07.2024
Автор: Петров Дмитрий Сергеевич

'''