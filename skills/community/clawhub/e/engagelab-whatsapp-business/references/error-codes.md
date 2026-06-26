# EngageLab WhatsApp API Error Codes

## Messaging Errors

| Error Code | HTTP Code | Description |
|------------|-----------|-------------|
| 1000 | 500 | Internal error |
| 2001 | 401 | Authentication failed — invalid or missing token |
| 2002 | 401 | Authentication failed — token expired or disabled |
| 2003 | 400 | WhatsApp (Meta) authentication failed — contact EngageLab support |
| 2004 | 403 | No permission to call this API (check sending number permission for this API key) |
| 3001 | 400 | Invalid request parameter format (not valid JSON) |
| 3002 | 400 | Invalid request parameters (do not meet requirements) |
| 3003 | 400 | Business validation failed — see `message` field for details |
| 4001 | 400 | Resource not found (e.g., template does not exist) |

## Template API Errors

| Error Code | HTTP Code | Description |
|------------|-----------|-------------|
| 1000 | 500 | Internal error |
| 2001 | 401 | Authentication failed — invalid or missing token |
| 2002 | 401 | Authentication failed — token expired or disabled |
| 2003 | 400 | WhatsApp (Meta) authentication failed |
| 2004 | 403 | No permission to call this API |
| 3001 | 400 | Invalid request parameter format |
| 3002 | 400 | Invalid request parameters |
| 3003 | 400 | Business validation failed |
| 4001 | 400 | Template does not exist |
| 5002 | 400 | Template request failed at Meta — see `message` field for details |

## Error Response Format

```json
{
  "code": 3002,
  "message": "whatsapp.template field must be set correctly when type is template"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `code` | `int` | Error code from the tables above |
| `message` | `string` | Human-readable error details |
