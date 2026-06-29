---
name: axiom-luhn-check
description: Luhn algorithm validator — credit cards (Visa, MC, Amex, Discover), SIRET/SIREN, IMEI, ISBN-10/13. Use when you need to validate any number that uses Luhn. Pure stdlib, no LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-luhn-check

**Version:** 0.1.2
**Axioma Tools**

Validates numbers using the Luhn algorithm with auto-detection of common types.

## What this skill does

- Luhn check on any number string
- Auto-detects type (Visa/MC/Amex/Discover/SIRET/IMEI/ISBN-10/13)
- JSON output for scripting
- Handles spaces and dashes in input

## When to use this skill

- ✅ Validate credit card before submission
- ✅ Audit IMEI of mobile devices
- ✅ Validate ISBN before cataloging books
- ✅ Validate French SIRET/SIREN
- ❌ Need PCI-compliant full validation (this is checksum only)

## Usage

```bash
python3 axiom_luhn_check.py "4532 0151 1283 0366"
python3 axiom_luhn_check.py "356938035643809" --json
```

```python
from axiom_luhn_check import validate, detect_type
validate('4532015112830366')  # True
detect_type('356938035643809')  # 'amex'
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 25+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
