# Binary To/From File Converter Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `binary-to-from-file-converter`

x402 availability: not enabled for this product.

## `base64_to_binary`

Action slug: `base64-to-binary`

Price: `10` credits

Convert a base64-encoded string to a binary (0s and 1s) string representation.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | Base64-encoded string to convert to binary representation. |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "Base64-encoded string to convert to binary representation.",
    "required": true,
    "type": "string"
  }
}
```

## `base64_to_file`

Action slug: `base64-to-file`

Price: `10` credits

Decode a base64 string and save it as a file in cloud storage with a signed download URL.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content_type` | `string` | no | MIME type for the created file (e.g., 'image/png', 'application/pdf'). |
| `expiration_days` | `integer` | no | Days until file expires (1-7). |
| `filename` | `string` | yes | Name for the created file (e.g., 'output.png'). |
| `input` | `string` | yes | Base64-encoded file content to decode and save. |
| `store_file` | `boolean` | no | Store output as a file in cloud storage (recommended for file management access). |

Sample parameters:

```json
{
  "content_type": "application/octet-stream",
  "expiration_days": 7,
  "filename": "example filename",
  "input": "example input",
  "store_file": true
}
```

Generated JSON parameter schema:

```json
{
  "content_type": {
    "default": "application/octet-stream",
    "description": "MIME type for the created file (e.g., 'image/png', 'application/pdf').",
    "required": false,
    "type": "string"
  },
  "expiration_days": {
    "default": 7,
    "description": "Days until file expires (1-7).",
    "maximum": 7,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "filename": {
    "description": "Name for the created file (e.g., 'output.png').",
    "required": true,
    "type": "string"
  },
  "input": {
    "description": "Base64-encoded file content to decode and save.",
    "required": true,
    "type": "string"
  },
  "store_file": {
    "default": true,
    "description": "Store output as a file in cloud storage (recommended for file management access).",
    "required": false,
    "type": "boolean"
  }
}
```

## `base64_to_hex`

Action slug: `base64-to-hex`

Price: `10` credits

Convert a base64-encoded string to hexadecimal representation.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | Base64-encoded string to convert to hex. |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "Base64-encoded string to convert to hex.",
    "required": true,
    "type": "string"
  }
}
```

## `binary_to_base64`

Action slug: `binary-to-base64`

Price: `10` credits

Convert a binary string (0s and 1s) back to base64 encoding.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | Binary string of 0s and 1s (length must be a multiple of 8; spaces between bytes are allowed). |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "Binary string of 0s and 1s (length must be a multiple of 8; spaces between bytes are allowed).",
    "required": true,
    "type": "string"
  }
}
```

## `file_to_base64`

Action slug: `file-to-base64`

Price: `10` credits

Read a previously uploaded file from cloud storage and return its contents as a base64-encoded string. Maximum file size is 10MB.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | yes | File ID of the uploaded file to read. |

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
    "description": "File ID of the uploaded file to read.",
    "required": true,
    "type": "string"
  }
}
```

## `hex_to_base64`

Action slug: `hex-to-base64`

Price: `10` credits

Convert a hexadecimal string to base64 encoding.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | Hexadecimal string to convert to base64 (even number of characters, 0-9 and a-f). |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "Hexadecimal string to convert to base64 (even number of characters, 0-9 and a-f).",
    "required": true,
    "type": "string"
  }
}
```
