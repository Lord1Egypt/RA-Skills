---
name: codia-usage
description: Inspect Codia Open API usage records from AI agents. Trigger when the user asks for Codia API usage, consumption records, billing history, or recent task cost details.
api: usage
endpoint: GET /v2/open/usage
cli: codia-design usage
credits_per_call: 0
sync: true
response_type: object
---

# codia-usage

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Paginated query API call history.

## CLI Command

```bash
codia-design usage \
  [--page 1] \
  [--page_size 50] \
  [--start_date YYYY-MM-DD] \
  [--end_date YYYY-MM-DD]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--page` | number | no | `1` | Account-history page number. Pass `1` for the first result page; the current API normalizes `0` to `1`, but callers should use `1` or greater. |
| `--page_size` | number | no | `50` | Number of items per page |
| `--start_date` | string | no | — | Filter start date, format `YYYY-MM-DD` |
| `--end_date` | string | no | — | Filter end date (including today), format `YYYY-MM-DD` |

## Response

```json
{
  "ok": true,
  "data": {
    "items": [
      {
        "request_id": "01HXYZ...",
        "endpoint": "/v2/open/image_to_design",
        "operation": "image_to_design",
        "credits_used": 13.0,
        "status": "success",
        "created_at": "2026-05-15T10:30:00Z"
      }
    ],
    "total": 150,
    "page": 1,
    "page_size": 50,
    "has_more": true
  }
}
```

| Field | Type | Description |
|---|---|---|
| `items[].request_id` | string | Request unique ID |
| `items[].endpoint` | string | API path called |
| `items[].operation` | string | Operation name (such as `image_to_design`, `image_upscale`) |
| `items[].credits_used` | number | The credits consumed by this call |
| `items[].status` | string | Fixed to `"success"` (failed requests are not billed and therefore not recorded) |
| `items[].created_at` | string | Calling time (RFC3339 UTC) |
| `total` | number | Total number of records |
| `has_more` | boolean | Is there a next page |

## Usage Example

```bash
# Query today’s usage
codia-design usage --start_date 2026-05-15 --end_date 2026-05-15

# Traverse all pages
PAGE=1
while true; do
  codia-design usage --page $PAGE --page_size 50 --out "page_$PAGE.json"
  HAS_MORE=$(node -e "console.log(require('./page_$PAGE.json').data.has_more)")
  [ "$HAS_MORE" = "false" ] && break
  PAGE=$((PAGE + 1))
done
```

## Errors & Billing

**Credit consumption**: 0 (the query itself does not consume credits)
