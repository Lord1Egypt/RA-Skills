---
name: database-schema-differ
description: Compare database schemas across environments, generate migration scripts, and track schema evolution.
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python:
        - sqlalchemy
        - alembic
---

# Database Schema Differ

## What This Does

A CLI tool to compare database schemas across different environments (development, staging, production), generate migration scripts, and track schema evolution over time. Support for PostgreSQL, MySQL, SQLite, and other databases via SQLAlchemy.

Key features:
- **Schema comparison**: Compare schemas between databases, branches, or points in time
- **Migration generation**: Automatically generate SQL migration scripts (up/down) for schema changes
- **Schema snapshots**: Capture and store schema snapshots for historical comparison
- **Drift detection**: Identify schema drift between environments (dev vs prod, etc.)
- **Multiple database support**: PostgreSQL, MySQL, SQLite, SQL Server, Oracle via SQLAlchemy
- **Export formats**: Generate SQL, JSON, or visual diff outputs
- **Integration ready**: Works with Alembic, Django migrations, or standalone
- **Change tracking**: Track schema evolution over time with versioning
- **CI/CD friendly**: Output machine-readable formats for automation pipelines

## When To Use

- You need to compare database schemas between development and production
- You want to generate migration scripts for schema changes
- You're managing multiple database environments and need to ensure consistency
- You need to detect schema drift in production databases
- You're refactoring databases and need to track changes
- You want to automate schema validation in CI/CD pipelines
- You need to document schema changes for compliance or team coordination
- You're onboarding new team members and need to understand schema evolution
- You want to visualize schema differences between branches or versions

## Usage

Basic commands:

```bash
# Compare two database connections
python3 scripts/main.py compare postgresql://user:pass@host1/db postgresql://user:pass@host2/db

# Generate migration script from schema differences
python3 scripts/main.py diff dev_db.sql prod_db.sql --output migration.sql

# Create schema snapshot for future comparison
python3 scripts/main.py snapshot postgresql://user:pass@host/db --save snapshot.json

# Compare current schema with saved snapshot
python3 scripts/main.py compare-snapshot postgresql://user:pass@host/db snapshot.json

# Generate visual diff between schemas
python3 scripts/main.py visual-diff schema1.sql schema2.sql --html diff.html

# Check for schema drift in CI pipeline
python3 scripts/main.py check-drift --expected expected_schema.json --actual actual_schema.json

# Track schema evolution over time
python3 scripts/main.py history postgresql://user:pass@host/db --days 30
```

## Examples

### Example 1: Compare development and production databases

```bash
python3 scripts/main.py compare \
  postgresql://dev_user:dev_pass@localhost/dev_db \
  postgresql://prod_user:prod_pass@prod-host/prod_db \
  --output diff-report.json
```

Output:
```
🔍 Comparing schemas: dev_db (localhost) vs prod_db (prod-host)

📊 Summary:
- Tables: 42 vs 45 (3 missing in dev)
- Columns: 287 vs 295 (8 differences)
- Indexes: 67 vs 72 (5 differences)
- Constraints: 34 vs 38 (4 differences)

⚠️  Differences found (15):
1. Table `audit_logs` missing in dev
   → CREATE TABLE audit_logs (...)
   
2. Column `users.email_verified` missing in dev
   → ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE
   
3. Index `idx_users_email` missing in prod
   → CREATE INDEX idx_users_email ON users(email)
   
4. Constraint `fk_orders_customer_id` differs
   → ALTER TABLE orders DROP CONSTRAINT fk_orders_customer_id_old;
   → ALTER TABLE orders ADD CONSTRAINT fk_orders_customer_id FOREIGN KEY ...

✅ Generated migration: diff-report.json
✅ SQL migration script: migration_20240306_143022.sql
```

### Example 2: Generate migration script

```bash
python3 scripts/main.py diff old_schema.sql new_schema.sql --format sql --output migration.sql
```

Output (migration.sql):
```sql
-- Generated: 2024-03-06 14:30:22
-- Database: PostgreSQL

-- UP Migration
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;

CREATE INDEX idx_users_email ON users(email);

ALTER TABLE orders 
    DROP CONSTRAINT fk_orders_customer_id_old,
    ADD CONSTRAINT fk_orders_customer_id 
    FOREIGN KEY (customer_id) REFERENCES customers(id) 
    ON DELETE CASCADE;

-- DOWN Migration (rollback)
DROP TABLE IF EXISTS audit_logs;

ALTER TABLE users DROP COLUMN IF EXISTS email_verified;

DROP INDEX IF EXISTS idx_users_email;

ALTER TABLE orders 
    DROP CONSTRAINT fk_orders_customer_id,
    ADD CONSTRAINT fk_orders_customer_id_old 
    FOREIGN KEY (customer_id) REFERENCES customers(id);
```

### Example 3: Check for schema drift in CI

```bash
python3 scripts/main.py check-drift \
  --expected schemas/expected/prod.json \
  --actual schemas/actual/prod.json \
  --fail-on-drift
```

Output (CI failure):
```
❌ Schema drift detected!

Differences:
1. Unexpected table `temp_backup` in production
2. Missing index `idx_orders_status` in production
3. Column `users.last_login` has different type (TIMESTAMP vs TIMESTAMPTZ)

Exit code: 1 (failed due to --fail-on-drift)
```

### Example 4: Track schema evolution

```bash
python3 scripts/main.py history postgresql://user:pass@host/db --days 90 --format timeline
```

Output:
```
📅 Schema Evolution Timeline (last 90 days)

2024-03-05: Added audit_logs table (v4.2.0 release)
2024-02-28: Added email_verified column to users table
2024-02-15: Created indexes for performance optimization  
2024-02-01: Added foreign key constraints for data integrity
2024-01-20: Initial schema snapshot (v4.0.0)

📈 Change Statistics:
- Tables: +3 (42 → 45)
- Columns: +23 (272 → 295)
- Indexes: +8 (64 → 72)
- Avg changes per week: 2.1
```

### Example 5: Visual schema comparison

```bash
python3 scripts/main.py visual-diff schema_v1.sql schema_v2.sql --html schema_diff.html
```

Output:
```
✨ Generated visual diff: schema_diff.html

Open in browser to see:
- Side-by-side schema comparison
- Color-coded differences (added/removed/changed)
- Interactive expand/collapse for tables
- Export options for documentation

Differences highlighted:
✅ 5 tables added (green)
❌ 2 tables removed (red)  
🔄 12 columns modified (yellow)
```

## Requirements

- Python 3.x
- SQLAlchemy (for database connectivity)
- Alembic (optional, for migration generation)
- Database drivers: psycopg2 (PostgreSQL), pymysql (MySQL), etc.

Install dependencies:
```bash
pip3 install sqlalchemy alembic psycopg2-binary pymysql
```

## Limitations

- Requires database credentials and network access to compare live databases
- Complex schema changes may require manual review of generated migrations
- Limited support for database-specific features not covered by SQLAlchemy
- Performance may be impacted with very large schemas (1000+ tables)
- No built-in support for NoSQL databases (MongoDB, Redis, etc.)
- Cannot compare encrypted or compressed database dumps
- Limited error handling for connection issues or permission problems
- No support for comparing materialized views or database functions across all DB types
- Generated migrations may not handle data migration or complex transformation
- No built-in support for distributed database comparisons
- Limited to schema structure; does not compare data or indexes optimally
- May not detect all schema differences for databases with custom types or extensions
- No support for comparing database triggers or stored procedures across all database types
- Performance may degrade with very large tables or complex relationships
- No built-in support for schema version control systems (like Liquibase or Flyway)
- Limited error recovery for malformed SQL or corrupted schema files
- No support for real-time schema change monitoring
- Cannot compare schemas across different database types (e.g., PostgreSQL vs MySQL)
- Limited support for database-specific optimizations or extensions
- No built-in notification system for schema drift alerts
- May require manual adjustment of generated migration scripts for production use

## Directory Structure

The tool works with database connection strings, SQL files, or schema snapshot files. No special configuration directories are required.

## Error Handling

- Invalid database connections show helpful error messages with connection details
- Permission errors suggest checking database credentials and access rights
- Schema parsing errors show line numbers and specific SQL issues
- Comparison errors suggest checking schema compatibility or database versions
- File not found errors suggest checking paths and file permissions
- Output generation errors suggest checking disk space and write permissions

## Contributing

This is a skill built by the Skill Factory. Issues and improvements should be reported through the OpenClaw project.