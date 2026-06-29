# 📄 `axiom_sql_formatter.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-sql-formatter/axiom_sql_formatter.py`  
**Size:** 8,037 bytes / 251 lines  
**Hash:** `0703b52bb23b181b`  
**Generated:** 2026-06-15T03:00:47.199627+00:00

## 📝 Module Docstring

```
🛠️ axiom-sql-formatter — SQL Formatter
=========================================

⚠️ LIMITATIONS CONNUES :
- Pas de CTE récursifs (WITH RECURSIVE)
- Pas de window functions avancées
- Pas de support multi-statement (split par `;`)

FORMATE LES REQUÊTES SQL AVEC INDENTATION CORRECTE
```

## 📦 Imports (3)

```python
import re
import sys
import argparse
```

## ⚡ Functions (4)

### `def _tokenize(sql):`
> Tokenize SQL into (type, value) tuples.

Types: word, string, number, operator, punctuation, comment

### `def _format_tokens(tokens):`
> Format tokens into a nicely indented SQL string.

### `def format_sql(sql):`
> Format a SQL query.

### `def main():`
