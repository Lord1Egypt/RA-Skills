---
title: Filter on ORDER BY Columns in Queries
impact: CRITICAL
impactDescription: "Skipping prefix columns prevents index usage"
tags: [schema, primary-key, query, filters]
---

## Filter on ORDER BY Columns in Queries

**Impact: CRITICAL**

The primary index only helps when queries filter on the ORDER BY columns in order. Skipping the leading columns prevents the index from being used effectively.

**Example ORDER BY:**
```sql
ORDER BY (event_type, event_date, user_id)
```

**Index usage by query pattern:**

| Query Filter | Index Used? | Why |
|--------------|-------------|-----|
| `WHERE event_type = 'X'` | ✅ Yes | Matches first column |
| `WHERE event_type = 'X' AND event_date = '2024-01-01'` | ✅ Yes | Matches prefix |
| `WHERE event_date = '2024-01-01'` | ❌ No | Skips first column |
| `WHERE user_id = 123` | ❌ No | Skips first two columns |

**Incorrect (skipping ORDER BY prefix):**
```sql
-- ORDER BY (event_type, event_date, user_id)

-- Skips event_type - can't use index efficiently
SELECT * FROM events WHERE event_date = '2024-01-01';

-- Skips event_type and event_date - full scan
SELECT * FROM events WHERE user_id = 123;
```

**Correct (using ORDER BY prefix):**
```sql
-- Always include leading columns when possible
SELECT * FROM events
WHERE event_type = 'click' AND event_date = '2024-01-01';

-- If you must filter on later columns, add skipping index
ALTER TABLE events
ADD INDEX idx_user_id user_id TYPE bloom_filter GRANULARITY 4;
```

Reference: [Choosing a Primary Key](https://clickhouse.com/docs/best-practices/choosing-a-primary-key)
