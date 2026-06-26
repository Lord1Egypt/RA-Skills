---
title: Use Native Format for Best Insert Performance
impact: MEDIUM
impactDescription: "Native > RowBinary > JSONEachRow for performance"
tags: [insert, format, Native, performance]
---

## Use Native Format for Best Insert Performance

**Impact: MEDIUM**

Different data formats have different parsing overhead. Native format provides the best performance, followed by RowBinary, then text formats like JSONEachRow.

**Format performance ranking:**

| Format | Performance | Use Case |
|--------|-------------|----------|
| Native | Fastest | ClickHouse-to-ClickHouse |
| RowBinary | Very fast | Binary protocols |
| JSONEachRow | Moderate | APIs, human-readable |
| CSV/TSV | Moderate | File imports |
| JSONCompactEachRow | Slower | Compact JSON |

**Using Native format:**
```python
# Python clickhouse-driver uses Native by default
from clickhouse_driver import Client
client = Client('localhost')
client.execute('INSERT INTO events VALUES', data)  # Native format
```

**Using RowBinary:**
```sql
-- For HTTP interface
INSERT INTO events FORMAT RowBinary
-- Binary data follows
```

**JSONEachRow (common but slower):**
```sql
INSERT INTO events FORMAT JSONEachRow
{"event_type": "click", "timestamp": "2024-01-15 10:30:00", "user_id": 123}
{"event_type": "view", "timestamp": "2024-01-15 10:31:00", "user_id": 456}
```

**Performance tips:**
1. Use Native format when possible (native clients)
2. Compress data in transit (LZ4 or ZSTD)
3. Avoid frequent format conversion
4. For HTTP API, consider RowBinary over JSON

```sql
-- Enable compression
SET network_compression_method = 'ZSTD';
SET network_zstd_compression_level = 3;
```

Reference: [Selecting an Insert Strategy](https://clickhouse.com/docs/best-practices/selecting-an-insert-strategy)
