# App Push API Error Codes

Error codes returned in the response body when the Push API (and related APIs) fail. The HTTP status is often 400 or 401.

## Create Push / Batch / Group Push — Common codes

| Code | Description | HTTP | Notes |
|------|-------------|------|--------|
| 20101 | Invalid push parameters | 400 | Registration ID invalid or does not belong to current AppKey. |
| 21001 | Only supports HTTP Post method | 405 | Use POST, not GET. |
| 21002 | Required parameter missing | 400 | Correct the request body. |
| 21003 | Invalid parameter value | 400 | Correct value or format. |
| 21004 | Verification failed | 401 | Check AppKey and Master Secret. |
| 21005 | Message body too large | 400 | Notification/Message length limit 4000 bytes. |
| 21008 | Invalid app_key parameter | 400 | Check AppKey (e.g. extra spaces). |
| 21009 | Internal system error | 400 | Contact support. |
| 21011 | No suitable push target found | 400 | Check the `to` field. |
| 21015 | Request parameter validation failed | 400 | Unexpected parameters. |
| 21016 | Request parameter validation failed | 400 | Parameter type or length error. |
| 21030 | Internal service timeout | 503 | Retry later. |
| 21038 | Push permission error | 401 | VIP expired or not activated. |
| 21050 | Incorrect live_activity event parameter | 400 | Event must be "start", "update", or "end". |
| 21051 | Incorrect live_activity audience parameter | 400 | For creation, target can only be broadcast or registration_id. |
| 21052 | Incorrect live_activity attributes-type | 400 | When event=start, attributes-type cannot be empty. |
| 21053 | Incorrect live_activity content-state | 400 | content-state cannot be empty. |
| 21054 | live_activity parameter error | 400 | notification, message, live_activity cannot coexist. |
| 21055 | live_activity ios non-p8 certificate | 400 | Live activity only supports P8 certificate. |
| 21056 | live_activity only supports ios platform | 400 | platform must be ios. |
| 21057 | voip not allowed with other message types | 400 | voip cannot coexist with notification/message/live_activity. |
| 21058 | voip only supports ios platform | 400 | platform must be ios. |
| 21059 | This message type does not support big_push_duration | 401 | — |
| 21306 | Notification and custom message cannot be pushed simultaneously | 401 | — |
| 23006 | Parameter error | 400 | e.g. big_push_duration exceeds 1440. |
| 23008 | Interface rate limited | 400 | QPS limit (500) reached. |
| 23009 | Push permission error | 400 | Current IP not in application IP whitelist. |
| 27000 | Internal memory error | 500 | Retry. |
| 27001 | Parameter error | 401 | Verification information empty. |
| 27008 | Parameter error | 401 | third_party_channel distribution set but notification alert empty. |
| 27009 | Parameter error | 401 | Invalid or empty distribution in third_party_channel. |
| 27303 | Empty plan id | — | Push Plan API. |
| 27002 | Unknown error | — | e.g. Delete User API. |

## Message Recall

| Code | HTTP | Description |
|------|------|-------------|
| 21003 | 400 | Parameter value invalid, e.g. msg_id not exist. |

## Delete User

| Code | HTTP | Description |
|------|------|-------------|
| 27002 | — | unknown error. |

## Push Plan / Statistics / Schedules

Refer to the respective API docs in `doc/apppush/REST API/` for plan-specific and report-specific error codes (e.g. 1003 for invalid parameter value).

## Response format

Failed responses typically look like:

```json
{
  "error": {
    "code": 21003,
    "message": "Parameter value is invalid"
  }
}
```

Use the `code` and `message` fields for handling errors in code.
