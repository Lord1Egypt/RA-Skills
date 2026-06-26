---
title: Use Async Inserts for High-Frequency Small Batches
impact: HIGH
impactDescription: "Server-side buffering when client batching isn't practical"
tags: [insert, async, buffering, high-frequency]
---

## Use Async Inserts for High-Frequency Small Batches

**Impact: HIGH**

When client-side batching isn't practical (many independent producers, real-time requirements), use async inserts to let ClickHouse buffer and batch server-side.

**Problem scenario:**
- Many microservices sending events
- Real-time data from IoT devices
- Can't coordinate batching across producers

**Incorrect (small sync inserts from many sources):**
```python
# Each producer sends immediately - creates many small parts
client.execute("INSERT INTO events VALUES", [single_event])
```

**Correct (async inserts):**
```python
# Enable async inserts
client.execute("SET async_insert = 1")
client.execute("SET wait_for_async_insert = 0")  # Don't wait for batch

# Inserts are buffered server-side
client.execute("INSERT INTO events VALUES", [single_event])
```

**Server configuration:**
```sql
-- Configure async insert behavior
SET async_insert = 1;
SET async_insert_max_data_size = 10000000;  -- 10MB buffer
SET async_insert_busy_timeout_ms = 1000;     -- Flush every 1s
SET wait_for_async_insert = 1;               -- Wait for durability
```

**Async insert settings:**

| Setting | Description | Recommended |
|---------|-------------|-------------|
| `async_insert` | Enable async mode | 1 |
| `async_insert_max_data_size` | Buffer size before flush | 10-100MB |
| `async_insert_busy_timeout_ms` | Max wait before flush | 1000-5000ms |
| `wait_for_async_insert` | Wait for flush acknowledgment | 1 for durability |

**When to use:**

| Scenario | Async? |
|----------|--------|
| Many small producers | ✅ Yes |
| Single large batch producer | ❌ No, use sync |
| Real-time requirements | ✅ Yes |
| Can batch client-side | ❌ No, batch yourself |

Reference: [Selecting an Insert Strategy](https://clickhouse.com/docs/best-practices/selecting-an-insert-strategy)
