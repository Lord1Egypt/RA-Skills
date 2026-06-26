# AgentMail.TO — Навык работы с агентскими почтами

Этот навык предоставляет инструменты для работы с сервисом [agentmail.to](https://agentmail.to) — платформой для создания и управления временными email адресами, предназначенными для агентов и автоматизированных систем.

## 📋 Содержание

- [Возможности](#возможности)
- [Быстрый старт](#быстрый-старт)
- [API документация](#api-документация)
- [Примеры использования](#примеры-использования)
- [Автоматизация](#автоматизация)

## Возможности

✅ Создание временных email адресов  
✅ Получение и чтение входящих писем  
✅ Поиск и фильтрация сообщений  
✅ Удаление ящиков  
✅ API интеграция для автоматизации  
✅ Поддержка browser-use для веб-интерфейса  

## Быстрый старт

### 1. Установка зависимостей

```bash
# Установить browser-use (для работы через браузер)
uv pip install browser-use[cli]
browser-use install
```

### 2. Получение API ключа

Зарегистрируйтесь на [agentmail.to](https://agentmail.to) и получите API ключ в настройках профиля.

```bash
export AGENTMAIL_API_KEY="your-api-key-here"
```

### 3. Первый запуск

Создайте временный email:

```bash
curl -X POST https://api.agentmail.to/v1/emails \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json"
```

## API документация

### Создание email адреса

**POST** `/v1/emails`

```bash
curl -X POST https://api.agentmail.to/v1/emails \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Ответ:
```json
{
  "id": "abc123",
  "email": "abc123@agentmail.to",
  "expires_at": "2026-03-17T14:00:00Z"
}
```

### Получение списка сообщений

**GET** `/v1/emails/{email_id}/messages`

```bash
curl -X GET https://api.agentmail.to/v1/emails/abc123/messages \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Ответ:
```json
{
  "messages": [
    {
      "id": "msg_123",
      "from": "sender@example.com",
      "subject": "Тема письма",
      "received_at": "2026-03-17T12:30:00Z"
    }
  ]
}
```

### Получение полного сообщения

**GET** `/v1/messages/{message_id}`

Включает тело письма и вложения.

### Удаление ящика

**DELETE** `/v1/emails/{email_id}`

Полностью удаляет адрес и все связанные сообщения.

## Примеры использования

### Регистрация на тестовом сайте

```bash
#!/bin/bash

# 1. Создаем временный email
EMAIL_DATA=$(curl -s -X POST https://api.agentmail.to/v1/emails \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY")

EMAIL=$(echo "$EMAIL_DATA" | jq -r '.email')
EMAIL_ID=$(echo "$EMAIL_DATA" | jq -r 'id')

echo "Используем временный email: $EMAIL"

# 2. Регистрируемся на сайте через браузер
browser-use open https://example.com/register
browser-use input "#email-field" "$EMAIL"
browser-use click ".submit-button"

# 3. Проверяем получение письма подтверждения
sleep 10
curl -s -X GET "https://api.agentmail.to/v1/emails/${EMAIL_ID}/messages" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY"
```

### Получение кода подтверждения

```bash
#!/bin/bash

EMAIL_ID="$1"
MAX_WAIT=300

for i in $(seq 1 $((MAX_WAIT / 10))); do
    MESSAGES=$(curl -s -X GET "https://api.agentmail.to/v1/emails/${EMAIL_ID}/messages" \
      -H "Authorization: Bearer $AGENTMAIL_API_KEY")
    
    if echo "$MESSAGES" | grep -q '"messages":\[\]'; then
        sleep 10
        continue
    fi
    
    MSG_ID=$(echo "$MESSAGES" | jq -r '.messages[0].id')
    CODE=$(curl -s -X GET "https://api.agentmail.to/v1/messages/${MSG_ID}" \
      -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
      | grep -oP '(?<=код: )\d{4,6}')
    
    if [ -n "$CODE" ]; then
        echo "Код подтверждения: $CODE"
        exit 0
    fi
    
    sleep 10
done

echo "❌ Код не получен"
exit 1
```

## Автоматизация

### Python клиент

Создайте файл `agentmail_client.py`:

```python
#!/usr/bin/env python3

import requests
import os

class AgentMailClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def create_email(self):
        response = requests.post(
            'https://api.agentmail.to/v1/emails',
            headers=self.headers
        )
        return response.json()
    
    def get_messages(self, email_id):
        response = requests.get(
            f'https://api.agentmail.to/v1/emails/{email_id}/messages',
            headers=self.headers
        )
        return response.json()

# Использование
client = AgentMailClient(os.getenv('AGENTMAIL_API_KEY'))
email_data = client.create_email()
print(f"Email: {email_data['email']}")
```

### Bash скрипт-обертка

Создайте файл `agentmail.sh`:

```bash
#!/bin/bash

API_KEY="${AGENTMAIL_API_KEY}"
BASE_URL="https://api.agentmail.to/v1"

create_email() {
    curl -s -X POST "${BASE_URL}/emails" \
      -H "Authorization: Bearer ${API_KEY}" | jq '.'
}

check_messages() {
    local email_id="$1"
    curl -s -X GET "${BASE_URL}/emails/${email_id}/messages" \
      -H "Authorization: Bearer ${API_KEY}" | jq '.'
}

case "$1" in
    create) create_email ;;
    check) check_messages "$2" ;;
    *) echo "Использование: $0 {create|check <email_id>}" ;;
esac
```

## Безопасность

⚠️ **Важные рекомендации:**

- Не используйте временные ящики для конфиденциальных данных
- Храните API ключи в переменных окружения, не в коде
- Регулярно удаляйте неиспользуемые ящики
- Временные адреса имеют ограниченный срок действия

## Дополнительная информация

- [Официальная документация](https://agentmail.to/docs)
- [Веб-интерфейс](https://agentmail.to)
- [Поддержка](mailto:support@agentmail.to)

---

*Этот навык является частью OpenClaw workspace и может быть использован для автоматизации задач, требующих временных email адресов.*
