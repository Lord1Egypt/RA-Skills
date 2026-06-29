---
name: axiom-cron-whisperer
description: Cron expression explainer — translate cron syntax to human language (English or French). Use when you need to understand, document, or validate a cron expression. Pure stdlib, no LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-cron-whisperer

**Version:** 0.1.2
**Axioma Tools**

Translates cron expressions into human-readable explanations.

## What this skill does

- Parses standard cron syntax (5 fields)
- Explains in English or French
- Validates cron before deployment
- Example: `0 9 * * 1-5` → 'At 09:00, Monday through Friday'

## When to use this skill

- ✅ Understand a cron expression you didn't write
- ✅ Document cron jobs
- ✅ Validate cron before deployment
- ❌ Calculate next N occurrences (use croniter)
- ❌ Quartz syntax (@yearly, L, W, #) — not supported

## Usage

```bash
python3 axiom_cron_whisperer.py "0 9 * * 1-5"
python3 axiom_cron_whisperer.py "*/15 * * * *" --lang fr
python3 axiom_cron_whisperer.py "0 9 * * 1-5" --validate
```

```python
from axiom_cron_whisperer import explain, validate
explain('0 9 * * 1-5')  # 'At 09:00, Monday through Friday'
validate('not a cron')  # False
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 17 cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
