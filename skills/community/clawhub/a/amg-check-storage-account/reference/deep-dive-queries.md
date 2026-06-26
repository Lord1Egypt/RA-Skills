# Deep-Dive Queries

Run these only if the user asks for more detail or if initial results reveal issues worth investigating.

## Error Analysis

### Error requests by status code over time

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where StatusCode >= 400
| summarize count() by StatusCode, bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

### Top error operations

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where StatusCode >= 400
| summarize count() by OperationName, StatusCode, StatusText
| order by count_ desc
| take 30
```

### Throttled requests (503) over time

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where StatusCode == 503
| summarize count() by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

### Authentication failures detail

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where StatusCode == 403
| summarize count() by CallerIpAddress, UserAgentHeader, AuthenticationType
| order by count_ desc
| take 20
```

### Not Found (404) requests — orphaned references

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where StatusCode == 404
| summarize count() by OperationName, Uri
| order by count_ desc
| take 20
```

## Latency Analysis

### Latency percentiles by operation

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ServerLatencyMs > 0
| summarize
    AvgLatency=round(avg(ServerLatencyMs), 2),
    P50=round(percentile(ServerLatencyMs, 50), 2),
    P90=round(percentile(ServerLatencyMs, 90), 2),
    P99=round(percentile(ServerLatencyMs, 99), 2),
    MaxLatency=max(ServerLatencyMs),
    Count=count()
    by OperationName
| order by AvgLatency desc
| take 20
```

### E2E vs Server latency comparison

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ServerLatencyMs > 0
| summarize
    AvgE2E=round(avg(E2ELatencyMs), 2),
    AvgServer=round(avg(ServerLatencyMs), 2),
    NetworkGap=round(avg(E2ELatencyMs) - avg(ServerLatencyMs), 2),
    Count=count()
    by bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

### Slow operations (>100ms server latency)

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ServerLatencyMs > 100
| project TimeGenerated, OperationName, Uri, ServerLatencyMs, E2ELatencyMs, StatusCode
| order by ServerLatencyMs desc
| take 50
```

### Latency by object size

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ServerLatencyMs > 0
| extend SizeBucket = case(
    ResponseBodySize < 1024, "<1KB",
    ResponseBodySize < 1048576, "1KB-1MB",
    ResponseBodySize < 104857600, "1MB-100MB",
    ">100MB")
| summarize
    AvgLatency=round(avg(ServerLatencyMs), 2),
    Count=count()
    by SizeBucket, OperationName
| order by AvgLatency desc
```

## Traffic Analysis

### Request volume trend

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize
    TotalRequests=count(),
    FailedRequests=countif(StatusCode >= 400),
    AvgLatencyMs=round(avg(ServerLatencyMs), 2)
    by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

### Request volume by operation type

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize Count=count() by OperationName
| order by Count desc
| take 20
```

### Top callers by IP

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize Count=count(), FailedCount=countif(StatusCode >= 400) by CallerIpAddress
| order by Count desc
| take 20
```

### Data transfer volume

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize
    TotalIngress=round(sum(RequestBodySize) / 1048576.0, 2),
    TotalEgress=round(sum(ResponseBodySize) / 1048576.0, 2),
    RequestCount=count()
    by bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

## Container-Level Analysis

### Activity by container

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| extend Container = extract("/([^/]+)/", 1, Uri)
| summarize Count=count(), AvgLatency=round(avg(ServerLatencyMs), 2), Errors=countif(StatusCode >= 400) by Container
| order by Count desc
| take 20
```

### Container-level error rate

```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| extend Container = extract("/([^/]+)/", 1, Uri)
| summarize Total=count(), Errors=countif(StatusCode >= 400) by Container
| extend ErrorRate=round(100.0 * Errors / Total, 2)
| where Errors > 0
| order by ErrorRate desc
| take 20
```

## Metric Queries

### Fine-grained E2E latency around a spike

Use `amgmcp_query_resource_metric` with `metricName: SuccessE2ELatency`, `aggregation: Average`, `interval: PT1H` and a 2-day window around the spike.

### Server vs E2E latency comparison via metrics

Query both `SuccessE2ELatency` and `SuccessServerLatency` with `aggregation: Average`, `interval: PT1H` for the same time window. Large gaps indicate network issues.

### Availability check around incidents

Use `amgmcp_query_resource_metric` with `metricName: Availability`, `aggregation: Average`, `interval: PT1H` around availability drop events.
