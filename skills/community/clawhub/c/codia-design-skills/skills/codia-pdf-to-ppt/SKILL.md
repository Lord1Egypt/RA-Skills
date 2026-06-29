---
name: codia-pdf-to-ppt
description: Convert PDF pages into downloadable PowerPoint files with Codia Design CLI. Trigger when the user asks to turn PDFs into PPTX slides or editable presentations.
api: pdf-to-ppt
endpoint: POST /v2/open/uploads  +  POST /v2/open/tasks  +  GET /v2/open/tasks/:task_id
cli: codia-design pdf-to-ppt
credits_per_call: 13
sync: false
response_type: task
---

# codia-pdf-to-ppt

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Convert NotebookLM-style image-only PDF pages to editable PowerPoint files (asynchronous task). If a source PDF is a normal text/vector/complex-layout PDF, tell the user the API expects each page to be one full-page image. Do not silently rasterize or create a substitute PPTX unless the user explicitly asks for a local fallback.

## CLI Command

```bash
# Submit task (no waiting)
codia-design pdf-to-ppt --pdf <PATH|URL> --pages <0,1,2> [--title "Title"] [--out task.json]

# Submit and automatically poll until completed
codia-design pdf-to-ppt --pdf <PATH|URL> --pages <0,1,2> --poll [--timeout 300000] [--download-dir DIR] [--no-download] [--out result.json]
```

> **Note**: `--pages` is **zero-based**. Use `0` for the first page and `1` for the second page. This matches `pdf-to-design`.

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--pdf` | path \| URL | yes | — | Local PDF path, or public HTTPS URL |
| `--upload-id` / `--upload_id` | string | no | — | Opaque upload id returned by `POST /v2/open/uploads`; use instead of `--pdf` when already uploaded |
| `--pages` | string | yes | — | Comma-separated **zero-based** page numbers, such as `0,1,2` (up to 20 pages) |
| `--title` | string | no | PDF file name | Output .pptx file title |
| `--callback` | URL | no | — | webhook HTTPS URL called when conversion is complete |
| `--idempotency` | string | no | — | Sends `Idempotency-Key` on task creation for retry-safe clients |
| `--poll` | flag | no | false | If enabled, the CLI will automatically poll until the task is completed |
| `--timeout` | ms | no | `300000` | Polling timeout (milliseconds), only valid in `--poll` mode |
| `--download-dir` | path | no | Current directory | Directory for the downloaded `.pptx` when `--poll` succeeds |
| `--no-download` | flag | no | false | Skip PPTX download and file validation; use only for JSON-only workflows |
| `--out` | path | no | stdout | Write JSON results to file |

## Workflow

### 1. Prepare input and submit task

```bash
codia-design pdf-to-ppt --pdf ./deck.pdf --pages 0,1,2 --title "Q4 Review" --out task.json
```

When `--pdf` is a local file, the CLI first uploads it to `POST /v2/open/uploads` as multipart field `file`, receives an opaque `upload_id`, then creates a task with `POST /v2/open/tasks`. When `--pdf` is a URL, the CLI sends `input.pdf_url` directly to `POST /v2/open/tasks`. `/v2/open/uploads` does not return a public PDF URL.

Equivalent raw API flow:

```bash
curl 'https://api.codia.ai/v2/open/uploads' \
  -H 'Authorization: Bearer <CODIA_API_KEY>' \
  -F 'file=@./deck.pdf'

curl 'https://api.codia.ai/v2/open/tasks' \
  -H 'Authorization: Bearer <CODIA_API_KEY>' \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: pdf-to-ppt-001' \
  --data '{
    "operation": "pdf_to_ppt",
    "input": {
      "upload_id": "upl_550e8400-e29b-41d4-a716-446655440000",
      "page_no": [0, 1, 2],
      "title": "Q4 Review"
    }
  }'
```

Submit response (`PdfToPptSubmitResponse`):

```json
{
  "ok": true,
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "pending",
    "created_at": 1700000000
  }
}
```

### 2. Polling status (manual mode)

The CLI `--poll` mode uses `GET /v2/open/tasks/:task_id` internally. The recommended polling interval is 5 seconds. The underlying task `status` value:

| status | meaning | next step |
|---|---|---|
| `pending` | Queuing | Continue polling |
| `processing` | Converting | Continue polling |
| `succeeded` | Done | Read `result.ppt_url` |
| `failed` | Failed | Read `error_code` / `error` |
| `canceled` | Canceled | Stop polling |

Task response:

```json
{
  "ok": true,
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "operation": "pdf_to_ppt",
    "status": "succeeded",
    "result": {
      "ppt_url": "https://static.codia.ai/pptx/deck.pptx"
    },
    "error_code": "",
    "created_at": 1700000000
  }
}
```

### 3. Automatic polling (recommended)

```bash
codia-design pdf-to-ppt --pdf ./deck.pdf --pages 0,1,2 --poll --download-dir ./outputs --out result.json
```

The CLI internally polls every 5 seconds and throws an error after `--timeout` is exceeded. When the task returns `succeeded`, the CLI normalizes the final JSON to `status: "done"`, downloads `ppt_url`, verifies that the response is a valid PPTX package, and writes the local path to `data.local_file` and `data.local_files`. If the URL returns an error such as 403 or the downloaded file is not an openable PPTX package, the command fails instead of returning `ok: true`.

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | Missing `input.upload_id` / `input.pdf_url`, pages format error, encrypted or unsupported PDF | Check parameters; pages must be zero-based integers; source should be image-only PDF |
| 402 | Insufficient credits | Each page converted consumes 13 credits |
| 403 | Feature unavailable for current plan | Report the API error directly; do not generate a local fallback unless explicitly requested |
| 429 | Rate limit exceeded | Retry after backing off |
| 500 | Service internal error | Try again |

**Credits**: 13 credits/page. After upload/task creation or completed polling, the CLI checks `available_credits` and reminds the user if the remaining balance is below 2x the estimated page cost; this does not block generation. · **Duration**: asynchronous, usually tens of seconds, longer for long documents
