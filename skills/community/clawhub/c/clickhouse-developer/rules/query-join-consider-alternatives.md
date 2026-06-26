---
title: Consider Alternatives to JOINs
impact: HIGH
impactDescription: "Dictionaries, denormalization, and IN subqueries often outperform JOINs"
tags: [query, JOIN, dictionary, denormalization]
---

## Consider Alternatives to JOINs

**Impact: HIGH**

JOINs in ClickHouse can be expensive. Consider these alternatives for better performance.

**Alternative 1: Dictionaries for Lookups**
```sql
-- Instead of JOIN for dimension lookup
SELECT o.*, dictGet('customers_dict', 'name', o.customer_id) as customer_name
FROM orders o;

-- Create dictionary
CREATE DICTIONARY customers_dict (
    id UInt64,
    name String
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(TABLE 'customers'))
LAYOUT(FLAT())
LIFETIME(3600);
```

**Alternative 2: Denormalization via Materialized Views**
```sql
-- Pre-join data at insert time
CREATE MATERIALIZED VIEW orders_enriched
ENGINE = MergeTree()
ORDER BY (order_date, customer_id)
AS SELECT
    o.*,
    c.name as customer_name,
    c.country as customer_country
FROM orders o
LEFT JOIN customers c ON c.id = o.customer_id;
```

**Alternative 3: IN Subquery for Filtering**
```sql
-- Instead of JOIN just for filtering
SELECT * FROM orders
WHERE customer_id IN (
    SELECT id FROM customers WHERE country = 'US'
);
```

**When to use each:**

| Alternative | Best For |
|-------------|----------|
| Dictionary | Small dimension tables, frequent lookups |
| Denormalization | High-frequency queries, predictable joins |
| IN subquery | Existence checks, filtering |
| Regular JOIN | Ad-hoc analysis, complex conditions |

Reference: [Minimize and Optimize JOINs](https://clickhouse.com/docs/best-practices/minimize-optimize-joins)
