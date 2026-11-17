# BounceBan API Introduction

> BounceBan is an email verification API. It verifies all kinds of emails and specializes in verifying emails that are accept-all (catch-all) or protected by SEGs (Secure Email Gateways). Instead of marking all accept-all emails as risky, BounceBan identifies which of them are actually deliverable.

## Base URLs

| API | Base URL |
| --- | --- |
| All standard endpoints | `https://api.bounceban.com` |
| Waterfall single verification (Clay, n8n, etc.) | `https://api-waterfall.bounceban.com` |

## Authentication

All endpoints require an API key sent in the `Authorization` header (no `Bearer` prefix):

```
Authorization: YOUR_API_KEY
```

Get your API key, set IP whitelist, and track usage at: https://bounceban.com/app/api/settings

```bash
curl "https://api.bounceban.com/v1/account" \
  -H "Authorization: YOUR_API_KEY"
```

## Credits

- Each successful verification costs **1 credit** (single or bulk).
- Credits are deducted for every request to `/v1/verify/single`, even for repeated verification of the same email.
- For the waterfall endpoint, retrying the same email within 30 minutes of the initial request does **not** deduct extra credits.
- When `disable_catchall_verify=1` and the result is `unknown` with `score: -1`, the credit cost is 0.
- For bulk tasks, credits for `unknown` results are refunded when the task finishes.
- The `/v1/check` endpoint uses a **separate** Check Plan credit balance.
- Buy credits: https://bounceban.com/pricing. Test credits: contact dev@bounceban.com.

## Verification results

Every verified email gets a `result` and a `score`:

| Field | Values | Meaning |
| --- | --- | --- |
| `result` | `deliverable` | Safe to send. |
| | `risky` | May bounce; check `score` (higher is better). |
| | `undeliverable` | Will bounce; do not send. |
| | `unknown` | Verification could not determine a result. |
| `score` | `0`-`100` | Deliverability confidence; higher is better. |

Additional boolean flags per email: `is_disposable`, `is_accept_all`, `is_role`, `is_free`. `mx_records` (array) and `smtp_provider` (string, e.g. `Google`) are also returned when available.

## Task status values

| Status | Meaning |
| --- | --- |
| `success` | Verification finished; final result included. |
| `verifying` | Still verifying (e.g. greylisting). Poll status endpoint or use a webhook. Do NOT resubmit - each request costs 1 credit. |
| `queue` | Account rate limit reached; email queued. Poll or use webhook. |

## Verification modes

| Mode | Description |
| --- | --- |
| `regular` | Default. Does not assume the email's domain matches the owner's current company website. |
| `deepverify` | Assumes the email's domain matches the owner's current company website (e.g. from LinkedIn). Improves success rate for accept-all emails. Learn more: https://support.bounceban.com/article/what-is-deepverify |

## Choosing the right endpoint

| Scenario | Use |
| --- | --- |
| One HTTP request, wait for result (Clay, n8n, Zapier-like waterfall) | `GET https://api-waterfall.bounceban.com/v1/verify/single` |
| Async single verification with polling or webhook | `GET /v1/verify/single` + `GET /v1/verify/single/status` |
| Verify a list of emails (up to ~500,000 per task) | `POST /v1/verify/bulk` |
| Verify emails from a CSV file (max 25 MB) | `POST /v1/verify/bulk/file` |
| Quick syntax/domain/role check (no SMTP verification) | `GET /v1/check` |
| Credits balance and rate limits | `GET /v1/account` |

## Rate limits

Default per-account limits (check live values via `GET /v1/account`):

| Endpoint | Limit |
| --- | --- |
| `/v1/verify/single` | 25 per second |
| `/v1/verify/single/status` | 25 per second |
| `/v1/verify/bulk` | 3 per second |
| `/v1/verify/bulk/status` | 25 per second |
| `/v1/verify/bulk/export` | 25 per second |
| `/v1/verify/bulk/dump` | 25 per second |
| `/v1/account` | 5 per second |

Request a higher limit: https://forms.gle/3De4UMZKpxPiPv5M8

## Data retention

Verification results are available for **90 days** after verification.

## Resources

- Interactive API reference (Redoc): https://bounceban.com/public/doc/api.html
- OpenAPI 3.0 spec: https://bounceban.com/public/doc/api.yaml
- Postman workspace: https://www.postman.com/galactic-comet-480286/workspace/bounceban-developers
- Support: dev@bounceban.com
