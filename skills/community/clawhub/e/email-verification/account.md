# Account API

Get account information: credits balance and per-endpoint rate limits.

## Endpoint

```
GET https://api.bounceban.com/v1/account
```

No parameters.

### Example request

```bash
curl "https://api.bounceban.com/v1/account" \
  -H "Authorization: YOUR_API_KEY"
```

### Example response (200)

```json
{
  "owner_email": "dev@bounceban.com",
  "available_credits": 375215,
  "rate_limit": [
    { "api": "/verify/single", "limit": "25 per second" },
    { "api": "/verify/single/status", "limit": "25 per second" },
    { "api": "/verify/bulk", "limit": "3 per second" },
    { "api": "/verify/bulk/status", "limit": "25 per second" },
    { "api": "/verify/bulk/export", "limit": "25 per second" },
    { "api": "/verify/bulk/dump", "limit": "25 per second" },
    { "api": "/account", "limit": "5 per second" }
  ]
}
```

### Response fields

| Field | Type | Description |
| --- | --- | --- |
| `owner_email` | string | Account owner's email. |
| `available_credits` | float | Credits remaining. `-1` means unlimited (custom plans only). |
| `rate_limit` | array | Per-endpoint rate limits (`api`, `limit`). |

Need a higher rate limit? Fill out https://forms.gle/3De4UMZKpxPiPv5M8 or email dev@bounceban.com.

### Error responses

| HTTP status | Meaning |
| --- | --- |
| `401` | Authorization missing or invalid. |
| `405` | Account blocked. |
| `429` | Rate limited. |
| `500` | Unexpected error. |
