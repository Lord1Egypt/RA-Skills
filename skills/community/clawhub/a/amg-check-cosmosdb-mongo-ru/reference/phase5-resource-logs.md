# Phase 5: Resource Logs for Abnormal Accounts

Query Cosmos DB resource logs using `amgmcp_query_resource_log` with the account's resource ID.

**IMPORTANT**: Always include tight time filters in resource log queries to avoid timeouts. Keep the range to 1-2 days. Resource logs depend on diagnostic settings being configured — if no data is returned, note it and skip.

Replace `<START>` and `<END>` with ISO 8601 UTC timestamps (e.g., `2026-04-09T00:00:00Z`).

---

## Query 1: Throttled Requests (429 Status Codes)

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ErrorCode == 429 or ErrorCode == 16500
| summarize ThrottledCount=count() by bin(TimeGenerated, 1h), DatabaseName, CollectionName
| order by TimeGenerated asc
```

## Query 2: High Latency Operations

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where DurationMs > 100
| summarize count(), avg(DurationMs), max(DurationMs), sum(RequestCharge) by OperationName, DatabaseName, CollectionName
| order by count_ desc
| take 20
```

## Query 3: Request Volume and Error Distribution

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize
    TotalRequests=count(),
    FailedRequests=countif(ErrorCode != 0 and ErrorCode != 200),
    ThrottledRequests=countif(ErrorCode == 429 or ErrorCode == 16500),
    AvgLatencyMs=round(avg(DurationMs), 2),
    TotalRU=round(sum(RequestCharge), 2)
    by bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

## Query 4: Top RU-Consuming Operations

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize
    TotalRU=round(sum(RequestCharge), 2),
    AvgRU=round(avg(RequestCharge), 2),
    MaxRU=round(max(RequestCharge), 2),
    Count=count()
    by OperationName, DatabaseName, CollectionName
| order by TotalRU desc
| take 20
```

## Query 5: Error Code Distribution

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ErrorCode != 0 and ErrorCode != 200
| summarize count() by ErrorCode
| order by count_ desc
| take 20
```

---

## Fallback Table

If `CDBMongoRequests` returns no data, try `CDBDataPlaneRequests` as a fallback. The available table depends on the diagnostic settings configuration.

For `CDBDataPlaneRequests`, adjust queries:
- Use `StatusCode` instead of `ErrorCode`
- Use `StatusCode == 429` for throttling detection
- Column names may differ — run `CDBDataPlaneRequests | take 5` first to discover the schema

## What to Report

For each abnormal account:
- **Throttling summary**: 429 error rate, affected databases/collections, throttling timeline
- **High-latency operations**: top slow operations by RU cost and latency
- **Error distribution**: error codes, affected operations
- **Diagnostic settings status**: If both tables return empty, note that diagnostic settings are not configured and recommend enabling them
