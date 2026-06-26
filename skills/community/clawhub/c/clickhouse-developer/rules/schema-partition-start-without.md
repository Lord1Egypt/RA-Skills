---
title: Consider Starting Without Partitioning
impact: MEDIUM
impactDescription: "Add partitioning later when clear lifecycle requirements exist"
tags: [schema, partitioning, design]
---

## Consider Starting Without Partitioning

**Impact: MEDIUM**

Partitioning adds complexity and can hurt query performance in some cases. Start without partitioning and add it later when you have clear lifecycle management requirements.

**Why start without partitioning:**
- Simpler schema management
- No partition key selection mistakes
- Fewer "too many parts" issues
- Query performance depends on ORDER BY, not partitions

**When to add partitioning later:**
1. Data volume grows large enough for lifecycle management
2. Need to DROP old data efficiently
3. Tiered storage requirements emerge
4. Clear retention policy established

**Starting simple:**
```sql
-- Start without partitioning
CREATE TABLE events (
    event_id UUID,
    event_type LowCardinality(String),
    timestamp DateTime,
    user_id UInt64,
    data String
)
ENGINE = MergeTree()
ORDER BY (event_type, toDate(timestamp), user_id);
-- No PARTITION BY clause
```

**Adding partitioning later:**
```sql
-- When lifecycle needs are clear, create new partitioned table
CREATE TABLE events_new (
    event_id UUID,
    event_type LowCardinality(String),
    timestamp DateTime,
    user_id UInt64,
    data String
)
ENGINE = MergeTree()
PARTITION BY toStartOfMonth(timestamp)
ORDER BY (event_type, toDate(timestamp), user_id);

-- Migrate data
INSERT INTO events_new SELECT * FROM events;

-- Swap tables
RENAME TABLE events TO events_old, events_new TO events;
```

**Decision checklist:**
- [ ] Data volume > 100GB?
- [ ] Clear retention policy (e.g., keep 90 days)?
- [ ] Need tiered storage?
- [ ] Frequent DROP PARTITION operations expected?

If all "No", start without partitioning.

Reference: [Choosing a Partitioning Key](https://clickhouse.com/docs/best-practices/choosing-a-partitioning-key)
