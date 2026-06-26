---
title: Minimize Bit-Width for Numeric Types
impact: HIGH
impactDescription: "Use smallest type that fits data range for storage efficiency"
tags: [schema, data-types, numeric, optimization]
---

## Minimize Bit-Width for Numeric Types

**Impact: HIGH**

Using UInt64 for all integers wastes storage. Choose the smallest type that accommodates your data range.

**Type selection guide:**

| Type | Range | Use For |
|------|-------|---------|
| UInt8 | 0-255 | age, rating, status codes |
| UInt16 | 0-65,535 | year, port number |
| UInt32 | 0-4.2B | unix timestamp, most IDs |
| UInt64 | 0-18E | very large counters |
| Int8/16/32/64 | signed versions | when negatives needed |

**Incorrect (oversized types):**
```sql
CREATE TABLE users (
    age UInt64,           -- Max age ~120, UInt64 is overkill
    status UInt64,        -- 5 possible values
    year_joined UInt64,   -- Years 2000-2100
    login_count UInt64    -- Rarely exceeds millions
)
```

**Correct (right-sized types):**
```sql
CREATE TABLE users (
    age UInt8,            -- 0-255 is plenty
    status UInt8,         -- 5 values fit in 1 byte
    year_joined UInt16,   -- 0-65535 covers years
    login_count UInt32    -- 0-4.2B is sufficient
)
```

**Storage impact (1 billion rows):**

| Column | UInt64 | Right-sized | Savings |
|--------|--------|-------------|---------|
| age | 8 GB | 1 GB (UInt8) | 87.5% |
| status | 8 GB | 1 GB (UInt8) | 87.5% |
| year | 8 GB | 2 GB (UInt16) | 75% |

**Note:** Consider future growth, but don't over-provision. UInt32 handles most use cases.

Reference: [Select Data Types](https://clickhouse.com/docs/best-practices/select-data-types)
