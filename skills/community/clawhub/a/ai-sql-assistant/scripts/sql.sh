#!/usr/bin/env bash
set -euo pipefail

# SQL Assistant — AI-powered SQL generation, analysis, and optimization
# Usage: bash sql.sh <command> [options]
#
# Commands:
#   databases                          — List supported databases
#   cheatsheet [database]              — Quick SQL reference
#   query <description> --db <db>      — AI generate SQL from natural language
#   explain <file>                     — AI explain a SQL query
#   optimize <file> --db <db>          — AI optimize a SQL query
#   review <file>                      — AI security review of SQL
#   migrate <description> --db <db>    — AI generate migration SQL

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
EVOLINK_API="https://api.evolink.ai/v1/messages"

# --- Helpers ---
err() { echo "Error: $*" >&2; exit 1; }

to_native_path() {
  if [[ "$1" =~ ^/([a-zA-Z])/ ]]; then
    echo "${BASH_REMATCH[1]}:/${1:3}"
  else
    echo "$1"
  fi
}

check_deps() {
  command -v python3 &>/dev/null || err "python3 not found."
  command -v curl &>/dev/null || err "curl not found."
}

read_file() {
  local file="$1"
  [ -f "$file" ] || err "File not found: $file"
  cat "$file"
}

evolink_ai() {
  local prompt="$1"
  local content="$2"

  local api_key="${EVOLINK_API_KEY:?Set EVOLINK_API_KEY for AI features. Get one at https://evolink.ai/signup}"
  local model="${EVOLINK_MODEL:-claude-opus-4-6}"

  local tmp_prompt tmp_content tmp_payload
  tmp_prompt=$(mktemp)
  tmp_content=$(mktemp)
  tmp_payload=$(mktemp)
  trap "rm -f '$tmp_prompt' '$tmp_content' '$tmp_payload'" EXIT

  printf '%s' "$prompt" > "$tmp_prompt"
  printf '%s' "$content" > "$tmp_content"

  local native_prompt native_content native_payload
  native_prompt=$(to_native_path "$tmp_prompt")
  native_content=$(to_native_path "$tmp_content")
  native_payload=$(to_native_path "$tmp_payload")

  python3 -c "
import json, sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    prompt = f.read()
with open(sys.argv[2], 'r', encoding='utf-8') as f:
    content = f.read()

data = {
    'model': sys.argv[4],
    'max_tokens': 4096,
    'messages': [
        {
            'role': 'user',
            'content': prompt + '\n\n' + content
        }
    ]
}
with open(sys.argv[3], 'w', encoding='utf-8') as f:
    json.dump(data, f)
" "$native_prompt" "$native_content" "$native_payload" "$model"

  local response
  response=$(curl -s -X POST "$EVOLINK_API" \
    -H "Authorization: Bearer $api_key" \
    -H "Content-Type: application/json" \
    -d "@$tmp_payload")

  echo "$response" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'content' in data:
    for block in data['content']:
        if block.get('type') == 'text':
            print(block['text'])
elif 'error' in data:
    print(f\"AI Error: {data['error'].get('message', str(data['error']))}\", file=sys.stderr)
else:
    print(json.dumps(data, indent=2))
"
}

# --- Cheatsheets ---

cheatsheet_sqlite() {
  cat <<'EOF'
SQLite Quick Reference:

  # Create / open database
  sqlite3 mydb.sqlite

  # Import CSV
  sqlite3 mydb.sqlite ".mode csv" ".import data.csv mytable"

  # One-liner query
  sqlite3 mydb.sqlite "SELECT * FROM users LIMIT 10;"

  # Export to CSV
  sqlite3 -header -csv mydb.sqlite "SELECT * FROM orders;" > orders.csv

  # Interactive mode with headers
  sqlite3 -header -column mydb.sqlite

  # View schema
  .schema users
  .tables

  # Backup
  sqlite3 mydb.sqlite ".backup backup.sqlite"

  # Performance
  PRAGMA journal_mode=WAL;    -- concurrent reads
  EXPLAIN QUERY PLAN SELECT ...;
EOF
}

cheatsheet_postgres() {
  cat <<'EOF'
PostgreSQL Quick Reference:

  # Connect
  psql -h localhost -U myuser -d mydb
  psql "postgresql://user:pass@host:5432/db?sslmode=require"

  # Useful psql commands
  \dt           -- list tables
  \d+ tablename -- describe table with details
  \di+          -- list indexes with sizes
  \x            -- toggle expanded display
  \timing       -- toggle query timing

  # Query performance
  EXPLAIN ANALYZE SELECT ...;

  # Common types
  SERIAL / BIGSERIAL          -- auto-increment
  TIMESTAMPTZ                 -- timezone-aware (always use this)
  JSONB                       -- binary JSON (indexable)
  UUID DEFAULT gen_random_uuid()

  # Backup / Restore
  pg_dump -h host -U user mydb > backup.sql
  pg_dump -Fc mydb > backup.dump          -- custom format (compressed)
  pg_restore -d mydb backup.dump

  # Copy to CSV
  \copy (SELECT * FROM users) TO 'users.csv' CSV HEADER
EOF
}

cheatsheet_mysql() {
  cat <<'EOF'
MySQL Quick Reference:

  # Connect
  mysql -h localhost -u root -p mydb

  # Useful commands
  SHOW TABLES;
  DESCRIBE users;
  SHOW CREATE TABLE users;
  SHOW INDEX FROM users;

  # Query performance
  EXPLAIN SELECT ...;
  SHOW PROFILE;

  # Common types
  INT AUTO_INCREMENT          -- auto-increment
  DATETIME / TIMESTAMP        -- date/time
  JSON                        -- JSON column
  VARCHAR(255)                -- variable string

  # Backup / Restore
  mysqldump -h host -u root -p mydb > backup.sql
  mysql -h host -u root -p mydb < backup.sql

  # Export to CSV
  SELECT * FROM users INTO OUTFILE '/tmp/users.csv'
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n';
EOF
}

cheatsheet_patterns() {
  cat <<'EOF'
Common SQL Patterns:

  -- Pagination
  SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 40;

  -- Upsert (PostgreSQL)
  INSERT INTO users (email, name) VALUES ('a@b.com', 'Alice')
  ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;

  -- Upsert (MySQL)
  INSERT INTO users (email, name) VALUES ('a@b.com', 'Alice')
  ON DUPLICATE KEY UPDATE name = VALUES(name);

  -- CTE (Common Table Expression)
  WITH active_users AS (
    SELECT * FROM users WHERE last_login > NOW() - INTERVAL '30 days'
  )
  SELECT * FROM active_users WHERE plan = 'pro';

  -- Window function
  SELECT name, department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
  FROM employees;

  -- Conditional aggregation
  SELECT
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE status = 'active') as active,  -- PostgreSQL
    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active2  -- universal
  FROM users;

  -- Recursive CTE (tree traversal)
  WITH RECURSIVE tree AS (
    SELECT id, name, parent_id, 0 as depth FROM categories WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, c.parent_id, t.depth + 1
    FROM categories c JOIN tree t ON c.parent_id = t.id
  )
  SELECT * FROM tree ORDER BY depth, name;
EOF
}

# --- Commands ---

cmd_databases() {
  echo "Supported Databases:"
  echo ""
  echo "  sqlite     Zero-setup, file-based, great for prototyping"
  echo "  postgres   Full-featured, JSONB, window functions, CTEs"
  echo "  mysql      Widely deployed, replication, JSON support"
}

cmd_cheatsheet() {
  local db="${1:-all}"
  case "$db" in
    sqlite|sqlite3)    cheatsheet_sqlite ;;
    postgres|pg|psql)  cheatsheet_postgres ;;
    mysql|mariadb)     cheatsheet_mysql ;;
    patterns|common)   cheatsheet_patterns ;;
    all)
      cheatsheet_sqlite; echo ""; echo "---"; echo ""
      cheatsheet_postgres; echo ""; echo "---"; echo ""
      cheatsheet_mysql; echo ""; echo "---"; echo ""
      cheatsheet_patterns ;;
    *) err "Unknown database: $db. Run 'sql.sh databases' for the list." ;;
  esac
}

cmd_query() {
  local description=""
  local db="postgres"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --db) db="${2:?Missing database}"; shift 2 ;;
      -*) err "Unknown option: $1" ;;
      *) description="$description $1"; shift ;;
    esac
  done

  description=$(echo "$description" | sed 's/^ //')
  [ -z "$description" ] && err "Usage: sql.sh query <description> --db <database>"
  check_deps

  echo "Generating SQL..." >&2
  evolink_ai "You are a senior database engineer. Generate a SQL query for $db based on the user's description.

Rules:
- Output ONLY the SQL query, properly formatted and indented.
- Use $db-specific syntax and best practices.
- Add brief inline comments for complex parts.
- Use parameterized placeholders (\$1, :param, or ?) where user input would go.
- If the request is ambiguous, pick the most common interpretation and note your assumption in a comment.
- Do NOT wrap in markdown code fences." "REQUEST:
$description"
}

cmd_explain() {
  local file="${1:?Usage: sql.sh explain <sql-file>}"
  check_deps

  echo "Reading SQL..." >&2
  local content
  content=$(read_file "$file")
  local truncated
  truncated=$(echo "$content" | head -c 12000)

  echo "Analyzing query..." >&2
  evolink_ai "You are a senior database engineer. Explain this SQL query in detail:

1. **Purpose** — What does this query do, in one sentence?
2. **Step-by-step** — Walk through each clause/subquery and explain what it does.
3. **Tables & Joins** — List all tables involved and how they're joined.
4. **Filters** — What conditions filter the data?
5. **Output** — What columns/shape does the result have?
6. **Performance notes** — Any obvious performance concerns (missing indexes, full scans, N+1 patterns)?

Be concise. Use the actual table and column names from the query." "SQL QUERY:
$truncated"
}

cmd_optimize() {
  local file=""
  local db="postgres"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --db) db="${2:?Missing database}"; shift 2 ;;
      -*) err "Unknown option: $1" ;;
      *) file="$1"; shift ;;
    esac
  done

  [ -z "$file" ] && err "Usage: sql.sh optimize <sql-file> --db <database>"
  check_deps

  echo "Reading SQL..." >&2
  local content
  content=$(read_file "$file")
  local truncated
  truncated=$(echo "$content" | head -c 12000)

  echo "Optimizing..." >&2
  evolink_ai "You are a senior database performance engineer specializing in $db. Analyze and optimize this SQL query:

1. **Current issues** — What performance problems exist?
2. **Optimized query** — Rewrite the query for better performance.
3. **Indexes needed** — What indexes should be created? Provide CREATE INDEX statements.
4. **EXPLAIN reading guide** — What to look for in EXPLAIN ANALYZE output for this query.
5. **Estimated improvement** — Rough estimate of performance gain (e.g., 'O(n) → O(log n) with index').

Use $db-specific optimizations (e.g., PostgreSQL partial indexes, MySQL covering indexes, SQLite WITHOUT ROWID)." "SQL QUERY:
$truncated"
}

cmd_review() {
  local file="${1:?Usage: sql.sh review <sql-file>}"
  check_deps

  echo "Reading SQL..." >&2
  local content
  content=$(read_file "$file")
  local truncated
  truncated=$(echo "$content" | head -c 12000)

  echo "Reviewing security..." >&2
  evolink_ai "You are a database security auditor. Review this SQL for security issues:

1. **SQL Injection risks** — Any string concatenation or unparameterized inputs?
2. **Privilege issues** — Does it require excessive permissions? Any GRANT/REVOKE concerns?
3. **Data exposure** — Could it leak sensitive data (PII, credentials, tokens)?
4. **Destructive operations** — Any DROP, TRUNCATE, DELETE without WHERE, or ALTER that could cause data loss?
5. **Best practices** — Missing constraints, unsafe defaults, or anti-patterns?

Rate overall risk: LOW / MEDIUM / HIGH / CRITICAL.
For each issue found, show the problematic line and the fix." "SQL TO REVIEW:
$truncated"
}

cmd_migrate() {
  local description=""
  local db="postgres"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --db) db="${2:?Missing database}"; shift 2 ;;
      -*) err "Unknown option: $1" ;;
      *) description="$description $1"; shift ;;
    esac
  done

  description=$(echo "$description" | sed 's/^ //')
  [ -z "$description" ] && err "Usage: sql.sh migrate <description> --db <database>"
  check_deps

  echo "Generating migration..." >&2
  evolink_ai "You are a senior database engineer. Generate a database migration for $db based on the description.

Rules:
- Output two sections: -- UP (apply) and -- DOWN (rollback).
- Use $db-specific syntax.
- Include safety checks (IF EXISTS, IF NOT EXISTS) where appropriate.
- Add indexes for foreign keys and commonly queried columns.
- Use appropriate column types and constraints for $db.
- Add comments explaining non-obvious decisions.
- Do NOT wrap in markdown code fences." "MIGRATION REQUEST:
$description"
}

# --- Main ---
COMMAND="${1:-help}"
shift || true

case "$COMMAND" in
  databases)    cmd_databases ;;
  cheatsheet)   cmd_cheatsheet "$@" ;;
  query)        cmd_query "$@" ;;
  explain)      cmd_explain "$@" ;;
  optimize)     cmd_optimize "$@" ;;
  review)       cmd_review "$@" ;;
  migrate)      cmd_migrate "$@" ;;
  help|*)
    echo "SQL Assistant — AI-powered SQL generation and analysis"
    echo ""
    echo "Usage: bash sql.sh <command> [options]"
    echo ""
    echo "Info Commands (no API key needed):"
    echo "  databases                          List supported databases"
    echo "  cheatsheet [database|patterns]     SQL quick reference"
    echo ""
    echo "AI Commands (requires EVOLINK_API_KEY):"
    echo "  query <description> --db <db>      Generate SQL from natural language"
    echo "  explain <sql-file>                 Explain a SQL query"
    echo "  optimize <sql-file> --db <db>      Optimize a SQL query"
    echo "  review <sql-file>                  Security review of SQL"
    echo "  migrate <description> --db <db>    Generate migration SQL"
    echo ""
    echo "Databases: sqlite, postgres, mysql"
    echo ""
    echo "Get a free EvoLink API key: https://evolink.ai/signup"
    ;;
esac
