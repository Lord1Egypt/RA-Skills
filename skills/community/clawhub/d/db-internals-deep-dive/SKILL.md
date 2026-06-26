---
name: db-internals-deep-dive
description: Deep dive into database and messaging system internals — PostgreSQL, MongoDB, Redis, RabbitMQ, Kafka. Covers storage engines, replication, consistency, performance tuning, and operational patterns at scale. Trigger for requests like "PostgreSQL internals", "how Kafka works internally", "Redis deep dive", "MongoDB storage engine", "RabbitMQ vs Kafka", "db internals today", or "deep dive vào database".
---

Teach ONE deep-dive topic per session, rotating across all 5 systems below. Go to the internals level — not surface docs.

---

## Systems & Topic Map

### PostgreSQL

- **Storage Engine**: heap file format, page structure (8KB pages, page header, item pointers, tuples), TOAST (The Oversized-Attribute Storage Technique)
- **MVCC**: transaction visibility rules, xmin/xmax, snapshot isolation, how dead tuples accumulate, vacuum mechanics (regular vs autovacuum vs VACUUM FULL)
- **WAL (Write-Ahead Log)**: WAL segments, LSN (Log Sequence Number), checkpoint mechanism, WAL archiving, pg_wal
- **Query Planner**: cost model (seq_page_cost, random_page_cost, cpu_tuple_cost), statistics (pg_statistic, ANALYZE), join strategies (nested loop / hash join / merge join), plan cache
- **Indexes**: B-tree internals (page splits, fill factor), GIN (for full-text / JSONB), GiST, BRIN (block range), partial indexes, index-only scans, HOT updates
- **Replication**: WAL-based streaming replication, synchronous vs asynchronous, replication slots, logical replication (publication/subscription), failover mechanics
- **Locking**: lock levels (table/row/page), advisory locks, deadlock detection cycle, lock contention patterns
- **Connection & Performance**: connection overhead (process-per-connection model), PgBouncer pooling (session/transaction/statement modes), shared_buffers, work_mem, effective_cache_size tuning

### MongoDB

- **WiredTiger Storage Engine**: B-tree structure for documents, MVCC with snapshot isolation, checkpoint (every 60s or 2GB), write-ahead journal (WiredTiger journal ≠ oplog)
- **Oplog**: capped collection, oplog entry structure (op, ns, o, ts), idempotency requirements, oplog window sizing
- **Replication Set**: election algorithm (Raft-inspired), primary/secondary roles, oplog replication, write concern (w:1/w:majority/w:all), read preference (primary/primaryPreferred/secondary/nearest)
- **Sharding**: shard key selection criteria (cardinality, write distribution, query isolation), chunk mechanics, balancer, scatter-gather vs targeted queries, jumbo chunks
- **Aggregation Pipeline**: execution stages, pipeline optimization (stage reordering, index utilization), $lookup internals, memory limits (100MB/stage), allowDiskUse
- **Indexes**: compound index prefix rule, ESR (Equality-Sort-Range) rule, sparse/partial indexes, TTL index mechanics, index intersection
- **Transactions**: multi-document ACID (since 4.0), snapshot isolation, performance overhead, retryable writes

### Redis

- **Data Structures Internals**: ziplist vs listpack vs skiplist (when Redis switches encoding — size thresholds), hashtable with incremental rehashing, quicklist for lists, intset for small integer sets
- **Persistence**: RDB (fork-based snapshot, BGSAVE, COW semantics), AOF (fsync policies: always/everysec/no, AOF rewrite/compaction), RDB+AOF hybrid mode
- **Memory Management**: jemalloc allocator, memory fragmentation ratio, maxmemory policies (noeviction, allkeys-lru, volatile-lru, allkeys-lfu, volatile-ttl), object encoding optimization
- **Replication**: async replication (PSYNC2), replication backlog (repl-backlog-size), partial resync vs full resync, replica lag detection
- **Cluster Mode**: hash slots (16384), gossip protocol, slot migration, MOVED vs ASK redirects, cluster topology change handling
- **Pub/Sub & Streams**: pub/sub fire-and-forget (no persistence), Redis Streams (XADD/XREAD/consumer groups, message acknowledgment, PEL — Pending Entry List)
- **Lua Scripting & Transactions**: MULTI/EXEC (optimistic — not true isolation), WATCH/CAS, Lua atomicity guarantee
- **Sentinel**: quorum-based leader election, ODOWN vs SDOWN, automatic failover flow

### RabbitMQ

- **AMQP Protocol**: connection vs channel multiplexing, frame types (method/header/body/heartbeat), flow control
- **Exchange Types**: direct (routing key exact match), topic (wildcard: `*` one word, `#` zero or more), fanout (broadcast), headers (attribute-based matching) — internal routing algorithm
- **Queue Internals**: message store (index + body store), queue index (journal + segment files), lazy queues (messages on disk by default), classic vs quorum queues
- **Quorum Queues**: Raft-based replication, leader election, how quorum queues guarantee durability, comparison with classic mirrored queues (deprecated)
- **Message Acknowledgment**: basic.ack / basic.nack / basic.reject, requeue semantics, consumer prefetch (QoS), unacknowledged message limits
- **Dead Letter Exchange (DLX)**: when messages go DLX (rejected, expired, queue length exceeded), DLX routing, dead-letter-routing-key
- **Clustering & High Availability**: Erlang distribution protocol, mnesia metadata replication, quorum queue replication across nodes, network partition handling (pause-minority / autoheal / ignore)
- **Flow Control & Backpressure**: credit-based flow control between producers and broker, memory/disk alarms (vm_memory_high_watermark, disk_free_limit)
- **Shovel & Federation**: when to use each (cross-cluster vs cross-datacenter), differences in message flow

### Kafka

- **Log Architecture**: topic → partition → segment files (.log + .index + .timeindex), log compaction vs log deletion (retention.ms / retention.bytes), offset management
- **Producer Internals**: batching (batch.size, linger.ms), compression (lz4/snappy/gzip/zstd), partitioner (sticky vs round-robin vs custom), idempotent producer (PID + sequence numbers), transactional producer
- **Consumer Internals**: consumer group protocol, group coordinator, partition assignment strategies (range / round-robin / sticky / cooperative-sticky), rebalance triggers and cooperative rebalancing
- **Broker Storage**: page cache reliance (zero-copy sendfile), log segment index (sparse — every `index.interval.bytes`), active segment vs rolled segments, leader vs follower replica
- **Replication**: ISR (In-Sync Replicas), acks=0/1/all, high watermark (HW), log end offset (LEO), replica lag (replica.lag.time.max.ms), leader epoch for fencing
- **Controller & Metadata**: KRaft mode (Kafka Raft — ZooKeeper removal), metadata log, controller quorum, leader election without ZK
- **Exactly-Once Semantics**: idempotent producer + transactions + transactional consumer (read_committed isolation), two-phase commit across partitions
- **Kafka Streams & Connect**: stream processing topology (processor graph, state stores — RocksDB backed), changelog topics, Kafka Connect (source/sink connectors, task parallelism, offset tracking)
- **Performance Tuning**: num.io.threads, num.network.threads, socket.send.buffer.bytes, log.flush.interval.messages, replica.fetch.max.bytes

---

## Procedure

1. Pick ONE topic from the map above, rotating across all 5 systems. Do NOT repeat topics covered in recent sessions.
2. Go deep — internals, not documentation summaries.
3. Use a concrete scenario or failure case to ground the explanation.
4. Explain trade-offs and why the design choice was made.
5. Give a mini challenge or follow-up question.

---

## Output Format

```
DB INTERNALS DEEP DIVE — [Date]

SYSTEM
[PostgreSQL / MongoDB / Redis / RabbitMQ / Kafka]

TOPIC
[Topic name]

HOW IT WORKS INTERNALLY
[Detailed mechanism — data structures, algorithms, disk layout, etc.]

WHY IT'S DESIGNED THIS WAY
[Trade-off reasoning — what problem this solves, what it sacrifices]

FAILURE SCENARIO
[What breaks, what symptoms appear, how to diagnose]

PRODUCTION IMPLICATIONS
[Config knobs, monitoring signals, common pitfalls]

MINI CHALLENGE
[A diagnostic question or design decision to think through]
```

**Important:**

- No markdown table.
- Match the caller's preferred language — but keep technical terms, config names, and command examples in English.
- Be precise about internals — no hand-waving. Name the data structures, file formats, and algorithms.
