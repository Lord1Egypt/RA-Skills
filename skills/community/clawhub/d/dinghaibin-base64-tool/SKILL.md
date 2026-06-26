---
name: base64-tool
description: Encode and decode base64 data. Support for standard and URL-safe variants.
---

# Base64 Tool - Encoding

Encode binary data to base64 and decode base64 back to original.

## Quick Start

```bash
echo 'Hello' | base64-tool --encode
```

## Features

- Encode to base64
- Decode from base64
- URL-safe variant
- File and stdin input

## Examples

```bash
echo 'Hello' | base64-tool --encode
echo 'SGVsbG8=' | base64-tool --decode
```

## See Also

- Related documentation: `man base64` (if available)
