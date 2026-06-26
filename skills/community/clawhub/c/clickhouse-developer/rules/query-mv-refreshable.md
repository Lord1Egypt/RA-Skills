---
title: Use Refreshable MVs for Complex Joins and Batch Workflows
impact: HIGH
impactDescription: "Sub-millisecond queries with periodic refresh"
tags: [query, materialized-view, refresh, joins]
---

## Use Refreshable MVs for Complex Joins and Batch Workflows

**Impact: HIGH**

Refreshable MVs periodically rebuild their contents, making them ideal for complex queries with JOINs or transformations that can't be done incrementally.

**When to use:**
- Complex JOINs across multiple tables
- Data transformations too complex for incremental MVs
- Batch workflows with periodic updates
- Pre-computed dashboards and reports

**Example: Complex JOIN refreshed hourly**
```sql
CREATE MATERIALIZED VIEW customer_orders_summary
REFRESH EVERY 1 HOUR
ENGINE = MergeTree()
ORDER BY customer_id
AS SELECT
    c.customer_id,
    c.name,
    c.country,
    count() as total_orders,
    sum(o.amount) as total_spent,
    max(o.order_date) as last_order
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name, c.country;

-- Queries now sub-millisecond
SELECT * FROM customer_orders_summary
WHERE country = 'US' AND total_spent > 1000;
```

**Refresh modes:**

| Mode | Behavior |
|------|----------|
| REPLACE (default) | Atomically replaces all data |
| APPEND | Adds to existing data |

**Refresh scheduling:**
```sql
-- Every hour
REFRESH EVERY 1 HOUR

-- At specific times
REFRESH EVERY 1 DAY AT '03:00'

-- After another MV refreshes
REFRESH AFTER other_mv
```

**Manual refresh:**
```sql
-- Force immediate refresh
SYSTEM REFRESH VIEW customer_orders_summary;

-- Check refresh status
SELECT * FROM system.view_refreshes WHERE view = 'customer_orders_summary';
```

Reference: [Using Materialized Views](https://clickhouse.com/docs/best-practices/using-materialized-views)
