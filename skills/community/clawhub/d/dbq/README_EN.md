# dbq — Multi-Environment Database Query & Write CLI for AI Agents

A universal **database CLI tool** / **database skill** that lets **Claude Code**, **OpenCode**, **Hermes**, **Cursor**, **WorkBuddy**, and any AI coding assistant execute SQL operations (SELECT / INSERT / UPDATE / DELETE / DDL) using pre-configured database aliases across multiple environments. Write operations are controlled via YAML configuration with fine-grained permissions. Use it as an **AI agent database tool** (db skill / database skills) — stop pasting host/port/user to your AI; just tell it the alias and query.

[中文](./README.md)

## Supported Databases

| Database | Driver | Extra Deps | Support Level |
|----------|--------|-----------|---------------|
| **SQLite** | `sqlite3` (stdlib) | **Zero dependencies** | ✅ Full support |
| MySQL | `pymysql` | `pip install pymysql` | ✅ Full support |
| MariaDB | `pymysql` | `pip install pymysql` | ✅ Full support |
| PostgreSQL | `psycopg2` | `pip install psycopg2-binary` | ✅ Full support |

**Works out of the box**: dev environment ships with a `sqlite_test` file-based database config — test everything with zero dependencies.

## Supported AI Assistants

Works with any AI agent that can execute shell commands:

| AI Assistant | Usage |
|-------------|-------|
| **Claude Code** | `python3 scripts/query.py my_db "SELECT ..."` |
| **OpenCode** | Execute in terminal, or use `/run` command |
| **Hermes** | Register as custom tool, or shell-exec in conversation |
| **Cursor Agent** | Terminal mode, or declare in `.cursorrules` |
| **WorkBuddy** | Install as skill, auto-detected by AI |
| **GitHub Copilot** | CLI mode execution |
| **Aider** | `/run python3 scripts/query.py ...` |
| **Tongyi Lingma / Comate** | Terminal execution |

It's just a shell command — no platform-specific API or plugin dependency.

## Features

### Query & Browse
- **Multi-Environment Isolation**: `dev` / `test` / `prod` with separate config files, switch with `--env`
- **Secure Password Management**: Three-tier lookup — macOS Keychain → `.env` file → env vars. Passwords are **never stored in YAML**
- **Large Table Protection**: Auto EXPLAIN before query, warning for >50K rows, auto-injected `LIMIT 100`
- **EXPLAIN Index Insights**: Shows `type=ref | key=idx_mobile | rows=42`. Full table scans marked `type=ALL`
- **Table Structure (3 Modes)**: `--show` for overview (with comments + row counts), `--desc` for columns + indexes (table format), `--ddl` for full `CREATE TABLE` statements
- **Wildcard Batch Operations**: `--show "user_*"`, `--desc "order_*"`, `--ddl "log_*"` — match multiple tables at once
- **Connection Reuse**: Batch operations (`--desc ALL` / `--ddl ALL`) use only 1 connection for N tables

### Write Operations
- **YAML-Controlled Permissions**: Write access is never enabled via CLI flags — must be configured in YAML with `readonly: false` / `allow_ddl: true`
- **4-Tier SQL Classification**: READ (SELECT/SHOW) always allowed → DML (INSERT/UPDATE/DELETE) requires `readonly: false` → DDL (ALTER/CREATE/DROP) requires `allow_ddl: true` → BLOCKED (GRANT/SET/CALL) always rejected
- **No-WHERE Protection**: DELETE/UPDATE without WHERE is rejected outright to prevent accidental full-table operations
- **`--dry-run` Preview**: Preview SQL + EXPLAIN plan before execution — safe way to verify write operations
- **`--limit` for DML**: DELETE/UPDATE support `--limit N` to manually control affected rows
- **Prod Confirmation**: Write operations on prod require interactive confirmation. Use `DB_QUERY_ASSUME_YES=1` for non-interactive / AI agent mode

### Operations
- **Query Logging**: All SQL (with EXPLAIN + operation type tags) auto-logged to `logs/YYYY-MM-DD.log` with full traceability
- **Connection Testing**: `--ping` for quick connectivity verification

## Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml pymysql
# For PostgreSQL:
pip install psycopg2-binary
# SQLite requires no extra dependencies (Python stdlib)
```

### 2. Configure Connections

```bash
# Generate config templates (safe to re-run, skips existing)
python3 scripts/query.py --init-config

# Edit with your host / user / database
vim assets/connections.dev.yaml
```

Example `connections.dev.yaml`:

```yaml
# Environment-level settings
settings:
  readonly_mode: false       # false allows DML write operations

connections:
  my_db:
    type: mysql
    host: 127.0.0.1
    port: 3306
    user: root
    password: ${MY_DB_PASS}  # References .env variable, never hardcoded
    database: mydb
    readonly: false          # Allow INSERT/UPDATE/DELETE on this connection
    allow_ddl: true          # Allow ALTER/CREATE/DROP on this connection

  sqlite_test:               # Zero-dependency test connection
    type: sqlite
    path: /tmp/test.db
    readonly: false
    allow_ddl: true
```

### 3. Configure Passwords (choose one)

| Method | Command | Security |
|--------|---------|----------|
| **A. Keychain** | `python3 scripts/query.py --keychain-set my_db --env dev` | ⭐⭐⭐ System-level encryption |
| **B. .env file** | `echo "MY_DB_PASS=xxx" >> assets/.env` | ⭐⭐ Local file |
| **C. Env var** | `export MY_DB_PASS=xxx` | ⭐ CI/CD injection |

### 4. Verify Connection

```bash
python3 scripts/query.py my_db --ping
# → ✅ [my_db] (dev) connected (mysql) - 0.012s
python3 scripts/query.py --env prod my_db --ping
# → ✅ [my_db] (prod) connected (mysql) - 0.008s
```

## Usage Examples

### Query Data

```bash
# ═══ Basic Queries ═══
python3 scripts/query.py my_db "SELECT * FROM users WHERE status=1"
# → 📊 [dev] EXPLAIN: type=ref | key=idx_status | rows=156 → Auto LIMIT 100

python3 scripts/query.py --env prod my_db "SELECT COUNT(*) FROM orders"

# --multi execute multiple SELECTs in one connection
python3 scripts/query.py my_db --multi "
  SELECT COUNT(*) FROM users;
  SELECT * FROM users WHERE status=1 LIMIT 5;
  SELECT COUNT(*) FROM orders
"

# --count: row count only, no data returned
python3 scripts/query.py my_db "SELECT * FROM orders WHERE status=1" --count

# --no-limit for full dataset
python3 scripts/query.py my_db "SELECT * FROM config" --no-limit

# --timeout for slow query protection
python3 scripts/query.py my_db "SELECT * FROM big_table" --timeout 30

# ═══ Browse Tables ═══
python3 scripts/query.py my_db --show                     # All tables (comment + row count)
python3 scripts/query.py my_db -s "user_*"                # Wildcard filter
python3 scripts/query.py my_db -s "user_*" --format json  # JSON output

# ═══ Table Structure ═══
python3 scripts/query.py my_db -d users                   # Structure (columns + indexes)
python3 scripts/query.py my_db --ddl users                # Full CREATE TABLE DDL
python3 scripts/query.py my_db -d "order_*"               # Wildcard batch

# ═══ Output Formats ═══
python3 scripts/query.py my_db "SELECT * FROM users" --format json
python3 scripts/query.py my_db "SELECT * FROM users" --format csv
python3 scripts/query.py my_db -d users --format json     # Structure output too
```

### Write Data

```bash
# ═══ INSERT ═══
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "INSERT INTO users (name, email) VALUES ('Alice', 'alice@test.com')"

# Batch insert
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "INSERT INTO users (name, email) VALUES ('Bob', 'bob@test.com'), ('Carol', 'carol@test.com')"

# ═══ UPDATE ═══
# Preview first with --dry-run (no execution)
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "UPDATE users SET status=0 WHERE id=1" --dry-run

# Execute after confirmation
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "UPDATE users SET status=0 WHERE id=1"

# Batch update with --limit
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "UPDATE logs SET archived=1 WHERE created_at < '2025-01-01'" --limit 1000

# ═══ DELETE ═══
# Conditional delete
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "DELETE FROM temp_logs WHERE created_at < '2025-01-01'" --limit 500

# No WHERE will be rejected
python3 scripts/query.py my_db "DELETE FROM users"
# → ❌ Rejected: DELETE requires a WHERE clause

# ═══ DDL ═══
DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "ALTER TABLE users ADD COLUMN dept VARCHAR(50) DEFAULT 'Engineering'"

DB_QUERY_ASSUME_YES=1 python3 scripts/query.py my_db \
  "CREATE INDEX idx_users_dept ON users (dept)"

# ═══ Global ═══
python3 scripts/query.py --list                           # Scan all environments
python3 scripts/query.py --list --env prod                # Filter by environment
```

## Using with AI Assistants

Once installed, just say in conversation:

> Query the orders table in dev/my_db for the last 10 unpaid records

> Insert a test record into the users table: name=Alice, email=alice@test.com

> Preview the SQL for deleting expired logs with --dry-run

The AI agent will construct and execute `python3 scripts/query.py ...` automatically.

**Claude Code / Cursor Agent / Hermes** — direct conversation, AI will shell-exec:

```
Show me all tables in prod user_db, then insert a test user with name=test
```

**For more reliable registration as a custom tool**:

```bash
alias dbq='python3 ~/.workbuddy/skills/dbq/scripts/query.py'
dbq my_db -d users
```

## Command Reference

| Command | Description |
|---------|-------------|
| `<alias> "SQL"` | Execute SQL (query or write) |
| `--list` | List configured connections across environments |
| `--show [TABLE]` | List tables (with comment + row count), supports wildcards |
| `-d TABLE / ALL / "pat*"` | Table structure (columns + indexes, table format) |
| `--ddl TABLE / ALL / "pat*"` | Full CREATE TABLE statement |
| `--ping` | Test database connectivity |
| `--count` | Run COUNT(*) only, no data |
| `--limit N` | Query: override row limit (default: 100); Write: limit DELETE/UPDATE affected rows |
| `--no-limit` | Disable auto LIMIT (queries only) |
| `--dry-run` | Preview write SQL + EXPLAIN without execution |
| `--multi` | Execute multiple SELECTs (semicolon-separated), one connection |
| `--timeout N` | Query timeout in seconds |
| `--keychain-set` | Save password to macOS Keychain |
| `--format json/csv` | Output format |

Common flags: `--env dev|test|prod` (default: dev), `--config <file>` (custom config)

Environment Variables:

| Variable | Description |
|----------|-------------|
| `DB_QUERY_DEFAULT_ENV` | Override default environment (default: `dev`) |
| `DB_QUERY_ASSUME_YES` | Set to `1` to skip write confirmation prompts (non-interactive / AI agent mode) |

## Directory Structure

```
dbq/
├── SKILL.md                           # WorkBuddy skill entry
├── README.md                          # Chinese docs (default on GitHub)
├── README_EN.md                       # English docs
├── scripts/
│   ├── query.py                       # Main script
│   └── test.py                        # Unit tests (no DB required)
├── assets/
│   ├── connections.dev.yaml           # Dev default config (with sqlite_test) ✅ committed
│   ├── connections.dev.yaml.example   # Dev template ✅ committed
│   ├── connections.test.yaml.example  # Test template ✅ committed
│   ├── connections.prod.yaml.example  # Prod template ✅ committed
│   ├── .env.example                   # Password template ✅ committed
│   ├── connections.test.yaml          # ❌ Local config, NOT committed
│   ├── connections.prod.yaml          # ❌ Local config, NOT committed
│   └── .env                           # ❌ Password file, NOT committed
├── references/
│   └── drivers.md                     # Driver installation guide
└── logs/                              # ❌ Query logs, NOT committed
    └── YYYY-MM-DD.log
```

## Running Tests

Verify all core logic without a database connection:

```bash
python3 scripts/test.py
# → 110/110 passed 🎉
```

Test coverage: YAML loading, `${VAR}` placeholder resolution, SQL classification & validation (READ/DML/DDL/BLOCKED), write permission resolution, no-WHERE protection, --dry-run, --limit for DML, password resolution chain, CLI arguments, wildcard matching, logging.

## Security

- `assets/connections*.yaml` (those with passwords) and `assets/.env` are in `.gitignore` — **never committed**
- Passwords never stored in YAML; resolved at runtime via Keychain / .env / env vars
- **4-Tier Operation Classification**:
  - READ (SELECT/SHOW/DESCRIBE/EXPLAIN) — always allowed
  - DML (INSERT/UPDATE/DELETE/REPLACE) — requires `readonly: false`
  - DDL (ALTER/CREATE/DROP/TRUNCATE) — requires `allow_ddl: true`
  - BLOCKED (CALL/GRANT/SET/EXECUTE) — always rejected
- **No-WHERE Protection**: DELETE/UPDATE without WHERE are rejected. Full-table ops require `WHERE 1=1`
- **Prod Confirmation**: Write operations on prod require interactive confirmation
- Query logs stored locally in `logs/`, never uploaded
- **AI agents must NOT directly read `assets/connections*.yaml` or `assets/.env`** — passwords injected at runtime via env vars

## License

MIT
