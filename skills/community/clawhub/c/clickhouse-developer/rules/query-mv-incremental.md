---
title: Use Incremental MVs for Real-Time Aggregations
impact: HIGH
impactDescription: "Read thousands of rows instead of billions"
tags: [query, materialized-view, aggregation, real-time]
---

## Use Incremental MVs for Real-Time Aggregations

**Impact: HIGH**

Materialized views can incrementally maintain aggregations, allowing queries to read pre-computed results instead of scanning raw data.

**Problem:** Query scans billions of rows for every request
```sql
-- Slow: scans all raw events
SELECT
    toStartOfHour(timestamp) as hour,
    event_type,
    count() as events,
    uniq(user_id) as unique_users
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
GROUP BY hour, event_type;
```

**Solution: Incremental Materialized View**
```sql
-- Create destination table with AggregatingMergeTree
CREATE TABLE events_hourly (
    hour DateTime,
    event_type LowCardinality(String),
    events AggregateFunction(count, UInt64),
    unique_users AggregateFunction(uniq, UInt64)
)
ENGINE = AggregatingMergeTree()
ORDER BY (event_type, hour);

-- Create MV that updates on each insert
CREATE MATERIALIZED VIEW events_hourly_mv
TO events_hourly
AS SELECT
    toStartOfHour(timestamp) as hour,
    event_type,
    countState() as events,
    uniqState(user_id) as unique_users
FROM events
GROUP BY hour, event_type;

-- Query the MV (reads thousands, not billions)
SELECT
    hour,
    event_type,
    countMerge(events) as events,
    uniqMerge(unique_users) as unique_users
FROM events_hourly
WHERE hour >= now() - INTERVAL 7 DAY
GROUP BY hour, event_type;
```

**Key patterns:**
- Use `-State` functions in MV definition
- Use `-Merge` functions in queries
- AggregatingMergeTree for destination table

Reference: [Using Materialized Views](https://clickhouse.com/docs/best-practices/using-materialized-views)
