---
name: coinmeta
description: Query cryptocurrency newsflashes. Trigger scenarios: crypto news, crypto flash, cryptocurrency news, market updates.
metadata:
  openclaw:
    emoji: "📰"
    primaryEnv: COINMETA_API_KEY
    requires:
      bins:
        - curl
      env:
        - COINMETA_API_KEY
    os:
      - darwin
      - linux
      - win32
    tags:
      - crypto
      - news
      - flash
    version: 1.0.0
---

# CoinMeta API

Query cryptocurrency newsflash data.

**Base URL**: `https://api.coinmeta.com`
**Auth**: Header `X-Api-Key: $COINMETA_API_KEY`
**Response format**: `{"code": 200, "data": [...], "msg": "success"}` — code 200 = success

---

## Newsflash List

**Endpoint:** `POST https://api.coinmeta.com/open/v1/newsflash/list`

**curl example:**
```bash
curl -s -X POST -H "Accept:*/*" \
  -H "X-Api-Key: ${COINMETA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"page":1,"size":10}' \
  "https://api.coinmeta.com/open/v1/newsflash/list"
```

**Request params:**
| Param | Type | Description |
|-------|------|-------------|
| page | int | Page number, default 1 |
| size | int | Page size, default 10 |

**Response fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | int | Newsflash ID |
| views | int | View count |
| title | string | Title |
| content | string | Content (HTML) |
| createdAt | int | Unix timestamp |

---

## Keyword Search

**Endpoint:** `POST https://www.coinmeta.com/open/v1/newsflash/search`

```bash
curl -s -X POST -H "Accept:*/*" \
  -H "X-Api-Key: ${COINMETA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"page":1,"size":10,"keyword":"btc"}' \
  "https://www.coinmeta.com/open/v1/newsflash/search"
```

**Request params:**
| Param | Type | Description |
|-------|------|-------------|
| page | int | Page number, default 1 |
| size | int | Page size, default 10 |
| keyword | string | Search keyword, required |

**Output format:**
```
📰 Crypto Newsflash · Page [N]

1. [Title]
   Views: [views] · [Time]
   [Summary...]

2. [Title]
   Views: [views] · [Time]
   [Summary...]
...
```

**Parsing rules:**
- `createdAt` is Unix timestamp, convert to readable time
- `content` contains HTML tags, strip tags to display plain text

---

## Article List

**Endpoint:** `POST https://api.coinmeta.com/open/v1/article/list`

**curl example:**
```bash
curl -s -X POST -H "Accept:*/*" \
  -H "X-Api-Key: ${COINMETA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"page":1,"size":10}' \
  "https://api.coinmeta.com/open/v1/article/list"
```

**Request params:**
| Param | Type | Description |
|-------|------|-------------|
| page | int | Page number, default 1 |
| size | int | Page size, default 10 |

**Response fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | int | Article ID |
| title | string | Title |
| summary | string | Summary |
| views | int | View count |
| createdAt | int | Unix timestamp |

---

## Article Search

**Endpoint:** `POST https://api.coinmeta.com/open/v1/article/search`

**curl example:**
```bash
curl -s -X POST -H "Accept:*/*" \
  -H "X-Api-Key: ${COINMETA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"page":1,"size":10,"keyword":"比特币"}' \
  "https://api.coinmeta.com/open/v1/article/search"
```

**Request params:**
| Param | Type | Description |
|-------|------|-------------|
| page | int | Page number, default 1 |
| size | int | Page size, default 10 |
| keyword | string | Search keyword, required |

**Response fields:** Same as Article List

---

## Error Handling

| code | msg | Description |
|------|-----|-------------|
| 401 | Missing API key | API key not set, set COINMETA_API_KEY environment variable |
| 401 | Invalid API key | API key invalid, please verify |
| 422 | Parameter error | Invalid request params, check page/size |
| != 200 | Other | Request failed, display msg content |
| network error | - | Prompt to retry |