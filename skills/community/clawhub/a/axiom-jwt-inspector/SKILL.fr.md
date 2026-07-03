---
name: axiom-jwt-inspector
description: Inspecteur JWT — décode les JSON Web Tokens et inspecte header, payload, claims, expiration. Utilisez pour debugger ou auditer des JWTs. Stdlib pur, sans LLM. **Pas de vérification de signature** (utilise une lib JWT pour ça).
version: 0.1.2
license: Apache-2.0
---

# axiom-jwt-inspector

**Version:** 0.1.2
**Axioma Tools**

Décode les JWTs et expose leur structure pour debug et audit.

## What this skill does

- Décode le header (alg, typ, kid, etc.)
- Décode le payload (claims)
- Montre le statut d'expiration (exp/nbf/iat)
- Flag les vulnérabilités communes (alg=none, secret faible)
- **NE vérifie PAS les signatures** — debug seulement

## When to use this skill

- ✅ Débugger un JWT que tu reçois
- ✅ Auditer la structure d'un token avant de lui faire confiance
- ✅ Inspecter expiration/issued-at
- ❌ Authentifier des users (utilise une lib JWT avec vérif sig)
- ❌ Remplacer pyjwt (inspection seulement)

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
