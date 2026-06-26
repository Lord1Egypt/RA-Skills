# Web Push API Error Codes

Error codes returned in the response body when the Web Push API (and related APIs) fail.

## Create Push / Batch / Group Push — Common codes

| Code | Description | HTTP | Notes |
|------|-------------|------|--------|
| 20101 | The push parameter is invalid | 400 | Registration ID invalid or does not belong to current AppKey. |
| 21001 | Only HTTP Post methods are supported | 405 | Use POST, not GET. |
| 21002 | Required parameters are missing | 400 | Correct the request body. |
| 21003 | Invalid parameter value | 400 | Correct value or format. |
| 21004 | Verification failed | 401 | Check AppKey and Master Secret. |
| 21005 | The message body is too large | 400 | Notification length limit 2048 bytes (total message 4000 bytes). |
| 21008 | The app_key parameter is invalid | 400 | Check AppKey (e.g. extra spaces). |
| 21009 | Internal system error | 400 | Contact support. |
| 21011 | There are no push targets that meet the conditions | 400 | Check the `to` field. |
| 21015 | Request parameter verification failed | 400 | Unexpected parameters. |
| 21016 | Request parameter verification failed | 400 | Parameter type or length error. |
| 21030 | Internal service timeout | 503 | Retry later. |
| 23006 | Parameter error | 400 | e.g. big_push_duration exceeds 1440. |
| 23008 | Interface speed limit | 400 | QPS limit (500) reached. |
| 27000 | System memory error | 500 | Retry. |
| 27001 | Parameter error | 401 | Verification information empty. |
| 27008 | Parameter error | 401 | third_party_channel distribution set but notification alert empty. |
| 27009 | Parameter error | 401 | Invalid or empty distribution in third_party_channel. |
| 27002 | Unknown error | — | e.g. Delete User API. |
| 1003 | Invalid message override | — | override_msg_id not valid (e.g. not within 1 day). |

## Delete User

| Code | HTTP | Description |
|------|------|-------------|
| 27002 | — | unknown error. |

## Response format

Failed responses typically look like:

```json
{
  "error": {
    "code": 21003,
    "message": "Invalid parameter value"
  }
}
```

Or directly:

```json
{
  "code": 21003,
  "message": "Invalid parameter value"
}
```

Use the `code` and `message` fields for error handling in code.
