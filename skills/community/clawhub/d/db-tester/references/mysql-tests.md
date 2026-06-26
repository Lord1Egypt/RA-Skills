# MySQL Specific Tests

## Connection & Version

```sql
SELECT VERSION();
SELECT @@global.innodb_buffer_pool_size / 1024 / 1024 AS buffer_pool_mb;
SHOW VARIABLES LIKE 'max_connections';
SHOW STATUS LIKE 'Threads_connected';
```

## Character Set & Collation

```sql
-- Verify UTF-8 support (important for CJK characters)
SHOW VARIABLES LIKE 'character_set%';
SHOW VARIABLES LIKE 'collation%';

-- Test CJK data
INSERT INTO test_table (name) VALUES ('测试中文');
INSERT INTO test_table (name) VALUES ('テスト');
INSERT INTO test_table (name) VALUES ('🔍 emoji test');
SELECT * FROM test_table WHERE name LIKE '%中文%';
```

## Deadlock Detection

```sql
-- Check recent deadlocks
SHOW ENGINE INNODB STATUS\G
-- Look for: LATEST DETECTED DEADLOCK section

-- Monitor lock waits
SELECT * FROM information_schema.innodb_lock_waits;

-- Test for deadlock (run in two sessions):
-- Session 1:
BEGIN; UPDATE accounts SET balance = 100 WHERE id = 1;
-- Session 2:
BEGIN; UPDATE accounts SET balance = 200 WHERE id = 2;
-- Session 1:
UPDATE accounts SET balance = 100 WHERE id = 2; -- waits
-- Session 2:
UPDATE accounts SET balance = 200 WHERE id = 1; -- deadlock!
```

## Stored Procedure Testing

```sql
-- Test procedure with known inputs
CALL calculate_order_total(1001, @total);
SELECT @total;
-- Verify against expected value

-- Test edge cases
CALL calculate_order_total(NULL, @total);  -- null input
CALL calculate_order_total(99999, @total); -- non-existent order
CALL calculate_order_total(-1, @total);    -- invalid ID
```

## Partition Testing

```sql
-- Verify partition pruning works
EXPLAIN SELECT * FROM logs WHERE created_at = '2024-01-15';
-- Should show: partitions: p202401 (only relevant partition)

-- Verify data in correct partition
SELECT PARTITION_NAME, TABLE_ROWS
FROM information_schema.partitions
WHERE TABLE_NAME = 'logs';
```
