---
name: db-tester
description: >
  Database testing for data integrity, SQL validation, migration verification,
  and performance. Test CRUD operations, constraints, transactions, stored procedures,
  and data consistency across MySQL, PostgreSQL, SQLite, and other RDBMS.
  Use when: (1) validating database operations, (2) testing data migrations,
  (3) checking constraints and triggers, (4) verifying data consistency after API calls,
  (5) writing SQL test scripts, (6) database performance testing (slow queries),
  (7) "数据库测试", "SQL验证", "数据一致性", "迁移测试", "数据校验",
  "存储过程测试", "数据库性能", "慢查询".
  NOT for: database administration (use DBA tools), schema design (use modeling tools),
  or ORM/application code testing (use api-tester or unit tests).
---

# Database Tester

Validate database operations, data integrity, and migrations.

## Test Categories

| Category | Focus | When |
|----------|-------|------|
| **CRUD** | Insert/Select/Update/Delete correctness | Every release |
| **Constraints** | PK, FK, UNIQUE, NOT NULL, CHECK | Schema changes |
| **Transactions** | ACID compliance, isolation levels | Concurrent features |
| **Migration** | Schema + data migration correctness | Version upgrades |
| **Performance** | Slow queries, index effectiveness | Performance issues |
| **Security** | SQL injection, permissions, encryption | Security reviews |

## Quick Database Validation

### Connect & Inspect

```bash
# MySQL
mysql -h $DB_HOST -u $DB_USER -p$DB_PASS $DB_NAME -e "SHOW TABLES;"

# PostgreSQL
PGPASSWORD=$DB_PASS psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "\dt"

# SQLite
sqlite3 $DB_FILE ".tables"
```

### Schema Comparison (Migration Verification)

```sql
-- MySQL: Get table structure
SHOW CREATE TABLE users;
DESCRIBE users;

-- PostgreSQL: Get table structure
\d+ users
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- Compare expected vs actual columns
-- After migration, verify:
-- 1. New columns exist with correct type/default
-- 2. Dropped columns are gone
-- 3. Modified columns have new type/constraints
-- 4. Indexes are created/dropped as expected
```

## Constraint Testing

For each table, verify constraints are enforced:

```sql
-- NOT NULL: Insert null into required field → should fail
INSERT INTO users (name, email) VALUES (NULL, 'test@example.com');
-- Expected: ERROR (NOT NULL violation)

-- UNIQUE: Insert duplicate value → should fail
INSERT INTO users (name, email) VALUES ('Test', 'existing@example.com');
-- Expected: ERROR (UNIQUE violation)

-- FOREIGN KEY: Insert invalid reference → should fail
INSERT INTO orders (user_id, total) VALUES (99999, 100.00);
-- Expected: ERROR (FK violation)

-- CHECK constraint
INSERT INTO products (name, price) VALUES ('Test', -10);
-- Expected: ERROR (CHECK violation, price must be >= 0)

-- CASCADE: Delete parent → verify child behavior
DELETE FROM users WHERE id = 1;
-- Verify: orders for user_id=1 are CASCADE deleted/SET NULL per FK rule
```

## Data Migration Testing

### Pre-Migration Checklist

```sql
-- 1. Record baseline counts
SELECT 'users' AS tbl, COUNT(*) AS cnt FROM users
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'products', COUNT(*) FROM products;

-- 2. Record sample checksums
SELECT MD5(GROUP_CONCAT(id, name, email ORDER BY id)) AS checksum
FROM users WHERE id BETWEEN 1 AND 100;

-- 3. Record key aggregates
SELECT SUM(total) AS total_revenue FROM orders;
SELECT COUNT(DISTINCT user_id) AS active_users FROM orders;
```

### Post-Migration Verification

```sql
-- 1. Row counts match (or differ by expected amount)
-- 2. Checksums match for unchanged data
-- 3. Aggregates match
-- 4. New columns have correct defaults
-- 5. Transformed data is correct

-- Verify data transformation
SELECT id, old_column, new_column,
  CASE WHEN new_column = EXPECTED_TRANSFORM(old_column)
    THEN 'OK' ELSE 'MISMATCH' END AS status
FROM migrated_table
WHERE status = 'MISMATCH';
```

### Migration Rollback Test

1. Take snapshot/backup before migration
2. Run migration forward
3. Verify data integrity
4. Run migration rollback
5. Verify data matches pre-migration snapshot

## Transaction & ACID Testing

### Atomicity

```sql
-- Start transaction, perform multiple operations, simulate failure
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- Simulate error before commit
ROLLBACK;
-- Verify: both balances unchanged
```

### Isolation Levels

| Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|-------|-----------|-------------------|-------------|
| READ UNCOMMITTED | ✅ possible | ✅ possible | ✅ possible |
| READ COMMITTED | ❌ prevented | ✅ possible | ✅ possible |
| REPEATABLE READ | ❌ prevented | ❌ prevented | ✅ possible |
| SERIALIZABLE | ❌ prevented | ❌ prevented | ❌ prevented |

Reference: SQL:2016 standard, ISO/IEC 9075

Test procedure: Open two concurrent sessions, verify isolation behavior.

## Performance: Slow Query Analysis

```sql
-- MySQL: Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- seconds

-- MySQL: Find slow queries
SELECT query, exec_count, avg_latency, rows_examined_avg
FROM sys.statements_with_runtimes_in_95th_percentile
ORDER BY avg_latency DESC LIMIT 10;

-- PostgreSQL: Find slow queries
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;

-- Check missing indexes
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
-- Look for: Seq Scan (bad) vs Index Scan (good)
-- Look for: high rows examined vs rows returned ratio
```

### Index Effectiveness

```sql
-- MySQL: Check index usage
SELECT table_name, index_name, seq_in_index, column_name
FROM information_schema.statistics
WHERE table_schema = DATABASE()
ORDER BY table_name, index_name, seq_in_index;

-- Unused indexes (MySQL 8.0+)
SELECT * FROM sys.schema_unused_indexes;

-- PostgreSQL: Unused indexes
SELECT indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Python Test Script Pattern

```python
"""Database test suite using pytest + direct DB connection.
Reference: PEP 249 (DB-API 2.0)
"""
import pytest
import os

# Use appropriate driver: mysql-connector-python, psycopg2, sqlite3
import mysql.connector  # or psycopg2 for PostgreSQL

@pytest.fixture
def db():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "test"),
        password=os.getenv("DB_PASS", "test"),
        database=os.getenv("DB_NAME", "testdb"),
    )
    yield conn
    conn.rollback()  # always rollback test changes
    conn.close()

class TestUserTable:
    def test_insert_valid_user(self, db):
        cur = db.cursor()
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            ("Test User", "test@example.com"))
        assert cur.rowcount == 1

    def test_insert_duplicate_email_fails(self, db):
        cur = db.cursor()
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            ("User1", "dup@example.com"))
        with pytest.raises(Exception):  # IntegrityError
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                ("User2", "dup@example.com"))

    def test_not_null_constraint(self, db):
        cur = db.cursor()
        with pytest.raises(Exception):
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (None, "test@example.com"))

    def test_cascade_delete(self, db):
        cur = db.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (1,))
        cur.execute("SELECT COUNT(*) FROM orders WHERE user_id = %s", (1,))
        assert cur.fetchone()[0] == 0  # orders cascade deleted
```

## Data Consistency Verification

After API operations, verify database state:

```bash
# Pattern: API call → DB check
# 1. Call API to create order
curl -X POST "$URL/api/orders" -d '{"item_id":1,"qty":2}'

# 2. Verify in database
mysql -e "SELECT * FROM orders ORDER BY id DESC LIMIT 1;" $DB_NAME
mysql -e "SELECT stock FROM products WHERE id = 1;" $DB_NAME
# Verify: stock decreased by 2
```

## References

For database-specific testing details:
- **MySQL specific tests**: See `references/mysql-tests.md`
- **PostgreSQL specific tests**: See `references/postgresql-tests.md`
