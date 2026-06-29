---
name: axiom-json-canonicalizer
description: JCS RFC 8785 — Canonical JSON. Convert any JSON to a deterministic, byte-to-byte identical canonical form. Use when you need to sign, hash, or compare JSON regardless of whitespace or key order. Pure stdlib, no LLM, no cloud.
version: 1.0.1
license: Apache-2.0
---

# axiom-json-canonicalizer

**Version:** 1.0.1
**Axioma Tools**

Converts any JSON to a canonical form per RFC 8785 (JCS).

## What this skill does

- Object keys sorted lexicographically (post-NFC)
- No insignificant whitespace
- Numbers: ECMAScript shortest round-trip
- Strings: NFC-normalized, surrogate-pair safe
- Output: UTF-8 bytes (byte-to-byte stable)

## When to use this skill

- ✅ Sign OAuth/JWT payloads (canonicalize before signing)
- ✅ Hash JSON for integrity verification
- ✅ Compare semantically-equivalent JSON
- ✅ Build tamper-evident audit logs
- ❌ Need pretty-printing (use json.dumps indent)
- ❌ Need JSON5/JSONL/JSONC (different specs)

## Usage

```bash
python3 axiom_json_canonicalizer.py input.json > canonical.json
python3 axiom_json_canonicalizer.py input.json --verify canonical.json
```

```python
from axiom_json_canonicalizer import canonicalize
canon_bytes = canonicalize(json_obj)  # UTF-8 bytes
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 81 cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
