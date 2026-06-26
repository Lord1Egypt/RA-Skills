# EngageLab OTP API Error Codes

## OTP Sending & Verification Errors

| Error Code | HTTP Code | Description |
|------------|-----------|-------------|
| 1000 | 500 | Internal error |
| 2001 | 401 | Authentication failed — invalid or missing token |
| 2002 | 401 | Authentication failed — token expired or disabled |
| 2004 | 403 | No permission to call this API |
| 3001 | 400 | Invalid request parameter format (not valid JSON) |
| 3002 | 400 | Invalid request parameters (do not meet requirements) |
| 3003 | 400 | Business validation failed — see `message` field for details. For verification: code expired or already verified |
| 3004 | 400 | Rate limit exceeded — cannot resend to the same template and target user within OTP validity period |
| 4001 | 400 | Resource not found (e.g., non-existent template or message ID) |
| 5001 | 400 | Sending failed (general/other) |
| 5011 | 400 | Invalid phone number format |
| 5012 | 400 | Destination unreachable |
| 5013 | 400 | Number added to blacklist |
| 5014 | 400 | Content does not comply with regulations |
| 5015 | 400 | Message intercepted/rejected |
| 5016 | 400 | Internal sending error |
| 5017 | 400 | No permission to send in China region |
| 5018 | 400 | Phone malfunction (powered off/suspended) |
| 5019 | 400 | User unsubscribed |
| 5020 | 400 | Number not registered/invalid number |

## Template API Errors

| Error Code | HTTP Code | Description |
|------------|-----------|-------------|
| 1000 | 500 | Internal error |
| 2001 | 401 | Authentication failed — incorrect token |
| 2002 | 401 | Authentication failed — token expired or disabled |
| 2004 | 403 | No permission to call this API |
| 3001 | 400 | Invalid request parameter format (not valid JSON) |
| 3002 | 400 | Invalid request parameters |
| 3003 | 400 | Business-level parameter error (e.g., missing channel config) |
| 4001 | 400 | Template does not exist |

## Error Response Format

All error responses follow this structure:

```json
{
  "code": 5001,
  "message": "sms send fail"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `code` | `int` | Error code from the tables above |
| `message` | `string` | Human-readable error details |
