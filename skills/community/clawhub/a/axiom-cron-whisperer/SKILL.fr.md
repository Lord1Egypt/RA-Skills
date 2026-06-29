---
name: axiom-cron-whisperer
description: Expliqueur d'expressions cron — traduit la syntaxe cron en langage humain (anglais ou français). Utilisez pour comprendre, documenter, ou valider. Stdlib pur, sans LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-cron-whisperer

**Version:** 0.1.2
**Axioma Tools**

Traduit les expressions cron en explications lisibles par un humain.

## What this skill does

- Parse la syntaxe cron standard (5 champs)
- Explique en anglais ou français
- Valide le cron avant déploiement
- Exemple : `0 9 * * 1-5` → 'À 09:00, du lundi au vendredi'

## When to use this skill

- ✅ Comprendre un cron que tu n'as pas écrit
- ✅ Documenter des cron jobs
- ✅ Valider avant déploiement
- ❌ Calculer les N prochaines occurrences (utilise croniter)
- ❌ Syntaxe Quartz (@yearly, L, W, #) — non supporté

## Usage

```bash
python3 axiom_cron_whisperer.py "0 9 * * 1-5"
python3 axiom_cron_whisperer.py "*/15 * * * *" --lang fr
python3 axiom_cron_whisperer.py "0 9 * * 1-5" --validate
```

```python
from axiom_cron_whisperer import explain, validate
explain('0 9 * * 1-5')  # 'À 09:00, du lundi au vendredi'
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
