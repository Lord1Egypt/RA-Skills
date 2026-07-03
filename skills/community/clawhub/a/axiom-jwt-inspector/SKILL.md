---
name: axiom-jwt-inspector
description: JWT inspector — decode JSON Web Tokens and inspect header, payload, claims, expiration. Use when you need to debug or audit JWTs. Pure stdlib, no LLM. **No signature verification** (use a JWT lib for that).
version: 0.1.2
license: Apache-2.0
---

# axiom-jwt-inspector

**Version:** 0.1.2
**Axioma Tools**

Decodes JWTs and exposes their structure for debugging and auditing.

## What this skill does

- Decodes header (alg, typ, kid, etc.)
- Decodes payload (claims)
- Shows expiration status (exp/nbf/iat)
- Flags common vulnerabilities (alg=none, weak secret)
- **Does NOT verify signatures** — debug only

## When to use this skill

- ✅ Debug a JWT you're receiving
- ✅ Audit token structure before trusting
- ✅ Inspect expiration/issued-at
- ❌ Authenticate users (use a JWT lib with sig verification)
- ❌ Replace pyjwt (this is inspection only)

## Usage

```bash
python3 axiom_jwt_inspector.py "eyJhbGciOiJIUzI1NiIs..."
python3 axiom_jwt_inspector.py token.txt --json
```

```python
from axiom_jwt_inspector import inspect_jwt
info = inspect_jwt('eyJhbGciOiJIUzI1NiIs...')
# {'header': {...}, 'payload': {...}, 'expired': False, 'warnings': []}
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 20+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
