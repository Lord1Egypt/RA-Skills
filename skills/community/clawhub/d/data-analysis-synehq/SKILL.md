---
name: kole
description: Execute queries against your databases using SQL, PostgreSQL commands, or natural language through SyneHQ's Kole platform. Use this skill whenever the user mentions databases, SQL queries, data analysis, PostgreSQL, querying data, database connections, checking database schemas, listing tables, or wants to explore or analyze data in their databases. Also use when user needs to sign up for SyneHQ or get their API credentials. IMPORTANT - Always use this skill when user asks about their data, even if they don't explicitly say "database" or "SQL".
tools: No special tools required - uses MCP server
compatibility: Requires synehq-kole MCP server to be configured
version: 1.1.2
requires_mcp:
  package: "@synehq/kole-mcp"
  source: "https://github.com/synehq/kole-mcp"
  npm: "https://www.npmjs.com/package/@synehq/kole-mcp"
  install: "npm install -g @synehq/kole-mcp"
  min_version: "1.0.0"
requires_env:
  - name: SYNEHQ_API_KEY
    required: true
    description: "SyneHQ API authentication key. Get from https://data.synehq.com/dashboard → Settings → API Keys"
    security: "Grants access to query connected databases. Treat as sensitive credential. Do not commit to version control."
  - name: SYNEHQ_CONNECTION_ID
    required: false
    description: "Default database connection ID. Can be overridden per-query. Get from https://data.synehq.com/dashboard → Connections"
    security: "Optional. If not set, must provide connectionId with each query."
install_steps:
  - "Install MCP server: npm install -g @synehq/kole-mcp"
  - "Get SyneHQ account: curl https://data.synehq.com/api/auth-info"
  - "Sign up at: https://data.synehq.com/signup"
  - "Get API key from: https://data.synehq.com/dashboard → Settings → API Keys"
  - "Configure connection at: https://data.synehq.com/dashboard → Connections"
  - "Set environment variables: SYNEHQ_API_KEY and SYNEHQ_CONNECTION_ID (optional)"
  - "Add MCP server to .mcp.json or claude_desktop_config.json (see documentation below)"
security_warnings:
  - "This MCP server can execute arbitrary SQL queries and DDL statements (CREATE, ALTER, DROP) against connected databases."
  - "Use least-privilege, read-only database credentials when possible for testing and exploration."
  - "For production use, ensure database user has only necessary permissions."
  - "All queries are logged for audit purposes with optional userId tracking."
  - "Test on non-production databases first to understand query capabilities and impacts."
  - "API key grants access to all databases connected to your SyneHQ account."
  - "Review MCP package source code at https://github.com/synehq/kole-mcp before installation."
audit_logging: "All queries logged server-side with timestamps, user IDs (if provided), and connection details. Access logs at https://data.synehq.com/dashboard → Audit Logs"
---

# kole - Query Your Data with SyneHQ

Execute SQL queries, PostgreSQL commands, and natural language questions against your databases through SyneHQ's intelligent data platform.

## ⚠️ IMPORTANT: Prerequisites

**This skill requires the SyneHQ Kole MCP server to be installed and configured.**

### Install the MCP Server

```bash
# Install via npm
npm install -g @synehq/kole-mcp

# Or from source
git clone https://github.com/synehq/kole-mcp.git
cd kole-mcp
npm install && npm run build
```

### Configure the MCP Server

Create `.mcp.json` in your project:

```json
{
  "synehq-kole": {
    "command": "npx",
    "args": ["-y", "@synehq/kole-mcp@latest"],
    "env": {
      "SYNEHQ_API_KEY": "${SYNEHQ_API_KEY}",
      "SYNEHQ_CONNECTION_ID": "${SYNEHQ_CONNECTION_ID}"
    }
  }
}
```

Or if you have it installed globally:

```json
{
  "synehq-kole": {
    "command": "synehq-kole-mcp",
    "env": {
      "SYNEHQ_API_KEY": "${SYNEHQ_API_KEY}",
      "SYNEHQ_CONNECTION_ID": "${SYNEHQ_CONNECTION_ID}"
    }
  }
}
```

### Set Environment Variables

```bash
export SYNEHQ_API_KEY="your_api_key"
export SYNEHQ_CONNECTION_ID="your_connection_id"
```

**Without the MCP server installed, this skill will not work!** The skill provides instructions and patterns, but the actual query execution happens through the MCP server's tools.

---

## What is Kole?

Kole is SyneHQ's data query platform that enables you to:
- Execute SQL queries against connected databases
- Use PostgreSQL-specific commands and DDL operations
- Ask questions in natural language and get structured results
- Discover database schemas and metadata
- Manage multiple database connections
- Test connections before querying

## Quick Start

### First Time User?

If the user doesn't have a SyneHQ account yet, use `get_auth_info` to get signup instructions:

```javascript
get_auth_info()
// Returns: signup URL, login URL, dashboard URL, setup instructions
```

### Check Available Connections

Always start by listing available connections:

```javascript
get_connections()
// Shows all database connections with IDs, names, types, and status
```

### Test Connection

Before running queries, verify the connection works:

```javascript
test_connection({
  connectionId: "conn_abc123"  // optional if SYNEHQ_CONNECTION_ID env var is set
})
```

## Core Operations

### 1. Execute SQL Queries

**Simple SELECT:**
```javascript
execute_query({
  query: "SELECT * FROM users WHERE created_at > '2024-01-01' LIMIT 10"
})
```

**With options:**
```javascript
execute_query({
  query: "SELECT * FROM large_table",
  connectionId: "prod-db",
  limit: 100,
  timeout: 60000,  // 60 seconds
  userId: "analyst_1"  // for audit tracking
})
```

### 2. PostgreSQL Mode (psql commands)

Enable PostgreSQL-specific commands with `psql: true`:

**List all tables:**
```javascript
execute_query({
  query: "\\dt",
  psql: true
})
```

**Describe table structure:**
```javascript
execute_query({
  query: "\\d+ users",
  psql: true
})
```

**DDL Operations:**
```javascript
execute_query({
  query: "CREATE TABLE analytics_cache (id SERIAL PRIMARY KEY, query_hash VARCHAR(64), result JSONB)",
  psql: true
})
```

### 3. Natural Language Queries

Ask questions in plain English:

```javascript
execute_query({
  query: "Show me the top 10 customers by revenue this month"
})

execute_query({
  query: "How many active users signed up last week?"
})

execute_query({
  query: "What are the best-selling products?"
})
```

### 4. Database Metadata Discovery

**List all tables:**
```javascript
get_tables({
  database: "production",  // optional filter
  schema: "public"        // optional filter
})
```

**Get detailed table schema:**
```javascript
get_table_schema({
  database: "production",
  schema: "public",
  table: "users"
})
// Returns: columns, types, constraints, indexes
```

## Common Query Patterns

See `references/query-patterns.md` for detailed examples. Here are the most common:

### Data Exploration
```sql
-- Quick table overview
SELECT * FROM users LIMIT 5;

-- Column statistics
SELECT 
  COUNT(*) as total_rows,
  COUNT(DISTINCT email) as unique_emails,
  MIN(created_at) as earliest_user,
  MAX(created_at) as latest_user
FROM users;
```

### Business Analytics
```sql
-- Monthly revenue
SELECT 
  DATE_TRUNC('month', order_date) as month,
  COUNT(*) as order_count,
  SUM(total_amount) as revenue
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY month
ORDER BY month DESC;

-- Customer lifetime value
SELECT 
  user_id,
  COUNT(*) as order_count,
  SUM(total_amount) as lifetime_value
FROM orders
GROUP BY user_id
ORDER BY lifetime_value DESC
LIMIT 20;
```

### Data Quality Checks
```sql
-- Find NULL values
SELECT 
  COUNT(*) as total_rows,
  COUNT(*) FILTER (WHERE email IS NULL) as null_emails,
  COUNT(*) FILTER (WHERE phone IS NULL) as null_phones
FROM users;

-- Find duplicates
SELECT 
  email,
  COUNT(*) as duplicate_count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

## Workflow Patterns

### Pattern 1: Data Discovery Workflow

When user wants to explore their data:

1. **List connections** → `get_connections()`
2. **Test connection** → `test_connection()`
3. **List tables** → `get_tables()`
4. **Inspect schema** → `get_table_schema()`
5. **Query data** → `execute_query()`

### Pattern 2: Analytics Workflow

When user wants to analyze data:

1. **Understand structure** → `get_table_schema()`
2. **Sample data** → `SELECT * FROM table LIMIT 10`
3. **Run aggregations** → Complex SELECT with GROUP BY
4. **Iterate based on results**

### Pattern 3: PostgreSQL Admin Workflow

When user needs database operations:

1. **Check current state** → `\dt`, `\d+ table_name` (psql mode)
2. **Execute DDL** → CREATE, ALTER, DROP (psql mode)
3. **Verify changes** → Check with `\dt` or queries
4. **Create indexes** → CREATE INDEX (psql mode)

## Best Practices

### 1. Always Start with Discovery

```javascript
// Step 1: List connections
get_connections()

// Step 2: Test the connection
test_connection({ connectionId: "chosen_connection" })

// Step 3: Discover tables
get_tables()

// Step 4: Understand schema
get_table_schema({ database: "db", schema: "public", table: "users" })

// Step 5: Query safely with LIMIT
execute_query({ query: "SELECT * FROM users LIMIT 10" })
```

### 2. Use LIMIT for Exploration

Always use LIMIT when exploring large tables:

```sql
-- Good: Limited results
SELECT * FROM large_table LIMIT 10

-- Bad: Might return millions of rows
SELECT * FROM large_table
```

### 3. Leverage PostgreSQL Features (psql mode)

```sql
-- JSON operations
SELECT data->>'name' as name FROM json_table

-- Array operations
SELECT * FROM users WHERE tags @> ARRAY['premium']

-- Window functions
SELECT 
  user_id,
  order_date,
  total_amount,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date DESC) as order_rank
FROM orders
```

### 4. Handle Errors Gracefully

```javascript
// Always test connection first
const connection = await test_connection()

if (connection.success) {
  // Then run your query
  const result = await execute_query({
    query: "SELECT * FROM users LIMIT 10"
  })
}
```

### 5. Use User IDs for Tracking

Track queries with user IDs for audit logs:

```javascript
execute_query({
  query: "SELECT * FROM sensitive_table",
  userId: "user_12345"  // Shows up in audit logs
})
```

### 6. Set Appropriate Timeouts

For complex queries, increase timeout:

```javascript
execute_query({
  query: "SELECT * FROM orders JOIN order_items USING(order_id)",
  timeout: 120000  // 2 minutes
})
```

## Troubleshooting

### Connection Issues

**Symptom:** "Connection failed" or "Invalid credentials"

**Solution:**
1. Test connection: `test_connection()`
2. List connections to verify ID: `get_connections()`
3. Check credentials in SyneHQ dashboard
4. Verify database is accessible

### Query Timeouts

**Symptom:** Query takes too long and times out

**Solution:**
```javascript
execute_query({
  query: "your_complex_query",
  limit: 100,        // Limit result size
  timeout: 120000    // Increase timeout to 2 minutes
})
```

### Large Result Sets

**Symptom:** Too much data returned

**Solution:**
```javascript
// Use LIMIT and OFFSET for pagination
execute_query({
  query: "SELECT * FROM users ORDER BY id LIMIT 100 OFFSET 0",
  limit: 100
})
```

### No API Key

**Symptom:** "SYNEHQ_API_KEY environment variable is required"

**Solution:**
1. Get signup info: `get_auth_info()`
2. Sign up at https://data.synehq.com/signup
3. Get API key from Settings → API Keys
4. Set environment variable: `export SYNEHQ_API_KEY="your_key"`

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `SYNEHQ_API_KEY` | ✅ Yes | - | Authentication |
| `SYNEHQ_CONNECTION_ID` | ⚠️ Recommended | - | Default database connection |
| `SYNEHQ_BASE_URL` | ❌ No | https://cosmos.synehq.com | API endpoint |
| `SYNEHQ_DATA_URL` | ❌ No | https://data.synehq.com | Data API endpoint |

## Advanced Features

### Multi-Connection Scenarios

Query multiple databases in the same session:

```javascript
// Production database
execute_query({
  query: "SELECT COUNT(*) as prod_users FROM users",
  connectionId: "prod-db"
})

// Staging database
execute_query({
  query: "SELECT COUNT(*) as staging_users FROM users",
  connectionId: "staging-db"
})

// Analytics database
execute_query({
  query: "SELECT * FROM daily_metrics WHERE date >= CURRENT_DATE - 30",
  connectionId: "analytics-db"
})
```

### Query Performance Analysis

Use EXPLAIN to analyze query performance:

```javascript
execute_query({
  query: "EXPLAIN ANALYZE SELECT * FROM users WHERE email LIKE '%@gmail.com'",
  psql: true
})
```

### Database Maintenance

Check table sizes and run maintenance:

```javascript
// Check table sizes
execute_query({
  query: `
    SELECT 
      schemaname,
      tablename,
      pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
    FROM pg_tables
    WHERE schemaname = 'public'
    ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
  `,
  psql: true
})

// Vacuum table
execute_query({
  query: "VACUUM ANALYZE users",
  psql: true
})
```

## Security Notes

- API keys are transmitted via secure headers (never in URLs)
- All communication over HTTPS
- User IDs tracked for audit logs
- Connection credentials managed server-side
- Never expose API keys in client code
- Use read-only database users when possible

## Resources

- **Signup**: https://data.synehq.com/signup
- **Login**: https://data.synehq.com/login
- **Dashboard**: https://data.synehq.com/dashboard
- **Documentation**: https://docs.synehq.com
- **Support**: support@synehq.com

## Quick Reference

### Get Started
```javascript
get_auth_info()           // Get signup/login URLs
get_connections()          // List all connections
test_connection()          // Test connection
```

### Query Data
```javascript
execute_query({ query: "SELECT * FROM users LIMIT 10" })
execute_query({ query: "\\dt", psql: true })  // PostgreSQL mode
execute_query({ query: "Show me top customers" })  // Natural language
```

### Discover Schema
```javascript
get_tables()
get_table_schema({ database: "db", schema: "schema", table: "table" })
```

---

**Built with ❤️ by SyneHQ** | Query your data, your way.
