---
name: SQL Assistant
description: AI-powered SQL assistant. Generate SQL from natural language, explain queries, optimize performance, review security, and generate migrations for SQLite, PostgreSQL, and MySQL. Powered by evolink.ai
version: 1.0.0
homepage: https://github.com/EvoLinkAI/sql-skill-for-openclaw
metadata: {"openclaw":{"homepage":"https://github.com/EvoLinkAI/sql-skill-for-openclaw","requires":{"bins":["python3","curl"],"env":["EVOLINK_API_KEY"]},"primaryEnv":"EVOLINK_API_KEY"}}
---

# SQL Assistant

AI-powered SQL generation, analysis, and optimization from your terminal. Supports SQLite, PostgreSQL, and MySQL. This skill never connects to or executes against any database — it only generates and analyzes SQL text.

Powered by [Evolink.ai](https://evolink.ai?utm_source=clawhub&utm_medium=skill&utm_campaign=sql)

## When to Use

- User says "write me a query that..." or "generate SQL for..."
- User has a SQL file and asks "what does this query do?"
- User says "this query is slow" or "optimize this SQL"
- User wants a security review of SQL before running it
- User needs to generate a database migration
- User needs quick SQL reference for a specific database

## Quick Start

### 1. Set your EvoLink API key

    export EVOLINK_API_KEY="your-key-here"

Get a free key: [evolink.ai/signup](https://evolink.ai/signup?utm_source=clawhub&utm_medium=skill&utm_campaign=sql)

### 2. Generate SQL from natural language

    bash scripts/sql.sh query "find all users who signed up last month with more than 5 orders" --db postgres

### 3. Analyze existing SQL

    bash scripts/sql.sh explain slow-query.sql

    bash scripts/sql.sh optimize report.sql --db postgres

## Capabilities

### AI Commands (require EVOLINK_API_KEY)

| Command | Description |
|---------|-------------|
| `query <description> --db <db>` | Generate SQL from natural language |
| `explain <sql-file>` | Explain what a query does step-by-step |
| `optimize <sql-file> --db <db>` | Performance optimization with index suggestions |
| `review <sql-file>` | Security audit — injection, privileges, data exposure |
| `migrate <description> --db <db>` | Generate UP/DOWN migration SQL |

### Info Commands (no API key needed)

| Command | Description |
|---------|-------------|
| `databases` | List supported databases |
| `cheatsheet [db\|patterns]` | Quick SQL reference and common patterns |

### Supported Databases

| Database | Cheatsheet | AI Generation |
|----------|-----------|---------------|
| `sqlite` | Connection, import/export, PRAGMA, backup | SQLite-specific syntax |
| `postgres` | psql commands, types, JSONB, backup/restore | PG-specific (TIMESTAMPTZ, partial indexes, CTEs) |
| `mysql` | Connection, types, EXPLAIN, backup | MySQL-specific (AUTO_INCREMENT, ON DUPLICATE KEY) |

### Cheatsheet Topics

| Topic | Content |
|-------|---------|
| `sqlite` | Zero-setup database, CSV import, WAL mode |
| `postgres` | psql shortcuts, common types, pg_dump |
| `mysql` | Connection, SHOW commands, mysqldump |
| `patterns` | Pagination, upsert, CTEs, window functions, recursive queries |

## Examples

### Generate SQL from natural language

    bash scripts/sql.sh query "monthly revenue by product category for the last 6 months" --db postgres

Output:

    SELECT
      c.name AS category,
      DATE_TRUNC('month', o.created_at) AS month,
      SUM(oi.quantity * oi.unit_price) AS revenue
    FROM order_items oi
    JOIN orders o ON o.id = oi.order_id
    JOIN products p ON p.id = oi.product_id
    JOIN categories c ON c.id = p.category_id
    WHERE o.created_at >= NOW() - INTERVAL '6 months'
    GROUP BY c.name, DATE_TRUNC('month', o.created_at)
    ORDER BY month DESC, revenue DESC;

### Security review

    bash scripts/sql.sh review migration.sql

### Generate migration

    bash scripts/sql.sh migrate "add soft delete to users and orders tables" --db postgres

## Configuration

| Variable | Default | Required | Description |
|---|---|---|---|
| `EVOLINK_API_KEY` | — | Yes | Your EvoLink API key. [Get one free](https://evolink.ai/signup?utm_source=clawhub&utm_medium=skill&utm_campaign=sql) |
| `EVOLINK_MODEL` | `claude-opus-4-6` | No | Model for AI analysis |

Required binaries: `python3`, `curl`

## Security

**Data Transmission**

AI commands send user-provided SQL text or natural language descriptions to `api.evolink.ai` for analysis by Claude. By setting `EVOLINK_API_KEY` and using these commands, you consent to this transmission. Data is not stored after the response is returned. The `databases` and `cheatsheet` commands run entirely locally and never transmit data.

**No Database Access**

This skill never connects to, reads from, or writes to any database. It only generates and analyzes SQL text. All generated SQL must be reviewed and executed by the user.

**Network Access**

- `api.evolink.ai` — AI SQL analysis (AI commands only)

**Persistence & Privilege**

This skill creates temporary files for API payload construction which are cleaned up automatically. No credentials or persistent data are stored. The skill only reads files explicitly passed as arguments.

## Links

- [GitHub](https://github.com/EvoLinkAI/sql-skill-for-openclaw)
- [EvoLink API](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=sql)
- [Community](https://discord.com/invite/5mGHfA24kn)
- [Support](mailto:support@evolink.ai)
