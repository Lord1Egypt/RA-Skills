# File Utilities and Editing Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `file-utilities-and-editing`

x402 availability: not enabled for this product.

## `file-base64-decode`

Action slug: `file-base64-decode`

Price: `5` credits

Decode a base64 string back to UTF-8 text.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | A valid base64-encoded string to decode |

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
    "description": "A valid base64-encoded string to decode",
    "required": true,
    "type": "string"
  }
}
```

## `file-base64-encode`

Action slug: `file-base64-encode`

Price: `5` credits

Encode a text string to base64 using UTF-8 encoding.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | The text to encode to base64 |

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
    "description": "The text to encode to base64",
    "required": true,
    "type": "string"
  }
}
```

## `file-csv-to-table`

Action slug: `file-csv-to-table`

Price: `5` credits

Parse CSV content and render it as a formatted ASCII table. The first row is treated as headers.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | CSV content as a string (e.g., 'Name,Age,City\nAlice,30,New York') |

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
    "description": "CSV content as a string (e.g., 'Name,Age,City\\nAlice,30,New York')",
    "required": true,
    "type": "string"
  }
}
```

## `file-extension-from-mime`

Action slug: `file-extension-from-mime`

Price: `5` credits

Look up the standard file extension for a given MIME type.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | A MIME type string (e.g., 'image/png', 'application/pdf') |

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
    "description": "A MIME type string (e.g., 'image/png', 'application/pdf')",
    "required": true,
    "type": "string"
  }
}
```

## `file-hash-generate`

Action slug: `file-hash-generate`

Price: `5` credits

Generate a cryptographic hash of the provided text content.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `hash_algorithm` | `string` | no | Hash algorithm to use: md5, sha1, sha256, or sha512 |
| `input` | `string` | yes | The content to hash |

Sample parameters:

```json
{
  "hash_algorithm": "sha256",
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "hash_algorithm": {
    "default": "sha256",
    "description": "Hash algorithm to use: md5, sha1, sha256, or sha512",
    "enum": [
      "md5",
      "sha1",
      "sha256",
      "sha512"
    ],
    "required": false,
    "type": "string"
  },
  "input": {
    "description": "The content to hash",
    "required": true,
    "type": "string"
  }
}
```

## `file-json-minify`

Action slug: `file-json-minify`

Price: `5` credits

Remove all unnecessary whitespace from a JSON string to produce the most compact representation.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | A valid JSON string to minify |

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
    "description": "A valid JSON string to minify",
    "required": true,
    "type": "string"
  }
}
```

## `file-json-pretty-print`

Action slug: `file-json-pretty-print`

Price: `5` credits

Format a compact JSON string with indentation for readability.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `indent` | `integer` | no | Number of spaces per indentation level (0-8) |
| `input` | `string` | yes | A valid JSON string to format |

Sample parameters:

```json
{
  "indent": 2,
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "indent": {
    "default": 2,
    "description": "Number of spaces per indentation level (0-8)",
    "maximum": 8,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "input": {
    "description": "A valid JSON string to format",
    "required": true,
    "type": "string"
  }
}
```

## `file-mime-type-detect`

Action slug: `file-mime-type-detect`

Price: `5` credits

Detect the MIME type of a file based on its filename/extension. Supports documents, images, audio, video, archives, and programming languages.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | The filename to analyze (e.g., 'report.pdf', 'photo.jpg') |

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
    "description": "The filename to analyze (e.g., 'report.pdf', 'photo.jpg')",
    "required": true,
    "type": "string"
  }
}
```

## `file-path-join`

Action slug: `file-path-join`

Price: `5` credits

Join multiple path components into a single path. Provide components as a comma-separated string in input, or use input, input2, and input3 fields for up to three components. At least 2 components required.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | First path component, or a comma-separated list of all components |
| `input2` | `string` | no | Second path component (when not using comma separation) |
| `input3` | `string` | no | Third path component (when not using comma separation) |

Sample parameters:

```json
{
  "input": "example input",
  "input2": "example input2",
  "input3": "example input3"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "First path component, or a comma-separated list of all components",
    "required": true,
    "type": "string"
  },
  "input2": {
    "description": "Second path component (when not using comma separation)",
    "required": false,
    "type": "string"
  },
  "input3": {
    "description": "Third path component (when not using comma separation)",
    "required": false,
    "type": "string"
  }
}
```

## `file-path-normalize`

Action slug: `file-path-normalize`

Price: `5` credits

Clean up a file path by resolving '..', '.', and redundant separators.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | A file path to normalize (e.g., '/home/user/../user/./documents//file.txt') |

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
    "description": "A file path to normalize (e.g., '/home/user/../user/./documents//file.txt')",
    "required": true,
    "type": "string"
  }
}
```

## `file-path-parse`

Action slug: `file-path-parse`

Price: `5` credits

Break a file path into its component parts: directory, filename, name, and extension.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | A file path to parse (e.g., '/home/user/documents/report.pdf') |

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
    "description": "A file path to parse (e.g., '/home/user/documents/report.pdf')",
    "required": true,
    "type": "string"
  }
}
```

## `file-size-format`

Action slug: `file-size-format`

Price: `5` credits

Convert a raw byte count into a human-readable size string (KB, MB, GB, etc.).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | File size in bytes as a string (e.g., '5242880') |

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
    "description": "File size in bytes as a string (e.g., '5242880')",
    "required": true,
    "type": "string"
  }
}
```
