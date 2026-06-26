# Feishu API Implementation Notes

This document explains the implementation details for the feishu-bitable-attachment skill.

## Part 1: Current Main Implementation

### Core Design Principle

**Upload to bitable_file upload point, not reuse IM/Drive file_token.**

When you upload a file to Feishu IM (chat) or Drive, you get a `file_token`. However, **this token cannot be directly written to a Bitable attachment field** because:

1. **Different storage contexts**: IM, Drive, and Bitable have separate file storage contexts
2. **Permission boundaries**: Cross-application file access requires explicit upload
3. **Reference counting**: Feishu tracks file usage per application for quota
4. **Security model**: Prevents cross-application data leakage

### Material Upload Flow

The correct flow for Bitable attachments:

```
POST /open-apis/drive/v1/upload
parent_type = bitable_file         ← Upload destination type
parent_node = {app_token}          ← Target Bitable
extra = {"drive_route_token": "{app_token}"}  ← Route through Bitable storage
file = <file content>
```

The returned `file_token` is then valid for Bitable attachment fields:

```json
{
  "fields": {
    "fld_xxxxx": [
      {"file_token": "vob_xxxxx"}
    ]
  }
}
```

### API Endpoints - Main Implementation

#### Authentication
```
POST /open-apis/auth/v3/tenant_access_token/internal
Body: {"app_id": "...", "app_secret": "..."}
Response: {"tenant_access_token": "...", "expire": 7200}
```

#### Direct Upload (≤20MB) - Main Implementation
```
POST /open-apis/drive/v1/upload
Content-Type: multipart/form-data

Multipart Fields (explicit and fixed):
  file: <file content>                    ← Binary file data
  file_name: <filename>                   ← Explicit filename field
  size: <file_size_bytes>                 ← Explicit size field (as string)
  parent_type: bitable_file               ← Required: upload destination type
  parent_node: {app_token}                ← Required: target Bitable app token
  extra: {"drive_route_token": "..."}     ← Required: route through Bitable storage
```

**Implementation note**: The current implementation uses `file` as the multipart field name for file content. This is the standard field name for Feishu Drive API uploads.

#### Chunked Upload (>20MB) - Main Implementation

**Step 1: Prepare**
```
POST /open-apis/drive/v1/chunked_upload/prepare
Content-Type: application/json

{
  "file_name": "...",
  "file_size": ...,
  "parent_type": "bitable_file",
  "parent_node": "{app_token}",
  "drive_route_token": "{app_token}"
}
Response: {"upload_id": "..."}
```

**Step 2: Upload Part**
```
POST /open-apis/drive/v1/chunked_upload
Content-Type: multipart/form-data

Multipart Fields:
  file: <chunk bytes>                     ← Binary chunk data
  upload_id: {upload_id}                  ← Session ID from prepare step
  part_number: {n}                        ← Part number (1-indexed)
  file_name: {filename}                   ← Filename for tracking
Response: {"etag": "..."}
```

**Step 3: Finish**
```
POST /open-apis/drive/v1/chunked_upload/finish
Content-Type: application/json

{
  "upload_id": "...",
  "parts": [{"index": 1, "etag": "..."}, ...],
  "file_name": "...",
  "parent_type": "bitable_file",
  "parent_node": "{app_token}",
  "drive_route_token": "{app_token}"
}
Response: {"file_token": "..."}
```

### Bitable APIs

**List Tables**
```
GET /open-apis/bitable/v1/apps/{app_token}/tables
Response: {"data": {"items": [{"table_id": "...", "name": "..."}]}}
```

**List Fields**
```
GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields
Response: {"data": {"items": [{"field_id": "...", "name": "...", "type": "..."}]}}
```

**Get Record**
```
GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}
Response: {"data": {"fields": {"{field_id}": [...]}}}
```

**Update Record**
```
PUT /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}
{
  "fields": {
    "{field_id}": [{"file_token": "vob..."}, ...]
  }
}
```

**Create Record**
```
POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create
{
  "records": [{"fields": {"{field_id}": [{"file_token": "vob..."}]}}]
}
```

**Search Records**
```
POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search
{
  "filter": [{"field_id": "...", "operator": "is", "value": "..."}]
}
```

---

## Part 2: Compatibility Notes

### API Paths

The current implementation uses the standard Feishu Drive upload API paths:

- Direct upload: `/open-apis/drive/v1/upload`
- Chunked prepare: `/open-apis/drive/v1/chunked_upload/prepare`
- Chunked upload: `/open-apis/drive/v1/chunked_upload`
- Chunked finish: `/open-apis/drive/v1/chunked_upload/finish`

These are the documented paths in Feishu's official API documentation.

### Known Environment Differences

#### Multipart Field Name for File Content

The current implementation uses `file` as the field name:

```python
files = {
    "file": (filename, open(file_path, "rb"), "application/octet-stream")
}
```

Some older Feishu API versions or different regions may use:
- `media` - less common, used in some media-specific endpoints
- `upload_file` - rarely used

**If direct upload fails** with the default `file` field name, check the error message. If it indicates an invalid field, modify `upload_to_bitable.py` function `upload_small_file()` to use the appropriate field name for your environment.

#### API Response Structure

The current implementation expects responses in this format:

```json
{
  "code": 0,              // 0 = success, non-zero = error
  "msg": "...",           // Human-readable message
  "data": {               // Actual response data
    "file_token": "..."
  }
}
```

The `parse_file_token()` function in `upload_to_bitable.py` extracts `file_token` from `data.file_token`. If your environment returns a different structure, this function may need adjustment.

#### Bitable Attachment Field Format

The current implementation uses this format for writing attachments:

```json
{
  "fields": {
    "fld_xxx": [
      {"file_token": "vob_xxx"},
      {"file_token": "vob_yyy"}
    ]
  }
}
```

This is the standard format for Feishu Bitable attachment fields. Some older API versions may have different requirements.

### Fallback Strategy

If the main implementation (`/open-apis/drive/v1/files/*`) fails in your environment:

1. **Check error messages** - Look for specific error codes or messages
2. **Verify API permissions** - Ensure your app has Drive and Bitable permissions
3. **Try legacy paths** - As a last resort, update `common.py` to use `LEGACY_API_*` constants
4. **Contact Feishu support** - API paths may vary by tenant or region

---

## Error Handling

The skill uses custom exception classes:

| Exception | Error Type | When Raised |
|-----------|------------|-------------|
| `SkillInputError` | `input_error` | Invalid input parameters |
| `SkillFileNotFoundError` | `file_not_found` | Local file does not exist |
| `SkillDownloadError` | `download_failed` | URL or Feishu download fails |
| `FeishuAuthError` | `auth_error` | Token acquisition fails |
| `FeishuUploadError` | `upload_error` | File upload fails |
| `BitableResolveError` | `resolve_error` | Table/field/record lookup fails |
| `BitableUpdateError` | `update_error` | Record create/update fails |

Each exception includes a human-readable message and optional details dictionary.

## Testing Recommendations

Before using in production:

1. **Test with a small file first** (≤20MB, uses direct upload)
2. **Verify table/field resolution** with both IDs and names
3. **Test append vs replace mode** to ensure correct behavior
4. **Check error messages** by intentionally using invalid parameters
5. **Run syntax check**: `python -m py_compile scripts/*.py`

## Base URL Configuration

| Region | Base URL |
|--------|----------|
| China (国内) | `https://open.feishu.cn` |
| International (海外) | `https://open.larksuite.com` |

Configure via environment variable:
```bash
export FEISHU_BASE_URL=https://open.feishu.cn
```
