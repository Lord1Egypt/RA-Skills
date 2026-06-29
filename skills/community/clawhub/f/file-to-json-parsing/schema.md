# File To JSON Parsing Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `file-to-json-parsing`

x402 availability: not enabled for this product.

## `extract-csv`

Action slug: `extract-csv`

Price: `5` credits

Parse a CSV file into structured row data.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | File ID from cloud storage. |
| `input_base64` | `string` | no | Base64-encoded file content. |
| `max_rows` | `integer` | no | Maximum rows to extract. |
| `output_field` | `string` | no | Key name for the extracted data in the response. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "input_base64": "example input base64",
  "max_rows": 1000,
  "output_field": "data"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File ID from cloud storage.",
    "required": false,
    "type": "string"
  },
  "input_base64": {
    "description": "Base64-encoded file content.",
    "required": false,
    "type": "string"
  },
  "max_rows": {
    "default": 1000,
    "description": "Maximum rows to extract.",
    "maximum": 100000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "output_field": {
    "default": "data",
    "description": "Key name for the extracted data in the response.",
    "required": false,
    "type": "string"
  }
}
```

## `extract-html`

Action slug: `extract-html`

Price: `5` credits

Parse an HTML file, extracting text content and/or table data.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | File ID from cloud storage. |
| `include_tables` | `boolean` | no | Include extracted table data. |
| `include_text` | `boolean` | no | Include extracted text content. |
| `input_base64` | `string` | no | Base64-encoded file content. |
| `max_rows` | `integer` | no | Maximum rows per table. |
| `output_field` | `string` | no | Key name for the extracted data in the response. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "include_tables": true,
  "include_text": true,
  "input_base64": "example input base64",
  "max_rows": 1000,
  "output_field": "data"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File ID from cloud storage.",
    "required": false,
    "type": "string"
  },
  "include_tables": {
    "default": true,
    "description": "Include extracted table data.",
    "required": false,
    "type": "boolean"
  },
  "include_text": {
    "default": true,
    "description": "Include extracted text content.",
    "required": false,
    "type": "boolean"
  },
  "input_base64": {
    "description": "Base64-encoded file content.",
    "required": false,
    "type": "string"
  },
  "max_rows": {
    "default": 1000,
    "description": "Maximum rows per table.",
    "maximum": 100000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "output_field": {
    "default": "data",
    "description": "Key name for the extracted data in the response.",
    "required": false,
    "type": "string"
  }
}
```

## `extract-ics`

Action slug: `extract-ics`

Price: `5` credits

Parse an ICS calendar file and extract events with summary, start, end, location, and description.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | File ID from cloud storage. |
| `input_base64` | `string` | no | Base64-encoded file content. |
| `output_field` | `string` | no | Key name for the extracted data in the response. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "input_base64": "example input base64",
  "output_field": "data"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File ID from cloud storage.",
    "required": false,
    "type": "string"
  },
  "input_base64": {
    "description": "Base64-encoded file content.",
    "required": false,
    "type": "string"
  },
  "output_field": {
    "default": "data",
    "description": "Key name for the extracted data in the response.",
    "required": false,
    "type": "string"
  }
}
```

## `extract-json`

Action slug: `extract-json`

Price: `5` credits

Parse a JSON file and return its contents as structured data.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | File ID from cloud storage. |
| `input_base64` | `string` | no | Base64-encoded file content. |
| `output_field` | `string` | no | Key name for the extracted data in the response. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "input_base64": "example input base64",
  "output_field": "data"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File ID from cloud storage.",
    "required": false,
    "type": "string"
  },
  "input_base64": {
    "description": "Base64-encoded file content.",
    "required": false,
    "type": "string"
  },
  "output_field": {
    "default": "data",
    "description": "Key name for the extracted data in the response.",
    "required": false,
    "type": "string"
  }
}
```

## `extract-ods`

Action slug: `extract-ods`

Price: `5` credits

Parse an OpenDocument Spreadsheet (.ods) file, returning sheets with row data.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | File ID from cloud storage. |
| `input_base64` | `string` | no | Base64-encoded file content. |
| `max_rows` | `integer` | no | Maximum rows per sheet. |
| `output_field` | `string` | no | Key name for the extracted data in the response. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "input_base64": "example input base64",
  "max_rows": 1000,
  "output_field": "data"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File ID from cloud storage.",
    "required": false,
    "type": "string"
  },
  "input_base64": {
    "description": "Base64-encoded file content.",
    "required": false,
    "type": "string"
  },
  "max_rows": {
    "default": 1000,
    "description": "Maximum rows per sheet.",
    "maximum": 100000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "output_field": {
    "default": "data",
    "description": "Key name for the extracted data in the response.",
    "required": false,
    "type": "string"
  }
}
```

## `extract-pdf`

Action slug: `extract-pdf`

Price: `5` credits

Extract text and/or tables from a PDF document, page by page.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | File ID from cloud storage. |
| `include_tables` | `boolean` | no | Include table extraction per page. |
| `include_text` | `boolean` | no | Include text extraction per page. |
| `input_base64` | `string` | no | Base64-encoded file content. |
| `max_pages` | `integer` | no | Maximum pages to process. |
| `output_field` | `string` | no | Key name for the extracted data in the response. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "include_tables": true,
  "include_text": true,
  "input_base64": "example input base64",
  "max_pages": 50,
  "output_field": "data"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File ID from cloud storage.",
    "required": false,
    "type": "string"
  },
  "include_tables": {
    "default": true,
    "description": "Include table extraction per page.",
    "required": false,
    "type": "boolean"
  },
  "include_text": {
    "default": true,
    "description": "Include text extraction per page.",
    "required": false,
    "type": "boolean"
  },
  "input_base64": {
    "description": "Base64-encoded file content.",
    "required": false,
    "type": "string"
  },
  "max_pages": {
    "default": 50,
    "description": "Maximum pages to process.",
    "maximum": 1000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "output_field": {
    "default": "data",
    "description": "Key name for the extracted data in the response.",
    "required": false,
    "type": "string"
  }
}
```

## `extract-rtf`

Action slug: `extract-rtf`

Price: `5` credits

Parse an RTF (Rich Text Format) file and extract plain text.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | File ID from cloud storage. |
| `input_base64` | `string` | no | Base64-encoded file content. |
| `output_field` | `string` | no | Key name for the extracted data in the response. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "input_base64": "example input base64",
  "output_field": "data"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File ID from cloud storage.",
    "required": false,
    "type": "string"
  },
  "input_base64": {
    "description": "Base64-encoded file content.",
    "required": false,
    "type": "string"
  },
  "output_field": {
    "default": "data",
    "description": "Key name for the extracted data in the response.",
    "required": false,
    "type": "string"
  }
}
```

## `extract-text`

Action slug: `extract-text`

Price: `5` credits

Read a plain text file and return its contents.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | File ID from cloud storage. |
| `input_base64` | `string` | no | Base64-encoded file content. |
| `output_field` | `string` | no | Key name for the extracted data in the response. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "input_base64": "example input base64",
  "output_field": "data"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File ID from cloud storage.",
    "required": false,
    "type": "string"
  },
  "input_base64": {
    "description": "Base64-encoded file content.",
    "required": false,
    "type": "string"
  },
  "output_field": {
    "default": "data",
    "description": "Key name for the extracted data in the response.",
    "required": false,
    "type": "string"
  }
}
```

## `extract-xls`

Action slug: `extract-xls`

Price: `5` credits

Parse a legacy Excel (.xls) file, returning sheets with row data.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | File ID from cloud storage. |
| `input_base64` | `string` | no | Base64-encoded file content. |
| `max_rows` | `integer` | no | Maximum rows per sheet. |
| `output_field` | `string` | no | Key name for the extracted data in the response. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "input_base64": "example input base64",
  "max_rows": 1000,
  "output_field": "data"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File ID from cloud storage.",
    "required": false,
    "type": "string"
  },
  "input_base64": {
    "description": "Base64-encoded file content.",
    "required": false,
    "type": "string"
  },
  "max_rows": {
    "default": 1000,
    "description": "Maximum rows per sheet.",
    "maximum": 100000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "output_field": {
    "default": "data",
    "description": "Key name for the extracted data in the response.",
    "required": false,
    "type": "string"
  }
}
```

## `extract-xlsx`

Action slug: `extract-xlsx`

Price: `5` credits

Parse a modern Excel (.xlsx) file, returning sheets with row data.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | File ID from cloud storage. |
| `input_base64` | `string` | no | Base64-encoded file content. |
| `max_rows` | `integer` | no | Maximum rows per sheet. |
| `output_field` | `string` | no | Key name for the extracted data in the response. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "input_base64": "example input base64",
  "max_rows": 1000,
  "output_field": "data"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File ID from cloud storage.",
    "required": false,
    "type": "string"
  },
  "input_base64": {
    "description": "Base64-encoded file content.",
    "required": false,
    "type": "string"
  },
  "max_rows": {
    "default": 1000,
    "description": "Maximum rows per sheet.",
    "maximum": 100000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "output_field": {
    "default": "data",
    "description": "Key name for the extracted data in the response.",
    "required": false,
    "type": "string"
  }
}
```

## `file-to-base64`

Action slug: `file-to-base64`

Price: `5` credits

Convert a file to base64-encoded string. File must be 10 MB or smaller for inline return.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | File ID from cloud storage. |
| `input_base64` | `string` | no | Base64-encoded file content. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "input_base64": "example input base64"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "File ID from cloud storage.",
    "required": false,
    "type": "string"
  },
  "input_base64": {
    "description": "Base64-encoded file content.",
    "required": false,
    "type": "string"
  }
}
```
