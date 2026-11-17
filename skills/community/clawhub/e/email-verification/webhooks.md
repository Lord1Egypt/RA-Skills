# Webhooks

Receive verification results in real time via HTTP POST instead of polling. Set a webhook by passing a `url` (and/or `url_finished` for bulk tasks) parameter when creating a verification request.

## Delivery behavior

- Payloads are JSON, sent via HTTP POST.
- Every event includes an `event-type` header for routing.
- On delivery failure, the system retries up to **2 more times** within a short interval.
- For high volume, make sure your webhook server can handle the traffic. Tunneling tools like ngrok often fail under load; for testing try https://typedwebhook.tools/ instead (not affiliated).

## Event types

| `event-type` header | Trigger | Set via |
| --- | --- | --- |
| `single.email_verification_finished` | A single email verification finished | `url` on `/v1/verify/single` (standard or waterfall) |
| `bulk.email_verification_finished` | One email in a bulk task finished | `url` on `/v1/verify/bulk` or `/v1/verify/bulk/file` |
| `bulk.task_finished` | A whole bulk task finished | `url_finished` on `/v1/verify/bulk` or `/v1/verify/bulk/file` |

## Payload: `single.email_verification_finished`

A single JSON object:

```json
{
  "id": "502abcde",
  "status": "success",
  "email": "dev@bounceban.com",
  "result": "deliverable",
  "score": 99,
  "is_disposable": false,
  "is_accept_all": false,
  "is_role": true,
  "is_free": false,
  "mx_records": ["alt1.aspmx.l.google.com", "aspmx.l.google.com"],
  "smtp_provider": "Google",
  "mode": "regular",
  "verify_at": "2022-11-16T07:21:24.943Z",
  "credits_consumed": 1.0,
  "credits_remaining": 375214.0
}
```

## Payload: `bulk.email_verification_finished`

A JSON **array** (one event per verified email):

```json
[
  {
    "task_id": "68b167c5d10abc82d391f13f",
    "status": "success",
    "email": "dev@bounceban.com",
    "result": "deliverable",
    "score": 99,
    "is_disposable": false,
    "is_accept_all": false,
    "is_role": true,
    "is_free": false,
    "mx_records": ["alt1.aspmx.l.google.com", "aspmx.l.google.com"],
    "smtp_provider": "Google",
    "verify_at": "2022-11-16T07:21:24.943Z"
  }
]
```

## Payload: `bulk.task_finished`

```json
{
  "id": "68b167c5d10abc82d391f13f",
  "status": "finished",
  "total_count": 2,
  "pushed_count": 2,
  "deliverable_count": 0,
  "risky_count": 2,
  "undeliverable_count": 0,
  "unknown_count": 0,
  "catchall_count": 2,
  "credits_consumed": 2.0,
  "credits_remaining": 1483505.176
}
```
