---
name: axiom-iban-validator
description: IBAN validator — check IBAN format and mod-97 checksum for 100+ countries. Use when you need to validate international bank account numbers. Pure stdlib, no LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-iban-validator

**Version:** 0.1.2
**Axioma Tools**

Validates IBANs using the mod-97 algorithm with country-specific length checks.

## What this skill does

- Mod-97 checksum validation
- Country-specific length check (FR=27, DE=22, GB=22, etc.)
- Strips spaces/dashes from input
- Returns BBAN breakdown

## When to use this skill

- ✅ Validate IBAN before payment submission
- ✅ Audit customer bank data
- ✅ Pre-validate in payment forms
- ❌ Verify if the account actually exists (separate API)

## Usage

```bash
python3 axiom_iban_validator.py "FR76 3000 6000 0112 3456 7890 189"
python3 axiom_iban_validator.py --country FR --number "3000600011234567890189"
```

```python
from axiom_iban_validator import validate_iban
validate_iban('FR7630006000011234567890189')  # True
# Returns: {valid, country, bban, checksum_ok, length_ok}
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
