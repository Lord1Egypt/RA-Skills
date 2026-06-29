# File Management Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `file-management`

x402 action routes are enabled for this product through `https://www.agentpmt.com/api/external`.

## `access_history`

Action slug: `access-history`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/file-management/actions/access-history/invoke`

Price: `0` credits

View password-protected share access history for a file.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | yes | File UUID returned from upload. |
| `limit` | `integer` | no | Maximum number of access records to return (1-100). |

Sample parameters:

```json
{
  "file_id": "example file id",
  "limit": 1
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File UUID returned from upload.",
    "required": true,
    "type": "string"
  },
  "limit": {
    "description": "Maximum number of access records to return (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `delete`

Action slug: `delete`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/file-management/actions/delete/invoke`

Price: `0` credits

Permanently delete a file from storage.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | yes | File UUID returned from upload. |

Sample parameters:

```json
{
  "file_id": "example file id"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File UUID returned from upload.",
    "required": true,
    "type": "string"
  }
}
```

## `download`

Action slug: `download`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/file-management/actions/download/invoke`

Price: `0` credits

Download file content as base64 for files up to 5MB, or return a signed URL for larger files.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | yes | File UUID returned from upload. |
| `return_content` | `boolean` | no | If true, returns base64 file content for files up to 5MB. Otherwise returns a signed URL. |
| `url_expiration_minutes` | `integer` | no | How long the signed URL should remain valid in minutes when returning a URL (1-10080, default: 10080). |

Sample parameters:

```json
{
  "file_id": "example file id",
  "return_content": true,
  "url_expiration_minutes": 1
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File UUID returned from upload.",
    "required": true,
    "type": "string"
  },
  "return_content": {
    "description": "If true, returns base64 file content for files up to 5MB. Otherwise returns a signed URL.",
    "required": false,
    "type": "boolean"
  },
  "url_expiration_minutes": {
    "description": "How long the signed URL should remain valid in minutes when returning a URL (1-10080, default: 10080).",
    "maximum": 10080,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `extend_expiration`

Action slug: `extend-expiration`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/file-management/actions/extend-expiration/invoke`

Price: `10` credits

Extend a file's expiration date by 7 days from the current expiration.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | yes | File UUID returned from upload. |

Sample parameters:

```json
{
  "file_id": "example file id"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File UUID returned from upload.",
    "required": true,
    "type": "string"
  }
}
```

## `get`

Action slug: `get`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/file-management/actions/get/invoke`

Price: `0` credits

Get file metadata and a fresh signed download URL for a specific file.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | yes | File UUID returned from upload. |
| `url_expiration_minutes` | `integer` | no | How long the signed URL should remain valid in minutes (1-10080, default: 10080). |

Sample parameters:

```json
{
  "file_id": "example file id",
  "url_expiration_minutes": 1
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File UUID returned from upload.",
    "required": true,
    "type": "string"
  },
  "url_expiration_minutes": {
    "description": "How long the signed URL should remain valid in minutes (1-10080, default: 10080).",
    "maximum": 10080,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `list`

Action slug: `list`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/file-management/actions/list/invoke`

Price: `0` credits

List active uploaded files for the current budget with optional filtering and pagination. Returns newest files first and includes cached preview URLs when available.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date_from` | `string` | no | Only files created on or after this date (ISO 8601). |
| `date_to` | `string` | no | Only files created on or before this date (ISO 8601). |
| `limit` | `integer` | no | Maximum number of files to return (1-100). |
| `offset` | `integer` | no | Number of files to skip for pagination. |
| `tags` | `array` | no | Filter to files matching any of these tags. |
| `url_expiration_minutes` | `integer` | no | Requested preview URL validity in minutes when a preview URL must be refreshed (1-10080, default: 10080). |

Sample parameters:

```json
{
  "date_from": "example date from",
  "date_to": "example date to",
  "limit": 1,
  "offset": 0,
  "tags": [
    "example tag"
  ],
  "url_expiration_minutes": 1
}
```

Generated JSON parameter schema:

```json
{
  "date_from": {
    "description": "Only files created on or after this date (ISO 8601).",
    "required": false,
    "type": "string"
  },
  "date_to": {
    "description": "Only files created on or before this date (ISO 8601).",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Maximum number of files to return (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "offset": {
    "description": "Number of files to skip for pagination.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "tags": {
    "description": "Filter to files matching any of these tags.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "url_expiration_minutes": {
    "description": "Requested preview URL validity in minutes when a preview URL must be refreshed (1-10080, default: 10080).",
    "maximum": 10080,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `share`

Action slug: `share`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/file-management/actions/share/invoke`

Price: `5` credits

Create or refresh a password-protected public share link for an existing file.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | yes | File UUID returned from upload. |
| `password_max_minutes` | `integer` | no | Minutes until the auto-generated password expires (1-10). Leave empty for no expiration. |
| `password_max_uses` | `integer` | no | Maximum number of times the auto-generated password can be used (1-10). Leave empty for unlimited uses. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "password_max_minutes": 1,
  "password_max_uses": 1
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File UUID returned from upload.",
    "required": true,
    "type": "string"
  },
  "password_max_minutes": {
    "description": "Minutes until the auto-generated password expires (1-10). Leave empty for no expiration.",
    "maximum": 10,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "password_max_uses": {
    "description": "Maximum number of times the auto-generated password can be used (1-10). Leave empty for unlimited uses.",
    "maximum": 10,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `update_metadata`

Action slug: `update-metadata`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/file-management/actions/update-metadata/invoke`

Price: `5` credits

Update metadata and tags on a file.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `add_tags` | `array` | no | Add these tags while preserving current tags. |
| `file_id` | `string` | yes | File UUID returned from upload. |
| `metadata` | `object` | no | Metadata key-value pairs to merge into existing metadata. |
| `remove_tags` | `array` | no | Remove these tags from the current tag set. |
| `tags` | `array` | no | Replace all existing tags with this list. |

Sample parameters:

```json
{
  "add_tags": [
    "example add tag"
  ],
  "file_id": "example file id",
  "metadata": {},
  "remove_tags": [
    "example remove tag"
  ],
  "tags": [
    "example tag"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "add_tags": {
    "description": "Add these tags while preserving current tags.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "file_id": {
    "description": "File UUID returned from upload.",
    "required": true,
    "type": "string"
  },
  "metadata": {
    "description": "Metadata key-value pairs to merge into existing metadata.",
    "required": false,
    "type": "object"
  },
  "remove_tags": {
    "description": "Remove these tags from the current tag set.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "tags": {
    "description": "Replace all existing tags with this list.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```

## `upload_large`

Action slug: `upload-large`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/file-management/actions/upload-large/invoke`

Price: `20` credits

Generate a signed upload URL for a file over 10MB and up to 100MB. After receiving the URL, perform a PUT request with the exact file bytes and returned headers.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content_length_bytes` | `integer` | yes | Exact file size in bytes. Must match the Content-Length header on PUT. File size must be over 10MB and up to 100MB. |
| `content_type` | `string` | no | MIME type of the file. Default: application/octet-stream. |
| `expiration_days` | `integer` | no | Days until file expires and is automatically deleted (1-7). Default: 7. |
| `filename` | `string` | no | Original filename including extension. If omitted, a filename is auto-generated. |
| `metadata` | `object` | no | Custom metadata as key-value pairs to attach to the file. |
| `password_max_minutes` | `integer` | no | Minutes until the auto-generated share password expires (1-10). Only relevant when shared is true. |
| `password_max_uses` | `integer` | no | Maximum number of uses for the auto-generated share password (1-10). Only relevant when shared is true. |
| `shared` | `boolean` | no | Whether the file should be shareable through a password-protected public URL. |
| `tags` | `array` | no | Tags for categorization. |

Sample parameters:

```json
{
  "content_length_bytes": 1,
  "content_type": "Draft marketing copy to check for banned phrases.",
  "expiration_days": 1,
  "filename": "example filename",
  "metadata": {},
  "password_max_minutes": 1,
  "password_max_uses": 1,
  "shared": true
}
```

Generated JSON parameter schema:

```json
{
  "content_length_bytes": {
    "description": "Exact file size in bytes. Must match the Content-Length header on PUT. File size must be over 10MB and up to 100MB.",
    "exclusiveMinimum": 10485760,
    "maximum": 104857600,
    "required": true,
    "type": "integer"
  },
  "content_type": {
    "description": "MIME type of the file. Default: application/octet-stream.",
    "required": false,
    "type": "string"
  },
  "expiration_days": {
    "description": "Days until file expires and is automatically deleted (1-7). Default: 7.",
    "maximum": 7,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "filename": {
    "description": "Original filename including extension. If omitted, a filename is auto-generated.",
    "required": false,
    "type": "string"
  },
  "metadata": {
    "description": "Custom metadata as key-value pairs to attach to the file.",
    "required": false,
    "type": "object"
  },
  "password_max_minutes": {
    "description": "Minutes until the auto-generated share password expires (1-10). Only relevant when shared is true.",
    "maximum": 10,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "password_max_uses": {
    "description": "Maximum number of uses for the auto-generated share password (1-10). Only relevant when shared is true.",
    "maximum": 10,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "shared": {
    "description": "Whether the file should be shareable through a password-protected public URL.",
    "required": false,
    "type": "boolean"
  },
  "tags": {
    "description": "Tags for categorization.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```

## `upload_standard`

Action slug: `upload-standard`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/file-management/actions/upload-standard/invoke`

Price: `10` credits

Generate a signed upload URL for a file up to 10MB. After receiving the URL, perform a PUT request with the exact file bytes and returned headers.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content_length_bytes` | `integer` | yes | Exact file size in bytes. Must match the Content-Length header on PUT. Range: 1-10485760 (10MB). |
| `content_type` | `string` | no | MIME type of the file. Default: application/octet-stream. |
| `expiration_days` | `integer` | no | Days until file expires and is automatically deleted (1-7). Default: 7. |
| `filename` | `string` | no | Original filename including extension. If omitted, a filename is auto-generated. |
| `metadata` | `object` | no | Custom metadata as key-value pairs to attach to the file. |
| `password_max_minutes` | `integer` | no | Minutes until the auto-generated share password expires (1-10). Only relevant when shared is true. |
| `password_max_uses` | `integer` | no | Maximum number of uses for the auto-generated share password (1-10). Only relevant when shared is true. |
| `shared` | `boolean` | no | Whether the file should be shareable through a password-protected public URL. |
| `tags` | `array` | no | Tags for categorization. |

Sample parameters:

```json
{
  "content_length_bytes": 1,
  "content_type": "Draft marketing copy to check for banned phrases.",
  "expiration_days": 1,
  "filename": "example filename",
  "metadata": {},
  "password_max_minutes": 1,
  "password_max_uses": 1,
  "shared": true
}
```

Generated JSON parameter schema:

```json
{
  "content_length_bytes": {
    "description": "Exact file size in bytes. Must match the Content-Length header on PUT. Range: 1-10485760 (10MB).",
    "maximum": 10485760,
    "minimum": 1,
    "required": true,
    "type": "integer"
  },
  "content_type": {
    "description": "MIME type of the file. Default: application/octet-stream.",
    "required": false,
    "type": "string"
  },
  "expiration_days": {
    "description": "Days until file expires and is automatically deleted (1-7). Default: 7.",
    "maximum": 7,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "filename": {
    "description": "Original filename including extension. If omitted, a filename is auto-generated.",
    "required": false,
    "type": "string"
  },
  "metadata": {
    "description": "Custom metadata as key-value pairs to attach to the file.",
    "required": false,
    "type": "object"
  },
  "password_max_minutes": {
    "description": "Minutes until the auto-generated share password expires (1-10). Only relevant when shared is true.",
    "maximum": 10,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "password_max_uses": {
    "description": "Maximum number of uses for the auto-generated share password (1-10). Only relevant when shared is true.",
    "maximum": 10,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "shared": {
    "description": "Whether the file should be shareable through a password-protected public URL.",
    "required": false,
    "type": "boolean"
  },
  "tags": {
    "description": "Tags for categorization.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```
