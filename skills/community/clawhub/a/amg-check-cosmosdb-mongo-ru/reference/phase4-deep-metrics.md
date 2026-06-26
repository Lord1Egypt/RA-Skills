# Phase 4: Tier 2 — Deep Metrics for Abnormal Accounts

Query additional metrics using `amgmcp_query_resource_metric` for each account flagged in Phase 3. Use `PT1H` interval.

## Response Size Management

Fleet-wide metric queries at PT1H x 7 days x 30 accounts will exceed the 500 KB MCP response limit (~5,000 data points per metric).

**Strategies:**
- **Fleet overview metrics** (ProvisionedThroughput, AutoscaleMaxThroughput): Use `FULL` interval or a 1-day window — only the current value matters. These produce small responses even for 30 accounts.
- **Time-series metrics** (NormalizedRU, Availability, Latency): Split into batches of **10-15 accounts per call**, or reduce the time window to 2-3 days.
- **If a response exceeds 500 KB**: The MCP server returns an error. Retry with fewer accounts or a shorter time window. Do NOT retry with the same parameters.
- **If a response is too large for context**: Save to a temp file and parse outside the context window. Prefer `node -e "..."` if installed; otherwise fall back to `python -c "..."`, `jq`, or `pwsh -Command "..."`.

## Fleet-Wide Triage (when >50% accounts flagged)

When the pulse check flags more than half the fleet, the issue is likely fleet-wide rather than per-account. Before deep-diving individual accounts, gather fleet-wide context:

1. **AutoscaleMaxThroughput** for all accounts (`FULL` interval) — determines manual vs autoscale split. Empty `timeSeries` = manual throughput.
2. **ProvisionedThroughput** for all accounts (`FULL` interval or 1-day window) — current RU/s values.
3. **Triage accounts into categories:**
   - **Sustained saturation** (100% for >6 consecutive hours): highest priority for deep dive
   - **Frequent spikes** (>3 spikes to 100% in 7 days): second priority
   - **Single peak**: likely transient — summarize from pulse check data, no deep dive needed
   - **Availability/latency issues**: always deep dive regardless of RU category
4. **Deep dive only the top 5-10 most critical accounts** in the sections below. Summarize the rest from pulse check data in the report.

## Batch Strategy

- Group accounts by anomaly window; batch those in the same window into one call.
- Up to **50** comma-separated resource IDs per call (but keep under the 500 KB limit — usually 10-15 accounts for hourly data over 7 days).
- Query different metrics in parallel (up to 5 calls per batch).
- If rate-limited, reduce batch size to 10, then 5.

## Core Metrics (always query for deep-dive accounts)

| Metric Name | Aggregation | Flag If |
|-------------|-------------|---------|
| `NormalizedRUConsumption` | `Maximum` | > 90% critical, > 70% warning |
| `ServiceAvailability` | `Average` | < 99.9% critical, < 99.99% warning |
| `ServerSideLatencyDirect` | `Average` | > 50ms critical, > 10ms warning |
| `ServerSideLatencyGateway` | `Average` | > 50ms critical, > 10ms warning |
| `ProvisionedThroughput` | `Maximum` | Informational — baseline RU/s |
| `TotalRequestUnits` | `Total` | Informational — total RU consumed |
| `MongoRequests` | `Count` | Informational — request volume |
| `MongoRequestCharge` | `Total` | Informational — RU cost of Mongo operations |

> **Note:** `ServerSideLatency` is deprecated (removed Aug 2025). Use `ServerSideLatencyDirect` and `ServerSideLatencyGateway` instead.

## Secondary Metrics (query if core metrics show anomalies)

| Metric Name | Aggregation | Flag If |
|-------------|-------------|---------|
| `AutoscaleMaxThroughput` | `Maximum` | Empty timeSeries = no autoscale (manual throughput) |
| `DataUsage` | `Total` | Informational — value in bytes. Use `PT1H` only |
| `DocumentCount` | `Total` | Informational. Use `PT1H` only |
| `ReplicationLatency` | `Average` | > 100ms warning, > 1000ms critical |

**Notes on specific metrics:**
- `AutoscaleMaxThroughput`: Empty `timeSeries` means manual (fixed) throughput — no autoscale. Non-empty means autoscale is enabled.
- `DataUsage` and `DocumentCount`: Use `PT1H` interval only — `P1D` is NOT supported.
- `ReplicationLatency`: Empty `timeSeries` means the account is not geo-replicated — silently skip, mark as N/A.
- `MongoRequestCharge`: Total RU consumed specifically by MongoDB API operations.

## Correlation Analysis (ultrathink)

Use extended thinking to reason through multi-metric correlations:

| Pattern | Likely Cause |
|---------|-------------|
| High NormalizedRU + high MongoRequests + normal latency | High request volume driving RU consumption (scale up or optimize queries) |
| High NormalizedRU + high latency + normal request count | Expensive queries consuming too many RUs per operation (index optimization needed) |
| NormalizedRU = 100% constant + high MongoRequestCharge | Sustained throttling — provisioned throughput insufficient |
| High NormalizedRU + AutoscaleMaxThroughput empty | Manual throughput account hitting ceiling (consider enabling autoscale) |
| High NormalizedRU + AutoscaleMaxThroughput non-empty | Autoscale hitting its max RU cap |
| ServiceAvailability drop + ReplicationLatency spike | Regional issue or failover event |
| High latency + normal NormalizedRU | Backend issue, not RU-related (check region health) |
| Sudden MongoRequests spike + RU spike | Workload burst (check if periodic job or traffic surge) |

## Per-Account Report

For each deep-dive account:
- **Metric timeline**: NormalizedRU, latency, availability, request volume over the anomaly window
- **Anomaly characterization**: spike vs sustained, onset time, duration, recovery
- **Correlation analysis**: which metrics moved together
- **Throughput context**: provisioned RU/s, autoscale status, RU consumption relative to limit
