---
name: database-skill
version: 1.0.0
type: skill
description: "Python-based database connectivity skill supporting MySQL, PostgreSQL, Oracle, SQL Server, and SQLite. Provides connection management, parameterized query execution, schema introspection, and transaction management. Requires Python 3.8+."
---

# database-skill — Python Database Connectivity Skill

English | [中文](#database-skill-中文文档)

This skill guides an AI Agent to connect to relational databases, execute queries,
manage transactions, and introspect schema using Python.

---

<a id="database-skill-中文文档"></a>

# database-skill — Python 数据库连接技能

本技能指导 AI Agent 使用 Python 连接关系型数据库、执行 SQL 查询、管理事务以及探查 Schema 元数据。

---

## When to call / When not to call · 何时调用

| Scenario | Call |
|---|---|
| User needs to run SQL queries | Yes |
| User needs schema introspection (tables, columns, indexes, FK) | Yes |
| User needs transaction control (commit / rollback) | Yes |
| Python 3.8+ not available or drivers not installed | No |
| User only needs text/regex analysis | No |

| 场景 | 调用 |
|---|---|
| 用户需要执行 SQL 查询 | 是 |
| 用户需要 Schema 探查（表、列、索引、外键） | 是 |
| 用户需要事务控制（提交/回滚） | 是 |
| 无 Python 3.8+ 或驱动未安装 | 否 |
| 用户仅需文本/正则分析 | 否 |

---

## Prerequisites · 前提条件

| Requirement | Check |
|---|---|
| Python 3.8+ | `python --version` |
| Target database reachable | `telnet <host> <port>` |
| Dependencies | `pip install pymysql psycopg2-binary oracledb pymssql pyyaml` |

---

## Quick start · 快速开始

```bash
# List all tables
python scripts/main.py \
  --url "jdbc:mysql://localhost:3306/mydb" \
  --user "root" \
  --password "${DB_PASS}" \
  --tables

# Parameterized query
python scripts/main.py \
  --url "jdbc:mysql://localhost:3306/mydb" \
  --user "root" \
  --password "${DB_PASS}" \
  --query "SELECT * FROM user WHERE name = ?" "zhangsan"
```

---

## Configuration (3 options) · 配置方式（三种）

### A — CLI arguments (recommended) · 命令行参数（推荐）

```bash
python scripts/main.py \
  --url "jdbc:mysql://host:3306/db" \
  --user "admin" \
  --password "${DB_PASS}" \
  --query "SELECT 1"
```

### B — YAML config file · 配置文件

```yaml
# datasource.yml
datasource:
  url: "jdbc:mysql://localhost:3306/mydb"
  username: "${DB_USER}"
  password: "${DB_PASS}"
```

```bash
python scripts/main.py --config datasource.yml --tables
```

### C — Built-in defaults · 内置默认

```bash
python scripts/main.py --tables
```

---

## Operations · 操作说明

| Flag | Description | 说明 |
|---|---|---|
| `--query <sql> [params...]` | SELECT with `?` placeholders | SELECT 查询，支持参数化 |
| `--update <sql> [params...]` | UPDATE/INSERT/DELETE | 更新/插入/删除 |
| `--batch <file>` | Execute SQL file | 批量执行文件中的 SQL |
| `--tables` | List all tables | 列出所有表 |
| `--columns <table>` | Show column metadata | 查看表结构 |
| `--list-connections` | Show saved connections | 查看已保存的连接 |
| `--forget <url>` | Remove a saved connection | 删除已保存的连接 |

Examples · 示例：

```bash
python scripts/main.py --url "jdbc:mysql://host:3306/db" --user root --password x --tables
python scripts/main.py --url "..." --user root --password x --query "SELECT * FROM t WHERE id = ?" 42
python scripts/main.py --url "..." --user root --password x --update "UPDATE t SET x = ? WHERE id = ?" "new" 1
python scripts/main.py --list-connections
```

---

## Scripts · 脚本结构

```
scripts/
├── main.py                  # CLI entry point · 命令行入口
├── connection_manager.py    # Connect / disconnect · 连接管理
├── connections_store.py     # Persist connections · 连接记录持久化
├── query_executor.py        # Query, update, batch, transaction · 查询执行
├── schema_inspector.py      # Schema introspection · Schema 探查
└── exceptions.py            # Exception hierarchy · 异常层次
```

---

## API overview · API 概览

### ConnectionManager · 连接管理器

```python
from connection_manager import ConnectionManager

cm = ConnectionManager(url="jdbc:mysql://localhost:3306/db",
                       username="root", password="secret",
                       driver="pymysql")
conn = cm.get_connection()                       # auto-commit
tx_conn = cm.get_connection_for_transaction()   # manual-commit
cm.close_connection(conn)
```

### QueryExecutor · 查询执行器

```python
from query_executor import QueryExecutor

qe = QueryExecutor(cm)
rows = qe.execute_query("SELECT * FROM users WHERE status = ?", "ACTIVE")
affected = qe.execute_update("UPDATE users SET status = ? WHERE id = ?", "INACTIVE", 1)
qe.execute_batch(["INSERT INTO log VALUES (1)", "INSERT INTO log VALUES (2)"])
qe.execute_transaction(lambda tx: (
    tx.execute_update("UPDATE accounts SET balance = balance - 100 WHERE id = ?", 1),
    tx.execute_update("UPDATE accounts SET balance = balance + 100 WHERE id = ?", 2),
))
```

### CaseInsensitiveDict · 大小写不敏感字典

Query results are wrapped in ``CaseInsensitiveDict`` so column names are case-insensitive:
查询结果的列名大小写不敏感：

```python
row["name"] == row["NAME"] == row["Name"]
```

### SchemaInspector · Schema 检查器

```python
from schema_inspector import SchemaInspector

si = SchemaInspector(cm)
si.get_tables()         # 获取所有表
si.get_columns("users") # 获取表结构
si.get_indexes("users") # 获取索引
si.get_foreign_keys("users")  # 获取外键
```

---

## Saved connections · 连接记录

After a successful connection, the skill saves the URL, username, and driver to
``%TEMP%/.database-skill-connections.json`` (``/tmp/`` on Linux/macOS).
**Passwords are never stored.**

连接成功后，技能会将 URL、用户名和驱动类型保存到用户临时目录。
**密码不会被保存。**

When no ``--url`` or ``--config`` is provided, the skill shows a numbered list:
不提供 ``--url`` 或 ``--config`` 时，显示已保存的连接供选择：

```
Saved connections:
  [0] MySQL@host1
  [1] Oracle@orahost
  [N] Enter a new connection
```

```bash
python scripts/main.py --list-connections    # 查看所有连接
python scripts/main.py --forget "jdbc:mysql://..."  # 删除连接
```

---

## Security rules · 安全守则

1. **Never hard-code passwords** — use environment variables `${DB_PASS}` or CLI.
   **禁止硬编码密码** — 使用环境变量或命令行参数。
2. **Always use parameterized queries** — values go as `?` placeholders.
   **始终使用参数化查询** — 值通过 `?` 占位符传递。
3. **Transactions auto-commit/rollback** — handled transparently.
   **事务自动提交/回滚** — 无需手动处理。
4. **Passwords never persisted** — saved connections store only URL and username.
   **密码不持久化** — 只保存 URL 和用户名。

---

## Building & testing · 构建与测试

```bash
pip install -e ".[dev]"
pytest
```
