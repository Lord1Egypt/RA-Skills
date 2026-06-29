---
name: axiom-phone-e164
description: Phone number normalizer — convert any phone number to E.164 international format. Use when you need a canonical phone representation for storage or comparison. Pure stdlib, no LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-phone-e164

**Version:** 0.1.2
**Axioma Tools**

Normalizes phone numbers to the E.164 standard (e.g., +14155552671).

## What this skill does

- Parses local and international formats
- Detects country code (default: US/CA)
- Returns canonical E.164 string
- Validates length and country prefix

## When to use this skill

- ✅ Normalize user-entered phone for storage
- ✅ Deduplicate contacts
- ✅ Format for SMS APIs (Twilio, etc.)
- ❌ Validate if a number is reachable (separate API)

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
