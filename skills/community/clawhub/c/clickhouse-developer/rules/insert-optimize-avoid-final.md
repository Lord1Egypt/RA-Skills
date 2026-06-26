---
title: Avoid OPTIMIZE TABLE FINAL
impact: HIGH
impactDescription: "Let background merges work; FINAL in SELECT for deduplication"
tags: [insert, OPTIMIZE, merge, ReplacingMergeTree]
---

## Avoid OPTIMIZE TABLE FINAL

**Impact: HIGH**

`OPTIMIZE TABLE FINAL` forces immediate merging of all parts into one, which is resource-intensive and blocks other operations. Let background merges work naturally instead.

**Incorrect (forcing merges):**
```sql
-- Expensive! Merges all parts immediately
OPTIMIZE TABLE events FINAL;

-- Running after every batch - unnecessary
INSERT INTO events VALUES (...);
OPTIMIZE TABLE events FINAL;  -- Don't do this!
```

**Correct (let background merges work):**
```sql
-- Insert data normally
INSERT INTO events VALUES (...);

-- Background merge process handles optimization
-- ClickHouse automatically merges parts over time
```

**For ReplacingMergeTree deduplication:**

Instead of OPTIMIZE FINAL, use FINAL modifier in queries:

```sql
-- Table with ReplacingMergeTree
CREATE TABLE users (
    user_id UInt64,
    name String,
    updated_at DateTime
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY user_id;

-- Query with FINAL to get deduplicated results
SELECT * FROM users FINAL WHERE user_id = 123;

-- Or use aggregation (often faster)
SELECT user_id, argMax(name, updated_at) as name
FROM users
GROUP BY user_id;
```

**When OPTIMIZE might be acceptable:**

| Scenario | Acceptable? |
|----------|-------------|
| One-time data migration | ⚠️ Maybe, off-peak |
| After bulk historical load | ⚠️ Maybe, off-peak |
| Regular production use | ❌ No |
| After every INSERT | ❌ Never |

Reference: [Avoid Mutations](https://clickhouse.com/docs/best-practices/avoid-mutations)
