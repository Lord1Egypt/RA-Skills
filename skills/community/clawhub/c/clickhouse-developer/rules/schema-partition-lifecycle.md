---
title: Use Partitioning for Data Lifecycle Management
impact: HIGH
impactDescription: "DROP PARTITION is instant; DELETE is expensive"
tags: [schema, partitioning, lifecycle, TTL]
---

## Use Partitioning for Data Lifecycle Management

**Impact: HIGH**

Partitioning's primary benefit is efficient data lifecycle management: instant partition drops, TTL-based retention, and tiered storage. Use it for lifecycle, not query optimization.

**Incorrect (partitioning for queries):**
```sql
-- Partitioning by user_id hoping to speed up user queries
CREATE TABLE events (...)
PARTITION BY user_id  -- Wrong approach!
ORDER BY (timestamp);
```

**Correct (partitioning for lifecycle):**
```sql
CREATE TABLE events (
    timestamp DateTime,
    event_type LowCardinality(String),
    data String
)
ENGINE = MergeTree()
PARTITION BY toStartOfMonth(timestamp)
ORDER BY (event_type, timestamp)
TTL timestamp + INTERVAL 90 DAY;

-- Instant deletion of old data
ALTER TABLE events DROP PARTITION '2023-01';

-- TTL automatically removes expired data
```

**Lifecycle use cases:**

| Use Case | Partition Key | Benefit |
|----------|---------------|---------|
| Retention | toStartOfMonth(ts) | DROP PARTITION for cleanup |
| Archival | toStartOfYear(ts) | Move old partitions to cold storage |
| Compliance | toStartOfMonth(ts) | Delete specific time ranges |

**Tiered storage example:**
```sql
CREATE TABLE events (...)
ENGINE = MergeTree()
PARTITION BY toStartOfMonth(timestamp)
ORDER BY (event_type, timestamp)
TTL
    timestamp + INTERVAL 7 DAY TO VOLUME 'hot',
    timestamp + INTERVAL 30 DAY TO VOLUME 'warm',
    timestamp + INTERVAL 365 DAY DELETE;
```

Reference: [Choosing a Partitioning Key](https://clickhouse.com/docs/best-practices/choosing-a-partitioning-key)
