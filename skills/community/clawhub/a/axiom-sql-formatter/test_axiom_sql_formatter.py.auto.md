# 📄 `test_axiom_sql_formatter.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-sql-formatter/test_axiom_sql_formatter.py`  
**Size:** 2,519 bytes / 80 lines  
**Hash:** `3629aee7c1c6026d`  
**Generated:** 2026-06-15T03:00:47.200035+00:00

## 📝 Module Docstring

```
Tests — axiom-sql-formatter 
```

## 📦 Imports (5)

```python
import pathlib.Path
import sys
import unittest
import axiom_sql_formatter._tokenize
import axiom_sql_formatter.format_sql
```

## 🏛️ Classes (3)

### `TestFormat`
**Methods:** `test_01_simple_select, test_02_uppercase_keywords, test_03_join, test_04_group_by, test_05_order_by, test_06_string_preserved, test_07_line_comment, test_08_no_newlines_added_to_strings`

### `TestTokenize`
**Methods:** `test_09_basic, test_10_string`

### `TestDeterminism`
**Methods:** `test_11_1000_runs`
