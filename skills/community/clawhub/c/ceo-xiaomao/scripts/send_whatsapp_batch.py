#!/usr/bin/env python3
import sys, csv, time, os, requests
from datetime import datetime

SERVICE_URL = os.environ.get('GREEN_API_URL')
INSTANCE_ID = os.environ.get('GREEN_API_INSTANCE_ID')
SERVICE_CREDENTIAL = os.environ.get('GREEN_API_CREDENTIAL') or os.environ.get('SERVICE_CREDENTIAL')

if not all([SERVICE_URL, INSTANCE_ID, SERVICE_CREDENTIAL]):
    print('Missing GREEN_API_URL / GREEN_API_INSTANCE_ID / GREEN_API_CREDENTIAL')
    sys.exit(1)

def send_wa(phone, message):
    phone = phone.strip().replace('+', '').replace(' ', '')
    chat_id = f"{phone}@c.us"
    url = f"{SERVICE_URL}/waInstance{INSTANCE_ID}/sendMessage/{SERVICE_CREDENTIAL}"
    return requests.post(url, json={'chatId': chat_id, 'message': message}, timeout=30).json()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 send_whatsapp_batch.py <csv_file> [delay_seconds]')
        sys.exit(1)
    csv_file = sys.argv[1]
    delay = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    log_file = f"message_dispatch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    success = failed = 0
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) < 2:
                continue
            phone, message = row[0].strip(), row[1]
            result = send_wa(phone, message)
            if 'idMessage' in result:
                success += 1
                print(f"✅ {phone} {result['idMessage']}")
            else:
                failed += 1
                print(f"❌ {phone} {result}")
            with open(log_file, 'a', encoding='utf-8') as lf:
                lf.write(f"{phone},{result}\n")
            time.sleep(delay)
    print(f"Done: success {success} | fail {failed} | log {log_file}")
