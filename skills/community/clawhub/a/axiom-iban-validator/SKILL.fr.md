---
name: axiom-iban-validator
description: Validateur IBAN — vérifie le format IBAN et le checksum mod-97 pour 100+ pays. Utilisez pour valider des numéros de compte bancaires internationaux. Stdlib pur, sans LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-iban-validator

**Version:** 0.1.2
**Axioma Tools**

Valide les IBAN avec l'algorithme mod-97 et les checks de longueur par pays.

## What this skill does

- Validation checksum mod-97
- Check de longueur par pays (FR=27, DE=22, GB=22, etc.)
- Strip les espaces/tirets de l'input
- Retourne le breakdown BBAN

## When to use this skill

- ✅ Valider un IBAN avant soumission de paiement
- ✅ Auditer les données bancaires client
- ✅ Pré-valider dans un formulaire de paiement
- ❌ Vérifier que le compte existe vraiment (API séparée)

## Usage

```bash
python3 axiom_iban_validator.py "FR76 3000 6000 0112 3456 7890 189"
python3 axiom_iban_validator.py --country FR --number "3000600011234567890189"
```

```python
from axiom_iban_validator import validate_iban
validate_iban('FR7630006000011234567890189')  # True
# Retourne: {valid, country, bban, checksum_ok, length_ok}
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
