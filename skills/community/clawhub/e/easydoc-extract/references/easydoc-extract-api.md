# EasyLink EasyDoc Extract API Reference

## Platform

| Platform | Base URL | Submit | Result | File Field |
| --- | --- | --- | --- | --- |
| CN (EasyLink) | `https://api.easylink-ai.com` | `POST /v1/easydoc/extract` | `GET /v1/easydoc/extract/{task_id}` | `files` |

Max file size: `100 MB` per file.

## Registration And API Key

1. Open `https://platform.easylink-ai.com`
2. Register or sign in
3. Create API key from key management page
4. Use key via header `api-key`
5. Recommended local env var: `EASYLINK_API_KEY`

## Submit Endpoint

`POST /v1/easydoc/extract`

Request format: `multipart/form-data`

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `files` | file | Yes | One or more files (JPG/PNG/BMP/TIFF/PDF) |
| `mode` | string | Yes | See Modes table below |
| `json_schema` | string (JSON) | Conditional | Enables closed extraction; required for `easydoc-extract-flash` |
| `prompt_cus` | string | No | Custom extraction prompt (`easydoc-extract` only, used when no schema) |

## Modes

| Mode | Description | json_schema | prompt_cus |
| --- | --- | --- | --- |
| `easydoc-extract` | Universal: open / closed / prompt-driven | Optional | Optional |
| `easydoc-extract-flash` | Universal with bounding boxes (closed only) | Required | Not supported |
| `bl-extract` | Business license fixed fields | Not supported | Not supported |
| `occ-extract` | Org-code certificate fixed fields | Not supported | Not supported |

**easydoc-extract** behavior:
- `json_schema` valid → closed extraction
- No schema + `prompt_cus` → prompt-driven extraction
- Neither → open extraction (auto-detects all key-value pairs)

## json_schema Format

```json
{
  "type": "object",
  "properties": {
    "字段名": { "type": "string" }
  }
}
```

## Fixed Fields by Mode

**bl-extract** (business license):
图片类型、名称、统一社会信用代码、注册资本、类型、成立日期、法定代表人、营业期限、经营范围、住所

**occ-extract** (org-code certificate):
图片类型、组织机构代码、机构名称、机构类型、地址、有效期、颁发单位、登记号

## Submit Examples

Open extraction:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/extract" \
  -H "api-key: your_apikey_here" \
  -F "files=@doc.pdf" \
  -F "mode=easydoc-extract"
```

Closed extraction:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/extract" \
  -H "api-key: your_apikey_here" \
  -F "files=@doc.pdf" \
  -F "mode=easydoc-extract" \
  -F 'json_schema={"type":"object","properties":{"姓名":{"type":"string"},"金额":{"type":"string"}}}'
```

Business license:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/extract" \
  -H "api-key: your_apikey_here" \
  -F "files=@license.jpg" \
  -F "mode=bl-extract"
```

## Poll Endpoint

`GET /v1/easydoc/extract/{task_id}`

```bash
curl -X GET "https://api.easylink-ai.com/v1/easydoc/extract/b_extract_xxx" \
  -H "api-key: your_apikey_here"
```

## Submit Response

```json
{
  "success": true,
  "data": {
    "task_id": "b_extract_81d006e2-9295-4752-9033-9a37f24bc11d",
    "status": "PROCESSING"
  }
}
```

## Poll Success Response

**easydoc-extract** (flat fields):

```json
{
  "data": {
    "task_id": "b_extract_xxx",
    "status": "SUCCESS",
    "results": [
      {
        "page_number": 1,
        "extract_data": [
          {
            "extracted_fields": {
              "姓名": "张三",
              "金额": "1000元"
            }
          }
        ]
      }
    ]
  }
}
```

**easydoc-extract-flash** (with bounding boxes):

```json
{
  "data": {
    "status": "SUCCESS",
    "results": [
      {
        "page_number": 1,
        "extract_data": [
          {
            "extracted_fields": {
              "姓名": [
                {
                  "bbox": [x, y, w, h],
                  "value": "张三",
                  "category": "text",
                  "source_page": 1,
                  "layout_width": 1200,
                  "layout_height": 1600
                }
              ]
            }
          }
        ]
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
      "page_number": 1,
      "fields": {
        "field_name": "value"
      }
    }
  ],
  "raw": {}
}
```

## Bundled Script Notes

`scripts/easydoc_extract.py` supports all four modes with submit, poll, and poll-only flows.

```bash
python3 scripts/easydoc_extract.py --file ./doc.pdf --mode easydoc-extract
python3 scripts/easydoc_extract.py --file ./doc.pdf --mode easydoc-extract \
  --fields "姓名" "金额" --save ./result.json
python3 scripts/easydoc_extract.py --file ./license.jpg --mode bl-extract
python3 scripts/easydoc_extract.py --poll-only --task-id "b_extract_xxx"
```

Useful options:

- `--output-format normalized|raw`
- `--query-retries 3`
- `--skip-local-checks`
- `--fields FIELD [FIELD ...]` — closed extraction via `json_schema`
- `--prompt TEXT` — prompt-driven extraction (`easydoc-extract` only)
- `--no-poll` — submit only, print task creation response
