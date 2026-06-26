---
title: Optimize NULL Handling in Outer JOINs
impact: MEDIUM
impactDescription: "join_use_nulls=0 uses default values instead of NULL"
tags: [query, JOIN, NULL, optimization]
---

## Optimize NULL Handling in Outer JOINs

**Impact: MEDIUM**

By default, LEFT/RIGHT/FULL JOINs return NULL for non-matching rows. The `join_use_nulls` setting controls this behavior.

**Default behavior (join_use_nulls = 1):**
```sql
SELECT o.order_id, c.name
FROM orders o
LEFT JOIN customers c ON c.id = o.customer_id;

-- Non-matching rows return:
-- order_id | name
-- 123      | NULL  (customer not found)
```

**With join_use_nulls = 0:**
```sql
SET join_use_nulls = 0;

SELECT o.order_id, c.name
FROM orders o
LEFT JOIN customers c ON c.id = o.customer_id;

-- Non-matching rows return default values:
-- order_id | name
-- 123      | ''    (empty string)
```

**When to use join_use_nulls = 0:**

| Scenario | Setting |
|----------|---------|
| Need to distinguish "not found" from "empty" | 1 (default) |
| Default values are acceptable | 0 (faster) |
| Downstream processing handles NULL poorly | 0 |
| Aggregations on results | 0 (avoids NULL handling) |

**Performance consideration:**
```sql
-- join_use_nulls = 0 is slightly faster
-- No need to track NULL status
-- Simpler result handling
SET join_use_nulls = 0;

SELECT
    o.customer_id,
    sum(o.amount) as total,
    c.country  -- Returns '' instead of NULL
FROM orders o
LEFT JOIN customers c ON c.id = o.customer_id
GROUP BY o.customer_id, c.country;
```

Reference: [Minimize and Optimize JOINs](https://clickhouse.com/docs/best-practices/minimize-optimize-joins)
