# Encryption Decryption Toolkit Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `encrytion-decryption-toolkit`

x402 availability: not enabled for this product.

## `decrypt`

Action slug: `decrypt`

Price: `5` credits

Decrypt AES-256-GCM ciphertext back to plaintext.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `aad` | `string` | no | Additional authenticated data (must match what was used during encryption). |
| `encoding` | `string` | no | Encoding for key, iv, and ciphertext. |
| `iv` | `string` | yes | 12-byte initialization vector/nonce (same value used during encryption). |
| `key` | `string` | yes | 32-byte AES encryption key (same encoding used during encryption). |
| `value` | `string` | yes | Ciphertext to decrypt (hex or base64 encoded). |

Sample parameters:

```json
{
  "aad": "example aad",
  "encoding": "hex",
  "iv": "example iv",
  "key": "example key",
  "value": "example value"
}
```

Generated JSON parameter schema:

```json
{
  "aad": {
    "description": "Additional authenticated data (must match what was used during encryption).",
    "required": false,
    "type": "string"
  },
  "encoding": {
    "default": "hex",
    "description": "Encoding for key, iv, and ciphertext.",
    "enum": [
      "hex",
      "base64"
    ],
    "required": false,
    "type": "string"
  },
  "iv": {
    "description": "12-byte initialization vector/nonce (same value used during encryption).",
    "required": true,
    "type": "string"
  },
  "key": {
    "description": "32-byte AES encryption key (same encoding used during encryption).",
    "required": true,
    "type": "string"
  },
  "value": {
    "description": "Ciphertext to decrypt (hex or base64 encoded).",
    "required": true,
    "type": "string"
  }
}
```

## `encrypt`

Action slug: `encrypt`

Price: `5` credits

Encrypt plaintext using AES-256-GCM authenticated encryption.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `aad` | `string` | no | Additional authenticated data (verified during decryption but not encrypted). |
| `encoding` | `string` | no | Encoding for key, iv, and output ciphertext. |
| `iv` | `string` | yes | 12-byte initialization vector/nonce, encoded as hex or base64. |
| `key` | `string` | yes | 32-byte AES encryption key, encoded as hex or base64. |
| `value` | `string` | yes | Plaintext to encrypt. |

Sample parameters:

```json
{
  "aad": "example aad",
  "encoding": "hex",
  "iv": "example iv",
  "key": "example key",
  "value": "example value"
}
```

Generated JSON parameter schema:

```json
{
  "aad": {
    "description": "Additional authenticated data (verified during decryption but not encrypted).",
    "required": false,
    "type": "string"
  },
  "encoding": {
    "default": "hex",
    "description": "Encoding for key, iv, and output ciphertext.",
    "enum": [
      "hex",
      "base64"
    ],
    "required": false,
    "type": "string"
  },
  "iv": {
    "description": "12-byte initialization vector/nonce, encoded as hex or base64.",
    "required": true,
    "type": "string"
  },
  "key": {
    "description": "32-byte AES encryption key, encoded as hex or base64.",
    "required": true,
    "type": "string"
  },
  "value": {
    "description": "Plaintext to encrypt.",
    "required": true,
    "type": "string"
  }
}
```

## `generate`

Action slug: `generate`

Price: `5` credits

Generate a cryptographically secure random value in ASCII, BASE64, HEX, or UUID format.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `generation_type` | `string` | yes | Type of value to generate: ASCII, BASE64, HEX, or UUID. |
| `length` | `integer` | no | Length of the generated value (ignored for UUID). Default: 32. |
| `property_name` | `string` | yes | Name of the property to write the output to. |

Sample parameters:

```json
{
  "generation_type": "ASCII",
  "length": 32,
  "property_name": "example property name"
}
```

Generated JSON parameter schema:

```json
{
  "generation_type": {
    "description": "Type of value to generate: ASCII, BASE64, HEX, or UUID.",
    "enum": [
      "ASCII",
      "BASE64",
      "HEX",
      "UUID"
    ],
    "required": true,
    "type": "string"
  },
  "length": {
    "default": 32,
    "description": "Length of the generated value (ignored for UUID). Default: 32.",
    "maximum": 256,
    "minimum": 4,
    "required": false,
    "type": "integer"
  },
  "property_name": {
    "description": "Name of the property to write the output to.",
    "required": true,
    "type": "string"
  }
}
```

## `hash`

Action slug: `hash`

Price: `5` credits

Compute a cryptographic hash of text or binary data using MD5, SHA, or SHA3 algorithms.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `binary_file` | `boolean` | no | Set to true to hash binary data from binary_value_base64 instead of text. |
| `binary_property_name` | `string` | no | Metadata label for the binary input. |
| `binary_value_base64` | `string` | no | Base64-encoded binary data to hash. Required when binary_file is true. |
| `encoding` | `string` | no | Output encoding format. |
| `hash_algorithm` | `string` | yes | Hash algorithm to use. |
| `property_name` | `string` | no | Output property name. Defaults to hash_result. |
| `value` | `string` | no | Plain text input to hash. Required unless binary_file is true. |

Sample parameters:

```json
{
  "binary_file": false,
  "binary_property_name": "example binary property name",
  "binary_value_base64": "example binary value base64",
  "encoding": "hex",
  "hash_algorithm": "MD5",
  "property_name": "example property name",
  "value": "example value"
}
```

Generated JSON parameter schema:

```json
{
  "binary_file": {
    "default": false,
    "description": "Set to true to hash binary data from binary_value_base64 instead of text.",
    "required": false,
    "type": "boolean"
  },
  "binary_property_name": {
    "description": "Metadata label for the binary input.",
    "required": false,
    "type": "string"
  },
  "binary_value_base64": {
    "description": "Base64-encoded binary data to hash. Required when binary_file is true.",
    "required": false,
    "type": "string"
  },
  "encoding": {
    "default": "hex",
    "description": "Output encoding format.",
    "enum": [
      "hex",
      "base64"
    ],
    "required": false,
    "type": "string"
  },
  "hash_algorithm": {
    "description": "Hash algorithm to use.",
    "enum": [
      "MD5",
      "SHA256",
      "SHA384",
      "SHA512",
      "SHA3-256",
      "SHA3-384",
      "SHA3-512"
    ],
    "required": true,
    "type": "string"
  },
  "property_name": {
    "description": "Output property name. Defaults to hash_result.",
    "required": false,
    "type": "string"
  },
  "value": {
    "description": "Plain text input to hash. Required unless binary_file is true.",
    "required": false,
    "type": "string"
  }
}
```

## `hmac`

Action slug: `hmac`

Price: `5` credits

Compute a keyed-hash message authentication code (HMAC) using a secret key.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `binary_file` | `boolean` | no | Set to true to use binary data from binary_value_base64. |
| `binary_value_base64` | `string` | no | Base64-encoded binary data. Required when binary_file is true. |
| `encoding` | `string` | no | Output encoding format. |
| `hash_algorithm` | `string` | yes | Hash algorithm to use for HMAC. |
| `property_name` | `string` | no | Output property name. Defaults to hmac_result. |
| `secret` | `string` | yes | Secret key for HMAC computation. |
| `value` | `string` | no | Plain text input. Required unless binary_file is true. |

Sample parameters:

```json
{
  "binary_file": false,
  "binary_value_base64": "example binary value base64",
  "encoding": "hex",
  "hash_algorithm": "MD5",
  "property_name": "example property name",
  "secret": "example secret",
  "value": "example value"
}
```

Generated JSON parameter schema:

```json
{
  "binary_file": {
    "default": false,
    "description": "Set to true to use binary data from binary_value_base64.",
    "required": false,
    "type": "boolean"
  },
  "binary_value_base64": {
    "description": "Base64-encoded binary data. Required when binary_file is true.",
    "required": false,
    "type": "string"
  },
  "encoding": {
    "default": "hex",
    "description": "Output encoding format.",
    "enum": [
      "hex",
      "base64"
    ],
    "required": false,
    "type": "string"
  },
  "hash_algorithm": {
    "description": "Hash algorithm to use for HMAC.",
    "enum": [
      "MD5",
      "SHA256",
      "SHA384",
      "SHA512",
      "SHA3-256",
      "SHA3-384",
      "SHA3-512"
    ],
    "required": true,
    "type": "string"
  },
  "property_name": {
    "description": "Output property name. Defaults to hmac_result.",
    "required": false,
    "type": "string"
  },
  "secret": {
    "description": "Secret key for HMAC computation.",
    "required": true,
    "type": "string"
  },
  "value": {
    "description": "Plain text input. Required unless binary_file is true.",
    "required": false,
    "type": "string"
  }
}
```

## `sign`

Action slug: `sign`

Price: `5` credits

Create a digital signature using RSA or ECDSA with a PEM-encoded private key.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `algorithm` | `string` | yes | Signing algorithm to use. |
| `encoding` | `string` | no | Output encoding format. |
| `private_key` | `string` | yes | PEM-encoded private key for signing. |
| `property_name` | `string` | no | Output property name. Defaults to signature. |
| `value` | `string` | yes | The text data to sign. |

Sample parameters:

```json
{
  "algorithm": "RS256",
  "encoding": "hex",
  "private_key": "example private key",
  "property_name": "example property name",
  "value": "example value"
}
```

Generated JSON parameter schema:

```json
{
  "algorithm": {
    "description": "Signing algorithm to use.",
    "enum": [
      "RS256",
      "RS512",
      "ES256",
      "ES384",
      "ES512"
    ],
    "required": true,
    "type": "string"
  },
  "encoding": {
    "default": "hex",
    "description": "Output encoding format.",
    "enum": [
      "hex",
      "base64"
    ],
    "required": false,
    "type": "string"
  },
  "private_key": {
    "description": "PEM-encoded private key for signing.",
    "required": true,
    "type": "string"
  },
  "property_name": {
    "description": "Output property name. Defaults to signature.",
    "required": false,
    "type": "string"
  },
  "value": {
    "description": "The text data to sign.",
    "required": true,
    "type": "string"
  }
}
```
