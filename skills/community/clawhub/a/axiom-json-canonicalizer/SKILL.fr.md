---
name: axiom-json-canonicalizer
description: JCS RFC 8785 — JSON canonique. Convertit n'importe quel JSON en forme canonique déterministe, byte-to-byte identique. Utilisez pour signer, hasher, ou comparer du JSON. Stdlib pur, sans LLM, sans cloud.
version: 1.0.1
license: Apache-2.0
---

# axiom-json-canonicalizer

**Version:** 1.0.1
**Axioma Tools**

Convertit n'importe quel JSON en forme canonique selon RFC 8785 (JCS).

## What this skill does

- Clés d'objet triées lexicographiquement (post-NFC)
- Pas d'espaces insignifiants
- Nombres : format ECMAScript round-trip le plus court
- Strings : NFC-normalisées, surrogate-pair safe
- Sortie : bytes UTF-8 (byte-to-byte stable)

## When to use this skill

- ✅ Signer des payloads OAuth/JWT (canoniser avant)
- ✅ Hasher du JSON pour intégrité
- ✅ Comparer des JSON sémantiquement équivalents
- ✅ Construire des audit logs tamper-evident
- ❌ Besoin de pretty-printing (utilise json.dumps indent)
- ❌ Besoin de JSON5/JSONL/JSONC (specs différentes)

## Usage

```bash
python3 axiom_json_canonicalizer.py input.json > canonical.json
python3 axiom_json_canonicalizer.py input.json --verify canonical.json
```

```python
from axiom_json_canonicalizer import canonicalize
canon_bytes = canonicalize(json_obj)  # bytes UTF-8
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
