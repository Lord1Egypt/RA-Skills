# API Reference

## Endpoint

- Frontend: `https://webmail.suilong.online`
- Backend: `https://mail-api.suilong.online`
- Read mails: `GET https://mail-api.suilong.online/admin/mails`

## Query Parameters

- `limit` integer, default `20`
- `offset` integer, default `0`
- `address` optional mailbox address filter

Example:

```text
https://mail-api.suilong.online/admin/mails?limit=20&offset=0&address=t2@suilong.online
```

## Request Headers

- `accept: application/json`
- `content-type: application/json`
- `x-admin-auth: <admin auth>` expected for admin access
- `Authorization: Bearer <token>` optional when the deployment requires it
- `x-custom-auth` optional
- `x-fingerprint` optional
- `x-lang` optional
- `x-user-token` optional

## Normalized Output

Successful reads return:

- `status`
- `query`
- `summary`
- `results`

Each normalized message result may include:

- `id`
- `message_id`
- `address`
- `source`
- `from`
- `to`
- `subject`
- `date`
- `metadata`
- `preview`
- `text`
- `html`
- `verification_code`
- `raw` only when `--include-raw` is used

Confirmed current upstream payload fields include:

- `results[]`
- `count`
- `results[].id`
- `results[].message_id`
- `results[].source`
- `results[].address`
- `results[].raw`
- `results[].metadata`
- `results[].created_at`

## Export Options

- `--output-format json` keeps the default structured JSON output
- `--output-format csv` writes a flat CSV stream
- `--output-file <path>` writes the rendered output to a file as well as stdout

CSV format:

- `row_type=query` contains query metadata
- `row_type=result` contains one row per normalized message

## Error Mapping

- Unauthorized or forbidden responses map to `auth_error`
- Validation failures, server errors, non-JSON responses, and network failures map to `error`

## Security Note

Do not store `x-admin-auth`, bearer tokens, or other management secrets inside the skill. Pass them at runtime and rotate any credential that has been exposed in chat logs or screenshots.
