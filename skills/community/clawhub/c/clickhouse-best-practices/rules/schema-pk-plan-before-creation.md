---
title: Plan PRIMARY KEY Before Table Creation
impact: CRITICAL
impactDescription: "ORDER BY is immutable after creation; wrong choice requires full data migration"
tags: [schema, primary-key, ORDER BY, planning]
---

## Plan PRIMARY KEY Before Table Creation

**Impact: CRITICAL**

The ORDER BY clause (which defines the primary key in MergeTree tables) cannot be changed after table creation. A wrong choice requires creating a new table and migrating all data.

**Why this matters:**
- ORDER BY defines how data is physically sorted on disk
- The primary index is built from ORDER BY columns
- Query performance depends heavily on ORDER BY alignment with filter patterns
- Changing ORDER BY requires full table recreation

**Questions to answer before creating:**
1. What columns will be in WHERE clauses?
2. What is the cardinality of each filter column?
3. Will queries filter on date ranges?
4. Are there mandatory filter columns (tenant_id, etc.)?

**Incorrect (no planning):**
```sql
-- Created without analyzing query patterns
CREATE TABLE events (
    id UUID,
    timestamp DateTime,
    event_type String,
    user_id UInt64
)
ENGINE = MergeTree()
ORDER BY (id);  -- Wrong! UUID has no query benefit
```

**Correct (planned based on queries):**
```sql
-- Analyzed: most queries filter by event_type, then date range
CREATE TABLE events (
    id UUID,
    timestamp DateTime,
    event_type LowCardinality(String),
    user_id UInt64
)
ENGINE = MergeTree()
ORDER BY (event_type, toDate(timestamp), user_id);
```

**Migration cost when ORDER BY is wrong:**
```sql
-- Must create new table and copy all data
CREATE TABLE events_new (...) ORDER BY (correct_columns);
INSERT INTO events_new SELECT * FROM events;
RENAME TABLE events TO events_old, events_new TO events;
DROP TABLE events_old;
```

Reference: [Choosing a Primary Key](https://clickhouse.com/docs/best-practices/choosing-a-primary-key)
