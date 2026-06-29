---
name: axiom-phone-e164
description: Normalisateur de numéros de téléphone — convertit tout numéro au format international E.164. Utilisez pour avoir une représentation canonique pour stockage ou comparaison. Stdlib pur, sans LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-phone-e164

**Version:** 0.1.2
**Axioma Tools**

Normalise les numéros de téléphone au standard E.164 (ex : +14155552671).

## What this skill does

- Parse les formats locaux et internationaux
- Détecte le code pays (défaut : US/CA)
- Retourne la chaîne E.164 canonique
- Valide longueur et préfixe pays

## When to use this skill

- ✅ Normaliser un téléphone user-entered pour stockage
- ✅ Dédupliquer des contacts
- ✅ Formater pour APIs SMS (Twilio, etc.)
- ❌ Valider qu'un numéro est joignable (API séparée)

## Usage

```bash
python3 axiom_phone_e164.py "(415) 555-2671"
python3 axiom_phone_e164.py "14155552671" --country US
```

```python
from axiom_phone_e164 import normalize
normalize('(415) 555-2671', default_country='US')  # '+14155552671'
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
