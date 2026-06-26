---
title: Use Enum for Finite Value Sets
impact: MEDIUM
impactDescription: "Insert-time validation, natural ordering, 1-2 bytes storage"
tags: [schema, data-types, Enum, validation]
---

## Use Enum for Finite Value Sets

**Impact: MEDIUM**

Enum provides insert-time validation, natural ordering, and efficient 1-2 byte storage for columns with a fixed set of values.

**Incorrect (String for finite values):**
```sql
CREATE TABLE orders (
    status String  -- "pending", "processing", "shipped", "delivered"
)
-- No validation: INSERT VALUES ('pendingg') succeeds with typo
```

**Correct (Enum for validation and efficiency):**
```sql
CREATE TABLE orders (
    status Enum8('pending' = 1, 'processing' = 2, 'shipped' = 3, 'delivered' = 4)
)
-- Validation: INSERT VALUES ('pendingg') fails immediately
```

**Enum types:**

| Type | Range | Use For |
|------|-------|---------|
| Enum8 | 1-127 values | Most use cases |
| Enum16 | 1-32767 values | Large value sets |

**Benefits:**
- **Validation**: Invalid values rejected at insert
- **Storage**: 1 byte (Enum8) vs variable String
- **Ordering**: Natural sort by enum position
- **Performance**: Integer comparisons vs string

**When to use Enum vs LowCardinality:**

| Scenario | Recommendation |
|----------|----------------|
| Fixed, known values | Enum |
| Values may change | LowCardinality |
| Need validation | Enum |
| Flexible schema | LowCardinality |

Reference: [Select Data Types](https://clickhouse.com/docs/best-practices/select-data-types)
