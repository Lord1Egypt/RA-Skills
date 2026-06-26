# DeBox API Reference

Complete API documentation for DeBox Community Management.

## Base URL

```
https://open.debox.pro/openapi
```

## Authentication

All requests require the `X-API-KEY` header:

```
X-API-KEY: your-api-key
```

Get your API key from https://developer.debox.pro

---

## Group Info

Get group information.

**Endpoint:** `GET /group/info`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| group_invite_url | string | Yes | Group invite URL (e.g., `https://m.debox.pro/group?id=fxi3hqo5`) |

**Example:**

```bash
curl -X GET -H "X-API-KEY: t2XAlEF6..." \
  "https://open.debox.pro/openapi/group/info?group_invite_url=https://m.debox.pro/group?id=fxi3hqo5"
```

**Response:**

```json
{
  "group_id": "fxi3hqo5",
  "name": "Group Name",
  "member_count": 1234,
  "description": "Group description",
  "creator_id": "abc123",
  "avatar": "https://...",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## Group Is Join

Check if a user has joined a group.

**Endpoint:** `GET /group/is_join`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| walletAddress | string | Yes | User's wallet address |
| url | string | Yes | Group invite URL |
| chain_id | number | No | Chain ID (default: 1) |

**Example:**

```bash
curl -X GET -H "X-API-KEY: t2XAlEF6..." \
  "https://open.debox.pro/openapi/group/is_join?walletAddress=0x2267...&url=https://m.debox.pro/group?id=fxi3hqo5"
```

**Response:**

```json
{
  "is_join": true,
  "join_time": "2024-01-01T00:00:00Z"
}
```

---

## User Info

Get user's profile information.

**Endpoint:** `GET /user/info`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| user_id | string | Yes | DeBox user ID |

**Example:**

```bash
curl -X GET -H "X-API-KEY: t2XAlEF6..." \
  "https://open.debox.pro/openapi/user/info?user_id=abc123"
```

**Response:**

```json
{
  "user_id": "abc123",
  "nickname": "Username",
  "avatar": "https://...",
  "wallet": "0x2267...",
  "bio": "User bio"
}
```

---

## Vote Info

Get user's voting statistics in a group.

**Endpoint:** `GET /vote/info`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| walletAddress | string | Yes | User's wallet address |
| group_id | string | Yes | Group ID |
| chain_id | number | No | Chain ID (default: 1) |

**Example:**

```bash
curl -X GET -H "X-API-KEY: t2XAlEF6..." \
  "https://open.debox.pro/openapi/vote/info?walletAddress=0x2267...&group_id=fxi3hqo5"
```

**Response:**

```json
{
  "count": 5,
  "votes": [
    {
      "vote_id": "xxx",
      "title": "Vote Title",
      "voted_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

## Lucky Draw Info

Get user's lottery/draw statistics in a group.

**Endpoint:** `GET /lucky_draw/info`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| walletAddress | string | Yes | User's wallet address |
| group_id | string | Yes | Group ID |
| chain_id | number | No | Chain ID (default: 1) |

**Example:**

```bash
curl -X GET -H "X-API-KEY: t2XAlEF6..." \
  "https://open.debox.pro/openapi/lucky_draw/info?walletAddress=0x2267...&group_id=fxi3hqo5"
```

**Response:**

```json
{
  "count": 3,
  "draws": [
    {
      "draw_id": "xxx",
      "prize": "Prize Name",
      "drawn_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

## Moment Praise Info

Get user's praise/like statistics.

**Endpoint:** `GET /moment/praise_info`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| wallet_address | string | Yes | User's wallet address |
| chain_id | number | No | Chain ID (default: 1) |

**Example:**

```bash
curl -X GET -H "X-API-KEY: t2XAlEF6..." \
  "https://open.debox.pro/openapi/moment/praise_info?wallet_address=0x2267...&chain_id=1"
```

**Response:**

```json
{
  "total_likes": 100,
  "likes_by_moment": [
    {
      "moment_id": "xxx",
      "likes": 25
    }
  ]
}
```

---

## Moment Give Praise

Check if a user has liked a specific moment.

**Endpoint:** `GET /moment/give_praise`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| wallet_address | string | Yes | User's wallet address |
| chain_id | number | Yes | Chain ID |
| moment_id | string | Yes | Moment ID |

---

## Moment Receive Praise

Get all likes for a specific moment.

**Endpoint:** `GET /moment/receive_praise`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| moment_id | string | Yes | Moment ID |

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or missing API key |
| 403 | Forbidden - No permission |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

---

## Rate Limits

- Default: 100 requests per minute
- Recommended: Add 200ms delay between batch requests

---

## Chain IDs

| Chain | ID |
|-------|-----|
| Ethereum | 1 |
| BSC | 56 |
| Polygon | 137 |
| Arbitrum | 42161 |
| Optimism | 10 |