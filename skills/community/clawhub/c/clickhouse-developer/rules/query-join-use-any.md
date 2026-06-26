---
title: Use ANY JOIN When Only One Match Needed
impact: HIGH
impactDescription: "Less memory, faster execution when duplicates don't matter"
tags: [query, JOIN, ANY, optimization]
---

## Use ANY JOIN When Only One Match Needed

**Impact: HIGH**

When you only need one matching row from the right table (not all matches), use `ANY JOIN` instead of regular `JOIN` for better performance.

**Incorrect (regular JOIN when one match suffices):**
```sql
-- Returns all matching rows, even if we only need one
SELECT o.*, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id;
```

**Correct (ANY JOIN for single match):**
```sql
-- Returns one arbitrary matching row - faster, less memory
SELECT o.*, c.name
FROM orders o
ANY LEFT JOIN customers c ON c.id = o.customer_id;
```

**When to use ANY JOIN:**

| Scenario | Use ANY? |
|----------|----------|
| Lookup from unique key | ✅ Yes |
| Need all matching rows | ❌ No |
| Right table has duplicates but you want one | ✅ Yes |
| Need specific match (latest, first) | ❌ No, use ASOF or subquery |

**ANY vs regular JOIN:**

| Aspect | Regular JOIN | ANY JOIN |
|--------|--------------|----------|
| Multiple matches | Returns all | Returns one |
| Memory usage | Higher | Lower |
| Execution speed | Slower | Faster |
| Result determinism | Deterministic | Non-deterministic |

**Note:** `ANY` returns an arbitrary matching row. If you need a specific one (e.g., latest), use `ASOF JOIN` or a subquery with ordering.

Reference: [Minimize and Optimize JOINs](https://clickhouse.com/docs/best-practices/minimize-optimize-joins)
