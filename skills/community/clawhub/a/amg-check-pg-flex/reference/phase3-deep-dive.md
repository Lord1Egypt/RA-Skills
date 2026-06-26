# Phase 3: Tier 2 — Deep Metrics for Abnormal Servers

Query additional metrics using `amgmcp_query_resource_metric` for each server flagged in Phase 2. Focus on the anomaly window (2 days around the spike), with `PT5M` interval for spikes or `PT1H` for sustained issues.

## Batch Strategy

- Group servers by anomaly window; batch all servers in the same window into one call.
- Up to 50 comma-separated resource IDs per call.
- Query different metrics in parallel (up to 5 calls per batch).
- If rate-limited, reduce batch size to 25, then 10.

## Core Metrics (always query)

| Metric Name | Aggregation | Flag If |
|-------------|-------------|---------|
| `cpu_percent` | Maximum | >90% critical, >70% warning |
| `memory_percent` | Maximum | >90% critical, >80% warning |
| `storage_percent` | Maximum | >85% critical, >70% warning |
| `is_db_alive` | Minimum | = 0 (server was down) |
| `active_connections` | Average | Drops or spikes indicate client issues |
| `connections_failed` | Total | >0 indicates connectivity issues |
| `iops` | Average | High with high CPU → query-driven load |
| `network_bytes_egress` | Total | Spikes → large result sets returned |
| `network_bytes_ingress` | Total | Spikes → large writes or bulk operations |

## Secondary Metrics (query if core metrics show anomalies)

| Metric Name | Aggregation | Flag If |
|-------------|-------------|---------|
| `deadlocks` | Total | Sustained >0 |
| `txlogs_storage_used` | Average | Growth → replication lag or long transactions |
| `longest_query_time_sec` | Maximum | >300s |
| `longest_transaction_time_sec` | Maximum | High → idle-in-transaction sessions |
| `disk_iops_consumed_percentage` | Maximum | >80% (disk-bound) |
| `disk_bandwidth_consumed_percentage` | Maximum | >80% |
| `maximum_used_transactionIDs` | Maximum | >1,000,000,000 |
| `physical_replication_delay_in_seconds` | Maximum | >30s |

Empty `timeSeries` on replication metrics means the server is not a replica — silently skip, mark as N/A.

## Correlation Analysis (ultrathink)

Use extended thinking to reason through multi-metric correlations:

| Pattern | Likely Cause |
|---------|-------------|
| High CPU + normal IOPS + high network egress | CPU-bound workload returning large results (in-memory scans) |
| High CPU + high IOPS | Disk-intensive queries (missing indexes, sequential scans) |
| High CPU + connection spike | Connection storm (TLS/auth overhead) |
| High CPU + connection drop (NULL data) | Server too overloaded to report metrics |
| Memory spike + storage spike | OOM or sort/hash spill to disk |
| `is_db_alive` = 0 | Server was down — check for crash-restart cycle |

## Per-Server Report

For each abnormal server:
- **Metric timeline**: CPU, memory, connections, IOPS, network I/O over the anomaly window
- **Anomaly characterization**: spike vs sustained, onset time, duration, recovery
- **Correlation analysis**: which metrics moved together
- **Post-anomaly state**: did metrics return to baseline or settle at a new level
