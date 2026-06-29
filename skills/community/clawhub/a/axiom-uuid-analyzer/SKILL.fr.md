---
name: axiom-uuid-analyzer
description: Inspecteur UUID — parse n'importe quel UUID et extrait version (1-8), variant (RFC 4122, Microsoft, NCS, Future), timestamp (v1, v7), adresse MAC (v1). Utilisez pour analyser, valider ou auditer. Stdlib pur, sans LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-uuid-analyzer

**Version:** 0.1.2
**Axioma Tools**

Inspecte les UUIDs et extrait leur contenu sémantique.

## What this skill does

- Valide le format UUID (8-4-4-4-12 hex)
- Extrait la version (1-8)
- Extrait le variant (RFC 4122, Microsoft, NCS, Future)
- Pour v1 : extrait timestamp + adresse MAC
- Pour v7 : extrait timestamp unix

## When to use this skill

- ✅ Analyser un UUID que tu n'as pas généré
- ✅ Auditer la cohérence des versions UUID en DB
- ✅ Extraire le timestamp des UUIDs temporels
- ✅ Valider des UUIDs en input utilisateur
- ❌ Générer des UUIDs (utilise le module uuid)

## Usage

```bash
python3 axiom_uuid_analyzer.py "550e8400-e29b-41d4-a716-446655440000"
python3 axiom_uuid_analyzer.py uuid-list.txt --json
```

```python
from axiom_uuid_analyzer import analyze_uuid
info = analyze_uuid('550e8400-e29b-41d4-a716-446655440000')
# {'version': 4, 'variant': 'RFC 4122', 'timestamp': None, 'mac': None}
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 30+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
