# EasyLink EasyDoc Mask API Reference

## Platform

| Platform | Base URL | Submit | Result | File Field | Mode |
| --- | --- | --- | --- | --- | --- |
| CN (EasyLink) | `https://api.easylink-ai.com` | `POST /v1/easydoc/mask` | `GET /v1/easydoc/mask/{task_id}` | `files` | `emr-mask` |

Max file size: `100 MB` per file.

## Registration And API Key

1. Open `https://platform.easylink-ai.com`
2. Register or sign in
3. Create API key from key management page
4. Use key via header `api-key`
5. Recommended local env var: `EASYLINK_API_KEY`

## Submit Endpoint

`POST /v1/easydoc/mask`

Request format: `multipart/form-data`

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `files` | file | Yes | One or more files to mask (JPG/PNG/BMP/TIFF/PDF) |
| `mode` | string | Yes | Fixed value: `emr-mask` |
| `json_schema` | string (JSON) | No | JSON object specifying custom fields to mask |

Submit with default masking:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/mask" \
  -H "api-key: your_apikey_here" \
  -F "files=@record.pdf" \
  -F "mode=emr-mask"
```

Submit with custom fields:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/mask" \
  -H "api-key: your_apikey_here" \
  -F "files=@record.pdf" \
  -F "mode=emr-mask" \
  -F 'json_schema={"properties": {"患者姓名": {"type": "string"}, "身份证号": {"type": "string"}, "联系电话": {"type": "string"}}}'
```

Successful submit response:

```json
{
  "success": true,
  "data": {
    "task_id": "b_mask_81d006e2-9295-4752-9033-9a37f24bc11d",
    "status": "PROCESSING"
  }
}
```

## Poll Endpoint

`GET /v1/easydoc/mask/{task_id}`

```bash
curl -X GET "https://api.easylink-ai.com/v1/easydoc/mask/b_mask_xxx" \
  -H "api-key: your_apikey_here"
```

Successful result response:

```json
{
  "data": {
    "status": "SUCCESS",
    "results": [
      {
        "url": "https://...",
        "masked_fields": ["患者姓名", "身份证号"],
        "page_count": 3
      }
    ]
  }
}
```

## Supported File Formats

- `.pdf`
- `.jpg` / `.jpeg`
- `.png`
- `.bmp`
- `.tif` / `.tiff`

## Common Status Handling

In-progress states (keep polling):

- `PENDING`
- `PROCESSING`
- `RUNNING`
- `IN_PROGRESS`
- `QUEUED`

Terminal states (stop polling):

- `SUCCESS`
- `ERROR`
- `FAILED`
- `COMPLETED`
- `DONE`

## Error Codes

| Code | Meaning |
| --- | --- |
| `API_UNAUTHORIZED` | Invalid or missing API key |
| `INSUFFICIENT_BALANCE` | Account credit exhausted |
| `INVALID_DOCUMENT` | File cannot be processed |
| `INVALID_PARAMETER` | Bad request parameter |
| `EMPTY_TASK` | Illegal or malformed task request |
| `ILLEGALITY_TASK_TYPE` | Invalid task type |

## Normalized Output Contract

```json
{
  "task_id": "string",
  "status": "string",
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

## Bundled Script Notes

`scripts/easydoc_mask.py` supports submit, poll, and poll-only modes.

Examples:

```bash
python3 scripts/easydoc_mask.py --api-key "$EASYLINK_API_KEY" \
  --file ./record.pdf --save ./result.json

python3 scripts/easydoc_mask.py --file ./record.pdf \
  --fields "患者姓名" "身份证号" --save ./result.json

python3 scripts/easydoc_mask.py --poll-only --task-id "b_mask_xxx"
```

Useful options:

- `--output-format normalized|raw`
- `--query-retries 3`
- `--skip-local-checks`
- `--fields FIELD [FIELD ...]` — custom fields to mask via `json_schema`
