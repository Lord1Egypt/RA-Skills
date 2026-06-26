---
title: Use Native Types Instead of String
impact: CRITICAL
impactDescription: "2-10x storage reduction; enables compression and correct semantics"
tags: [schema, data-types, storage, performance]
---

## Use Native Types Instead of String

**Impact: CRITICAL**

Storing everything as String is a common anti-pattern. Native types provide 2-10x storage reduction, better compression, and proper semantics (sorting, arithmetic, etc.).

**Incorrect (String for everything):**
```sql
CREATE TABLE events (
    id String,           -- UUID stored as 36-char string
    timestamp String,    -- DateTime as "2024-01-15 10:30:00"
    user_id String,      -- Integer as "12345678"
    amount String,       -- Decimal as "99.99"
    is_active String     -- Boolean as "true"/"false"
)
```

**Correct (native types):**
```sql
CREATE TABLE events (
    id UUID,                    -- 16 bytes vs 36 bytes
    timestamp DateTime64(3),    -- 8 bytes vs 19 bytes
    user_id UInt64,             -- 8 bytes vs variable
    amount Decimal(10,2),       -- Fixed precision
    is_active Bool              -- 1 byte vs 4-5 bytes
)
```

**Storage comparison:**

| Data | String Size | Native Size | Savings |
|------|-------------|-------------|---------|
| UUID | 36 bytes | 16 bytes | 56% |
| DateTime | 19 bytes | 4-8 bytes | 58-79% |
| Integer | 1-20 bytes | 1-8 bytes | varies |
| Boolean | 4-5 bytes | 1 byte | 75-80% |
| IPv4 | 7-15 bytes | 4 bytes | 43-73% |

**Additional benefits:**
- Proper sorting (numeric vs lexicographic)
- Arithmetic operations work correctly
- Better compression ratios
- Type validation on insert

Reference: [Select Data Types](https://clickhouse.com/docs/best-practices/select-data-types)
