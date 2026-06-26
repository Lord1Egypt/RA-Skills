# Finam Trade-API REST

API для торговых операций

**Server:** https://api.finam.ru

---

## AccountsService

- [GET /v1/accounts/{accountId}](#получение-информации-по-конкретному-аккаунту)
- [GET /v1/accounts/{accountId}/trades](#получение-истории-по-сделкам-аккаунта)
- [GET /v1/accounts/{accountId}/transactions](#получение-списка-транзакций-аккаунта)

---

### Получение информации по конкретному аккаунту

`GET /v1/accounts/{accountId}`

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| accountId | string | yes | Идентификатор аккаунта |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/accounts/{accountId}' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "accountId": "string",
  "type": "string",
  "status": "string",
  "equity": {
    "value": "string"
  },
  "unrealizedProfit": {
    "value": "string"
  },
  "positions": [
    {
      "symbol": "string",
      "quantity": {
        "value": "string"
      },
      "averagePrice": {
        "value": "string"
      },
      "currentPrice": {
        "value": "string"
      },
      "maintenanceMargin": {
        "value": "string"
      },
      "dailyPnl": {
        "value": "string"
      },
      "unrealizedPnl": {
        "value": "string"
      }
    }
  ],
  "cash": [
    {
      "currencyCode": "string",
      "units": "string",
      "nanos": 1
    }
  ],
  "portfolioMc": {
    "availableCash": {
      "value": "string"
    },
    "initialMargin": {
      "value": "string"
    },
    "maintenanceMargin": {
      "value": "string"
    }
  },
  "portfolioMct": {},
  "portfolioForts": {
    "availableCash": {
      "value": "string"
    },
    "moneyReserved": {
      "value": "string"
    }
  },
  "openAccountDate": "2026-03-27T13:09:52.291Z",
  "firstTradeDate": "2026-03-27T13:09:52.291Z",
  "firstNonTradeDate": "2026-03-27T13:09:52.291Z"
}
```

---

### Получение истории по сделкам аккаунта

`GET /v1/accounts/{accountId}/trades`

Параметры:
- `accountId` — передается в URL пути
- `limit` и `interval` — передаются как query-параметры

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| accountId | string | yes | Идентификатор аккаунта |

**Query Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| limit | integer (int32) | no | Лимит количества сделок |
| interval.start_time | string (date-time) | no | Inclusive start of the interval. If specified, a Timestamp matching this interval will have to be the same or after the start. |
| interval.end_time | string (date-time) | no | Exclusive end of the interval. If specified, a Timestamp matching this interval will have to be before the end. |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 400 | Неверно передан интервал |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/accounts/{accountId}/trades?limit=1&interval.start_time=&interval.end_time=' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "trades": [
    {
      "tradeId": "string",
      "symbol": "string",
      "price": {
        "value": "string"
      },
      "size": {
        "value": "string"
      },
      "side": "SIDE_UNSPECIFIED",
      "timestamp": "2026-03-27T13:09:52.291Z",
      "orderId": "string",
      "accountId": "string",
      "comment": "string"
    }
  ]
}
```

---

### Получение списка транзакций аккаунта

`GET /v1/accounts/{accountId}/transactions`

Параметры:
- `accountId` — передается в URL пути
- `limit` и `interval` — передаются как query-параметры

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| accountId | string | yes | Идентификатор аккаунта |

**Query Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| limit | integer (int32) | no | Лимит количества транзакций |
| interval.start_time | string (date-time) | no | Inclusive start of the interval. If specified, a Timestamp matching this interval will have to be the same or after the start. |
| interval.end_time | string (date-time) | no | Exclusive end of the interval. If specified, a Timestamp matching this interval will have to be before the end. |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 400 | Неверно передан интервал |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/accounts/{accountId}/transactions?limit=1&interval.start_time=&interval.end_time=' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "transactions": [
    {
      "id": "string",
      "category": "string",
      "timestamp": "2026-03-27T13:09:52.291Z",
      "symbol": "string",
      "change": {
        "currencyCode": "string",
        "units": "string",
        "nanos": 1
      },
      "trade": {
        "size": {
          "value": "string"
        },
        "price": {
          "value": "string"
        },
        "accruedInterest": {
          "value": "string"
        }
      },
      "transactionCategory": "OTHERS",
      "transactionName": "string",
      "changeQty": {
        "value": "string"
      }
    }
  ]
}
```

---

## AssetsService

- [GET /v1/assets](#получение-списка-доступных-инструментов-их-описание)
- [GET /v1/assets/all](#получение-списка-всех-инструментов-их-описание)
- [GET /v1/assets/clock](#получение-времени-на-сервере)
- [GET /v1/assets/{symbol}](#получение-информации-по-конкретному-инструменту)
- [GET /v1/assets/{symbol}/params](#получение-торговых-параметров-по-инструменту)
- [GET /v1/assets/{symbol}/schedule](#получение-расписания-торгов-для-инструмента)
- [GET /v1/assets/{underlyingSymbol}/options](#получение-цепочки-опционов-для-базового-актива)
- [GET /v1/exchanges](#получение-списка-доступных-бирж-названия-и-mic-коды)

---

### Получение списка доступных инструментов, их описание

`GET /v1/assets`

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl https://api.finam.ru/v1/assets \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "assets": [
    {
      "symbol": "string",
      "id": "string",
      "ticker": "string",
      "mic": "string",
      "isin": "string",
      "type": "string",
      "name": "string",
      "isArchived": true
    }
  ]
}
```

---

### Получение списка всех инструментов, их описание

`GET /v1/assets/all`

**Query Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| cursor | string (int64) | no | Курсор для пагинации. Указывает sec_id инструмента, с которого должен начинаться список. Для первого запроса оставьте поле пустым (значение 0). Для последующих запросов используйте значение next_cursor из предыдущего ответа. |
| only_active | boolean | no | Фильтрация по статусу инструмента: выбираются только активные (неархивные) инструменты. По умолчанию: false. |
| only_disabled | boolean | no | Фильтрация по статусу инструмента: выбираются только неактивные (архивные) инструменты. По умолчанию: false. |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/assets/all?cursor=&only_active=true&only_disabled=true' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "assets": [
    {
      "symbol": "string",
      "id": "string",
      "ticker": "string",
      "mic": "string",
      "isin": "string",
      "type": "string",
      "name": "string",
      "isArchived": true
    }
  ],
  "nextCursor": "string"
}
```

---

### Получение времени на сервере

`GET /v1/assets/clock`

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl https://api.finam.ru/v1/assets/clock \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "timestamp": "2026-03-27T13:09:52.291Z"
}
```

---

### Получение информации по конкретному инструменту

`GET /v1/assets/{symbol}`

Параметры:
- `symbol` — передается в URL пути
- `account_id` — передаётся как query-параметр

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| symbol | string | yes | Символ инструмента |

**Query Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| account_id | string | no | ID аккаунта для которого будет подбираться информация по инструменту |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 400 | Неверно передан символ или счет. Символ должен быть в виде ticker@mic. Где ticker — это, например, SBER. А mic, например, MISX |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/assets/{symbol}?account_id=' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "board": "string",
  "id": "string",
  "ticker": "string",
  "mic": "string",
  "isin": "string",
  "type": "string",
  "name": "string",
  "decimals": 1,
  "minStep": "string",
  "lotSize": {
    "value": "string"
  },
  "expirationDate": {
    "year": 1,
    "month": 1,
    "day": 1
  },
  "quoteCurrency": "string"
}
```

---

### Получение торговых параметров по инструменту

`GET /v1/assets/{symbol}/params`

Параметры:
- `symbol` — передается в URL пути
- `account_id` — передаётся как query-параметр

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| symbol | string | yes | Символ инструмента |

**Query Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| account_id | string | no | ID аккаунта для которого будут подбираться торговые параметры |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 400 | Неверно передан символ или счет. Символ должен быть в виде ticker@mic. Где ticker — это, например, SBER. А mic, например, MISX |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/assets/{symbol}/params?account_id=' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "symbol": "string",
  "accountId": "string",
  "tradeable": true,
  "longable": {
    "value": "NOT_AVAILABLE",
    "haltedDays": 1
  },
  "shortable": {
    "value": "NOT_AVAILABLE",
    "haltedDays": 1
  },
  "longRiskRate": {
    "value": "string"
  },
  "longCollateral": {
    "currencyCode": "string",
    "units": "string",
    "nanos": 1
  },
  "shortRiskRate": {
    "value": "string"
  },
  "shortCollateral": {
    "currencyCode": "string",
    "units": "string",
    "nanos": 1
  },
  "longInitialMargin": {
    "currencyCode": "string",
    "units": "string",
    "nanos": 1
  },
  "shortInitialMargin": {
    "currencyCode": "string",
    "units": "string",
    "nanos": 1
  },
  "isTradable": true,
  "priceType": "UNKNOWN"
}
```

---

### Получение расписания торгов для инструмента

`GET /v1/assets/{symbol}/schedule`

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| symbol | string | yes | Символ инструмента |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 400 | Неверно передан символ. Символ должен быть в виде ticker@mic. Где ticker — это, например, SBER. А mic, например, MISX |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/assets/{symbol}/schedule' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "symbol": "string",
  "sessions": [
    {
      "type": "string",
      "interval": {
        "startTime": "2026-03-27T13:09:52.291Z",
        "endTime": "2026-03-27T13:09:52.291Z"
      }
    }
  ]
}
```

---

### Получение цепочки опционов для базового актива

`GET /v1/assets/{underlyingSymbol}/options`

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| underlyingSymbol | string | yes | Символ базового актива опциона |

**Query Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| root | string | no | Опциональный параметр. Актуален для опционов на фьючерсы, по типу (недельные, месячные). Если параметр не указан, будут возвращены опционы с ближайшей датой экспирации. |
| expirationDate.year | integer (int32) | no | Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. |
| expirationDate.month | integer (int32) | no | Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. |
| expirationDate.day | integer (int32) | no | Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 400 | Неверно передан символ. Символ должен быть в виде ticker@mic. Где ticker — это, например, SBER. А mic, например, MISX |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/assets/{underlyingSymbol}/options?root=&expirationDate.year=1&expirationDate.month=1&expirationDate.day=1' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "symbol": "string",
  "options": [
    {
      "symbol": "string",
      "type": "TYPE_UNSPECIFIED",
      "contractSize": {
        "value": "string"
      },
      "tradeFirstDay": {
        "year": 1,
        "month": 1,
        "day": 1
      },
      "tradeLastDay": {
        "year": 1,
        "month": 1,
        "day": 1
      },
      "strike": {
        "value": "string"
      },
      "multiplier": {
        "value": "string"
      },
      "expirationFirstDay": {
        "year": 1,
        "month": 1,
        "day": 1
      },
      "expirationLastDay": {
        "year": 1,
        "month": 1,
        "day": 1
      }
    }
  ]
}
```

---

### Получение списка доступных бирж, названия и mic коды

`GET /v1/exchanges`

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl https://api.finam.ru/v1/exchanges \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "exchanges": [
    {
      "mic": "string",
      "name": "string"
    }
  ]
}
```

---

## AuthService

- [POST /v1/sessions](#получение-jwt-токена-из-api-токена)
- [POST /v1/sessions/details](#получение-информации-о-токене-сессии)

---

### Получение JWT токена из API токена

`POST /v1/sessions`

Все поля передаются в теле запроса.

**Body** (required, application/json)

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| secret | string | yes | API токен (secret key) |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl https://api.finam.ru/v1/sessions \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Authorization: YOUR_SECRET_TOKEN' \
  --data '{
  "secret": ""
}'
```

**Response Schema (200)**

```json
{
  "token": "string"
}
```

---

### Получение информации о токене сессии

`POST /v1/sessions/details`

Токен передается в теле запроса для безопасности. Получение информации о токене. Также включает список доступных счетов.

**Body** (required, application/json)

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| token | string | yes | JWT-токен |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl https://api.finam.ru/v1/sessions/details \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Authorization: YOUR_SECRET_TOKEN' \
  --data '{
  "token": ""
}'
```

**Response Schema (200)**

```json
{
  "createdAt": "2026-03-27T13:09:52.291Z",
  "expiresAt": "2026-03-27T13:09:52.291Z",
  "mdPermissions": [
    {
      "quoteLevel": "QUOTE_LEVEL_UNSPECIFIED",
      "delayMinutes": 1,
      "mic": "string",
      "country": "string",
      "continent": "string",
      "worldwide": true
    }
  ],
  "accountIds": [
    "string"
  ],
  "readonly": true
}
```

---

## MarketDataService

- [GET /v1/instruments/{symbol}/bars](#получение-исторических-данных-по-инструменту-агрегированные-свечи)
- [GET /v1/instruments/{symbol}/orderbook](#получение-текущего-стакана-по-инструменту)
- [GET /v1/instruments/{symbol}/quotes/latest](#получение-последней-котировки-по-инструменту)
- [GET /v1/instruments/{symbol}/trades/latest](#получение-списка-последних-сделок-по-инструменту)

---

### Получение исторических данных по инструменту (агрегированные свечи)

`GET /v1/instruments/{symbol}/bars`

Параметры:
- `symbol` — передается в URL пути
- `timeframe` и `interval` — передаются как query-параметры

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| symbol | string | yes | Символ инструмента |

**Query Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| timeframe | string (enum) | no | Необходимый таймфрейм. Значения: `TIME_FRAME_UNSPECIFIED` (не указан), `TIME_FRAME_M1` (1 мин, глубина 7 дней), `TIME_FRAME_M5` (5 мин, 30 дней), `TIME_FRAME_M15` (15 мин, 30 дней), `TIME_FRAME_M30` (30 мин, 30 дней), `TIME_FRAME_H1` (1 час, 30 дней), `TIME_FRAME_H2` (2 часа, 30 дней), `TIME_FRAME_H4` (4 часа, 30 дней), `TIME_FRAME_H8` (8 часов, 30 дней), `TIME_FRAME_D` (день, 365 дней), `TIME_FRAME_W` (неделя, 365*5 дней), `TIME_FRAME_MN` (месяц, 365*5 дней), `TIME_FRAME_QR` (квартал, 365*5 дней) |
| interval.start_time | string (date-time) | no | Inclusive start of the interval. If specified, a Timestamp matching this interval will have to be the same or after the start. |
| interval.end_time | string (date-time) | no | Exclusive end of the interval. If specified, a Timestamp matching this interval will have to be before the end. |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 400 | Неверно передан символ или интервал. Символ должен быть в виде ticker@mic. Где ticker — это, например, SBER. А mic, например, MISX |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/instruments/{symbol}/bars?timeframe=TIME_FRAME_UNSPECIFIED&interval.start_time=&interval.end_time=' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "symbol": "string",
  "bars": [
    {
      "timestamp": "2026-03-27T13:09:52.291Z",
      "open": {
        "value": "string"
      },
      "high": {
        "value": "string"
      },
      "low": {
        "value": "string"
      },
      "close": {
        "value": "string"
      },
      "volume": {
        "value": "string"
      }
    }
  ]
}
```

---

### Получение текущего стакана по инструменту

`GET /v1/instruments/{symbol}/orderbook`

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| symbol | string | yes | Символ инструмента |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/instruments/{symbol}/orderbook' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "symbol": "string",
  "orderbook": {
    "rows": [
      {
        "price": {
          "value": "string"
        },
        "sellSize": {
          "value": "string"
        },
        "buySize": {
          "value": "string"
        },
        "action": "ACTION_UNSPECIFIED",
        "mpid": "string",
        "timestamp": "2026-03-27T13:09:52.291Z"
      }
    ]
  }
}
```

---

### Получение последней котировки по инструменту

`GET /v1/instruments/{symbol}/quotes/latest`

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| symbol | string | yes | Символ инструмента |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/instruments/{symbol}/quotes/latest' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "symbol": "string",
  "quote": {
    "symbol": "string",
    "timestamp": "2026-03-27T13:09:52.291Z",
    "ask": {
      "value": "string"
    },
    "askSize": {
      "value": "string"
    },
    "bid": {
      "value": "string"
    },
    "bidSize": {
      "value": "string"
    },
    "last": {
      "value": "string"
    },
    "lastSize": {
      "value": "string"
    },
    "volume": {
      "value": "string"
    },
    "turnover": {
      "value": "string"
    },
    "open": {
      "value": "string"
    },
    "high": {
      "value": "string"
    },
    "low": {
      "value": "string"
    },
    "close": {
      "value": "string"
    },
    "change": {
      "value": "string"
    },
    "option": {
      "openInterest": {
        "value": "string"
      },
      "impliedVolatility": {
        "value": "string"
      },
      "theoreticalPrice": {
        "value": "string"
      },
      "delta": {
        "value": "string"
      },
      "gamma": {
        "value": "string"
      },
      "theta": {
        "value": "string"
      },
      "vega": {
        "value": "string"
      },
      "rho": {
        "value": "string"
      }
    }
  }
}
```

---

### Получение списка последних сделок по инструменту

`GET /v1/instruments/{symbol}/trades/latest`

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| symbol | string | yes | Символ инструмента |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/instruments/{symbol}/trades/latest' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "symbol": "string",
  "trades": [
    {
      "tradeId": "string",
      "mpid": "string",
      "timestamp": "2026-03-27T13:09:52.291Z",
      "price": {
        "value": "string"
      },
      "size": {
        "value": "string"
      },
      "side": "SIDE_UNSPECIFIED"
    }
  ]
}
```

---

## UsageMetricsService

- [GET /v1/usage](#получение-текущих-метрик-использования-для-пользователя)

---

### Получение текущих метрик использования для пользователя

`GET /v1/usage`

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl https://api.finam.ru/v1/usage \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "quotas": [
    {
      "name": "string",
      "limit": "string",
      "remaining": "string",
      "resetTime": "2026-03-27T13:09:52.291Z"
    }
  ]
}
```

---

## OrdersService

- [GET /v1/accounts/{accountId}/orders](#получение-списка-заявок-для-аккаунта)
- [POST /v1/accounts/{accountId}/orders](#выставление-биржевой-заявки)
- [GET /v1/accounts/{accountId}/orders/{orderId}](#получение-информации-о-конкретном-ордере)
- [DELETE /v1/accounts/{accountId}/orders/{orderId}](#отмена-биржевой-заявки)
- [POST /v1/accounts/{accountId}/sltp-orders](#выставление-sltp-заявки)

---

### Получение списка заявок для аккаунта

`GET /v1/accounts/{accountId}/orders`

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| accountId | string | yes | Идентификатор аккаунта |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/accounts/{accountId}/orders' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "orders": [
    {
      "orderId": "string",
      "execId": "string",
      "status": "ORDER_STATUS_UNSPECIFIED",
      "order": {
        "accountId": "string",
        "symbol": "string",
        "quantity": {
          "value": "string"
        },
        "side": "SIDE_UNSPECIFIED",
        "type": "ORDER_TYPE_UNSPECIFIED",
        "timeInForce": "TIME_IN_FORCE_UNSPECIFIED",
        "limitPrice": {
          "value": "string"
        },
        "stopPrice": {
          "value": "string"
        },
        "stopCondition": "STOP_CONDITION_UNSPECIFIED",
        "legs": [
          {
            "symbol": "string",
            "quantity": {
              "value": "string"
            },
            "side": "SIDE_UNSPECIFIED"
          }
        ],
        "clientOrderId": "string",
        "validBefore": "VALID_BEFORE_UNSPECIFIED",
        "comment": "string"
      },
      "transactAt": "2026-03-27T13:09:52.291Z",
      "acceptAt": "2026-03-27T13:09:52.291Z",
      "withdrawAt": "2026-03-27T13:09:52.291Z",
      "initialQuantity": {
        "value": "string"
      },
      "executedQuantity": {
        "value": "string"
      },
      "remainingQuantity": {
        "value": "string"
      },
      "sltpOrder": {
        "accountId": "string",
        "symbol": "string",
        "side": "SIDE_UNSPECIFIED",
        "quantitySl": {
          "value": "string"
        },
        "slPrice": {
          "value": "string"
        },
        "limitPrice": {
          "value": "string"
        },
        "quantityTp": {
          "value": "string"
        },
        "tpPrice": {
          "value": "string"
        },
        "tpGuardSpread": {
          "value": "string"
        },
        "tpSpreadMeasure": "TP_SPREAD_MEASURE_UNDEFINED",
        "clientOrderId": "string",
        "validBefore": "VALID_BEFORE_UNSPECIFIED",
        "validExpiryTime": "2026-03-27T13:09:52.291Z",
        "comment": "string"
      }
    }
  ]
}
```

---

### Выставление биржевой заявки

`POST /v1/accounts/{accountId}/orders`

Поле `accountId` берется из URL-пути, остальные поля передаются в теле запроса.

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| accountId | string | yes | Идентификатор аккаунта |

**Body** (required, application/json)

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| symbol | string | yes | Символ инструмента |
| quantity | object | yes | Количество (decimal value) |
| side | string (enum) | yes | Сторона сделки: `SIDE_UNSPECIFIED`, `SIDE_BUY` (покупка), `SIDE_SELL` (продажа) |
| type | string (enum) | yes | Тип заявки: `ORDER_TYPE_UNSPECIFIED`, `ORDER_TYPE_MARKET` (рыночная), `ORDER_TYPE_LIMIT` (лимитная), `ORDER_TYPE_STOP` (стоп рыночная), `ORDER_TYPE_STOP_LIMIT` (стоп лимитная), `ORDER_TYPE_MULTI_LEG` (мульти лег) |
| timeInForce | string (enum) | no | Срок действия: `TIME_IN_FORCE_UNSPECIFIED`, `TIME_IN_FORCE_DAY` (до конца дня), `TIME_IN_FORCE_GOOD_TILL_CANCEL` (до отмены), `TIME_IN_FORCE_GOOD_TILL_CROSSING` (до пересечения), `TIME_IN_FORCE_EXT` (внебиржевая), `TIME_IN_FORCE_ON_OPEN` (на открытии), `TIME_IN_FORCE_ON_CLOSE` (на закрытии), `TIME_IN_FORCE_IOC` (исполнить или отменить), `TIME_IN_FORCE_FOK` (исполнить полностью или отменить) |
| limitPrice | object | no | Лимитная цена (decimal value) |
| stopPrice | object | no | Стоп цена (decimal value) |
| stopCondition | string (enum) | no | Условие срабатывания стопа: `STOP_CONDITION_UNSPECIFIED`, `STOP_CONDITION_LAST_UP` (цена выше текущей), `STOP_CONDITION_LAST_DOWN` (цена ниже текущей) |
| legs | array | no | Ноги для мульти лег заявки |
| clientOrderId | string | no | Уникальный идентификатор заявки (максимум 20 символов). Автоматически генерируется, если не отправлен. |
| validBefore | string (enum) | no | Срок действия условной заявки: `VALID_BEFORE_UNSPECIFIED`, `VALID_BEFORE_END_OF_DAY` (до конца торгового дня), `VALID_BEFORE_GOOD_TILL_CANCEL` (до отмены), `VALID_BEFORE_GOOD_TILL_DATE` (до указанной даты-времени, только для SL/TP) |
| comment | string | no | Метка заявки (максимум 128 символов) |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 400 | Неверно переданы торговые параметры |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт или инструмент не были найдены |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/accounts/{accountId}/orders' \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Authorization: YOUR_SECRET_TOKEN' \
  --data '{
  "symbol": "",
  "quantity": {
    "value": ""
  },
  "side": "SIDE_UNSPECIFIED",
  "type": "ORDER_TYPE_UNSPECIFIED",
  "timeInForce": "TIME_IN_FORCE_UNSPECIFIED",
  "limitPrice": {
    "value": ""
  },
  "stopPrice": {
    "value": ""
  },
  "stopCondition": "STOP_CONDITION_UNSPECIFIED",
  "legs": [
    {
      "symbol": "",
      "quantity": {
        "value": ""
      },
      "side": "SIDE_UNSPECIFIED"
    }
  ],
  "clientOrderId": "",
  "validBefore": "VALID_BEFORE_UNSPECIFIED",
  "comment": ""
}'
```

**Response Schema (200)**

```json
{
  "orderId": "string",
  "execId": "string",
  "status": "ORDER_STATUS_UNSPECIFIED",
  "order": {
    "accountId": "string",
    "symbol": "string",
    "quantity": {
      "value": "string"
    },
    "side": "SIDE_UNSPECIFIED",
    "type": "ORDER_TYPE_UNSPECIFIED",
    "timeInForce": "TIME_IN_FORCE_UNSPECIFIED",
    "limitPrice": {
      "value": "string"
    },
    "stopPrice": {
      "value": "string"
    },
    "stopCondition": "STOP_CONDITION_UNSPECIFIED",
    "legs": [
      {
        "symbol": "string",
        "quantity": {
          "value": "string"
        },
        "side": "SIDE_UNSPECIFIED"
      }
    ],
    "clientOrderId": "string",
    "validBefore": "VALID_BEFORE_UNSPECIFIED",
    "comment": "string"
  },
  "transactAt": "2026-03-27T13:09:52.291Z",
  "acceptAt": "2026-03-27T13:09:52.291Z",
  "withdrawAt": "2026-03-27T13:09:52.291Z",
  "initialQuantity": {
    "value": "string"
  },
  "executedQuantity": {
    "value": "string"
  },
  "remainingQuantity": {
    "value": "string"
  },
  "sltpOrder": {
    "accountId": "string",
    "symbol": "string",
    "side": "SIDE_UNSPECIFIED",
    "quantitySl": {
      "value": "string"
    },
    "slPrice": {
      "value": "string"
    },
    "limitPrice": {
      "value": "string"
    },
    "quantityTp": {
      "value": "string"
    },
    "tpPrice": {
      "value": "string"
    },
    "tpGuardSpread": {
      "value": "string"
    },
    "tpSpreadMeasure": "TP_SPREAD_MEASURE_UNDEFINED",
    "clientOrderId": "string",
    "validBefore": "VALID_BEFORE_UNSPECIFIED",
    "validExpiryTime": "2026-03-27T13:09:52.291Z",
    "comment": "string"
  }
}
```

---

### Получение информации о конкретном ордере

`GET /v1/accounts/{accountId}/orders/{orderId}`

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| accountId | string | yes | Идентификатор аккаунта |
| orderId | string | yes | Идентификатор заявки |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт или заявка не были найдены |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/accounts/{accountId}/orders/{orderId}' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "orderId": "string",
  "execId": "string",
  "status": "ORDER_STATUS_UNSPECIFIED",
  "order": {
    "accountId": "string",
    "symbol": "string",
    "quantity": {
      "value": "string"
    },
    "side": "SIDE_UNSPECIFIED",
    "type": "ORDER_TYPE_UNSPECIFIED",
    "timeInForce": "TIME_IN_FORCE_UNSPECIFIED",
    "limitPrice": {
      "value": "string"
    },
    "stopPrice": {
      "value": "string"
    },
    "stopCondition": "STOP_CONDITION_UNSPECIFIED",
    "legs": [
      {
        "symbol": "string",
        "quantity": {
          "value": "string"
        },
        "side": "SIDE_UNSPECIFIED"
      }
    ],
    "clientOrderId": "string",
    "validBefore": "VALID_BEFORE_UNSPECIFIED",
    "comment": "string"
  },
  "transactAt": "2026-03-27T13:09:52.291Z",
  "acceptAt": "2026-03-27T13:09:52.291Z",
  "withdrawAt": "2026-03-27T13:09:52.291Z",
  "initialQuantity": {
    "value": "string"
  },
  "executedQuantity": {
    "value": "string"
  },
  "remainingQuantity": {
    "value": "string"
  },
  "sltpOrder": {
    "accountId": "string",
    "symbol": "string",
    "side": "SIDE_UNSPECIFIED",
    "quantitySl": {
      "value": "string"
    },
    "slPrice": {
      "value": "string"
    },
    "limitPrice": {
      "value": "string"
    },
    "quantityTp": {
      "value": "string"
    },
    "tpPrice": {
      "value": "string"
    },
    "tpGuardSpread": {
      "value": "string"
    },
    "tpSpreadMeasure": "TP_SPREAD_MEASURE_UNDEFINED",
    "clientOrderId": "string",
    "validBefore": "VALID_BEFORE_UNSPECIFIED",
    "validExpiryTime": "2026-03-27T13:09:52.291Z",
    "comment": "string"
  }
}
```

---

### Отмена биржевой заявки

`DELETE /v1/accounts/{accountId}/orders/{orderId}`

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| accountId | string | yes | Идентификатор аккаунта |
| orderId | string | yes | Идентификатор заявки |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 400 | Заявка не может быть отменена так как она уже исполнена |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт или заявка не были найдены |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/accounts/{accountId}/orders/{orderId}' \
  --request DELETE \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "orderId": "string",
  "execId": "string",
  "status": "ORDER_STATUS_UNSPECIFIED",
  "order": {
    "accountId": "string",
    "symbol": "string",
    "quantity": {
      "value": "string"
    },
    "side": "SIDE_UNSPECIFIED",
    "type": "ORDER_TYPE_UNSPECIFIED",
    "timeInForce": "TIME_IN_FORCE_UNSPECIFIED",
    "limitPrice": {
      "value": "string"
    },
    "stopPrice": {
      "value": "string"
    },
    "stopCondition": "STOP_CONDITION_UNSPECIFIED",
    "legs": [
      {
        "symbol": "string",
        "quantity": {
          "value": "string"
        },
        "side": "SIDE_UNSPECIFIED"
      }
    ],
    "clientOrderId": "string",
    "validBefore": "VALID_BEFORE_UNSPECIFIED",
    "comment": "string"
  },
  "transactAt": "2026-03-27T13:09:52.291Z",
  "acceptAt": "2026-03-27T13:09:52.291Z",
  "withdrawAt": "2026-03-27T13:09:52.291Z",
  "initialQuantity": {
    "value": "string"
  },
  "executedQuantity": {
    "value": "string"
  },
  "remainingQuantity": {
    "value": "string"
  },
  "sltpOrder": {
    "accountId": "string",
    "symbol": "string",
    "side": "SIDE_UNSPECIFIED",
    "quantitySl": {
      "value": "string"
    },
    "slPrice": {
      "value": "string"
    },
    "limitPrice": {
      "value": "string"
    },
    "quantityTp": {
      "value": "string"
    },
    "tpPrice": {
      "value": "string"
    },
    "tpGuardSpread": {
      "value": "string"
    },
    "tpSpreadMeasure": "TP_SPREAD_MEASURE_UNDEFINED",
    "clientOrderId": "string",
    "validBefore": "VALID_BEFORE_UNSPECIFIED",
    "validExpiryTime": "2026-03-27T13:09:52.291Z",
    "comment": "string"
  }
}
```

---

### Выставление SL/TP заявки

`POST /v1/accounts/{accountId}/sltp-orders`

Поле `accountId` берется из URL-пути, остальные поля передаются в теле запроса.

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| accountId | string | yes | Идентификатор аккаунта |

**Body** (required, application/json)

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| symbol | string | yes | Символ инструмента |
| side | string (enum) | yes | Сторона сделки: `SIDE_UNSPECIFIED`, `SIDE_BUY` (покупка), `SIDE_SELL` (продажа) |
| quantitySl | object | no | Количество для стоп-лосс (decimal value) |
| slPrice | object | no | Цена стоп-лосс (decimal value) |
| limitPrice | object | no | Лимитная цена (decimal value) |
| quantityTp | object | no | Количество для тейк-профит (decimal value) |
| tpPrice | object | no | Цена тейк-профит (decimal value) |
| tpGuardSpread | object | no | Величина защитного спреда для цены исполнения TP (decimal value) |
| tpSpreadMeasure | string (enum) | no | Единица измерения защитного спреда TP: `TP_SPREAD_MEASURE_UNDEFINED`, `TP_SPREAD_MEASURE_VALUE` (в единицах цены), `TP_SPREAD_MEASURE_PERCENT` (в процентах, до сотых) |
| clientOrderId | string | no | Уникальный идентификатор заявки (максимум 20 символов). Автоматически генерируется, если не отправлен. |
| validBefore | string (enum) | no | Срок действия: `VALID_BEFORE_UNSPECIFIED`, `VALID_BEFORE_END_OF_DAY` (до конца торгового дня), `VALID_BEFORE_GOOD_TILL_CANCEL` (до отмены), `VALID_BEFORE_GOOD_TILL_DATE` (до указанной даты-времени, только для SL/TP) |
| comment | string | no | Метка заявки (максимум 128 символов) |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 400 | Неверно переданы торговые параметры |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт или инструмент не были найдены |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/accounts/{accountId}/sltp-orders' \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Authorization: YOUR_SECRET_TOKEN' \
  --data '{
  "symbol": "",
  "side": "SIDE_UNSPECIFIED",
  "quantitySl": {
    "value": ""
  },
  "slPrice": {
    "value": ""
  },
  "limitPrice": {
    "value": ""
  },
  "quantityTp": {
    "value": ""
  },
  "tpPrice": {
    "value": ""
  },
  "tpGuardSpread": {
    "value": ""
  },
  "tpSpreadMeasure": "TP_SPREAD_MEASURE_UNDEFINED",
  "clientOrderId": "",
  "validBefore": "VALID_BEFORE_UNSPECIFIED",
  "validExpiryTime": "",
  "comment": ""
}'
```

**Response Schema (200)**

```json
{
  "orderId": "string",
  "execId": "string",
  "status": "ORDER_STATUS_UNSPECIFIED",
  "order": {
    "accountId": "string",
    "symbol": "string",
    "quantity": {
      "value": "string"
    },
    "side": "SIDE_UNSPECIFIED",
    "type": "ORDER_TYPE_UNSPECIFIED",
    "timeInForce": "TIME_IN_FORCE_UNSPECIFIED",
    "limitPrice": {
      "value": "string"
    },
    "stopPrice": {
      "value": "string"
    },
    "stopCondition": "STOP_CONDITION_UNSPECIFIED",
    "legs": [
      {
        "symbol": "string",
        "quantity": {
          "value": "string"
        },
        "side": "SIDE_UNSPECIFIED"
      }
    ],
    "clientOrderId": "string",
    "validBefore": "VALID_BEFORE_UNSPECIFIED",
    "comment": "string"
  },
  "transactAt": "2026-03-27T13:09:52.291Z",
  "acceptAt": "2026-03-27T13:09:52.291Z",
  "withdrawAt": "2026-03-27T13:09:52.291Z",
  "initialQuantity": {
    "value": "string"
  },
  "executedQuantity": {
    "value": "string"
  },
  "remainingQuantity": {
    "value": "string"
  },
  "sltpOrder": {
    "accountId": "string",
    "symbol": "string",
    "side": "SIDE_UNSPECIFIED",
    "quantitySl": {
      "value": "string"
    },
    "slPrice": {
      "value": "string"
    },
    "limitPrice": {
      "value": "string"
    },
    "quantityTp": {
      "value": "string"
    },
    "tpPrice": {
      "value": "string"
    },
    "tpGuardSpread": {
      "value": "string"
    },
    "tpSpreadMeasure": "TP_SPREAD_MEASURE_UNDEFINED",
    "clientOrderId": "string",
    "validBefore": "VALID_BEFORE_UNSPECIFIED",
    "validExpiryTime": "2026-03-27T13:09:52.291Z",
    "comment": "string"
  }
}
```

---

## ReportsService

- [POST /v1/report](#запустить-генерацию-отчета-по-счету-за-период)
- [GET /v1/report/{reportId}/info](#получение-информации-о-результате-генерации-отчета-по-счету)

---

### Запустить генерацию отчета по счету за период

`POST /v1/report`

**Body** (required, application/json)

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| accountId | string (int64) | yes | Идентификатор счета |
| dateRange | object | yes | Временной интервал |
| reportForm | string (enum) | no | Форма отчета: `REPORT_FORM_UNKNOWN` (не указана), `REPORT_FORM_SHORT` (краткая), `REPORT_FORM_LONG` (полная) |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl https://api.finam.ru/v1/report \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Authorization: YOUR_SECRET_TOKEN' \
  --data '{
  "dateRange": {
    "dateBegin": "",
    "dateEnd": ""
  },
  "reportForm": "REPORT_FORM_UNKNOWN",
  "accountId": ""
}'
```

**Response Schema (200)**

```json
{
  "reportId": "string"
}
```

---

### Получение информации о результате генерации отчета по счету

`GET /v1/report/{reportId}/info`

**Path Parameters**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| reportId | string | yes | Идентификатор отчёта |

**Responses**

| Code | Description |
| --- | --- |
| 200 | Успешный ответ |
| 401 | Срок действия токена истек или токен недействителен |
| 404 | Счёт не был найден в токене |
| 429 | Слишком много запросов. Доступный лимит - 200 запросов в минуту |
| 500 | Внутренняя ошибка сервиса. Попробуйте позже |
| 503 | Сервис на данный момент не доступен. Попробуйте позже |
| 504 | Крайний срок истек до завершения операции |
| default | Непредвиденная ошибка |

**Request Example**

```curl
curl 'https://api.finam.ru/v1/report/{reportId}/info' \
  --header 'Authorization: YOUR_SECRET_TOKEN'
```

**Response Schema (200)**

```json
{
  "info": {
    "reportId": "string",
    "status": "NOT_FOUND",
    "dateRange": {
      "dateBegin": "2026-03-27T13:09:52.291Z",
      "dateEnd": "2026-03-27T13:09:52.291Z"
    },
    "reportForm": "REPORT_FORM_UNKNOWN",
    "accountId": "string",
    "url": "string"
  }
}
```
