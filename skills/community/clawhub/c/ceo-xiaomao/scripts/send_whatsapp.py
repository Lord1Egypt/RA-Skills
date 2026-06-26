#!/usr/bin/env python3
import os, sys, requests

SERVICE_URL = os.environ.get('GREEN_API_URL')
INSTANCE_ID = os.environ.get('GREEN_API_INSTANCE_ID')
SERVICE_CREDENTIAL = os.environ.get('GREEN_API_CREDENTIAL') or os.environ.get('SERVICE_CREDENTIAL')

if not all([SERVICE_URL, INSTANCE_ID, SERVICE_CREDENTIAL]):
    print('Missing GREEN_API_URL / GREEN_API_INSTANCE_ID / GREEN_API_CREDENTIAL')
    sys.exit(1)

def send_message(phone, message):
    phone = phone.strip().replace('+', '').replace(' ', '')
    chat_id = f"{phone}@c.us"
    url = f"{SERVICE_URL}/waInstance{INSTANCE_ID}/sendMessage/{SERVICE_CREDENTIAL}"
    response = requests.post(url, json={'chatId': chat_id, 'message': message}, timeout=30)
    result = response.json()
    return ('idMessage' in result), result

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python3 send_whatsapp.py <phone> <message>')
        sys.exit(1)
    ok, result = send_message(sys.argv[1], sys.argv[2])
    print(f"✅ Sent: {result['idMessage']}" if ok else f"❌ Failed: {result}")
