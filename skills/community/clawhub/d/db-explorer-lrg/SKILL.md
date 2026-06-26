---
name: db-explorer
description: "Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis). Run queries, inspect schemas, export data. Use when user wants to query a database, explore schema, check data, export results, or debug database issues."
version: 2.5.0
author: lrg913427-dot
license: MIT
metadata:
  hermes:
    tags: [database, sql, postgresql, mysql, sqlite, mongodb, redis, query, schema, data]
    related_skills: [jupyter-live-kernel, airtable]
---

# DB Explorer

Connect to databases, run queries, explore schemas, and export data — all from the terminal.

## When to Use

Activate this skill when the user:
- Says "check the database", "query the DB", "show me the data"
- Wants to see table structure, row counts, or sample data
- Needs to export data to CSV/JSON
- Wants to find slow queries or check DB health
- Mentions a database connection string or DB name

## Supported Databases

| Database   | CLI Tool     | Install (macOS)           | Install (Linux)                    |
|-----------|-------------|---------------------------|-----------------------------------|
| PostgreSQL | psql        | brew install postgresql    | apt install postgresql-client      |
| MySQL      | mysql       | brew install mysql         | apt install mysql-client           |
| SQLite     | sqlite3     | (built-in on macOS)       | apt install sqlite3                |
| MongoDB    | mongosh     | brew install mongosh       | See mongodb.com/docs/shell         |
| Redis      | redis-cli   | brew install redis         | apt install redis-tools            |

## Quick Start

### 1. Identify the Database

Ask the user for:
- Database type (postgres/mysql/sqlite/mongo/redis)
- Connection string OR host/port/database/user/password
- For SQLite: just the file path

### 2. Connect and Explore

```bash
# PostgreSQL
psql "postgresql://user:password@host:5432/dbname" -c "\dt"           # list tables
psql "postgresql://user:password@host:5432/dbname" -c "\d table_name" # describe table
psql "postgresql://user:password@host:5432/dbname" -c "SELECT count(*) FROM table_name;"

# MySQL
mysql -h host -u user -p dbname -e "SHOW TABLES;"
mysql -h host -u user -p dbname -e "DESCRIBE table_name;"
mysql -h host -u user -p dbname -e "SELECT count(*) FROM table_name;"

# SQLite
sqlite3 /path/to/db.db ".tables"                    # list tables
sqlite3 /path/to/db.db ".schema table_name"         # describe table
sqlite3 /path/to/db.db "SELECT count(*) FROM table_name;"

# MongoDB
mongosh "mongodb://user:password@host:27017/dbname" --eval "db.getCollectionNames()"
mongosh "mongodb://user:password@host:27017/dbname" --eval "db.collection_name.countDocuments()"

# Redis
redis-cli -h host -p 6379 -a password INFO keyspace
redis-cli -h host -p 6379 -a password DBSIZE
redis-cli -h host -p 6379 -a password KEYS "*"
```

### 3. Safety Rules

**ALWAYS follow these rules:**

1. **Read-only by default** — Never run INSERT/UPDATE/DELETE/DROP without explicit user confirmation
2. **Limit results** — Always add `LIMIT 100` (or equivalent) to SELECT queries unless user asks for all
3. **Show before execute** — For any write operation, show the exact SQL/command and ask for confirmation
4. **No passwords in history** — Use environment variables or connection strings, don't echo passwords
5. **Transaction safety** — For writes, wrap in BEGIN/ROLLBACK first, show results, then ask to COMMIT

### 4. Schema Exploration Workflow

When user says "explore the database" or "show me the schema":

```bash
# Step 1: List all tables
# Step 2: For each table, show columns, types, and constraints
# Step 3: Show row counts
# Step 4: Show foreign key relationships
# Step 5: Summarize as a readable schema map
```

PostgreSQL full schema dump:
```bash
psql "$CONN" -c "
SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
"
```

MySQL full schema dump:
```bash
mysql "$CONN" -e "
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME, ORDINAL_POSITION;
"
```

### 5. Export Formats

Export query results to common formats:

```bash
# CSV (PostgreSQL)
psql "$CONN" -c "\copy (SELECT * FROM table_name) TO '/tmp/export.csv' WITH CSV HEADER"

# CSV (MySQL)
mysql "$CONN" -e "SELECT * FROM table_name" | sed 's/\t/,/g' > /tmp/export.csv

# JSON (PostgreSQL)
psql "$CONN" -t -c "SELECT json_agg(t) FROM (SELECT * FROM table_name LIMIT 100) t;" > /tmp/export.json

# SQLite to CSV
sqlite3 /path/to/db.db ".mode csv" ".headers on" ".output /tmp/export.csv" "SELECT * FROM table_name;" ".quit"
```

### 6. Common Diagnostic Queries

```sql
-- PostgreSQL: Table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables WHERE schemaname = 'public' ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- PostgreSQL: Active connections
SELECT pid, usename, application_name, client_addr, state, query_start, query
FROM pg_stat_activity WHERE state != 'idle';

-- PostgreSQL: Slow queries (> 1s)
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity WHERE state = 'active' AND now() - pg_stat_activity.query_start > interval '1 second';

-- MySQL: Table sizes
SELECT table_name, ROUND(data_length/1024/1024, 2) AS data_mb, table_rows
FROM information_schema.tables WHERE table_schema = DATABASE() ORDER BY data_length DESC;

-- MySQL: Process list
SHOW FULL PROCESSLIST;
```

## Performance Analysis

### PostgreSQL Performance

```bash
# Slow queries (active for > 1s)
psql "$CONN" -c "
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > interval '1 second'
ORDER BY duration DESC;
"

# Index usage
psql "$CONN" -c "
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC LIMIT 20;
"

# Table bloat
psql "$CONN" -c "
SELECT schemaname, tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
  pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC LIMIT 10;
"

# Cache hit ratio (should be > 99%)
psql "$CONN" -c "
SELECT
  sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS cache_hit_ratio
FROM pg_statio_user_tables;
"
```

### MySQL Performance

```bash
# Slow queries
mysql "$CONN" -e "SELECT * FROM information_schema.processlist WHERE TIME > 1 ORDER BY TIME DESC;"

# Index usage
mysql "$CONN" -e "
SELECT table_name, index_name, cardinality
FROM information_schema.statistics
WHERE table_schema = DATABASE()
ORDER BY cardinality DESC LIMIT 20;
"

# Table sizes
mysql "$CONN" -e "
SELECT table_name,
  ROUND(data_length/1024/1024, 2) AS data_mb,
  ROUND(index_length/1024/1024, 2) AS index_mb,
  table_rows
FROM information_schema.tables
WHERE table_schema = DATABASE()
ORDER BY data_length DESC LIMIT 10;
"
```

## Backup & Restore

### PostgreSQL

```bash
# Backup single database
pg_dump "$CONN" > backup_$(date +%Y%m%d).sql

# Backup single table
pg_dump "$CONN" -t table_name > table_backup.sql

# Restore
psql "$CONN" < backup.sql

# Backup with compression
pg_dump "$CONN" | gzip > backup_$(date +%Y%m%d).sql.gz
```

### MySQL

```bash
# Backup single database
mysqldump -h host -u user -p dbname > backup_$(date +%Y%m%d).sql

# Backup single table
mysqldump -h host -u user -p dbname table_name > table_backup.sql

# Restore
mysql -h host -u user -p dbname < backup.sql
```

### SQLite

```bash
# Backup
sqlite3 /path/to/db.db ".backup /tmp/backup.db"

# Or just copy
cp /path/to/db.db /tmp/backup_$(date +%Y%m%d).db
```

## Data Migration Helpers

### Copy table between databases

```bash
# PostgreSQL to CSV to MySQL
psql "$PG_CONN" -c "\copy table_name TO '/tmp/export.csv' WITH CSV HEADER"
mysql "$MYSQL_CONN" -e "LOAD DATA LOCAL INFILE '/tmp/export.csv' INTO TABLE table_name FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"
```

### Schema comparison

```bash
# Get PostgreSQL schema hash for comparison
psql "$CONN" -c "
SELECT md5(string_agg(table_name || column_name || data_type, '' ORDER BY table_name, ordinal_position))
FROM information_schema.columns
WHERE table_schema = 'public';
"
```

## Pitfalls

- **Connection strings with special chars** — URL-encode passwords containing @, :, /, etc.
- **SSL requirements** — Many cloud databases (RDS, Cloud SQL, Supabase) require `?sslmode=require` or `--ssl-mode=REQUIRED`
- **Timeout on large tables** — Always LIMIT unless user explicitly wants full export
- **SQLite locking** — Only one writer at a time; use WAL mode for concurrent reads: `PRAGMA journal_mode=WAL;`
- **MongoDB auth database** — Sometimes auth is on `admin` db, not the target db: `?authSource=admin`
- **Redis SELECT** — Redis has 16 databases (0-15); check which one: `redis-cli INFO keyspace`

## Verification

After connecting:
1. Run a simple query to confirm connection works
2. List tables/collections to show the schema
3. Run a count query on a key table to verify data access
4. Check cache hit ratio (PostgreSQL) or slow queries (MySQL)
5. Verify backup capability with a test dump

## Environment Variables

The skill uses these if available:
- `DATABASE_URL` — Full connection string (takes priority)
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` — Individual params
- `DB_TYPE` — postgres/mysql/sqlite/mongo/redis
