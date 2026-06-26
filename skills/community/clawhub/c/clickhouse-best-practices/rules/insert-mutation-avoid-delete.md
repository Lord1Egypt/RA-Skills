---
title: Avoid ALTER TABLE DELETE
impact: CRITICAL
impactDescription: "Use lightweight DELETE, CollapsingMergeTree, or DROP PARTITION"
tags: [insert, mutation, DELETE, CollapsingMergeTree]
---

## Avoid ALTER TABLE DELETE

**Impact: CRITICAL**

`ALTER TABLE DELETE` is a mutation that rewrites data parts. For frequent deletes, use alternatives that don't require rewriting data.

**Incorrect (mutation for deletes):**
```sql
-- Rewrites parts containing matching rows
ALTER TABLE events DELETE WHERE timestamp < '2023-01-01';

-- Frequent single-row deletes
ALTER TABLE orders DELETE WHERE order_id = 12345;
```

**Alternative 1: Lightweight DELETE (23.3+)**
```sql
-- Marks rows as deleted without immediate rewrite
DELETE FROM events WHERE timestamp < '2023-01-01';

-- Rows cleaned up during normal merges
-- Faster than mutation, less I/O impact
```

**Alternative 2: DROP PARTITION**
```sql
-- Instant deletion of entire partitions
ALTER TABLE events DROP PARTITION '2023-01';

-- Requires proper partitioning strategy
```

**Alternative 3: CollapsingMergeTree**
```sql
CREATE TABLE orders (
    order_id UInt64,
    status String,
    amount Decimal(10,2),
    sign Int8  -- 1 for insert, -1 for delete
)
ENGINE = CollapsingMergeTree(sign)
ORDER BY order_id;

-- "Delete" by inserting with sign = -1
INSERT INTO orders VALUES (12345, 'cancelled', 99.99, -1);
```

**Comparison:**

| Method | Speed | I/O Impact | When to Use |
|--------|-------|------------|-------------|
| ALTER DELETE | Slow | High | Rare, bulk operations |
| Lightweight DELETE | Fast | Low | Frequent deletes |
| DROP PARTITION | Instant | None | Time-based retention |
| CollapsingMergeTree | Fast | None | Frequent record deletes |

Reference: [Avoid Mutations](https://clickhouse.com/docs/best-practices/avoid-mutations)
