# Query Patterns Reference

Comprehensive collection of SQL query patterns for common use cases with SyneHQ Kole.

## Table of Contents

- [Data Exploration](#data-exploration)
- [Business Analytics](#business-analytics)
- [Customer Analysis](#customer-analysis)
- [Time-Series Analysis](#time-series-analysis)
- [Data Quality](#data-quality)
- [Performance Optimization](#performance-optimization)
- [PostgreSQL Specific](#postgresql-specific)

## Data Exploration

### Quick Table Samples

```sql
-- Get first 10 rows
SELECT * FROM users LIMIT 10;

-- Get random sample
SELECT * FROM users ORDER BY RANDOM() LIMIT 100;

-- Get recent records
SELECT * FROM orders 
ORDER BY created_at DESC 
LIMIT 20;
```

### Column Statistics

```sql
-- Basic statistics
SELECT 
  COUNT(*) as total_rows,
  COUNT(DISTINCT email) as unique_emails,
  COUNT(*) FILTER (WHERE email IS NULL) as null_emails,
  MIN(created_at) as earliest_record,
  MAX(created_at) as latest_record
FROM users;

-- Numeric column stats
SELECT 
  COUNT(*) as count,
  AVG(total_amount) as avg_amount,
  MIN(total_amount) as min_amount,
  MAX(total_amount) as max_amount,
  STDDEV(total_amount) as stddev_amount,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_amount) as median_amount
FROM orders;
```

### Value Distribution

```sql
-- Count by category
SELECT 
  status,
  COUNT(*) as count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
FROM orders
GROUP BY status
ORDER BY count DESC;

-- Top values
SELECT 
  country,
  COUNT(*) as user_count
FROM users
GROUP BY country
ORDER BY user_count DESC
LIMIT 10;
```

## Business Analytics

### Revenue Analysis

```sql
-- Daily revenue
SELECT 
  DATE(order_date) as date,
  COUNT(*) as order_count,
  SUM(total_amount) as daily_revenue,
  AVG(total_amount) as avg_order_value
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(order_date)
ORDER BY date DESC;

-- Monthly revenue with growth
SELECT 
  DATE_TRUNC('month', order_date) as month,
  SUM(total_amount) as revenue,
  LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)) as prev_month_revenue,
  ROUND(
    ((SUM(total_amount) - LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('month', order_date))) 
    / LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)) * 100)::numeric, 
    2
  ) as growth_pct
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month DESC;
```

### Product Analysis

```sql
-- Best selling products
SELECT 
  p.product_name,
  COUNT(oi.id) as units_sold,
  SUM(oi.quantity * oi.unit_price) as total_revenue,
  AVG(oi.quantity) as avg_quantity_per_order
FROM order_items oi
JOIN products p ON oi.product_id = p.id
WHERE oi.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY p.id, p.product_name
ORDER BY total_revenue DESC
LIMIT 20;

-- Product performance by category
SELECT 
  p.category,
  COUNT(DISTINCT oi.order_id) as order_count,
  COUNT(oi.id) as item_count,
  SUM(oi.quantity * oi.unit_price) as revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.category
ORDER BY revenue DESC;
```

## Customer Analysis

### Customer Lifetime Value

```sql
-- CLV by customer
SELECT 
  u.id,
  u.email,
  u.name,
  COUNT(o.id) as total_orders,
  SUM(o.total_amount) as lifetime_value,
  AVG(o.total_amount) as avg_order_value,
  MIN(o.order_date) as first_order_date,
  MAX(o.order_date) as last_order_date,
  EXTRACT(DAY FROM NOW() - MAX(o.order_date)) as days_since_last_order
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.email, u.name
HAVING COUNT(o.id) > 0
ORDER BY lifetime_value DESC
LIMIT 50;
```

### Customer Segmentation

```sql
-- RFM segmentation
WITH rfm_calc AS (
  SELECT 
    user_id,
    EXTRACT(DAY FROM NOW() - MAX(order_date)) as recency_days,
    COUNT(*) as frequency,
    SUM(total_amount) as monetary
  FROM orders
  GROUP BY user_id
),
rfm_scores AS (
  SELECT 
    user_id,
    recency_days,
    frequency,
    monetary,
    NTILE(5) OVER (ORDER BY recency_days ASC) as r_score,
    NTILE(5) OVER (ORDER BY frequency DESC) as f_score,
    NTILE(5) OVER (ORDER BY monetary DESC) as m_score
  FROM rfm_calc
)
SELECT 
  user_id,
  recency_days,
  frequency,
  monetary,
  r_score || f_score || m_score as rfm_score,
  CASE 
    WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
    WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
    WHEN r_score >= 4 AND f_score <= 2 THEN 'Promising'
    WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
    WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
    ELSE 'Others'
  END as customer_segment
FROM rfm_scores
ORDER BY monetary DESC;
```

### New vs Returning Customers

```sql
-- Customer type analysis
WITH first_orders AS (
  SELECT 
    user_id,
    MIN(order_date) as first_order_date
  FROM orders
  GROUP BY user_id
)
SELECT 
  DATE(o.order_date) as date,
  COUNT(CASE WHEN o.order_date::date = fo.first_order_date::date THEN 1 END) as new_customers,
  COUNT(CASE WHEN o.order_date::date > fo.first_order_date::date THEN 1 END) as returning_customers,
  SUM(CASE WHEN o.order_date::date = fo.first_order_date::date THEN o.total_amount ELSE 0 END) as new_customer_revenue,
  SUM(CASE WHEN o.order_date::date > fo.first_order_date::date THEN o.total_amount ELSE 0 END) as returning_customer_revenue
FROM orders o
JOIN first_orders fo ON o.user_id = fo.user_id
WHERE o.order_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(o.order_date)
ORDER BY date DESC;
```

## Time-Series Analysis

### Cohort Analysis

```sql
-- Monthly cohort retention
WITH cohorts AS (
  SELECT 
    user_id,
    DATE_TRUNC('month', MIN(order_date)) as cohort_month
  FROM orders
  GROUP BY user_id
),
monthly_activity AS (
  SELECT 
    c.cohort_month,
    DATE_TRUNC('month', o.order_date) as activity_month,
    COUNT(DISTINCT o.user_id) as active_users
  FROM cohorts c
  JOIN orders o ON c.user_id = o.user_id
  WHERE c.cohort_month >= '2024-01-01'
  GROUP BY c.cohort_month, DATE_TRUNC('month', o.order_date)
)
SELECT 
  cohort_month,
  activity_month,
  active_users,
  EXTRACT(MONTH FROM AGE(activity_month, cohort_month)) as months_since_first_order
FROM monthly_activity
ORDER BY cohort_month, activity_month;
```

### Moving Averages

```sql
-- 7-day moving average of revenue
SELECT 
  DATE(order_date) as date,
  SUM(total_amount) as daily_revenue,
  AVG(SUM(total_amount)) OVER (
    ORDER BY DATE(order_date)
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) as seven_day_avg
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '60 days'
GROUP BY DATE(order_date)
ORDER BY date DESC;
```

### Trends and Growth

```sql
-- Year-over-year growth
SELECT 
  DATE_TRUNC('month', order_date) as month,
  SUM(total_amount) as revenue,
  LAG(SUM(total_amount), 12) OVER (ORDER BY DATE_TRUNC('month', order_date)) as same_month_last_year,
  ROUND(
    ((SUM(total_amount) - LAG(SUM(total_amount), 12) OVER (ORDER BY DATE_TRUNC('month', order_date))) 
    / LAG(SUM(total_amount), 12) OVER (ORDER BY DATE_TRUNC('month', order_date)) * 100)::numeric,
    2
  ) as yoy_growth_pct
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month DESC;
```

## Data Quality

### Find Missing Data

```sql
-- NULL values analysis
SELECT 
  COUNT(*) as total_rows,
  COUNT(*) FILTER (WHERE email IS NULL) as null_emails,
  COUNT(*) FILTER (WHERE phone IS NULL) as null_phones,
  COUNT(*) FILTER (WHERE address IS NULL) as null_addresses,
  COUNT(*) FILTER (WHERE city IS NULL) as null_cities,
  ROUND(100.0 * COUNT(*) FILTER (WHERE email IS NULL) / COUNT(*), 2) as null_email_pct,
  ROUND(100.0 * COUNT(*) FILTER (WHERE phone IS NULL) / COUNT(*), 2) as null_phone_pct
FROM users;
```

### Find Duplicates

```sql
-- Duplicate emails
SELECT 
  email,
  COUNT(*) as duplicate_count,
  ARRAY_AGG(id) as user_ids
FROM users
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;

-- Duplicate orders (potential data issue)
SELECT 
  user_id,
  order_date,
  total_amount,
  COUNT(*) as duplicate_count
FROM orders
GROUP BY user_id, order_date, total_amount
HAVING COUNT(*) > 1;
```

### Data Freshness

```sql
-- Check when tables were last updated
SELECT 
  'users' as table_name,
  MAX(created_at) as latest_record,
  COUNT(*) as total_records,
  EXTRACT(DAY FROM NOW() - MAX(created_at)) as days_since_last_update
FROM users
UNION ALL
SELECT 
  'orders' as table_name,
  MAX(order_date) as latest_record,
  COUNT(*) as total_records,
  EXTRACT(DAY FROM NOW() - MAX(order_date)) as days_since_last_update
FROM orders
UNION ALL
SELECT 
  'products' as table_name,
  MAX(updated_at) as latest_record,
  COUNT(*) as total_records,
  EXTRACT(DAY FROM NOW() - MAX(updated_at)) as days_since_last_update
FROM products;
```

## Performance Optimization

### Query Analysis

```sql
-- Use EXPLAIN ANALYZE to see query plan
EXPLAIN ANALYZE
SELECT * FROM users 
WHERE email LIKE '%@gmail.com'
LIMIT 100;
```

### Index Usage

```sql
-- Check if indexes are being used
SELECT 
  schemaname,
  tablename,
  indexname,
  idx_scan as index_scans,
  idx_tup_read as tuples_read,
  idx_tup_fetch as tuples_fetched,
  pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT 
  schemaname,
  tablename,
  indexname,
  idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Table Sizes

```sql
-- Check table sizes
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
  pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) as index_size,
  pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## PostgreSQL Specific

### JSON Operations

```sql
-- Extract JSON fields
SELECT 
  id,
  data->>'name' as name,
  data->>'email' as email,
  data->'address'->>'city' as city
FROM json_table;

-- Query JSON arrays
SELECT 
  id,
  jsonb_array_elements_text(tags) as tag
FROM products
WHERE tags @> '["featured"]'::jsonb;
```

### Array Operations

```sql
-- Array contains
SELECT * FROM users 
WHERE tags @> ARRAY['premium', 'verified'];

-- Array overlap
SELECT * FROM users
WHERE tags && ARRAY['premium', 'vip'];

-- Unnest array
SELECT 
  user_id,
  unnest(tags) as tag
FROM users;
```

### Full-Text Search

```sql
-- Basic full-text search
SELECT 
  id,
  title,
  content,
  ts_rank(to_tsvector('english', content), query) as rank
FROM articles,
     to_tsquery('english', 'postgresql & database') query
WHERE to_tsvector('english', content) @@ query
ORDER BY rank DESC;
```

### Window Functions

```sql
-- Ranking within groups
SELECT 
  user_id,
  order_date,
  total_amount,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date DESC) as order_rank,
  RANK() OVER (PARTITION BY user_id ORDER BY total_amount DESC) as amount_rank,
  SUM(total_amount) OVER (PARTITION BY user_id) as user_total
FROM orders;

-- Running totals
SELECT 
  order_date,
  total_amount,
  SUM(total_amount) OVER (ORDER BY order_date) as running_total
FROM orders
ORDER BY order_date;
```

---

For more query examples, see the examples directory or visit https://docs.synehq.com
