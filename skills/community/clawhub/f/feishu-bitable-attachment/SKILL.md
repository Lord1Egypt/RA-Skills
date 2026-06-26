---
name: feishu-bitable-attachment
description: uploads files from local/url/feishu-message to any accessible feishu bitable attachment field via material upload flow (parent_type=bitable_file)
---

## Overview

This skill uploads files to Feishu (Lark) Bitable attachment fields through the **material upload flow**:

1. Get source file (local copy, URL download, or Feishu message download)
2. Upload to Bitable upload endpoint with `parent_type=bitable_file`
3. Get `file_token` from upload response
4. Create/Update record with attachment field

**Key design**: This is a **general-purpose skill** for ANY Bitable your app can access. Nothing is hardcoded.

## Verification Status

### Local Tests Passed
- [x] All Python modules pass syntax check (py_compile)
- [x] All custom exception classes are properly imported
- [x] File not found raises `SkillFileNotFoundError` (not NameError)
- [x] Input validation raises `SkillInputError` for missing parameters
- [x] All payload example files are valid JSON
- [x] `main.py --help` runs successfully

### Requires Real Environment Verification
- [ ] Bitable record update/create response format
- [ ] Table/field listing API response structure
- [ ] Record search API filter syntax

If any API calls fail in your environment, check `references/feishu-api-notes.md` for extensibility points.

## Supported Source Types

| Type | Description | Example |
|------|-------------|---------|
| `local` | Local file path | `{"type": "local", "ref": "/tmp/file.pdf"}` |
| `url` | Download from HTTP(S) URL | `{"type": "url", "ref": "https://example.com/file.pdf"}` |
| `feishu_message` | Feishu message attachment | `{"type": "feishu_message", "ref": {"file_key": "file_xxx"}}` |

## Target Resolution

This skill supports flexible target specification to work with any Bitable:

### Table Specification (priority: table_id > table_name)
- Provide `table_id` directly for fastest resolution
- Or provide `table_name` for automatic lookup (lists all tables and matches by name)

### Field Specification (priority: field_id > field_name)
- Provide `field_id` directly for fastest resolution
- Or provide `field_name` for automatic lookup (lists all fields and matches by name)

### Record Specification
- Provide `record_id` to update existing record
- Or provide `lookup` to search for record by field value
- Or omit both to create new record

## Input JSON Structure

```json
{
  "target": {
    "app_token": "bascxxxxxxxxxxxxx",
    "table_id": "tblxxxxxxxxxx",
    "table_name": "",
    "record_id": "recxxxxxxxxxx",
    "field_id": "fldxxxxxxxxxx",
    "field_name": "附件",
    "lookup": {
      "field_name": "合同编号",
      "field_id": "",
      "value": "HT-2026-001"
    },
    "allow_create_if_lookup_missing": false
  },
  "source": {
    "type": "local",
    "ref": "/path/to/file.pdf"
  },
  "append": true
}
```

### Target Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `app_token` | Yes | Bitable app token (basc...) |
| `table_id` | No* | Table ID (tbl...). *Required if table_name not provided |
| `table_name` | No* | Table display name. *Required if table_id not provided |
| `record_id` | No | Record ID (rec...). Leave empty to create new record |
| `field_id` | No* | Field ID. *Required if field_name not provided |
| `field_name` | No* | Field display name. *Required if field_id not provided |
| `lookup` | No | Config to find record_id by searching |
| `allow_create_if_lookup_missing` | No | If true, create new record when lookup finds nothing |

### Lookup Config

```json
"lookup": {
  "field_name": "合同编号",
  "field_id": "",
  "value": "HT-2026-001"
}
```

### Source Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `type` | Yes | One of: `local`, `url`, `feishu_message` |
| `ref` | Yes | local: file path / url: download URL / feishu_message: `{file_key, filename}` |

### Append Mode

| Value | Behavior |
|-------|----------|
| `true` | Read existing attachments, append new file to the list |
| `false` | Replace attachment field with new file only |

## Upload Flow

### Small Files (≤20MB)
Direct upload to material endpoint:
```
POST /open-apis/drive/v1/upload
multipart/form-data fields:
  - file: <file content>
  - file_name: filename
  - size: file size in bytes
  - parent_type: bitable_file
  - parent_node: {app_token}
  - extra: {"drive_route_token": "{app_token}"}
```

### Large Files (>20MB)
Chunked upload in 5MB parts:
1. `POST /open-apis/drive/v1/chunked_upload/prepare` → upload_id
2. `POST /open-apis/drive/v1/chunked_upload` (per part) → etag
3. `POST /open-apis/drive/v1/chunked_upload/finish` → file_token

## Environment Variables

Set these before running:

```bash
export FEISHU_APP_ID=your_app_id
export FEISHU_APP_SECRET=your_app_secret
export FEISHU_BASE_URL=https://open.feishu.cn  # optional
```

## Usage Examples

### Local file with known record_id
```bash
python scripts/main.py --input payload.local.json
```

### URL download with replace mode
```bash
python scripts/main.py --input payload.url.json
```

### Feishu message attachment
```bash
python scripts/main.py --input payload.feishu_message.json
```

### Auto-resolve table by name
```bash
python scripts/main.py --input payload.table_name.json
```

### Lookup record by field value
```bash
python scripts/main.py --input payload.lookup.json
```

### Create new record with attachment
```bash
python scripts/main.py --input payload.create_record.json
```

## Basic Verification

Run syntax check before use:

```bash
python -m py_compile scripts/*.py
```

This verifies:
- All Python modules have valid syntax
- No undefined variables or imports

## Output

### Success
```json
{
  "ok": true,
  "file_token": "vobxxxxxxxxxx",
  "app_token": "bascxxxxxxxxxx",
  "table_id": "tblxxxxxxxxxx",
  "table_name": "合同归档",
  "record_id": "recxxxxxxxxxx",
  "field_name": "附件",
  "field_id": "fldxxxxxxxxxx",
  "upload_type": "direct",
  "attachment_count": 3,
  "mode": "append",
  "message": "Successfully uploaded 'report.pdf'..."
}
```

### Error
```json
{
  "ok": false,
  "error": "Table 'xxx' not found. Available tables: 表 1, 表 2",
  "error_type": "resolve_error"
}
```

## Common Errors

| Error Type | Cause | Solution |
|------------|-------|----------|
| `file_not_found` | Local file does not exist | Check file path |
| `download_failed` | URL download failed | Verify URL accessibility |
| `input_error` | Invalid parameters | Check input JSON structure |
| `auth_error` | Invalid credentials | Check FEISHU_APP_ID/SECRET |
| `upload_error` | Upload failed | Check app permissions |
| `resolve_error` | Table/field/record not found | Verify names or IDs |
| `update_error` | Record update failed | Check record exists |

## Why This Skill Works with Any Bitable

This skill is **not hardcoded** to a specific Bitable:

1. **Dynamic app_token**: Read from input, not hardcoded
2. **Dynamic table resolution**: Supports table_id (direct) or table_name (API lookup)
3. **Dynamic field resolution**: Supports field_id (direct) or field_name (API lookup)
4. **Dynamic record resolution**: Supports record_id, lookup search, or create-new mode

## References

See `references/feishu-api-notes.md` for:
- Why file_token from IM/Drive cannot be reused directly
- Why upload to bitable_file upload point is required
- API implementation notes and extensibility points
- Known uncertainties that may need environment-specific verification
