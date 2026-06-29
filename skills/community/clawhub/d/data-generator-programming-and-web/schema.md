# Data Generator - Programming and Web Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `data-generator-programming-and-web`

x402 availability: not enabled for this product.

## `api-key`

Action slug: `api-key`

Price: `5` credits

Generate a URL-safe API key with an optional prefix.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `length` | `integer` | yes | Key length excluding prefix (16-128). |
| `prefix` | `string` | no | Optional prefix prepended to the key (e.g., 'sk_', 'pk_test_'). Default: empty string. |

Sample parameters:

```json
{
  "length": 16,
  "prefix": ""
}
```

Generated JSON parameter schema:

```json
{
  "length": {
    "description": "Key length excluding prefix (16-128).",
    "maximum": 128,
    "minimum": 16,
    "required": true,
    "type": "integer"
  },
  "prefix": {
    "default": "",
    "description": "Optional prefix prepended to the key (e.g., 'sk_', 'pk_test_'). Default: empty string.",
    "required": false,
    "type": "string"
  }
}
```

## `iso-date`

Action slug: `iso-date`

Price: `5` credits

Return the current date and time in ISO 8601 format.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `jwt-secret`

Action slug: `jwt-secret`

Price: `5` credits

Generate a secure JWT signing secret.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `length` | `integer` | no | Secret length (minimum 32, default 64). |

Sample parameters:

```json
{
  "length": 64
}
```

Generated JSON parameter schema:

```json
{
  "length": {
    "default": 64,
    "description": "Secret length (minimum 32, default 64).",
    "minimum": 32,
    "required": false,
    "type": "integer"
  }
}
```

## `lorem-ipsum`

Action slug: `lorem-ipsum`

Price: `5` credits

Generate Lorem Ipsum placeholder text. Priority: words > sentences > paragraphs.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `paragraphs` | `integer` | no | Return this many paragraphs. Default: 1. |
| `sentences` | `integer` | no | Return this many sentences (overrides paragraphs). |
| `words` | `integer` | no | Return exactly this many words (overrides sentences and paragraphs). |

Sample parameters:

```json
{
  "paragraphs": 1,
  "sentences": 1,
  "words": 1
}
```

Generated JSON parameter schema:

```json
{
  "paragraphs": {
    "default": 1,
    "description": "Return this many paragraphs. Default: 1.",
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "sentences": {
    "description": "Return this many sentences (overrides paragraphs).",
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "words": {
    "description": "Return exactly this many words (overrides sentences and paragraphs).",
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `password`

Action slug: `password`

Price: `5` credits

Generate a secure random password with configurable character types.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `include_lowercase` | `boolean` | no | Include lowercase letters. Default: true. |
| `include_numbers` | `boolean` | no | Include numbers. Default: true. |
| `include_symbols` | `boolean` | no | Include special symbols. Default: true. |
| `include_uppercase` | `boolean` | no | Include uppercase letters. Default: true. |
| `length` | `integer` | yes | Password length (4-128). |

Sample parameters:

```json
{
  "include_lowercase": true,
  "include_numbers": true,
  "include_symbols": true,
  "include_uppercase": true,
  "length": 4
}
```

Generated JSON parameter schema:

```json
{
  "include_lowercase": {
    "default": true,
    "description": "Include lowercase letters. Default: true.",
    "required": false,
    "type": "boolean"
  },
  "include_numbers": {
    "default": true,
    "description": "Include numbers. Default: true.",
    "required": false,
    "type": "boolean"
  },
  "include_symbols": {
    "default": true,
    "description": "Include special symbols. Default: true.",
    "required": false,
    "type": "boolean"
  },
  "include_uppercase": {
    "default": true,
    "description": "Include uppercase letters. Default: true.",
    "required": false,
    "type": "boolean"
  },
  "length": {
    "description": "Password length (4-128).",
    "maximum": 128,
    "minimum": 4,
    "required": true,
    "type": "integer"
  }
}
```

## `random-bytes`

Action slug: `random-bytes`

Price: `5` credits

Generate random bytes returned as a hexadecimal string.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `length` | `integer` | yes | Number of bytes to generate (1-1024). |

Sample parameters:

```json
{
  "length": 1
}
```

Generated JSON parameter schema:

```json
{
  "length": {
    "description": "Number of bytes to generate (1-1024).",
    "maximum": 1024,
    "minimum": 1,
    "required": true,
    "type": "integer"
  }
}
```

## `random-color`

Action slug: `random-color`

Price: `5` credits

Generate a random hex color code (e.g., #a3f1c2).

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `random-email`

Action slug: `random-email`

Price: `5` credits

Generate a random test email address using example domains.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `random-hex`

Action slug: `random-hex`

Price: `5` credits

Generate a random hexadecimal string.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `length` | `integer` | yes | Number of hex characters to generate (1-64). |

Sample parameters:

```json
{
  "length": 1
}
```

Generated JSON parameter schema:

```json
{
  "length": {
    "description": "Number of hex characters to generate (1-64).",
    "maximum": 64,
    "minimum": 1,
    "required": true,
    "type": "integer"
  }
}
```

## `random-ipv4`

Action slug: `random-ipv4`

Price: `5` credits

Generate a random IPv4 address.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `random-number`

Action slug: `random-number`

Price: `5` credits

Generate a random integer within a specified range.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `max_value` | `integer` | no | Maximum value (inclusive). Default: 100. |
| `min_value` | `integer` | no | Minimum value (inclusive). Default: 0. |

Sample parameters:

```json
{
  "max_value": 100,
  "min_value": 0
}
```

Generated JSON parameter schema:

```json
{
  "max_value": {
    "default": 100,
    "description": "Maximum value (inclusive). Default: 100.",
    "required": false,
    "type": "integer"
  },
  "min_value": {
    "default": 0,
    "description": "Minimum value (inclusive). Default: 0.",
    "required": false,
    "type": "integer"
  }
}
```

## `random-string`

Action slug: `random-string`

Price: `5` credits

Generate a random string of specified length and character set.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `charset` | `string` | no | Character set to use. Default: alphanumeric. |
| `length` | `integer` | yes | Number of characters to generate (1-1000). |

Sample parameters:

```json
{
  "charset": "alphanumeric",
  "length": 1
}
```

Generated JSON parameter schema:

```json
{
  "charset": {
    "default": "alphanumeric",
    "description": "Character set to use. Default: alphanumeric.",
    "enum": [
      "alphanumeric",
      "alpha",
      "numeric",
      "ascii",
      "hex"
    ],
    "required": false,
    "type": "string"
  },
  "length": {
    "description": "Number of characters to generate (1-1000).",
    "maximum": 1000,
    "minimum": 1,
    "required": true,
    "type": "integer"
  }
}
```

## `timestamp`

Action slug: `timestamp`

Price: `5` credits

Return the current Unix timestamp (seconds since epoch).

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `uuid-v1`

Action slug: `uuid-v1`

Price: `5` credits

Generate a UUID version 1 (timestamp-based).

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `uuid-v4`

Action slug: `uuid-v4`

Price: `5` credits

Generate a random UUID version 4.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```
