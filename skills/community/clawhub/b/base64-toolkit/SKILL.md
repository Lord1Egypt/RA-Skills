---
name: base64-toolkit
description: Base64 encoding and decoding toolkit. Encode/decode text, URL-safe Base64, and image to Base64 conversion.
metadata: { "openclaw": { "emoji": "🔐", "requires": { "bins": ["python3"] } } }
---

# Base64 Toolkit

A comprehensive Base64 encoding and decoding tool for developers.

## Features

- **Encode** - Convert text to Base64
- **Decode** - Convert Base64 back to text
- **URL-Safe** - URL-safe Base64 encoding (+/- instead of /+)
- **Image to Base64** - Convert images to Base64 data URI

## Usage

```bash
python3 skills/base64-toolkit/scripts/base64_toolkit.py <action> [options]
```

## Actions

| Action | Description |
|--------|-------------|
| `encode` | Encode text to Base64 |
| `decode` | Decode Base64 to text |
| `encode-url` | URL-safe Base64 encoding |
| `decode-url` | URL-safe Base64 decoding |
| `image-encode` | Convert image to Base64 data URI |

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--input` | string | - | Input string or file path |
| `--file` | bool | false | Treat input as file path |

## Examples

```bash
# Encode text
python3 skills/base64-toolkit/scripts/base64_toolkit.py encode --input "Hello, World!"

# Decode Base64
python3 skills/base64-toolkit/scripts/base64_toolkit.py decode --input "SGVsbG8sIFdvcmxkIQ=="

# URL-safe encode
python3 skills/base64-toolkit/scripts/base64_toolkit.py encode-url --input "Hello+World?"

# URL-safe decode
python3 skills/base64-toolkit/scripts/base64_toolkit.py decode-url --input "SGVsbG8rV29ybGQ_"

# Image to Base64
python3 skills/base64-toolkit/scripts/base64_toolkit.py image-encode --input /path/to/image.png
```

## Use Cases

1. **API authentication** - Encode credentials for Basic Auth
2. **Data transmission** - Safely transmit binary data as text
3. **URL parameters** - Use URL-safe Base64 in URLs
4. **Image embedding** - Embed images in HTML/CSS as data URIs
5. **JWT tokens** - Decode and inspect JWT payload

## Current Status

Ready for testing.
