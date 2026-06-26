---
title: Use JSON Type for Dynamic Schemas
impact: MEDIUM
impactDescription: "JSON for dynamic schemas; typed columns for known fields"
tags: [schema, JSON, dynamic, semi-structured]
---

## Use JSON Type for Dynamic Schemas

**Impact: MEDIUM**

The JSON type enables efficient storage and querying of semi-structured data with dynamic schemas. Use it when field structure varies or is unknown at design time.

**When to use JSON:**
- Event properties that vary by event type
- User attributes from different sources
- API responses with varying structure
- Log data with inconsistent fields

**When NOT to use JSON:**
- Known, stable schema → use typed columns
- High-frequency filtering → use typed columns in ORDER BY
- Aggregations on specific fields → extract to typed columns

**Example: Events with variable properties**
```sql
CREATE TABLE events (
    event_id UUID,
    event_type LowCardinality(String),
    timestamp DateTime,
    user_id UInt64,
    properties JSON  -- Dynamic fields per event type
)
ENGINE = MergeTree()
ORDER BY (event_type, timestamp);

-- Insert with different property structures
INSERT INTO events VALUES
    (generateUUIDv4(), 'page_view', now(), 123,
     '{"url": "/home", "referrer": "google.com", "duration_ms": 5000}'),
    (generateUUIDv4(), 'purchase', now(), 456,
     '{"product_id": 789, "amount": 99.99, "currency": "USD"}');
```

**Querying JSON:**
```sql
-- Access nested fields
SELECT
    event_type,
    properties.url as url,
    properties.amount as amount
FROM events
WHERE properties.currency = 'USD';

-- Type inference works automatically
SELECT
    sum(properties.amount::Float64) as total_revenue
FROM events
WHERE event_type = 'purchase';
```

**Hybrid approach (recommended):**
```sql
-- Known fields as typed columns, unknown as JSON
CREATE TABLE events (
    event_id UUID,
    event_type LowCardinality(String),
    timestamp DateTime,
    user_id UInt64,                    -- Known, frequently filtered
    properties JSON                     -- Variable properties
)
ENGINE = MergeTree()
ORDER BY (event_type, timestamp, user_id);
```

Reference: [Select Data Types](https://clickhouse.com/docs/best-practices/select-data-types)
