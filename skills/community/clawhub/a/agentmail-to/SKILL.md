# SKILL.md - agentmail-to

Работа с сервисом agentmail.to для управления агентскими почтами. Используйте для создания, чтения, отправки и управления временными/агентскими email адресами через API или веб-интерфейс.

## Конфигурация

API ключ хранится в: `/home/pit/.openclaw/workspace/scripts/.env.agentmail`

### Переменные окружения

```bash
AGENTMAIL_API_KEY=am_us_9c78f14e6adbd64bae61ad49513bd13d7e0c3b7ff9002a6b8651c58b386165fc
AGENTMAIL_INBOX=swaudiobrain@agentmail.to
```

## Команды

### Проверить почту (список сообщений)

```bash
python3 /home/pit/.openclaw/workspace/scripts/swaudiobot_smart_reply.py --check-inbox
```

### Отправить ответ

```bash
python3 /home/pit/.openclaw/workspace/scripts/swaudiobot_smart_reply.py --send-reply <inbox_id> <to> <subject> <text>
```

### Создать новый ящик

```bash
python3 /home/pit/.openclaw/workspace/scripts/create_clean_inbox.py
```

## Скрипты

- `swaudiobot_smart_reply.py` — Умная обработка писем с эскалацией
- `agentmail_client.py` — Базовый клиент для работы с API
- `clear_agentmail.py` — Очистка ящика от старых сообщений
- `create_clean_inbox.py` — Создание нового чистого ящика

## Веб-интерфейс

Консоль: https://console.agentmail.to  
Документация: https://docs.agentmail.to/quickstart
