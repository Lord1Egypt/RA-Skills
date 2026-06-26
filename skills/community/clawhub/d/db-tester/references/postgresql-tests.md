# PostgreSQL Specific Tests

## Connection & Version

```sql
SELECT version();
SHOW shared_buffers;
SHOW max_connections;
SELECT count(*) AS active_connections FROM pg_stat_activity;
```

## JSONB Testing

```sql
-- PostgreSQL JSONB is commonly used; test operators
INSERT INTO events (data) VALUES ('{"type":"click","page":"/home","ts":1234}');

-- Query JSONB fields
SELECT * FROM events WHERE data->>'type' = 'click';
SELECT * FROM events WHERE data @> '{"type":"click"}';

-- JSONB index effectiveness
EXPLAIN ANALYZE SELECT * FROM events WHERE data->>'type' = 'click';
-- Should use GIN index if created:
-- CREATE INDEX idx_events_data ON events USING GIN (data);
```

## CTE & Window Function Testing

```sql
-- Test complex queries used in reporting
WITH monthly_sales AS (
  SELECT DATE_TRUNC('month', created_at) AS month,
         SUM(total) AS revenue,
         COUNT(*) AS order_count
  FROM orders
  GROUP BY 1
)
SELECT month, revenue, order_count,
       LAG(revenue) OVER (ORDER BY month) AS prev_month,
       revenue - LAG(revenue) OVER (ORDER BY month) AS growth
FROM monthly_sales;
-- Verify: results match manual calculation for known data
```

## VACUUM & Bloat

```sql
-- Check table bloat
SELECT schemaname, tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
  n_dead_tup, n_live_tup,
  ROUND(n_dead_tup::numeric / NULLIF(n_live_tup, 0) * 100, 2) AS dead_pct
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC LIMIT 10;

-- After bulk operations, verify autovacuum ran
SELECT last_vacuum, last_autovacuum, vacuum_count
FROM pg_stat_user_tables
WHERE relname = 'target_table';
```

## Row-Level Security (RLS)

```sql
-- Test RLS policies
SET ROLE user_a;
SELECT * FROM documents;
-- Should only see user_a's documents

SET ROLE user_b;
SELECT * FROM documents;
-- Should only see user_b's documents

-- Verify bypass not possible
SET ROLE user_a;
UPDATE documents SET owner = 'user_a' WHERE owner = 'user_b';
-- Should affect 0 rows or error
```

## Extension Testing

```sql
-- Common extensions to verify
SELECT extname, extversion FROM pg_extension;

-- PostGIS spatial queries
SELECT ST_Distance(
  ST_GeogFromText('POINT(116.4074 39.9042)'),  -- Beijing
  ST_GeogFromText('POINT(121.4737 31.2304)')    -- Shanghai
) / 1000 AS distance_km;

-- pg_trgm fuzzy search
SELECT * FROM users
WHERE name % '张三'  -- trigram similarity
ORDER BY similarity(name, '张三') DESC;
```
