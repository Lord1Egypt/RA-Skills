---
title: Filter Tables Before Joining
impact: CRITICAL
impactDescription: "Reduces data processed in JOIN; prevents memory pressure"
tags: [query, JOIN, filter, optimization]
---

## Filter Tables Before Joining

**Impact: CRITICAL**

Apply filters to tables before joining to reduce the data size processed. This prevents memory pressure and speeds up queries significantly.

**Incorrect (filter after join):**
```sql
-- Joins all data, then filters
SELECT *
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'completed' AND c.country = 'US';
```

**Correct (filter before join with subqueries):**
```sql
-- Filter each table before joining
SELECT *
FROM (
    SELECT * FROM orders WHERE status = 'completed'
) o
JOIN (
    SELECT * FROM customers WHERE country = 'US'
) c ON c.id = o.customer_id;
```

**Even better (aggregate before join when possible):**
```sql
-- Aggregate first, then join smaller result
SELECT c.country, o.total_orders
FROM (
    SELECT customer_id, count() as total_orders
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
) o
JOIN customers c ON c.id = o.customer_id;
```

**Impact on memory:**

| Scenario | Right Table Size |
|----------|------------------|
| No pre-filter | Full table in memory |
| Pre-filtered | Only matching rows |
| Pre-aggregated | Much smaller result set |

Reference: [Minimize and Optimize JOINs](https://clickhouse.com/docs/best-practices/minimize-optimize-joins)
