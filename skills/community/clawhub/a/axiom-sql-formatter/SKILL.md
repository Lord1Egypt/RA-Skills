---
name: axiom-sql-formatter
description: SQL formatter — format SQL queries with consistent style: uppercase keywords, proper indentation, aligned clauses. Use when you need readable SQL output. Pure stdlib, no LLM. No SQL parsing, no execution.
version: 0.1.2
license: Apache-2.0
---

# axiom-sql-formatter

**Version:** 0.1.2
**Axioma Tools**

Formats SQL queries with consistent style without parsing or executing them.

## What this skill does

- Uppercase SQL keywords (SELECT, FROM, WHERE, etc.)
- Consistent indentation (4 spaces or configurable)
- Newline before major clauses
- Single-quote string preservation
- Configurable keyword list

## When to use this skill

- ✅ Format raw SQL for readability
- ✅ Standardize team SQL style
- ✅ Pre-process before code review
- ❌ Parse SQL into AST (use sqlparse)
- ❌ Validate SQL syntax (use EXPLAIN)

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
