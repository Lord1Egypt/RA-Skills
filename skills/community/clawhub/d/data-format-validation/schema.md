# Data Format Validation Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `data-format-validation`

x402 availability: not enabled for this product.

## `validate-base64`

Action slug: `validate-base64`

Price: `5` credits

Validate whether a string is properly Base64-encoded. Returns valid status and decoded byte length.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The Base64 string to validate. |

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
    "description": "The Base64 string to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-credit-card`

Action slug: `validate-credit-card`

Price: `5` credits

Validate a credit card number using the Luhn algorithm. Detects card type (Visa, Mastercard, Amex, Discover). Spaces and hyphens are stripped.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The credit card number to validate. |

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
    "description": "The credit card number to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-email`

Action slug: `validate-email`

Price: `5` credits

Validate an email address format (RFC 5322 simplified). Returns valid status, local_part, and domain.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The email address to validate. |

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
    "description": "The email address to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-hex-color`

Action slug: `validate-hex-color`

Price: `5` credits

Validate a hexadecimal color code (#RGB or #RRGGBB). Returns valid status, format, and RGB values or expanded form.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The hex color string to validate (e.g., '#FF5733' or '#F00'). |

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
    "description": "The hex color string to validate (e.g., '#FF5733' or '#F00').",
    "required": true,
    "type": "string"
  }
}
```

## `validate-iban`

Action slug: `validate-iban`

Price: `5` credits

Validate an International Bank Account Number (mod-97 checksum). Spaces are stripped. Returns country_code, check_digits, BBAN.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The IBAN to validate. |

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
    "description": "The IBAN to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-ipv4`

Action slug: `validate-ipv4`

Price: `5` credits

Validate an IPv4 address and classify it. Returns valid status, octets, is_private, is_loopback.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The IPv4 address to validate. |

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
    "description": "The IPv4 address to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-ipv6`

Action slug: `validate-ipv6`

Price: `5` credits

Validate an IPv6 address and classify it. Returns valid status, is_loopback, is_link_local, compressed flag.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The IPv6 address to validate. |

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
    "description": "The IPv6 address to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-isbn`

Action slug: `validate-isbn`

Price: `5` credits

Validate an ISBN-10 or ISBN-13 with checksum verification. Hyphens and spaces are stripped.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The ISBN to validate. |

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
    "description": "The ISBN to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-json`

Action slug: `validate-json`

Price: `5` credits

Validate whether a string is well-formed JSON. Returns valid status and parsed type.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The JSON string to validate. |

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
    "description": "The JSON string to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-json-syntax`

Action slug: `validate-json-syntax`

Price: `5` credits

Alias for validate-json. Validates whether a string is well-formed JSON.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The JSON string to validate. |

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
    "description": "The JSON string to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-mac-address`

Action slug: `validate-mac-address`

Price: `5` credits

Validate a MAC address (colon or hyphen separated). Returns valid status, format, octets, canonical form.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The MAC address to validate (XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX). |

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
    "description": "The MAC address to validate (XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX).",
    "required": true,
    "type": "string"
  }
}
```

## `validate-phone`

Action slug: `validate-phone`

Price: `5` credits

Validate a phone number format (10-15 digits, optional international prefix). Parentheses, spaces, hyphens, dots are stripped.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The phone number to validate. |

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
    "description": "The phone number to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-regex`

Action slug: `validate-regex`

Price: `5` credits

Validate whether a string is a compilable regular expression. Returns valid status and specific regex error if invalid.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The regex pattern to validate. |

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
    "description": "The regex pattern to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-url`

Action slug: `validate-url`

Price: `5` credits

Validate a URL format (checks for scheme and domain). Returns valid status, scheme, domain, path, query and fragment flags.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The URL to validate. |

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
    "description": "The URL to validate.",
    "required": true,
    "type": "string"
  }
}
```

## `validate-uuid`

Action slug: `validate-uuid`

Price: `5` credits

Validate a UUID string (versions 1-5, RFC 4122). Returns valid status, version, and variant.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The UUID string to validate. |

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
    "description": "The UUID string to validate.",
    "required": true,
    "type": "string"
  }
}
```
