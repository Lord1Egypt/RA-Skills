---
name: clickhouse
description: >
  Comprehensive ClickHouse skill covering everything you need to work with a ClickHouse analytics database:
  schema design, query optimization, insert strategies, CLI usage, table creation and migrations,
  backend integration (Node.js, Python, Go), Redis caching strategy, cluster vs single-node differences,
  and how to test/debug data in the database. MUST USE whenever the user mentions ClickHouse, asks about
  analytics tables, high-volume insert pipelines, MergeTree schemas, ORDER BY / PRIMARY KEY design,
  materialized views, ClickHouse query performance, connecting to ClickHouse from code, or running
  ClickHouse CLI commands to inspect data.
---

# ClickHouse Skill

A complete reference for designing, operating, querying, and integrating ClickHouse from backend services.
ClickHouse is a **columnar, append-optimized** analytics database — it is NOT a transactional database.
Design everything around that fact.

> Official docs: https://clickhouse.com/docs/best-practices

---

## Quick Reference — Read the Right Section

| Task | Go To |
|------|-------|
| Design a new table | [Schema Design](#schema-design) |
| Write a migration | [Migrations](#migrations) |
| Insert data from code | [Insert Strategy](#insert-strategy) |
| Run queries / inspect the DB | [CLI Reference](#cli-reference) |
| Connect from Node.js / Python / Go | [Backend Integration](#backend-integration) |
| Optimize a slow query | [Query Optimization](#query-optimization) |
| Decide on Redis vs direct query | [Redis Caching Strategy](#redis-caching-strategy) |
| Understand cluster behavior | [Cluster Considerations](#cluster-considerations) |

---

## Core Mental Model

ClickHouse is an **append-only, batch-oriented** analytics database.
The biggest performance wins come from:

1. **Writing large batches** (10K–100K rows), not individual rows
2. **Choosing ORDER BY carefully** — it is immutable and drives all query performance
3. **Using native types** — never store everything as String
4. **Reading many rows across few columns** — not few rows across many columns

Avoid ClickHouse for:
- OLTP workloads (frequent single-row reads/writes)
- Complex multi-table JOINs on huge tables
- Frequent UPDATE/DELETE patterns

---

## Schema Design

### Step 1 — Plan ORDER BY Before Creating Any Table

**ORDER BY is immutable.** Changing it requires creating a new table and migrating all data.
Get it right before writing a single row.

Questions to answer first:
- What columns appear in `WHERE` clauses most often?
- What is the cardinality (number of distinct values) of each filter column?
- Is there a mandatory filter that every query has (e.g. `tenant_id`, `app_id`)?
- Are date ranges a common filter?

```sql
-- BAD: UUID as first ORDER BY column — no index benefit
CREATE TABLE events (
    id UUID,
    timestamp DateTime,
    event_type String,
    user_id UInt64
) ENGINE = MergeTree()
ORDER BY (id);

-- GOOD: Low cardinality first, then date, then higher cardinality
CREATE TABLE events (
    id UUID,
    timestamp DateTime,
    event_type LowCardinality(String),
    user_id UInt64
) ENGINE = MergeTree()
ORDER BY (event_type, toDate(timestamp), user_id);
```

**Cardinality ordering rule:** Put columns with **fewer distinct values first**.

| Position | Cardinality | Examples |
|----------|-------------|----------|
| 1st | Low (2–1,000) | `event_type`, `status`, `country` |
| 2nd | Date (coarse) | `toDate(timestamp)` |
| 3rd+ | Medium-High | `user_id`, `session_id` |
| Last | High (if needed) | `event_id`, UUID |

**Index usage by query pattern** (for `ORDER BY (event_type, event_date, user_id)`):

| Filter | Index Used? |
|--------|-------------|
| `WHERE event_type = 'X'` | ✅ Yes |
| `WHERE event_type = 'X' AND event_date = '...'` | ✅ Yes |
| `WHERE event_date = '...'` | ❌ No — skips first column |
| `WHERE user_id = 123` | ❌ No — skips first two |

For columns that can't be in ORDER BY, add a **data skipping index** (see [Query Optimization](#query-optimization)).

---

### Step 2 — Choose the Right Engine

| Engine | Use When |
|--------|----------|
| `MergeTree` | Standard append-only analytics |
| `ReplacingMergeTree(ver)` | Need logical "upserts" (new version replaces old) |
| `AggregatingMergeTree` | Pre-aggregated data for materialized views |
| `CollapsingMergeTree(sign)` | Logical deletes via insert pattern |
| `SummingMergeTree` | Automatically sum numeric columns on merge |
| `ReplicatedMergeTree` | Any engine on a cluster with replication |

For clusters, prefix engine name with `Replicated`: `ReplicatedMergeTree(...)`.

---

### Step 3 — Pick Native Types (Never Store Everything as String)

| Data | Wrong | Right | Savings |
|------|-------|-------|---------|
| UUID | `String` | `UUID` | 56% |
| Timestamp | `String` | `DateTime` / `DateTime64(3)` | 58–79% |
| Integer ID | `String` | `UInt32` / `UInt64` | varies |
| Boolean | `String` | `Bool` | 75–80% |
| IPv4 | `String` | `IPv4` | 43–73% |
| Decimal amount | `String` | `Decimal(10,2)` | significant |

**Use the smallest numeric type that fits:**

| Type | Range | Use For |
|------|-------|---------|
| `UInt8` | 0–255 | age, rating, status code |
| `UInt16` | 0–65,535 | year, port |
| `UInt32` | 0–4.2B | most IDs, unix timestamps |
| `UInt64` | 0–18E | very large counters |

**Use LowCardinality for repeated strings with < 10,000 unique values:**
```sql
country LowCardinality(String),   -- ~200 unique values
browser LowCardinality(String),   -- ~50 unique values
event_type LowCardinality(String) -- ~100 unique values
```

**Use Enum for fixed, known value sets:**
```sql
-- Provides insert-time validation + 1-byte storage
status Enum8('pending' = 1, 'processing' = 2, 'shipped' = 3, 'delivered' = 4)
```

**Avoid Nullable unless the null is semantically meaningful:**
```sql
-- BAD: Nullable everywhere
name Nullable(String),
login_count Nullable(UInt32)

-- GOOD: Use defaults; Nullable only when null has distinct meaning
name String DEFAULT '',
login_count UInt32 DEFAULT 0,
deleted_at Nullable(DateTime),   -- NULL = "not deleted" is semantically distinct
parent_id Nullable(UInt64)       -- NULL = "no parent" is semantically distinct
```

---

### Step 4 — Partitioning Strategy

**Partition for lifecycle management, NOT for query performance.**
Query performance comes from ORDER BY. Partitions enable fast data expiry.

```sql
-- GOOD: Monthly partitions for TTL and lifecycle
CREATE TABLE events (
    timestamp DateTime,
    event_type LowCardinality(String),
    user_id UInt64
) ENGINE = MergeTree()
PARTITION BY toStartOfMonth(timestamp)
ORDER BY (event_type, toDate(timestamp), user_id)
TTL timestamp + INTERVAL 90 DAY;

-- Instant deletion of a month
ALTER TABLE events DROP PARTITION '2024-01';
```

**Keep partition count between 100–1,000.** Daily partitions grow unbounded; monthly is usually safe.

**Tiered storage:**
```sql
TTL
    timestamp + INTERVAL 7 DAY TO VOLUME 'hot',
    timestamp + INTERVAL 30 DAY TO VOLUME 'warm',
    timestamp + INTERVAL 365 DAY DELETE;
```

**If you're unsure, start without partitioning.** You can add it later by creating a new table, migrating data, and renaming.

---

### Complete Table Example

```sql
CREATE TABLE page_events (
    -- Identifiers
    event_id     UUID DEFAULT generateUUIDv4(),
    tenant_id    UInt32,
    user_id      UInt64,

    -- Low-cardinality dimensions (great for ORDER BY)
    event_type   LowCardinality(String),
    country      LowCardinality(String) DEFAULT '',
    browser      LowCardinality(String) DEFAULT '',
    platform     Enum8('web'=1, 'ios'=2, 'android'=3, 'api'=4),

    -- Timestamps
    occurred_at  DateTime64(3),
    inserted_at  DateTime DEFAULT now(),

    -- Metrics
    duration_ms  UInt32 DEFAULT 0,
    revenue      Decimal(12,4) DEFAULT 0,

    -- Flexible properties
    properties   JSON,

    -- Skipping index for user lookups
    INDEX idx_user_id user_id TYPE bloom_filter GRANULARITY 4
) ENGINE = MergeTree()
PARTITION BY toStartOfMonth(occurred_at)
ORDER BY (tenant_id, event_type, toDate(occurred_at), user_id)
TTL occurred_at + INTERVAL 365 DAY
SETTINGS index_granularity = 8192;
```

---

## Migrations

ClickHouse does NOT support transactional DDL. There is no rollback. Plan carefully.

### ORMs / Migration Tools Compatibility

| Tool | ClickHouse Support |
|------|--------------------|
| Prisma | ❌ No native support — use raw SQL migrations |
| Drizzle | ❌ No native support — use raw SQL migrations |
| TypeORM | ⚠️ Unofficial community driver only |
| Flyway | ✅ Supported via JDBC driver |
| Liquibase | ✅ Supported |
| golang-migrate | ✅ Works well — recommended for Go |
| Custom SQL files | ✅ Always works |

**For Node.js projects:** maintain a `migrations/` folder with numbered `.sql` files and a small runner script.

**For Go projects:** use `golang-migrate` with the ClickHouse driver.

**Do NOT use Prisma/Drizzle to generate ClickHouse DDL.** They have no concept of MergeTree engines, ORDER BY, or PARTITION BY.

---

### Migration Patterns

#### Adding a Column
```sql
-- Safe: adding a column with a DEFAULT
ALTER TABLE events ADD COLUMN IF NOT EXISTS session_id UUID DEFAULT generateUUIDv4();

-- For a cluster: ON CLUSTER must come first
ALTER TABLE events ON CLUSTER '{cluster}' ADD COLUMN IF NOT EXISTS session_id UUID DEFAULT generateUUIDv4();
```

#### Changing an ORDER BY (requires table recreation)
```sql
-- 1. Create new table with correct ORDER BY
CREATE TABLE events_v2 AS events;   -- Copies structure
ALTER TABLE events_v2 MODIFY ORDER BY (tenant_id, event_type, toDate(occurred_at), user_id);

-- Or create from scratch:
CREATE TABLE events_v2 (...) ENGINE = MergeTree() ORDER BY (...);

-- 2. Migrate data
INSERT INTO events_v2 SELECT * FROM events;

-- 3. Swap
RENAME TABLE events TO events_old, events_v2 TO events;

-- 4. Verify, then drop
DROP TABLE events_old;
```

#### Adding a Skipping Index
```sql
ALTER TABLE events ADD INDEX IF NOT EXISTS idx_user_id user_id TYPE bloom_filter GRANULARITY 4;
ALTER TABLE events MATERIALIZE INDEX idx_user_id;  -- Backfill existing data
```

#### Node.js Migration Runner Example
```javascript
// migrations/runner.js
import { createClient } from '@clickhouse/client';
import fs from 'fs';
import path from 'path';

const client = createClient({
  url: process.env.CLICKHOUSE_URL,
  username: process.env.CLICKHOUSE_USER,
  password: process.env.CLICKHOUSE_PASSWORD,
  database: process.env.CLICKHOUSE_DB,
});

// Track applied migrations
await client.command({
  query: `CREATE TABLE IF NOT EXISTS _migrations (
    name String,
    applied_at DateTime DEFAULT now()
  ) ENGINE = MergeTree() ORDER BY (applied_at, name)`
});

const applied = new Set(
  (await client.query({ query: 'SELECT name FROM _migrations', format: 'JSONEachRow' }))
    .json().map(r => r.name)
);

const files = fs.readdirSync('./migrations').filter(f => f.endsWith('.sql')).sort();

for (const file of files) {
  if (applied.has(file)) continue;
  const sql = fs.readFileSync(path.join('./migrations', file), 'utf-8');
  // Execute each statement separately (ClickHouse doesn't support multi-statement by default)
  for (const stmt of sql.split(';').map(s => s.trim()).filter(Boolean)) {
    await client.command({ query: stmt });
  }
  await client.command({ query: `INSERT INTO _migrations (name) VALUES ('${file}')` });
  console.log(`Applied: ${file}`);
}
```

#### Go Migration Runner (golang-migrate)
```go
import (
    "github.com/golang-migrate/migrate/v4"
    _ "github.com/golang-migrate/migrate/v4/database/clickhouse"
    _ "github.com/golang-migrate/migrate/v4/source/file"
)

m, err := migrate.New(
    "file://migrations",
    "clickhouse://localhost:9000?database=mydb&username=default&password=",
)
if err != nil { log.Fatal(err) }
if err := m.Up(); err != nil && err != migrate.ErrNoChange {
    log.Fatal(err)
}
```

---

## Insert Strategy

### Rule 1 — Batch 10,000–100,000 Rows Per INSERT

Each `INSERT` creates a **data part**. Many small inserts = many small parts = merge pressure = cluster instability.

```python
# BAD: one row at a time
for event in events:
    client.execute("INSERT INTO events VALUES", [event])  # Creates 10,000 parts!

# GOOD: batch appropriately
BATCH_SIZE = 10_000
for i in range(0, len(events), BATCH_SIZE):
    client.execute("INSERT INTO events VALUES", events[i:i+BATCH_SIZE])
```

**Monitor part health:**
```sql
SELECT table, count() as parts, sum(rows) as total_rows
FROM system.parts
WHERE active AND database = currentDatabase()
GROUP BY table
ORDER BY parts DESC;
-- Warning: > 3,000 parts per table is trouble
```

### Rule 2 — Use Async Inserts for Many Small Producers

When batching client-side isn't practical (many microservices, IoT, etc.):

```sql
SET async_insert = 1;
SET async_insert_max_data_size = 10000000;   -- 10MB buffer
SET async_insert_busy_timeout_ms = 1000;      -- Flush every 1s
SET wait_for_async_insert = 1;                -- Wait for durability confirmation
```

### Rule 3 — Avoid Mutations (UPDATE/DELETE)

ClickHouse is not built for mutations. They rewrite entire data parts.

| Need | Use Instead |
|------|-------------|
| UPDATE rows | `ReplacingMergeTree` + insert new version |
| DELETE rows frequently | Lightweight DELETE (23.3+): `DELETE FROM events WHERE ...` |
| Delete old data in bulk | `DROP PARTITION` |
| Track deletions | `CollapsingMergeTree(sign)` with `sign = -1` row |

**ReplacingMergeTree pattern:**
```sql
CREATE TABLE users (
    user_id UInt64,
    name String,
    status LowCardinality(String),
    updated_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree(updated_at)
ORDER BY user_id;

-- "Update" by inserting a new version
INSERT INTO users (user_id, name, status) VALUES (123, 'Alice', 'inactive');

-- Query deduplicated (FINAL is slower but consistent)
SELECT * FROM users FINAL WHERE user_id = 123;

-- Or use argMax for better performance at scale
SELECT user_id, argMax(status, updated_at) as status
FROM users GROUP BY user_id;
```

### Rule 4 — Never Run OPTIMIZE TABLE FINAL in Production

Background merges handle part consolidation automatically. Forcing it:
- Blocks other operations
- Causes severe disk I/O spikes
- Provides no lasting benefit

---

## CLI Reference

### Connect

```bash
# Basic
clickhouse-client -h <host> -u <user> --password <pass> -d <database>

# Using env vars (recommended — hides password from process list)
export CLICKHOUSE_PASSWORD=yourpassword
clickhouse-client -h 127.0.0.1 -u app_user -d app_db

# With SSL
clickhouse-client -h <host> -u <user> -d <db> --secure --port 9440
```

Parse a JDBC URL (`jdbc:clickhouse://host:8123/db`):
```bash
JDBC="jdbc:clickhouse://myhost.com:8123/mydb"
HOST=$(echo $JDBC | sed 's|.*://\([^:]*\):.*|\1|')
PORT=$(echo $JDBC | sed 's|.*:\([0-9]*\)/.*|\1|')
DB=$(echo $JDBC   | sed 's|.*/||')
clickhouse-client -h "$HOST" --port "$PORT" -d "$DB"
```

### Inspect the Database

```bash
# List databases
clickhouse-client -h <host> -u <user> -q "SHOW DATABASES;" --format=TSV

# List tables
clickhouse-client -h <host> -u <user> -d <db> -q "SHOW TABLES;" --format=TSV

# Describe a table
clickhouse-client -h <host> -u <user> -d <db> -q "DESCRIBE TABLE my_table;" --format=TSV

# Show CREATE statement (includes engine, ORDER BY, partitioning)
clickhouse-client -h <host> -u <user> -d <db> -q "SHOW CREATE TABLE my_table;" --format=TSV

# Table sizes
clickhouse-client -h <host> -u <user> -d <db> -q "
SELECT table, total_rows as rows,
       formatReadableSize(total_bytes) as size,
       formatReadableSize(data_bytes) as data
FROM system.tables WHERE database = currentDatabase()
ORDER BY total_bytes DESC;" --format=PrettyCompact

# Check primary key / partition key columns
clickhouse-client -h <host> -u <user> -d <db> -q "
SELECT name, type, is_in_primary_key, is_in_partition_key
FROM system.columns
WHERE database = '<db>' AND table = '<table>'
ORDER BY position;" --format=PrettyCompact

# Part health check
clickhouse-client -h <host> -u <user> -d <db> -q "
SELECT table, count() as parts, sum(rows) as rows,
       formatReadableSize(sum(bytes_on_disk)) as size
FROM system.parts WHERE active AND database = currentDatabase()
GROUP BY table ORDER BY parts DESC;" --format=PrettyCompact
```

### Query Data

```bash
# Basic query — JSON output
clickhouse-client -h <host> -u <user> -d <db> \
  -q "SELECT * FROM events LIMIT 10;" --format=JSONEachRow | jq -s '.'

# Aggregation
clickhouse-client -h <host> -u <user> -d <db> \
  -q "SELECT event_type, count() as n FROM events GROUP BY event_type ORDER BY n DESC;" \
  --format=PrettyCompact

# Export to CSV
clickhouse-client -h <host> -u <user> -d <db> \
  -q "SELECT * FROM events FORMAT CSV" > /tmp/events.csv
```

### Analyze Query Performance

```bash
# Execution plan
clickhouse-client -h <host> -u <user> -d <db> \
  -q "EXPLAIN SELECT * FROM events WHERE user_id = 123;" --format=TSV

# With actual timing (ClickHouse 21.1+)
clickhouse-client -h <host> -u <user> -d <db> \
  -q "EXPLAIN ANALYZE SELECT * FROM events WHERE user_id = 123;" --format=TSV

# See which indexes were used
clickhouse-client -h <host> -u <user> -d <db> \
  -q "EXPLAIN indexes = 1 SELECT * FROM events WHERE user_id = 123;" --format=TSV
```

Look for:
- `Rows` in EXPLAIN output — fewer is better
- `Skip` entries showing granules skipped by indexes
- `Full scan` — indicates missing index coverage

### Insert / Modify Data

```bash
# Insert from file (CSV)
clickhouse-client -h <host> -u <user> -d <db> \
  -q "INSERT INTO events FORMAT CSV" < data.csv

# Insert from file (JSONEachRow)
clickhouse-client -h <host> -u <user> -d <db> \
  -q "INSERT INTO events FORMAT JSONEachRow" < data.ndjson

# Run a SQL script
clickhouse-client -h <host> -u <user> -d <db> --multiquery < migration.sql

# Lightweight delete (23.3+)
clickhouse-client -h <host> -u <user> -d <db> \
  -q "DELETE FROM events WHERE occurred_at < '2023-01-01';"

# Drop partition (instant, for lifecycle)
clickhouse-client -h <host> -u <user> -d <db> \
  -q "ALTER TABLE events DROP PARTITION '2023-01';"
```

---

## Backend Integration

### Node.js

**Install:**
```bash
npm install @clickhouse/client
```

**Module setup (`src/clickhouse.js` or `src/clickhouse.ts`):**
```javascript
// src/clickhouse.js
import { createClient } from '@clickhouse/client';

let _client = null;

export function getClickHouseClient() {
  if (_client) return _client;
  _client = createClient({
    url: process.env.CLICKHOUSE_URL ?? 'http://localhost:8123',
    username: process.env.CLICKHOUSE_USER ?? 'default',
    password: process.env.CLICKHOUSE_PASSWORD ?? '',
    database: process.env.CLICKHOUSE_DB ?? 'default',
    clickhouse_settings: {
      async_insert: 1,                       // Buffer small inserts server-side
      wait_for_async_insert: 1,              // Confirm durability
      async_insert_busy_timeout_ms: 1000,
    },
    compression: { request: true },           // Compress inserts
    request_timeout: 30_000,
  });
  return _client;
}
```

**Environment variables (`.env`):**
```env
CLICKHOUSE_URL=http://localhost:8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=secret
CLICKHOUSE_DB=analytics
```

**Insert (batch — always batch):**
```javascript
import { getClickHouseClient } from './clickhouse.js';

// Accumulate rows, then flush in a batch
const BATCH_SIZE = 10_000;
const buffer = [];

export async function trackEvent(event) {
  buffer.push(event);
  if (buffer.length >= BATCH_SIZE) {
    await flush();
  }
}

export async function flush() {
  if (buffer.length === 0) return;
  const rows = buffer.splice(0, buffer.length);
  const client = getClickHouseClient();
  await client.insert({
    table: 'events',
    values: rows,
    format: 'JSONEachRow',
  });
}

// Also flush on process exit / interval
setInterval(flush, 5_000);
process.on('beforeExit', flush);
```

**Query (analytics — aggregate, don't fetch rows one by one):**
```javascript
export async function getEventStats({ startDate, endDate, eventType }) {
  const client = getClickHouseClient();
  const result = await client.query({
    query: `
      SELECT
        toStartOfHour(occurred_at) AS hour,
        count() AS events,
        uniq(user_id) AS unique_users
      FROM events
      WHERE
        event_type = {eventType: String}
        AND occurred_at >= {startDate: DateTime}
        AND occurred_at < {endDate: DateTime}
      GROUP BY hour
      ORDER BY hour
    `,
    query_params: { eventType, startDate, endDate },
    format: 'JSONEachRow',
  });
  return result.json();
}
```

**TypeScript types:**
```typescript
interface EventRow {
  event_id: string;
  tenant_id: number;
  event_type: string;
  user_id: number;
  occurred_at: string;  // ClickHouse returns DateTime as string
  properties: Record<string, unknown>;
}

const result = await client.query({
  query: 'SELECT * FROM events LIMIT 100',
  format: 'JSONEachRow',
});
const rows = await result.json<EventRow[]>();
```

---

### Python

**Install:**
```bash
pip install clickhouse-connect   # Official Anthropic-maintained driver
# or
pip install clickhouse-driver    # Older but widely used
```

**Module setup (`clickhouse.py`):**
```python
# clickhouse.py
import os
import clickhouse_connect
from functools import lru_cache

@lru_cache(maxsize=1)
def get_client():
    return clickhouse_connect.get_client(
        host=os.environ.get('CLICKHOUSE_HOST', 'localhost'),
        port=int(os.environ.get('CLICKHOUSE_PORT', 8123)),
        username=os.environ.get('CLICKHOUSE_USER', 'default'),
        password=os.environ.get('CLICKHOUSE_PASSWORD', ''),
        database=os.environ.get('CLICKHOUSE_DB', 'default'),
        settings={
            'async_insert': 1,
            'wait_for_async_insert': 1,
            'async_insert_busy_timeout_ms': 1000,
        },
        compress=True,
    )
```

**Batch insert:**
```python
from clickhouse import get_client
from datetime import datetime

BATCH_SIZE = 10_000

def insert_events(events: list[dict]):
    """Always insert in batches of 10K+ rows."""
    client = get_client()
    # clickhouse_connect expects column-oriented data
    column_names = ['tenant_id', 'event_type', 'user_id', 'occurred_at', 'properties']
    data = [
        [e['tenant_id'] for e in events],
        [e['event_type'] for e in events],
        [e['user_id'] for e in events],
        [e['occurred_at'] for e in events],
        [e.get('properties', {}) for e in events],
    ]
    client.insert('events', data, column_names=column_names)

def batch_insert(events: list[dict]):
    for i in range(0, len(events), BATCH_SIZE):
        insert_events(events[i:i+BATCH_SIZE])
```

**Query:**
```python
def get_event_stats(event_type: str, start_date: str, end_date: str):
    client = get_client()
    result = client.query("""
        SELECT
            toStartOfHour(occurred_at) AS hour,
            count() AS events,
            uniq(user_id) AS unique_users
        FROM events
        WHERE event_type = {event_type:String}
          AND occurred_at >= {start_date:DateTime}
          AND occurred_at < {end_date:DateTime}
        GROUP BY hour
        ORDER BY hour
    """, parameters={'event_type': event_type, 'start_date': start_date, 'end_date': end_date})
    return result.named_results()  # Returns list of dicts
```

**With pandas (for data pipelines):**
```python
def get_dataframe(query: str, params: dict = None):
    client = get_client()
    return client.query_df(query, parameters=params or {})

df = get_dataframe("SELECT event_type, count() as n FROM events GROUP BY event_type")
```

---

### Go

**Install:**
```bash
go get github.com/ClickHouse/clickhouse-go/v2
```

**Module setup (`internal/clickhouse/client.go`):**
```go
package clickhouse

import (
    "context"
    "crypto/tls"
    "fmt"
    "os"
    "sync"
    "time"

    ch "github.com/ClickHouse/clickhouse-go/v2"
    "github.com/ClickHouse/clickhouse-go/v2/lib/driver"
)

var (
    once   sync.Once
    client driver.Conn
)

func GetClient() (driver.Conn, error) {
    var err error
    once.Do(func() {
        options := &ch.Options{
            Addr: []string{fmt.Sprintf("%s:%s",
                getEnv("CLICKHOUSE_HOST", "localhost"),
                getEnv("CLICKHOUSE_PORT", "9000"),
            )},
            Auth: ch.Auth{
                Database: getEnv("CLICKHOUSE_DB", "default"),
                Username: getEnv("CLICKHOUSE_USER", "default"),
                Password: getEnv("CLICKHOUSE_PASSWORD", ""),
            },
            Settings: ch.Settings{
                "async_insert":                1,
                "wait_for_async_insert":       1,
                "async_insert_busy_timeout_ms": 1000,
            },
            DialTimeout:     time.Second * 5,
            MaxOpenConns:    10,
            MaxIdleConns:    5,
            ConnMaxLifetime: time.Hour,
            Compression: &ch.Compression{
                Method: ch.CompressionLZ4,
            },
        }

        // Enable TLS for production
        if os.Getenv("CLICKHOUSE_TLS") == "true" {
            options.TLS = &tls.Config{InsecureSkipVerify: false}
        }

        client, err = ch.Open(options)
    })
    return client, err
}

func getEnv(key, fallback string) string {
    if v := os.Getenv(key); v != "" {
        return v
    }
    return fallback
}
```

**Batch insert:**
```go
package clickhouse

import (
    "context"
    "time"
)

type Event struct {
    TenantID   uint32    `ch:"tenant_id"`
    EventType  string    `ch:"event_type"`
    UserID     uint64    `ch:"user_id"`
    OccurredAt time.Time `ch:"occurred_at"`
}

func InsertEvents(ctx context.Context, events []Event) error {
    conn, err := GetClient()
    if err != nil {
        return err
    }

    batch, err := conn.PrepareBatch(ctx, "INSERT INTO events")
    if err != nil {
        return err
    }

    for _, e := range events {
        if err := batch.AppendStruct(&e); err != nil {
            return err
        }
    }
    return batch.Send()
}
```

**Query:**
```go
type HourlyStats struct {
    Hour        time.Time `ch:"hour"`
    Events      uint64    `ch:"events"`
    UniqueUsers uint64    `ch:"unique_users"`
}

func GetEventStats(ctx context.Context, eventType, start, end string) ([]HourlyStats, error) {
    conn, err := GetClient()
    if err != nil {
        return nil, err
    }

    rows, err := conn.Query(ctx, `
        SELECT toStartOfHour(occurred_at) AS hour,
               count() AS events,
               uniq(user_id) AS unique_users
        FROM events
        WHERE event_type = @eventType
          AND occurred_at >= @start
          AND occurred_at < @end
        GROUP BY hour ORDER BY hour`,
        ch.Named("eventType", eventType),
        ch.Named("start", start),
        ch.Named("end", end),
    )
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var stats []HourlyStats
    for rows.Next() {
        var s HourlyStats
        if err := rows.ScanStruct(&s); err != nil {
            return nil, err
        }
        stats = append(stats, s)
    }
    return stats, rows.Err()
}
```

---

## Query Optimization

### Use ORDER BY Prefix in Every WHERE Clause

Always filter on the leftmost columns of ORDER BY first.
If you can't, add a data skipping index.

### Data Skipping Indexes

For columns NOT in ORDER BY that you filter on:

```sql
-- Add bloom filter for high-cardinality equality lookups
ALTER TABLE events ADD INDEX idx_user_id user_id TYPE bloom_filter GRANULARITY 4;
ALTER TABLE events MATERIALIZE INDEX idx_user_id;  -- Backfill

-- Index types:
-- bloom_filter: equality on high-cardinality (user IDs, session IDs)
-- set(N):       low-cardinality equality (status IN ('a','b'))  
-- minmax:       range queries (amount > 1000)
-- ngrambf_v1:  text search (LIKE '%term%')
-- tokenbf_v1:  token search (hasToken(text, 'word'))

-- Verify it's being used
EXPLAIN indexes = 1
SELECT * FROM events WHERE user_id = 12345;
-- Look for "Skip" entries in output
```

### JOINs

ClickHouse JOINs load the **right table into memory**. Always put the smaller table on the right.

```sql
-- BAD: large table on right
SELECT * FROM small_table s JOIN large_table l ON l.id = s.id;

-- GOOD: small table on right
SELECT * FROM large_table l JOIN small_table s ON s.id = l.id;
```

**Filter BEFORE joining:**
```sql
-- GOOD: reduce data before the join
SELECT * FROM
    (SELECT * FROM orders WHERE status = 'completed') o
JOIN
    (SELECT * FROM customers WHERE country = 'US') c
ON c.id = o.customer_id;
```

**Choose the right algorithm:**
```sql
SET join_algorithm = 'auto';          -- Default: ClickHouse decides
SET join_algorithm = 'partial_merge'; -- Large-to-large, memory-constrained
SET join_algorithm = 'grace_hash';    -- Large datasets, can spill to disk
```

**Use ANY JOIN when you only need one match:**
```sql
SELECT o.*, c.name
FROM orders o
ANY LEFT JOIN customers c ON c.id = o.customer_id;
-- Faster and less memory when right table may have duplicates
```

**Alternatives to JOINs (often faster):**
```sql
-- Dictionary for dimension lookups
SELECT o.*, dictGet('customers_dict', 'name', o.customer_id) as name
FROM orders o;

-- IN subquery for filtering
SELECT * FROM orders
WHERE customer_id IN (SELECT id FROM customers WHERE country = 'US');
```

### Materialized Views

Use materialized views to pre-aggregate data instead of scanning raw tables.

**Incremental MV (updates in real time):**
```sql
-- Destination table
CREATE TABLE events_hourly (
    hour DateTime,
    event_type LowCardinality(String),
    events AggregateFunction(count, UInt64),
    unique_users AggregateFunction(uniq, UInt64)
) ENGINE = AggregatingMergeTree()
ORDER BY (event_type, hour);

-- MV triggers on every INSERT into events
CREATE MATERIALIZED VIEW events_hourly_mv TO events_hourly AS
SELECT
    toStartOfHour(occurred_at) AS hour,
    event_type,
    countState() AS events,
    uniqState(user_id) AS unique_users
FROM events
GROUP BY hour, event_type;

-- Query (reads thousands instead of billions)
SELECT hour, event_type, countMerge(events), uniqMerge(unique_users)
FROM events_hourly
WHERE hour >= now() - INTERVAL 7 DAY
GROUP BY hour, event_type;
```

**Refreshable MV (periodic rebuild, good for complex JOINs):**
```sql
CREATE MATERIALIZED VIEW customer_summary
REFRESH EVERY 1 HOUR
ENGINE = MergeTree() ORDER BY customer_id
AS SELECT
    c.customer_id, c.name,
    count() as orders, sum(o.amount) as total_spent
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name;

-- Force refresh
SYSTEM REFRESH VIEW customer_summary;
```

### Avoid Small/Single-Row Queries

ClickHouse is built for scanning many rows and returning aggregates.
**Do not use it like a key-value store.**

```javascript
// BAD: Fetching one user's data from ClickHouse on every request
app.get('/user/:id/events', async (req, res) => {
  const events = await ch.query(`SELECT * FROM events WHERE user_id = ${req.params.id}`);
  res.json(events); // This is a key-value access pattern
});

// GOOD: Aggregate query that leverages ClickHouse's strength
app.get('/analytics/summary', async (req, res) => {
  const stats = await ch.query(`
    SELECT event_type, count() as n, uniq(user_id) as users
    FROM events
    WHERE occurred_at >= today() - 7
    GROUP BY event_type
  `);
  res.json(stats);
});
```

---

## Redis Caching Strategy

### When to Use Redis in Front of ClickHouse

| Scenario | Use Redis? | Reason |
|----------|-----------|--------|
| Dashboard with same query run by many users | ✅ Yes | Prevents redundant large scans |
| Single user fetching their own recent events | ✅ Yes | ClickHouse isn't a KV store |
| Aggregation query taking > 500ms | ✅ Yes | Cache computed result |
| Real-time per-user event counts | ✅ Yes | Maintain counter in Redis, bulk-sync to CH |
| Ad-hoc analytics queries (new filters every time) | ❌ No | Cache hit rate will be low |
| Time-series queries where time range keeps moving | ❌ Careful | Invalidation is complex |
| Backfill / batch ETL pipeline | ❌ No | No user-facing latency concern |

### Recommended Cache Pattern

```javascript
// Cache ClickHouse aggregation results in Redis
async function getDashboardStats(tenantId, dateRange) {
  const cacheKey = `stats:${tenantId}:${dateRange}`;
  const TTL = 300; // 5 minutes

  // 1. Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // 2. Run the (potentially expensive) ClickHouse query
  const result = await clickhouse.query({
    query: `
      SELECT event_type, count() as n, uniq(user_id) as users
      FROM events
      WHERE tenant_id = {tenantId: UInt32}
        AND occurred_at >= {start: DateTime}
      GROUP BY event_type
    `,
    query_params: { tenantId, start: dateRange },
    format: 'JSONEachRow',
  });
  const data = await result.json();

  // 3. Cache for TTL
  await redis.setex(cacheKey, TTL, JSON.stringify(data));
  return data;
}
```

### When to Query ClickHouse Directly (No Redis)

- The query is already fast (< 100ms) due to good schema design and materialized views
- The query parameters are always unique (ad-hoc analytics, no cache benefit)
- You have a materialized view pre-aggregating the data — query the MV directly
- It's an internal/batch process with no latency requirement

**The right answer is usually:** build good materialized views so the ClickHouse query is already fast enough that you don't need Redis.

---

## Cluster Considerations

On a ClickHouse cluster, DDL and certain operations must include `ON CLUSTER`.

### Engine Naming

| Single-node | Cluster |
|-------------|---------|
| `MergeTree` | `ReplicatedMergeTree('/clickhouse/tables/{shard}/{database}/{table}', '{replica}')` |
| `ReplacingMergeTree(ver)` | `ReplicatedReplacingMergeTree(...)` |
| All MergeTree variants | `Replicated` prefix |

In practice, use macros defined in `config.xml`:
```sql
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/{database}/{table}', '{replica}')
```

### DDL on Cluster

```sql
-- Always include ON CLUSTER for DDL on distributed setups
CREATE TABLE events ON CLUSTER '{cluster}' ( ... )
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/{database}/{table}', '{replica}')
ORDER BY (...);

ALTER TABLE events ON CLUSTER '{cluster}' ADD COLUMN new_col UInt32 DEFAULT 0;
```

### Distributed Tables

```sql
-- Create local table first (on cluster)
CREATE TABLE events_local ON CLUSTER '{cluster}' ( ... )
ENGINE = ReplicatedMergeTree(...)
ORDER BY (...);

-- Then create a Distributed table as the access layer
CREATE TABLE events ON CLUSTER '{cluster}' ( ... )
ENGINE = Distributed('{cluster}', currentDatabase(), 'events_local', rand());
```

Applications connect to the Distributed table; ClickHouse routes queries to shards transparently.

### INSERT Routing

On a cluster, insert into the Distributed table (not the local table) unless you are doing a shard-local operation intentionally.

### System Queries on Clusters

```sql
-- Check part health across all shards
SELECT hostName(), table, count() as parts
FROM clusterAllReplicas('{cluster}', system.parts)
WHERE active GROUP BY hostName(), table ORDER BY parts DESC;

-- Check replication lag
SELECT database, table, replica_name, queue_size
FROM system.replication_queue
WHERE queue_size > 0;
```

---

## Rules Reference

Detailed per-rule files are in `rules/` (loaded on demand):

- Schema / Primary Key: `rules/schema-pk-*.md`
- Schema / Types: `rules/schema-types-*.md`
- Schema / Partitioning: `rules/schema-partition-*.md`
- Schema / JSON: `rules/schema-json-when-to-use.md`
- Query / JOINs: `rules/query-join-*.md`
- Query / Indexes: `rules/query-index-skipping-indices.md`
- Query / Materialized Views: `rules/query-mv-*.md`
- Insert / Batching: `rules/insert-batch-size.md`
- Insert / Async: `rules/insert-async-small-batches.md`
- Insert / Format: `rules/insert-format-native.md`
- Insert / Mutations: `rules/insert-mutation-*.md`
- Insert / Optimize: `rules/insert-optimize-avoid-final.md`
