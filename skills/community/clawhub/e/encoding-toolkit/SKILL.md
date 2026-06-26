---
name: encoding-toolkit
description: Multi-format encoder, decoder, and hasher supporting Base64, Base64URL, Base32, Hex, URL-encoding, HTML entities, ROT13, Binary, and ASCII85. Also computes MD5, SHA-1, SHA-256, SHA-512, and SHA3-256 hashes. Can auto-detect encoding format. Use when encoding or decoding data, computing file or string hashes, converting between formats, or identifying unknown encoded strings. Triggers on "encode base64", "decode hex", "hash sha256", "what encoding is this", "url encode", "html decode", "convert to binary".
---

# Encoding Toolkit

All-in-one encoder, decoder, and hasher. Supports 9 encoding formats and 5 hash algorithms with encoding auto-detection.

## Quick Start

```bash
# Encode
python3 scripts/encode_decode.py encode base64 "Hello World"
python3 scripts/encode_decode.py encode url "hello world & goodbye"
python3 scripts/encode_decode.py encode hex "Hello"

# Decode
python3 scripts/encode_decode.py decode base64 "SGVsbG8gV29ybGQ="
python3 scripts/encode_decode.py decode hex "48656c6c6f"
python3 scripts/encode_decode.py decode url "hello%20world"

# Hash
python3 scripts/encode_decode.py hash sha256 "my secret"
python3 scripts/encode_decode.py hash md5 "test" --all  # show all algorithms

# Auto-detect encoding
python3 scripts/encode_decode.py detect "SGVsbG8gV29ybGQ="

# List all supported formats
python3 scripts/encode_decode.py list

# Read from stdin or file
echo "data" | python3 scripts/encode_decode.py encode base64 --stdin
python3 scripts/encode_decode.py hash sha256 --file secret.txt
```

## Supported Formats

**Encodings:** base64, base64url, base32, hex, url, html, rot13, binary, ascii85

**Hashes:** md5, sha1, sha256, sha512, sha3-256

## Features

- Encode, decode, hash, detect, and list in one tool
- Auto-detection tries to identify unknown encoded strings
- Supports stdin and file input for all operations
- No external dependencies — pure Python stdlib
