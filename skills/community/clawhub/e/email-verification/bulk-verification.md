# Bulk Verification

Verify a list of emails as an asynchronous task. Typical flow:

1. Create a task: `POST /v1/verify/bulk` (JSON list) or `POST /v1/verify/bulk/file` (CSV upload) -> returns task `id`.
2. Track progress: `GET /v1/verify/bulk/status` (or `url_finished` webhook).
3. Get results: `GET /v1/verify/bulk/dump` (JSON), `POST /v1/verify/bulk/emails` (specific emails), or `POST /v1/verify/bulk/export` (CSV download link).
4. Optionally delete: `POST /v1/verify/bulk/destroy`.

All endpoints use base URL `https://api.bounceban.com` and the `Authorization: YOUR_API_KEY` header.

---

## Create bulk task from a list of emails

```
POST https://api.bounceban.com/v1/verify/bulk
Content-Type: application/json
```

Recommended max: **500,000 emails per task** (contact support for more). A dynamic soft limit applies to concurrent verifying emails per account.

### Body parameters

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `emails` | string[] | Yes | Emails to verify. |
| `name` | string | No | Task name; auto-generated if omitted. |
| `url` | string | No | Webhook URL - one event per verified email. Header: `event-type: bulk.email_verification_finished`. |
| `url_finished` | string | No | Webhook URL - one event when the whole task finishes. Header: `event-type: bulk.task_finished`. |
| `mode` | string | No | `regular` (default) or `deepverify`, applied to all emails. |
| `greylisting_bypass` | string | No | `auto` (default), `speed` (~1 min retry delay; small/time-sensitive lists; more `risky` flags), or `robust` (~5 min retry delay; large lists; fewer `risky` flags). |
| `disable_catchall_verify` | string | No | `0` (default) or `1`. When `1`, catch-all/SEG-protected emails return `unknown`, `score: -1`, cost 0 credits. |

### Example request

```bash
curl -X POST "https://api.bounceban.com/v1/verify/bulk" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"emails": ["dev@bounceban.com", "support@bounceban.com"]}'
```

### Example response (200)

```json
{ "id": "6374973d2307debafb85a58d", "credits_remaining": 14973 }
```

---

## Create bulk task from a CSV file

```
POST https://api.bounceban.com/v1/verify/bulk/file
Content-Type: multipart/form-data
```

Max file size **25 MB**. The file may contain multiple columns; one column is used for emails. All original columns are preserved in exports.

### Form parameters

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | No | Task name; defaults to the file name. |
| `email_column` | integer | No | Zero-based index of the email column. If omitted, auto-detected from the first 6 rows; an error is returned if emails are found in multiple columns. |
| `mode_column` | integer | No | Zero-based index of a column with per-email DeepVerify settings. Values `deepverify`, `yes`, `y`, `1`, `true` enable DeepVerify for that row. |
| `greylisting_bypass` | string | No | `auto` / `speed` / `robust` - same as above. |
| `url` | string | No | Per-email webhook. Header: `event-type: bulk.email_verification_finished`. |
| `url_finished` | string | No | Task-finished webhook. Header: `event-type: bulk.task_finished`. |
| `disable_catchall_verify` | string | No | `0` (default) or `1`. |
| `file` | binary | Yes | CSV file. **Must be the LAST field in the multipart form**, otherwise other fields (e.g. `url_finished`) may not work. |

### Example request

```bash
curl -X POST "https://api.bounceban.com/v1/verify/bulk/file" \
  -H "Authorization: YOUR_API_KEY" \
  -F "name=My import" \
  -F "email_column=0" \
  -F "file=@emails.csv"
```

### Example response (200)

```json
{ "id": "6374973d2307debafb85a58d", "credits_remaining": 14973 }
```

---

## Get bulk task status

```
GET https://api.bounceban.com/v1/verify/bulk/status?id=TASK_ID
```

### Response fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Task ID. |
| `status` | string | `importing` -> `verifying` -> `finished`. |
| `total_count` | integer | Emails to verify (importing/verifying) or verified (finished). |
| `finished_count` | integer | Emails imported (importing) or verified (verifying). |
| `pushed_count` | integer | Webhook events delivered (if a webhook was set). |
| `deliverable_count` / `undeliverable_count` / `risky_count` / `unknown_count` / `catchall_count` | integer | Result counts; only when `finished`. |
| `credits_consumed` | float | Only when `finished`. |
| `credits_remaining` | float | Only when `finished`. `-1` means unlimited. |

### Example

```bash
curl "https://api.bounceban.com/v1/verify/bulk/status?id=6374973d2307debafb85a58d" \
  -H "Authorization: YOUR_API_KEY"
```

```json
{
  "id": "6374973d2307debafb85a58d",
  "status": "finished",
  "total_count": 2,
  "deliverable_count": 2,
  "undeliverable_count": 0,
  "risky_count": 0,
  "unknown_count": 0,
  "credits_consumed": 2.0,
  "credits_remaining": 14973.0
}
```

---

## Get results for specific emails

```
POST https://api.bounceban.com/v1/verify/bulk/emails
Content-Type: application/json
```

### Body parameters

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | string | Yes | Bulk task ID. |
| `emails` | string[] | Yes | Up to **100** emails, all from this task. |

### Example

```bash
curl -X POST "https://api.bounceban.com/v1/verify/bulk/emails" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "6374973d2307debafb85a58d", "emails": ["dev@bounceban.com"]}'
```

```json
{
  "result": "ok",
  "items": [
    {
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
      "verify_at": "2022-11-16T07:54:37.480Z"
    }
  ]
}
```

`result` is `ok` on success, `err` if the task hasn't finished yet.

---

## Dump all results as JSON (paginated)

```
GET https://api.bounceban.com/v1/verify/bulk/dump?id=TASK_ID
```

Works even while the task is still running (omit `state` to get everything verified so far). Results available for 90 days.

### Parameters (query)

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | string | Yes | Bulk task ID. |
| `state` | string | No | Filter: `deliverable`, `risky`, `undeliverable`, `unknown`. Omit to get all verified emails, including in-progress tasks. |
| `cursor` | string | No | Pagination cursor from the previous response. |
| `page_size` | integer | No | 100-3000, default 100. |
| `retrieve_all` | string | No | Set `1` to fetch everything at once (only if the task has <= 20,000 emails; ignores `cursor` and `page_size`). |

### Pagination loop for agents

1. Request without `cursor`.
2. Read `items` and `cursor` from the response.
3. If `cursor` is non-null, request again with `cursor=<value>`.
4. Stop when `cursor` is null.

### Example

```bash
curl "https://api.bounceban.com/v1/verify/bulk/dump?id=6374973d2307debafb85a58d&page_size=100" \
  -H "Authorization: YOUR_API_KEY"
```

```json
{
  "result": "ok",
  "cursor": null,
  "items": [
    {
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
      "verify_at": "2022-11-16T07:54:37.480Z"
    }
  ]
}
```

---

## Export results to a CSV file

```
POST https://api.bounceban.com/v1/verify/bulk/export
Content-Type: application/json
```

Returns a public download link that **expires after 4 hours** (you can request a new one anytime within the 90-day retention window). Only works after the task has **finished**. Link generation may take time: ~30 s for 100k emails, ~2 min for 400k. If the link isn't ready, wait a few seconds and retry - max **15 requests per export per 15 minutes**.

### Body parameters

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | string | Yes | Completed bulk task ID. |
| `keep_all_rows` | boolean | No | `true` keeps all source CSV rows (even without email). Only for tasks created via `/v1/verify/bulk/file`. Default `false`. |
| `criteria` | object | No | Filter which emails to export (see below). |

### `criteria` fields (all optional booleans unless noted)

| Field | Default | Description |
| --- | --- | --- |
| `deliverable` | `true` | Include deliverable emails. |
| `risky` | `false` | Include risky emails. |
| `risky_score` | `50` | Integer 0-100. Minimum score for risky emails; only if `risky` is `true`. |
| `undeliverable` | `false` | Include undeliverable emails. |
| `unknown` | `false` | Include unknown emails. |
| `free` | `true` | Include free-provider emails. |
| `role` | `true` | Include role emails. |
| `accept_all` | `true` | Include accept-all emails. |
| `disposable` | `false` | Include disposable emails. |

### Example

```bash
curl -X POST "https://api.bounceban.com/v1/verify/bulk/export" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "6374973d2307debafb85a58d", "criteria": {"deliverable": true, "risky": true, "risky_score": 70}}'
```

```json
{
  "result": "ok",
  "download_url": "https://bounceban.s3.us-west-2.amazonaws.com/export/bulk/laHkQ.csv?..."
}
```

---

## Delete a bulk task

```
POST https://api.bounceban.com/v1/verify/bulk/destroy
Content-Type: application/json
```

**Irreversible.** The task and all its data are removed immediately.

### Body parameters

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | string | Yes | Bulk task ID. |

### Example

```bash
curl -X POST "https://api.bounceban.com/v1/verify/bulk/destroy" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "6374973d2307debafb85a58d"}'
```

```json
{ "result": "ok" }
```

---

## Error responses (all bulk endpoints)

| HTTP status | Meaning |
| --- | --- |
| `400` | Invalid parameter. |
| `401` | Authorization missing or invalid. |
| `403` | Insufficient credits (`credits_required`, `credits_remaining`, `message` in body). |
| `405` | Account blocked. |
| `429` | Rate limited. |
| `500` | Unexpected error. |
