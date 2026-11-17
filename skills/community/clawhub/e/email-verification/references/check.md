# Check API

Quickly check basic information about an email or domain **without SMTP verification**: domain type (work / free / disposable), username type (personal / role), and syntax validity. Useful for blocking disposable emails at sign-up or free emails on demo-request forms.

**Cost:** 1 credit per successful request from your **Check Plan** - a separate balance from verification credits. Check balances: https://bounceban.com/app/account/billing

## Endpoint

```
GET https://api.bounceban.com/v1/check
```

### Parameters (query)

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `email` | string | No* | Email to check. Takes precedence if both are provided. |
| `domain` | string | No* | Domain to check. |

*Provide at least one of `email` or `domain`.

### Example request

```bash
curl "https://api.bounceban.com/v1/check?email=sales@example.com" \
  -H "Authorization: YOUR_API_KEY"
```

### Example response (200)

```json
{
  "status": "success",
  "domain_type": "work",
  "username_type": "role",
  "syntax_valid": true,
  "credits_consumed": 1,
  "credits_remaining": 5
}
```

### Response fields

| Field | Type | Description |
| --- | --- | --- |
| `status` | string | `success` or `error` (on `error`, try again). |
| `domain_type` | string | `work` (business domain), `free` (e.g. gmail.com), or `disposable` (e.g. 001xs.org). |
| `username_type` | string | `personal` (e.g. john@) or `role` (e.g. sales@). Only returned when an email was submitted. |
| `syntax_valid` | boolean | Whether the email syntax is valid (e.g. `k&32@example.com` -> `false`). |
| `credits_consumed` | float | Credits consumed. |
| `credits_remaining` | float | Check Plan credits remaining. `-1` means unlimited. |

### Error responses

| HTTP status | Meaning |
| --- | --- |
| `400` | Invalid parameter. |
| `401` | Authorization missing or invalid. |
| `403` | Insufficient credits. |
| `405` | Account blocked. |
| `429` | Rate limited. |
| `500` | Unexpected error. |
