---
name: easylink-easydoc-extract
description: "Use when tasks need EasyLink extraction API to extract structured fields from documents. Trigger for requests about POST /v1/easydoc/extract and GET /v1/easydoc/extract/{task_id}, selecting mode (easydoc-extract, easydoc-extract-flash, bl-extract, occ-extract), customizing extracted fields via json_schema, using custom prompts, and handling async polling until SUCCESS or FAILED."
metadata:
  short-description: Extract structured fields from documents via EasyLink extraction API
  openclaw:
    requires:
      env:
        - EASYLINK_API_KEY
      bins:
        - python3
        - curl
    primaryEnv: EASYLINK_API_KEY
---

# EasyLink EasyDoc Extract

## Overview

Use this skill to call the EasyLink async extraction API and return structured field data from documents.
Always follow the same lifecycle: validate inputs, submit task, poll result, present extracted fields.

## Onboarding

If user has no API key, guide first:

1. Open `https://platform.easylink-ai.com`
2. Register or sign in
3. Enter API key management page and create a key
4. Store as `EASYLINK_API_KEY`

## Platform

Single platform only (CN/EasyLink):

- Base URL: `https://api.easylink-ai.com`
- Submit: `POST /v1/easydoc/extract`
- Poll: `GET /v1/easydoc/extract/{task_id}`
- File form field: `files`

## Modes

| Mode | Description | json_schema | prompt_cus |
|------|-------------|-------------|------------|
| `easydoc-extract` | Universal extraction | Optional (enables closed extraction) | Optional (used when no schema) |
| `easydoc-extract-flash` | Universal extraction with bounding boxes | Required | Not supported |
| `bl-extract` | Business license (fixed fields) | Not supported | Not supported |
| `occ-extract` | Org-code certificate (fixed fields) | Not supported | Not supported |

**easydoc-extract** has three behaviors based on parameters:
- `json_schema` provided → closed extraction (schema fields only)
- No schema, `prompt_cus` provided → prompt-driven extraction
- Neither provided → open extraction (auto-detects all key-value pairs)

## Workflow

1. Validate request inputs
   - Require `api-key` from user input or `EASYLINK_API_KEY` env var.
   - Require at least one file. Validate extension against supported list.
   - Validate file size (`<= 100MB`).
   - Validate mode/schema/prompt combination (see Modes table).
   - If key is missing, return onboarding steps.

2. Submit async extraction task
   - POST `multipart/form-data` with `files`, `mode`, and optional `json_schema` or `prompt_cus`.
   - Read `task_id` from response.

3. Poll task status
   - GET `/v1/easydoc/extract/{task_id}` until terminal status.
   - Terminal: `SUCCESS`, `ERROR`, `FAILED`, `COMPLETED`, `DONE`
   - In-progress: `PENDING`, `PROCESSING`, `RUNNING`, `IN_PROGRESS`, `QUEUED`
   - Stop on terminal or timeout.

4. Normalize output
   - Keep raw response as `raw`.
   - Return stable envelope: `task_id`, `status`, `results`.
   - Each result entry contains `page_number` and `fields` (flat key→value map).

5. Handle failures predictably
   - Include `task_id` in error reports when available.
   - Report HTTP status and response body for API errors.
   - For failures, suggest checking file format or re-submission.

## json_schema Format (universal modes only)

```json
{
  "type": "object",
  "properties": {
    "字段名": { "type": "string" }
  }
}
```

## Quick Commands

Open extraction (auto-detect all fields):

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/extract" \
  -H "api-key: $EASYLINK_API_KEY" \
  -F "files=@doc.pdf" \
  -F "mode=easydoc-extract"
```

Closed extraction with custom fields:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/extract" \
  -H "api-key: $EASYLINK_API_KEY" \
  -F "files=@doc.pdf" \
  -F "mode=easydoc-extract" \
  -F 'json_schema={"type":"object","properties":{"姓名":{"type":"string"},"金额":{"type":"string"}}}'
```

Business license:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/extract" \
  -H "api-key: $EASYLINK_API_KEY" \
  -F "files=@license.jpg" \
  -F "mode=bl-extract"
```

Org-code certificate:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/extract" \
  -H "api-key: $EASYLINK_API_KEY" \
  -F "files=@cert.jpg" \
  -F "mode=occ-extract"
```

Poll status:

```bash
curl -X GET "https://api.easylink-ai.com/v1/easydoc/extract/{task_id}" \
  -H "api-key: $EASYLINK_API_KEY"
```

Bundled Python helper:

```bash
# Open extraction
python3 scripts/easydoc_extract.py --file ./doc.pdf --mode easydoc-extract

# Closed extraction with custom fields
python3 scripts/easydoc_extract.py --file ./doc.pdf --mode easydoc-extract \
  --fields "姓名" "日期" "金额" --save ./result.json

# Flash mode (returns bounding boxes, requires --fields)
python3 scripts/easydoc_extract.py --file ./doc.pdf --mode easydoc-extract-flash \
  --fields "姓名" "金额"

# Custom prompt
python3 scripts/easydoc_extract.py --file ./doc.pdf --mode easydoc-extract \
  --prompt "提取所有金额和日期"

# Business license
python3 scripts/easydoc_extract.py --file ./license.jpg --mode bl-extract

# Org-code certificate
python3 scripts/easydoc_extract.py --file ./cert.jpg --mode occ-extract

# Poll existing task only
python3 scripts/easydoc_extract.py --poll-only --task-id "b_extract_xxx"
```

## References And Scripts

- Read `references/easydoc-extract-api.md` for endpoint details and error codes.
- Use `scripts/easydoc_extract.py` for deterministic submit and polling.
- Script default output is `normalized`; use `--output-format raw` for raw payload.

## Output Contract

```json
{
  "task_id": "string",
  "status": "SUCCESS|ERROR|PENDING|PROCESSING|FAILED|COMPLETED|DONE",
  "results": [
    {
      "page_number": 1,
      "fields": {
        "field_name": "value"
      }
    }
  ],
  "raw": {}
}
```
