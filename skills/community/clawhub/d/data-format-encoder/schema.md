# Data Format Encoder Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `data-format-encoder`

x402 availability: not enabled for this product.

## `encode-base64-decode`

Action slug: `encode-base64-decode`

Price: `5` credits

Decode a Base64-encoded string back to plain text.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The Base64-encoded string to decode. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The Base64-encoded string to decode.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-base64-encode`

Action slug: `encode-base64-encode`

Price: `5` credits

Encode plain text to Base64 format.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The plain text to encode to Base64. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The plain text to encode to Base64.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-binary-to-text`

Action slug: `encode-binary-to-text`

Price: `5` credits

Convert an 8-bit binary string back to plain text. The binary string length must be a multiple of 8 bits.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The binary string to convert to text (spaces between bytes are optional). |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The binary string to convert to text (spaces between bytes are optional).",
    "required": true,
    "type": "string"
  }
}
```

## `encode-escape-json`

Action slug: `encode-escape-json`

Price: `5` credits

Escape special characters in text for safe embedding inside JSON strings (newlines, tabs, quotes, backslashes).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The text to JSON-escape. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The text to JSON-escape.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-hex-to-text`

Action slug: `encode-hex-to-text`

Price: `5` credits

Convert a hexadecimal string back to plain text. Spaces, colons, and hyphens between hex bytes are automatically removed.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The hexadecimal string to convert to text. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The hexadecimal string to convert to text.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-html-entity-decode`

Action slug: `encode-html-entity-decode`

Price: `5` credits

Convert HTML entities back to their original characters.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The HTML-entity-encoded string to decode. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The HTML-entity-encoded string to decode.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-html-entity-encode`

Action slug: `encode-html-entity-encode`

Price: `5` credits

Escape special HTML characters into HTML entities (e.g., < becomes &lt;).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The text containing HTML characters to escape. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The text containing HTML characters to escape.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-rot13-encode`

Action slug: `encode-rot13-encode`

Price: `5` credits

Apply the ROT13 substitution cipher to text. ROT13 is its own inverse — apply it again to decode.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The text to encode with ROT13. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The text to encode with ROT13.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-text-to-binary`

Action slug: `encode-text-to-binary`

Price: `5` credits

Convert text to its 8-bit binary representation (space-separated bytes).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The plain text to convert to binary. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The plain text to convert to binary.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-text-to-hex`

Action slug: `encode-text-to-hex`

Price: `5` credits

Convert text to its hexadecimal byte representation.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The plain text to convert to hexadecimal. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The plain text to convert to hexadecimal.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-unescape-json`

Action slug: `encode-unescape-json`

Price: `5` credits

Convert JSON-escaped sequences back to their original characters.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The JSON-escaped string to unescape. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The JSON-escaped string to unescape.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-unicode-escape`

Action slug: `encode-unicode-escape`

Price: `5` credits

Convert Unicode characters to their escape sequences (\uXXXX format).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The text containing Unicode characters to escape. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The text containing Unicode characters to escape.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-unicode-unescape`

Action slug: `encode-unicode-unescape`

Price: `5` credits

Convert Unicode escape sequences back to their original characters.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The string containing \uXXXX escape sequences to convert. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The string containing \\uXXXX escape sequences to convert.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-url-decode`

Action slug: `encode-url-decode`

Price: `5` credits

Decode a percent-encoded (URL-encoded) string back to plain text.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The URL-encoded string to decode. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The URL-encoded string to decode.",
    "required": true,
    "type": "string"
  }
}
```

## `encode-url-encode`

Action slug: `encode-url-encode`

Price: `5` credits

Percent-encode text for safe use in URLs (query strings, path segments).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The text to URL-encode. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The text to URL-encode.",
    "required": true,
    "type": "string"
  }
}
```
