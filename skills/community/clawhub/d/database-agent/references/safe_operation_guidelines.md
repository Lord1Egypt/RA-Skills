# Safe Database Operation Guidelines

## Overview

Database operations, especially bulk updates and deletions, carry significant risk. This guide establishes safety protocols to prevent data loss, ensure reversibility, and maintain data integrity.

## Core Safety Principles

### 1. Always Have a Backup

**Before any data modification:**
```sql
-- Create backup table
CREATE TABLE users_backup_20240101 AS SELECT * FROM users;

-- Or export to file
SELECT * INTO OUTFILE '/tmp/users_backup.csv'
FIELDS TERMINATED BY ','
FROM users;
```

### 2. Always Use Transactions

```sql
-- Start transaction
START TRANSACTION;

-- Perform operations
UPDATE users SET status = 1 WHERE created_at < '2024-01-01';

-- Verify results
SELECT COUNT(*) FROM users WHERE status = 1;

-- Commit only if everything is correct
COMMIT;
-- Or rollback if issues found
-- ROLLBACK;
```

### 3. Test in Non-Production First

- Always test SQL scripts in development/staging environment
- Verify data volume and execution time
- Check for unexpected side effects

### 4. Get Confirmation for Large Operations

- Operations affecting >1000 rows require review
- Operations affecting >10000 rows require approval
- Always estimate affected rows before execution

## Risk Assessment Matrix

| Operation Type | Risk Level | Required Actions |
|---------------|------------|------------------|
| SELECT queries | Low | None |
| Single-row INSERT | Low | None |
| Single-row UPDATE with WHERE by PK | Low | Backup recommended |
| Multi-row UPDATE (1-1000 rows) | Medium | Backup + Transaction + Review |
| Multi-row UPDATE (1000+ rows) | High | Backup + Transaction + Approval + Batch Processing |
| DELETE with WHERE by PK | Medium | Backup + Transaction + Review |
| DELETE with complex WHERE | High | Backup + Transaction + Approval |
| DELETE without WHERE | CRITICAL | NEVER ALLOWED |
| TRUNCATE TABLE | CRITICAL | NEVER ALLOWED |
| DROP TABLE | CRITICAL | NEVER ALLOWED |

## Dangerous Operations Checklist

### ❌ NEVER Do These

1. **UPDATE/DELETE without WHERE clause**
   ```sql
   -- NEVER DO THIS
   UPDATE users SET status = 1;  -- Updates ALL rows!
   DELETE FROM orders;  -- Deletes ALL rows!
   
   -- ALWAYS use WHERE
   UPDATE users SET status = 1 WHERE id = 123;
   DELETE FROM orders WHERE id = 456;
   ```

2. **WHERE clause that's always true**
   ```sql
   -- NEVER DO THIS
   DELETE FROM users WHERE 1=1;
   DELETE FROM users WHERE TRUE;
   
   -- Use specific conditions
   DELETE FROM users WHERE created_at < '2020-01-01' AND status = 'inactive';
   ```

3. **OR 1=1 injection pattern**
   ```sql
   -- NEVER DO THIS
   DELETE FROM users WHERE id = 123 OR 1=1;
   ```

4. **TRUNCATE without backup**
   ```sql
   -- AVOID THIS - irreversible
   TRUNCATE TABLE orders;
   
   -- Use DELETE instead (slower but safer)
   DELETE FROM orders WHERE created_at < '2023-01-01';
   ```

5. **DROP TABLE without backup**
   ```sql
   -- AVOID THIS - irreversible
   DROP TABLE old_data;
   
   -- Rename instead
   RENAME TABLE old_data TO old_data_backup_20240101;
   ```

### ⚠️ REQUIRES Extra Caution

1. **Updating primary keys**
   ```sql
   -- Dangerous - may break foreign key relationships
   UPDATE users SET id = 999 WHERE id = 1;
   
   -- Better: Don't update primary keys
   -- Or ensure all FKs are updated first
   ```

2. **Deleting by non-indexed column**
   ```sql
   -- Slow on large tables, may lock table
   DELETE FROM orders WHERE YEAR(created_at) = 2023;
   
   -- Better: Use indexed column
   DELETE FROM orders 
   WHERE created_at BETWEEN '2023-01-01' AND '2023-12-31'
   LIMIT 1000;  -- Batch delete
   ```

3. **Cascading deletes**
   ```sql
   -- Dangerous - may delete more than expected
   CREATE TABLE orders (
       user_id INT,
       FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
   );
   
   -- Better: Use RESTRICT and delete manually
   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
   ```

## Safe Operation Procedures

### For UPDATE Operations

#### Step 1: Estimate Affected Rows
```sql
-- Count before executing
SELECT COUNT(*) FROM users 
WHERE last_login < '2023-01-01' AND status = 'active';

-- Expected: 1234 rows
```

#### Step 2: Create Backup
```sql
-- Create backup table with timestamp
CREATE TABLE users_backup_20240101_143000 AS 
SELECT * FROM users 
WHERE last_login < '2023-01-01' AND status = 'active';
```

#### Step 3: Start Transaction
```sql
START TRANSACTION;
```

#### Step 4: Execute UPDATE
```sql
-- For large operations, batch process
UPDATE users 
SET status = 'inactive' 
WHERE last_login < '2023-01-01' 
  AND status = 'active'
LIMIT 1000;

-- Repeat until all rows updated
-- Check rows affected after each batch
```

#### Step 5: Verify Results
```sql
-- Check the update
SELECT status, COUNT(*) 
FROM users 
WHERE last_login < '2023-01-01'
GROUP BY status;

-- Verify count matches expected
```

#### Step 6: Commit or Rollback
```sql
-- If verification passed
COMMIT;

-- If issues found
ROLLBACK;
-- Restore from backup if needed
INSERT INTO users SELECT * FROM users_backup_20240101_143000;
```

### For DELETE Operations

#### Step 1: Estimate and Backup
```sql
-- Count
SELECT COUNT(*) FROM logs WHERE created_at < '2023-01-01';

-- Backup (IMPORTANT!)
CREATE TABLE logs_backup_20240101 AS 
SELECT * FROM logs WHERE created_at < '2023-01-01';
```

#### Step 2: Batch Delete with LIMIT
```sql
-- Start transaction
START TRANSACTION;

-- Batch delete (repeat until 0 rows affected)
DELETE FROM logs 
WHERE created_at < '2023-01-01' 
LIMIT 1000;

-- Repeat...
-- When done, commit
COMMIT;
```

#### Step 3: Verify and Rollback Script Ready
```sql
-- Verification
SELECT COUNT(*) FROM logs WHERE created_at < '2023-01-01';
-- Should be 0

-- Rollback script (prepare before operation)
INSERT INTO logs SELECT * FROM logs_backup_20240101;
```

### For Bulk INSERT Operations

#### Use Batch Insert
```sql
-- Bad: Individual inserts
INSERT INTO users (name) VALUES ('User1');
INSERT INTO users (name) VALUES ('User2');
-- ... slow and inefficient

-- Good: Batch insert
INSERT INTO users (name, email) VALUES
    ('User1', 'user1@test.com'),
    ('User2', 'user2@test.com'),
    ('User3', 'user3@test.com');
-- Up to 1000 rows per batch
```

#### For Very Large Datasets
```sql
-- Use LOAD DATA INFILE (MySQL)
LOAD DATA INFILE '/path/to/data.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(name, email, created_at);

-- Or use COPY (PostgreSQL)
COPY users(name, email, created_at)
FROM '/path/to/data.csv'
DELIMITER ','
CSV HEADER;
```

## Rollback Procedures

### 1. Using Transaction Rollback
```sql
-- If operation is still in transaction
ROLLBACK;
```

### 2. Using Backup Table
```sql
-- For UPDATE
UPDATE target_table t
JOIN backup_table b ON t.id = b.id
SET t.column = b.column;

-- For DELETE
INSERT INTO target_table 
SELECT * FROM backup_table;

-- For DROP
RENAME TABLE backup_table TO target_table;
```

### 3. Using Binary Logs (MySQL)
```bash
# Find the transaction in binlog
mysqlbinlog /var/lib/mysql/mysql-bin.000123

# Generate rollback SQL
mysqlbinlog --flashback \
  --start-datetime="2024-01-01 14:00:00" \
  --stop-datetime="2024-01-01 14:30:00" \
  /var/lib/mysql/mysql-bin.000123 > rollback.sql

# Execute rollback
mysql -u root -p database < rollback.sql
```

## Monitoring and Logging

### Log All Data Modifications
```sql
-- Create audit log table
CREATE TABLE data_modification_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    affected_rows INT NOT NULL,
    sql_statement TEXT NOT NULL,
    executed_by VARCHAR(50) NOT NULL,
    executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Log after each operation
INSERT INTO data_modification_log 
(table_name, operation, affected_rows, sql_statement, executed_by)
VALUES 
('users', 'UPDATE', 1234, 'UPDATE users SET status = ...', 'admin');
```

### Monitor Long-Running Operations
```sql
-- Check running queries
SHOW PROCESSLIST;

-- Kill long-running query if needed
KILL 12345;  -- Process ID
```

## Emergency Procedures

### Accidental Data Deletion

1. **Stop all writes immediately**
   ```sql
   -- Lock tables (if needed)
   FLUSH TABLES WITH READ LOCK;
   ```

2. **Don't close the connection** - Transaction may still be rollbackable

3. **Check for backup availability**
   - Check backup table
   - Check binary logs
   - Check database backups

4. **Contact DBA immediately**

### Recovery Steps
```sql
-- Option 1: Restore from backup table
INSERT INTO target_table SELECT * FROM backup_table;

-- Option 2: Use binary logs
-- (See Rollback Procedures section)

-- Option 3: Restore from database backup
-- (Contact DBA)
```

## Checklist Before Data Modification

- [ ] Estimated number of affected rows
- [ ] Created backup table or exported data
- [ ] Started transaction
- [ ] Prepared rollback script
- [ ] Tested in non-production environment
- [ ] Verified WHERE clause logic
- [ ] Added LIMIT for large operations
- [ ] Got approval for high-risk operations (>1000 rows)
- [ ] Scheduled during low-traffic period
- [ ] Notified team members
- [ ] Monitoring tools ready
- [ ] Documented the operation

## Best Practices Summary

1. ✅ **ALWAYS use WHERE clause** in UPDATE/DELETE
2. ✅ **ALWAYS use LIMIT** for batch operations
3. ✅ **ALWAYS use transactions** for data modifications
4. ✅ **ALWAYS create backup** before risky operations
5. ✅ **ALWAYS test in staging** before production
6. ✅ **ALWAYS estimate affected rows** first
7. ✅ **ALWAYS verify results** before committing
8. ✅ **ALWAYS have rollback plan** ready
9. ✅ **ALWAYS log operations** for audit trail
10. ✅ **ALWAYS get approval** for large operations

## Prohibited Actions

1. ❌ UPDATE/DELETE without WHERE clause
2. ❌ TRUNCATE TABLE without explicit approval
3. ❌ DROP TABLE without backup
4. ❌ Executing untested SQL in production
5. ❌ Modifying data without transaction
6. ❌ Skipping backup for bulk operations
7. ❌ WHERE 1=1 or WHERE TRUE conditions
8. ❌ OR 1=1 patterns (injection risk)
9. ❌ Updating primary key columns
10. ❌ Disabling foreign key checks
