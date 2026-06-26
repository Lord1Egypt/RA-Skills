---
name: avito-pro
description: Работа с API Авито (Авторизация, Мессенджер, Объявления, Статистика). Позволяет получать токены, читать/отправлять сообщения в чатах Авито и управлять объявлениями.
---

# Avito API Skill

Этот навык предоставляет знания для взаимодействия с API Авито.

## Базовые URL
- **API**: `https://api.avito.ru`
- **OAuth (для получения кода)**: `https://avito.ru/oauth`
- **Документация**: `https://developers.avito.ru/`

## Авторизация (OAuth 2.0)

Авито поддерживает два типа авторизации:

### 1. Персональная авторизация (Client Credentials)
Используется для работы от своего имени (личный кабинет/бизнес-аккаунт).
- **Endpoint**: `POST /token`
- **Параметры (URL-encoded)**:
  - `grant_type`: `client_credentials`
  - `client_id`: Ваш Client ID (из личного кабинета)
  - `client_secret`: Ваш Client Secret
- **Срок действия**: 24 часа.

**Пример запроса**:
```bash
curl -X POST 'https://api.avito.ru/token' \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     --data-urlencode 'grant_type=client_credentials' \
     --data-urlencode 'client_id=<CLIENT_ID>' \
     --data-urlencode 'client_secret=<CLIENT_SECRET>'
```

### 2. Авторизация для приложений (Authorization Code)
Для работы с данными других пользователей.
- **Шаг 1**: Редирект пользователя на `https://avito.ru/oauth?response_type=code&client_id=<CLIENT_ID>&scope=<SCOPES>&state=<STATE>`.
- **Шаг 2**: Обмен `code` на токены через `POST /token` с `grant_type=authorization_code`.

## Мессенджер API (Messenger)

Методы для работы с чатами. Позволяют интегрировать Авито в CRM.

### Ключевые эндпоинты:
- **Список чатов**: `GET /messenger/v2/accounts/{user_id}/chats`
- **Сообщения в чате**: `GET /messenger/v3/accounts/{user_id}/chats/{chat_id}/messages`
- **Отправить сообщение**: `POST /messenger/v1/accounts/{user_id}/chats/{chat_id}/messages`
  - Тело: `{"message": {"text": "текст"}, "type": "text"}`
- **Отправить изображение**: `POST /messenger/v1/accounts/{user_id}/chats/{chat_id}/messages/image`
- **Загрузить изображение**: `POST /messenger/v1/accounts/{user_id}/uploadImages` (multipart/form-data)
- **Прочитать чат**: `POST /messenger/v1/accounts/{user_id}/chats/{chat_id}/read`
- **Голосовые сообщения**: `GET /messenger/v1/accounts/{user_id}/getVoiceFiles?voice_ids={ids}`

### Вебхуки (Webhooks):
- **Подписка**: `POST /messenger/v1/webhook`
- **Отписка**: `POST /messenger/v1/webhook/unsubscribe`

## Объявления и Статистика (Items & Stats)

- **Получение информации об объявлениях**: `GET /core/v1/items`
- **Статистика объявлений**: `POST /stats/v1/accounts/{user_id}/items`
- **Применение доп. услуг (VAS)**: `POST /vas/v1/accounts/{user_id}/vas`

## Доступные Scopes:
- `messenger:read`, `messenger:write`
- `items:info`, `items:apply_vas`
- `stats:read`
- `user:read`, `user_balance:read`, `user_operations:read`
- `autoload:reports`
- `job:cv`, `job:vacancy`, `job:write`

## Важные примечания:
1. Для работы API требуется один из платных тарифов («Базовый», «Расширенный» или «Максимальный»).
2. Все запросы должны содержать заголовок `Authorization: Bearer <ACCESS_TOKEN>`.
3. Сообщения от чат-ботов имеют `type: system` и `flow_id`.
