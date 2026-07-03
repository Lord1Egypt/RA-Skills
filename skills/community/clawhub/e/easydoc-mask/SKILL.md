---
name: easylink-easydoc-mask
description: "Use when tasks need EasyLink masking API to redact sensitive fields from medical records (EMR) or other documents. Trigger for requests about POST /v1/easydoc/mask and GET /v1/easydoc/mask/{task_id}, selecting mode (emr-mask), customizing masked fields via json_schema, downloading masked output files, and handling async polling until SUCCESS or FAILED."
metadata:
  short-description: Redact sensitive fields from medical records via EasyLink masking API
  openclaw:
    requires:
      env:
        - EASYLINK_API_KEY
      bins:
        - python3
        - curl
    primaryEnv: EASYLINK_API_KEY
---

# EasyLink EasyDoc Mask

## Overview

Use this skill to call the EasyLink async masking API and return masked document download URLs.
Always follow the same lifecycle: validate inputs, submit task, poll result, present output URLs.

## Onboarding

If user has no API key, guide first:

1. Open `https://platform.easylink-ai.com`
2. Register or sign in
3. Enter API key management page and create a key
4. Store as `EASYLINK_API_KEY`

## Platform

Single platform only (CN/EasyLink):

- Base URL: `https://api.easylink-ai.com`
- Submit: `POST /v1/easydoc/mask`
- Poll: `GET /v1/easydoc/mask/{task_id}`
- File form field: `files`
- Required mode: `emr-mask`

## Workflow

1. Validate request inputs
   - Require `api-key` from user input or `EASYLINK_API_KEY` env var.
   - Require at least one file. Validate extension against supported list.
   - Validate file size (`<= 100MB`).
   - If key is missing, return onboarding steps.

2. Submit async mask task
   - POST `multipart/form-data` with `files`, `mode=emr-mask`, and optional `json_schema`.
   - Read `task_id` from response.

3. Poll task status
   - GET `/v1/easydoc/mask/{task_id}` until terminal status.
   - Terminal: `SUCCESS`, `ERROR`, `FAILED`, `COMPLETED`, `DONE`
   - In-progress: `PENDING`, `PROCESSING`, `RUNNING`, `IN_PROGRESS`, `QUEUED`
   - Stop on terminal or timeout.

4. Normalize output
   - Keep raw response as `raw`.
   - Return stable envelope: `task_id`, `status`, `results`.
   - Each result includes `url` (download link for masked file) and `masked_fields`.

5. Handle failures predictably
   - Include `task_id` in error reports when available.
   - Report HTTP status and response body for API errors.
   - For failures, suggest checking file format or re-submission.

## Custom Masking Fields (json_schema)

By default, `emr-mask` redacts the following fields:
住址、姓名、生日、病例ID、账户ID、医保号、商品名、样本号、病床号、病案号、登记号、医生姓名、家属信息、检查单号、联系方式、身份证号、发票二维码、发票个人信息、患者账号余额、检查单二维码、检查单条形码

To customize which fields are masked, pass `json_schema` as a JSON string:

```bash
-F 'json_schema={"type": "object", "properties": {"姓名": {"type": "string"}, "身份证号": {"type": "string"}, "联系方式": {"type": "string"}}}'
```

If the user does not specify fields, omit `json_schema` and let the API use defaults.

## Quick Commands

Submit and poll:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/mask" \
  -H "api-key: $EASYLINK_API_KEY" \
  -F "files=@record.pdf" \
  -F "mode=emr-mask"
```

With custom fields:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/mask" \
  -H "api-key: $EASYLINK_API_KEY" \
  -F "files=@record.pdf" \
  -F "mode=emr-mask" \
  -F 'json_schema={"type": "object", "properties": {"姓名": {"type": "string"}, "身份证号": {"type": "string"}}}'
```

Poll status:

```bash
curl -X GET "https://api.easylink-ai.com/v1/easydoc/mask/{task_id}" \
  -H "api-key: $EASYLINK_API_KEY"
```

Bundled Python helper:

```bash
python3 scripts/easydoc_mask.py --api-key "$EASYLINK_API_KEY" \
  --file ./record.pdf --save ./result.json

# Key from environment
export EASYLINK_API_KEY="your-key"
python3 scripts/easydoc_mask.py --file ./record.pdf --save ./result.json

# Custom fields
python3 scripts/easydoc_mask.py --file ./record.pdf \
  --fields "姓名" "身份证号" "联系方式" --save ./result.json

# Poll existing task only
python3 scripts/easydoc_mask.py --poll-only --task-id "b_mask_xxx" --save ./result.json
```

## References And Scripts

- Read `references/easydoc-mask-api.md` for endpoint details and error codes.
- Use `scripts/easydoc_mask.py` for deterministic submit and polling.
- Script default output is `normalized`; use `--output-format raw` for raw payload.

## Output Contract

```json
{
  "task_id": "string",
  "status": "SUCCESS|ERROR|PENDING|PROCESSING|FAILED|COMPLETED|DONE",
  "results": [
    {
      "url": "string",
      "masked_fields": ["string"],
      "page_count": 0
    }
  ],
  "raw": {}
}
```
