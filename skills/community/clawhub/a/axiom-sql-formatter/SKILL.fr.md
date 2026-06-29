---
name: axiom-sql-formatter
description: Formateur SQL — formate les requêtes SQL avec un style cohérent : keywords en uppercase, indentation correcte, clauses alignées. Utilisez pour avoir un SQL lisible. Stdlib pur, sans LLM. Pas de parsing, pas d'exécution.
version: 0.1.2
license: Apache-2.0
---

# axiom-sql-formatter

**Version:** 0.1.2
**Axioma Tools**

Formate les requêtes SQL avec un style cohérent sans les parser ou les exécuter.

## What this skill does

- Keywords SQL en uppercase (SELECT, FROM, WHERE, etc.)
- Indentation cohérente (4 espaces ou configurable)
- Newline avant les clauses majeures
- Préservation des strings single-quote
- Liste de keywords configurable

## When to use this skill

- ✅ Formater du SQL brut pour lisibilité
- ✅ Standardiser le style SQL d'équipe
- ✅ Pre-process avant code review
- ❌ Parser du SQL en AST (utilise sqlparse)
- ❌ Valider la syntaxe SQL (utilise EXPLAIN)

## Usage

```bash
python3 axiom_sql_formatter.py query.sql
python3 axiom_sql_formatter.py --indent 2 query.sql
```

```python
from axiom_sql_formatter import format_sql
formatted = format_sql('select a,b from t where x=1')
# 'SELECT a, b\nFROM t\nWHERE x = 1'
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
