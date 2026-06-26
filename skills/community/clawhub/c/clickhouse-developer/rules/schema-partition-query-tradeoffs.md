---
title: Understand Partition Query Performance Trade-offs
impact: MEDIUM
impactDescription: "Partition pruning helps some queries, hurts others spanning many partitions"
tags: [schema, partitioning, query, performance]
---

## Understand Partition Query Performance Trade-offs

**Impact: MEDIUM**

Partitioning affects query performance in both directions. Queries matching partition keys benefit from pruning, but queries spanning many partitions may suffer.

**Partition pruning benefits:**
```sql
-- Table partitioned by month
CREATE TABLE events (...)
PARTITION BY toStartOfMonth(timestamp)
ORDER BY (event_type, timestamp);

-- Good: Single partition access
SELECT * FROM events
WHERE timestamp >= '2024-01-01' AND timestamp < '2024-02-01';
-- Only reads January partition

-- Good: Few partitions
SELECT * FROM events
WHERE timestamp >= '2024-01-01' AND timestamp < '2024-04-01';
-- Reads 3 partitions
```

**Partition spanning costs:**
```sql
-- Bad: Spanning all partitions
SELECT count() FROM events
WHERE event_type = 'purchase';
-- Must read from every partition

-- Bad: Aggregation across time
SELECT toStartOfWeek(timestamp), count()
FROM events
WHERE event_type = 'click'
GROUP BY 1;
-- Touches many partitions
```

**Query pattern analysis:**

| Query Type | Partitioned Impact |
|------------|-------------------|
| Date-range filtered | ✅ Faster (pruning) |
| Cross-time aggregation | ⚠️ May be slower |
| Non-partition filtered | ➡️ No change |
| Full table scan | ➡️ No change |

**Recommendations:**
1. Analyze your query patterns before partitioning
2. Prefer ORDER BY optimization over partitioning for queries
3. Use partitioning primarily for lifecycle management
4. Test performance with realistic queries

```sql
-- Check which partitions a query touches
EXPLAIN SELECT * FROM events WHERE ...;
-- Look for "Partition" information in output
```

Reference: [Choosing a Partitioning Key](https://clickhouse.com/docs/best-practices/choosing-a-partitioning-key)
