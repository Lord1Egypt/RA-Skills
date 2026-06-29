---
name: axiom-sql-formatter
description: SQL 格式化器 — 使用一致样式格式化 SQL 查询:大写关键字、正确缩进、对齐子句。在需要可读 SQL 输出时使用。纯标准库,无需 LLM。不解析 SQL,不执行。
version: 0.1.2
license: Apache-2.0
---

# axiom-sql-formatter

**Version:** 0.1.2
**Axioma Tools**

使用一致样式格式化 SQL 查询,而不解析或执行它们。

## What this skill does

- SQL 关键字大写 (SELECT、FROM、WHERE 等)
- 一致的缩进 (4 个空格或可配置)
- 主要子句前换行
- 保留单引号字符串
- 可配置的关键字列表

## When to use this skill

- ✅ 为可读性格式化原始 SQL
- ✅ 标准化团队 SQL 样式
- ✅ 代码审查前预处理
- ❌ 将 SQL 解析为 AST (使用 sqlparse)
- ❌ 验证 SQL 语法 (使用 EXPLAIN)

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
