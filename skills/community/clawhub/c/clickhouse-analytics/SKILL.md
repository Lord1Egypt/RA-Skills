---
name: clickhouse-analytics
description: Inspect ClickHouse databases, review schemas, and run SQL analytics queries via the ClickHouse HTTP API. Use this skill when users want to query analytics data, explore database schemas, or run read-only SQL queries for business intelligence.
---

# ClickHouse

![ClickHouse](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/clickhouse.svg)

Work with ClickHouse from chat — inspect databases, review schemas, and run read-only SQL analytics queries via the ClickHouse HTTP API with API key authentication.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clickhouse-analytics) for hosted connection flows and credentials so you do not need to configure ClickHouse API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect ClickHouse |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect ClickHouse |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ ClickHouse HTTP API│
│   (User Chat)   │     │   (API Key)  │     │ (SQL Queries)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect ClickHouse│                       │
         │                       │  4. Secure Key │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ ClickHouse│
   │  File    │           │ Auth     │           │ Queries  │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for ClickHouse again."

## Quick Start

```bash
# List databases
clawlink_call_tool --tool "clickhouse_list_databases" --params '{}'

# List tables in a database
clawlink_call_tool --tool "clickhouse_list_tables" --params '{"database": "default"}'

# Get database schema overview
clawlink_call_tool --tool "clickhouse_get_database_schema" --params '{"database": "default"}'
```

## Authentication

All ClickHouse tool calls are authenticated automatically by ClawLink using the user's connected ClickHouse account.

**No credentials are required in chat.** ClawLink stores the connection details securely and injects them into every ClickHouse request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=clickhouse and connect ClickHouse.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `clickhouse` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration clickhouse
```

**Response:** Returns the live tool catalog for ClickHouse.

### Reconnect

If ClickHouse tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=clickhouse
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration clickhouse`

## Security & Permissions

- ClickHouse queries are read-only by design in ClawLink — no INSERT, ALTER, DROP, or TRUNCATE operations are exposed.
- **Query operations require user confirmation** for large result sets or expensive queries (full table scans, GROUP BY without limits).
- Avoid running queries that could lock tables or consume excessive resources.

## Tool Reference

### Schema Discovery

| Tool | Description | Mode |
|------|-------------|------|
| `clickhouse_list_databases` | List all databases in the ClickHouse instance | Read |
| `clickhouse_list_tables` | List tables in a database with engine, size, and row count | Read |
| `clickhouse_get_database_schema` | Get full schema overview including all tables and columns | Read |
| `clickhouse_get_table_schema` | Get detailed schema for a specific table including columns and types | Read |

### Query Execution

| Tool | Description | Mode |
|------|-------------|------|
| `clickhouse_execute_query` | Execute a read-only SQL query and return results | Read |

### Interface

| Tool | Description | Mode |
|------|-------------|------|
| `clickhouse_get_play_interface` | Get the ClickHouse Play web interface URL for interactive queries | Read |

## Code Examples

### List all databases

```bash
clawlink_call_tool --tool "clickhouse_list_databases" \
  --params '{}'
```

### Get database schema

```bash
clawlink_call_tool --tool "clickhouse_get_database_schema" \
  --params '{
    "database": "analytics"
  }'
```

### Execute a simple query

```bash
clawlink_call_tool --tool "clickhouse_execute_query" \
  --params '{
    "query": "SELECT * FROM events WHERE date >= today() - 7 LIMIT 100"
  }'
```

### Get table schema

```bash
clawlink_call_tool --tool "clickhouse_get_table_schema" \
  --params '{
    "database": "analytics",
    "table": "events"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm ClickHouse is connected.
2. Call `clawlink_list_tools --integration clickhouse` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `clickhouse`.
5. If no ClickHouse tools appear, direct the user to https://claw-link.dev/dashboard?add=clickhouse.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  SCHEMA DISCOVERY (Always first)                           │
│  list_databases → list_tables → get_table_schema          │
│                                                             │
│  Example: Discover tables → Understand schema → Then query   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  QUERY EXECUTION (Read-only)                                │
│  describe → preview → confirm → execute                     │
│                                                             │
│  Example: Describe query → Preview results → User approves   │
│           → Execute read-only query                          │
└─────────────────────────────────────────────────────────────┘
```

1. Always explore the schema first with `clickhouse_list_databases` and `clickhouse_get_database_schema` before running queries.
2. For unfamiliar tables, call `clickhouse_get_table_schema` to understand column names and types.
3. Keep queries targeted with WHERE clauses and LIMIT — avoid full table scans when possible.
4. For large or complex queries, confirm the expected result size with the user before executing.
5. If the tool call fails, report the real error. Do not invent results.

## Notes

- ClickHouse SQL syntax differs from standard SQL — use ClickHouse-specific functions and syntax.
- All queries are read-only — no data modification is possible through ClawLink tools.
- Use `LIMIT` to prevent accidentally large result sets.
- Sample data can be included in table schema responses — use it to understand data types.
- The Play interface provides an interactive HTML UI with Monaco Editor for manual query writing.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration clickhouse`. |
| Missing connection | ClickHouse is not connected. Direct the user to https://claw-link.dev/dashboard?add=clickhouse. |
| `SyntaxError` | SQL syntax error in query. Check ClickHouse SQL syntax. |
| `TableNotFound` | Table or database does not exist. Verify names with schema tools first. |
| `Query error` | Query failed. Check query logic and table structure. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Query Errors

1. Always use schema tools first to verify table and column names.
2. Verify the database name with `clickhouse_list_databases`.
3. Use `LIMIT` to test queries with small result sets first.

## Resources

- [ClickHouse Documentation](https://clickhouse.com/docs)
- [ClickHouse SQL Reference](https://clickhouse.com/docs/en/sql-reference/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clickhouse-analytics
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Datadog](https://clawhub.ai/hith3sh/datadog-monitoring) — For Datadog observability and metrics
- [Snowflake](https://clawhub.ai/hith3sh/snowflake-data) — For Snowflake data warehouse queries
- [PostgreSQL](https://clawhub.ai/hith3sh/postgresql-database) — For PostgreSQL database operations

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clickhouse-analytics)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
