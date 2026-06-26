# SQL Optimization Rules and Best Practices

## Index Optimization

### When to Create Indexes

1. **Columns frequently used in WHERE clauses**
   ```sql
   -- Good: Add index on frequently queried column
   CREATE INDEX idx_user_id ON orders(user_id);
   
   -- Query benefits from index
   SELECT * FROM orders WHERE user_id = 123;
   ```

2. **Columns used in JOIN conditions**
   ```sql
   -- Add index on foreign key columns
   CREATE INDEX idx_order_user_fk ON orders(user_id);
   
   -- JOIN performs better
   SELECT o.*, u.name 
   FROM orders o 
   JOIN users u ON o.user_id = u.id;
   ```

3. **Columns used in ORDER BY and GROUP BY**
   ```sql
   -- Composite index for ORDER BY
   CREATE INDEX idx_status_created ON orders(status, created_at);
   
   -- Query with both WHERE and ORDER BY
   SELECT * FROM orders 
   WHERE status = 'pending' 
   ORDER BY created_at DESC;
   ```

### When NOT to Create Indexes

1. **Small tables** (< 1000 rows)
   - Full table scan may be faster than index lookup

2. **Columns with low cardinality**
   - Gender, status with few distinct values
   - MySQL may ignore the index anyway

3. **Frequently updated columns**
   - Index maintenance overhead
   - Write performance degradation

4. **Columns with many NULL values**
   - Index may not be effective

## Query Optimization Patterns

### 1. Avoid SELECT *

```sql
-- Bad: Retrieves unnecessary columns
SELECT * FROM users WHERE id = 1;

-- Good: Select only needed columns
SELECT id, name, email FROM users WHERE id = 1;
```

### 2. Use Index-Friendly LIKE

```sql
-- Bad: Leading wildcard prevents index usage
SELECT * FROM users WHERE name LIKE '%john%';

-- Good: Trailing wildcard can use index
SELECT * FROM users WHERE name LIKE 'john%';

-- Better: Use full-text search for complex patterns
SELECT * FROM users WHERE MATCH(name) AGAINST('john');
```

### 3. Avoid Functions on Indexed Columns

```sql
-- Bad: Function prevents index usage
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-01';

-- Good: Use range query
SELECT * FROM orders 
WHERE created_at >= '2024-01-01' 
  AND created_at < '2024-01-02';

-- Or use BETWEEN
SELECT * FROM orders 
WHERE created_at BETWEEN '2024-01-01' AND '2024-01-01 23:59:59';
```

### 4. Optimize OR Conditions

```sql
-- Bad: OR may prevent index usage
SELECT * FROM orders 
WHERE user_id = 1 OR user_id = 2 OR user_id = 3;

-- Good: Use IN clause
SELECT * FROM orders WHERE user_id IN (1, 2, 3);

-- Or use UNION for complex conditions
SELECT * FROM orders WHERE user_id = 1
UNION
SELECT * FROM orders WHERE status = 'pending';
```

### 5. Use EXISTS Instead of IN for Subqueries

```sql
-- Bad: IN with subquery may be slow
SELECT * FROM users 
WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);

-- Good: EXISTS is usually faster
SELECT u.* 
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.user_id = u.id AND o.total > 1000
);
```

### 6. Avoid DISTINCT When Possible

```sql
-- Bad: DISTINCT indicates duplicate data
SELECT DISTINCT user_id FROM orders;

-- Good: Use GROUP BY or fix the join
SELECT user_id FROM orders GROUP BY user_id;

-- Or check join conditions
SELECT DISTINCT o.user_id 
FROM orders o 
JOIN order_items oi ON o.id = oi.order_id;
-- May need: AND oi.deleted = 0
```

### 7. Optimize Pagination

```sql
-- Bad: Large offset is slow
SELECT * FROM orders ORDER BY id LIMIT 10000, 20;

-- Good: Use cursor-based pagination
SELECT * FROM orders 
WHERE id > 10000 
ORDER BY id 
LIMIT 20;

-- Or use deferred join for complex queries
SELECT o.* 
FROM orders o
INNER JOIN (
    SELECT id FROM orders ORDER BY id LIMIT 10000, 20
) tmp ON o.id = tmp.id;
```

### 8. Use Covering Indexes

```sql
-- Create covering index with all selected columns
CREATE INDEX idx_user_covering ON users(status, name, email);

-- Query can be satisfied by index only
SELECT name, email FROM users WHERE status = 'active';
-- No need to access table data
```

## Join Optimization

### 1. Use Appropriate Join Types

```sql
-- INNER JOIN: Only matching rows
SELECT o.*, u.name 
FROM orders o 
INNER JOIN users u ON o.user_id = u.id;

-- LEFT JOIN: All from left, matching from right
SELECT u.*, o.id as order_id
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Use LEFT JOIN to find users without orders
SELECT u.* 
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

### 2. Join Order Matters

```sql
-- Start with smallest table or most selective filter
SELECT o.*, u.name, p.title
FROM orders o  -- Filter first
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id
WHERE o.created_at > '2024-01-01';  -- Reduces rows early
```

### 3. Avoid Cartesian Products

```sql
-- Bad: Missing join condition
SELECT u.name, o.total
FROM users u, orders o;

-- Good: Always specify join condition
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

## Subquery Optimization

### 1. Correlated vs Non-Correlated Subqueries

```sql
-- Correlated: Executed for each row (slow)
SELECT * FROM users u
WHERE (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) > 5;

-- Better: Use JOIN with GROUP BY
SELECT u.* 
FROM users u
INNER JOIN orders o ON u.id = o.user_id
GROUP BY u.id
HAVING COUNT(o.id) > 5;
```

### 2. Use Derived Tables for Complex Queries

```sql
-- Derived table for intermediate results
SELECT u.name, order_stats.total_orders
FROM users u
INNER JOIN (
    SELECT user_id, COUNT(*) as total_orders
    FROM orders
    GROUP BY user_id
) order_stats ON u.id = order_stats.user_id;
```

## Execution Plan Analysis

### Key Metrics to Check

1. **type** (MySQL) / **Scan Type** (PostgreSQL)
   - `ALL`: Full table scan (usually bad)
   - `index`: Full index scan
   - `range`: Index range scan (good)
   - `ref`: Index lookup (good)
   - `const`: Single row lookup (best)

2. **Extra** field warnings
   - `Using filesort`: Slow sorting
   - `Using temporary`: Temporary table created
   - `Using index`: Good - covering index used
   - `Using where`: Filtering in progress

### Example Analysis

```sql
EXPLAIN SELECT o.*, u.name 
FROM orders o 
JOIN users u ON o.user_id = u.id 
WHERE o.status = 'pending';

-- Look for:
-- 1. No 'ALL' type scans
-- 2. Appropriate indexes used (key column)
-- 3. Reasonable rows estimate
-- 4. No filesort or temporary table warnings
```

## Common Anti-Patterns

### 1. N+1 Query Problem

```java
// Bad: Query inside loop
List<User> users = getUsers();
for (User user : users) {
    List<Order> orders = getOrdersByUser(user.getId());
}

-- Good: Single query with JOIN
SELECT u.*, o.id as order_id, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

### 2. Unnecessary Subqueries

```sql
-- Bad: Subquery for simple value
SELECT * FROM orders 
WHERE user_id = (SELECT id FROM users WHERE email = 'test@example.com');

-- Good: Use JOIN
SELECT o.* 
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.email = 'test@example.com';
```

### 3. Implicit Type Conversion

```sql
-- Bad: String comparison with number column
SELECT * FROM orders WHERE user_id = '123';  -- user_id is INT

-- Good: Use correct type
SELECT * FROM orders WHERE user_id = 123;
```

## Performance Monitoring Queries

### Find Slow Queries

```sql
-- MySQL: Query performance schema
SELECT * FROM sys.statements_with_runtimes_in_95th_percentile;

-- PostgreSQL: pg_stat_statements
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### Find Missing Indexes

```sql
-- MySQL: Unused indexes
SELECT * FROM sys.schema_unused_indexes;

-- PostgreSQL: Suggested indexes
SELECT * FROM pg_stat_user_indexes 
WHERE idx_scan = 0 AND idx_tup_read = 0;
```

### Table Size Analysis

```sql
-- MySQL
SELECT 
    table_name,
    ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = DATABASE()
ORDER BY (data_length + index_length) DESC;

-- PostgreSQL
SELECT 
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(relid)) AS size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```
