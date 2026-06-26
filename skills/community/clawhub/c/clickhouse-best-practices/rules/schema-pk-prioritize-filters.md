---
title: Prioritize Filter Columns in ORDER BY
impact: CRITICAL
impactDescription: "Columns not in ORDER BY cause full table scans"
tags: [schema, primary-key, filters, ORDER BY]
---

## Prioritize Filter Columns in ORDER BY

**Impact: CRITICAL**

Columns frequently used in WHERE clauses should be included in ORDER BY. Filtering on columns not in ORDER BY results in scanning all granules, negating the benefits of ClickHouse's sparse indexing.

**Incorrect (filter columns not in ORDER BY):**
```sql
CREATE TABLE events (
    timestamp DateTime,
    event_type String,
    user_id UInt64,
    country String
)
ENGINE = MergeTree()
ORDER BY (timestamp);

-- Query filters on event_type - full scan required!
SELECT * FROM events WHERE event_type = 'purchase';
```

**Correct (filter columns in ORDER BY):**
```sql
CREATE TABLE events (
    timestamp DateTime,
    event_type LowCardinality(String),
    user_id UInt64,
    country LowCardinality(String)
)
ENGINE = MergeTree()
ORDER BY (event_type, toDate(timestamp), user_id);

-- Query can use index to skip non-matching granules
SELECT * FROM events WHERE event_type = 'purchase';
```

**Analysis steps:**
1. Identify your most common queries
2. List columns in WHERE clauses
3. Determine cardinality of each column
4. Order: low cardinality filters first, then date, then higher cardinality

**When you can't include all filter columns:**
- Use data skipping indices for secondary filter columns
- Consider materialized views with different ORDER BY

Reference: [Choosing a Primary Key](https://clickhouse.com/docs/best-practices/choosing-a-primary-key)
