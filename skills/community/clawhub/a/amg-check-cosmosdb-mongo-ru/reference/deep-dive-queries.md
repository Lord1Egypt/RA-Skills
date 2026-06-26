# Deep-Dive Queries

Run these only if the user asks for more detail or if initial results reveal issues worth investigating.

## Throttling Analysis

### Throttled requests over time

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ErrorCode == 429 or ErrorCode == 16500
| summarize ThrottledCount=count(), TotalRU=round(sum(RequestCharge), 2) by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

### Throttling by collection

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ErrorCode == 429 or ErrorCode == 16500
| summarize ThrottledCount=count() by DatabaseName, CollectionName
| order by ThrottledCount desc
| take 20
```

### Throttling by operation type

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ErrorCode == 429 or ErrorCode == 16500
| summarize ThrottledCount=count() by OperationName
| order by ThrottledCount desc
```

## Latency Analysis

### Latency percentiles by operation

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize
    AvgLatency=round(avg(DurationMs), 2),
    P50=round(percentile(DurationMs, 50), 2),
    P90=round(percentile(DurationMs, 90), 2),
    P99=round(percentile(DurationMs, 99), 2),
    MaxLatency=max(DurationMs),
    Count=count()
    by OperationName
| order by AvgLatency desc
| take 20
```

### Slow queries (>100ms)

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where DurationMs > 100
| project TimeGenerated, OperationName, DatabaseName, CollectionName, DurationMs, RequestCharge, ErrorCode
| order by DurationMs desc
| take 50
```

### Latency trend over time

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize
    AvgLatency=round(avg(DurationMs), 2),
    P99Latency=round(percentile(DurationMs, 99), 2),
    Count=count()
    by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

## RU Consumption Analysis

### Top RU-consuming collections

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize
    TotalRU=round(sum(RequestCharge), 2),
    AvgRUPerOp=round(avg(RequestCharge), 2),
    MaxRUPerOp=round(max(RequestCharge), 2),
    Count=count()
    by DatabaseName, CollectionName
| order by TotalRU desc
| take 20
```

### Most expensive individual operations

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where RequestCharge > 100
| project TimeGenerated, OperationName, DatabaseName, CollectionName, RequestCharge, DurationMs
| order by RequestCharge desc
| take 30
```

### RU consumption trend by database

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize TotalRU=round(sum(RequestCharge), 2) by bin(TimeGenerated, 1h), DatabaseName
| order by TimeGenerated asc
```

## Error Analysis

### Error code distribution over time

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ErrorCode != 0 and ErrorCode != 200
| summarize count() by ErrorCode, bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

### Failed operations detail

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ErrorCode != 0 and ErrorCode != 200
| summarize count(), avg(DurationMs), sum(RequestCharge) by OperationName, ErrorCode, DatabaseName, CollectionName
| order by count_ desc
| take 30
```

## Request Volume Analysis

### Request volume by operation type

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize Count=count(), TotalRU=round(sum(RequestCharge), 2) by OperationName
| order by Count desc
| take 20
```

### Request volume trend (detects burst patterns)

```kql
CDBMongoRequests
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize Count=count() by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

## Metric Queries

### Fine-grained NormalizedRU around a spike

Use `amgmcp_query_resource_metric` with `metricName: NormalizedRUConsumption`, `aggregation: Maximum`, `interval: PT1H` and a 2-day window around the spike.

### Provisioned throughput changes

Use `amgmcp_query_resource_metric` with `metricName: ProvisionedThroughput`, `aggregation: Maximum`, `interval: PT1H` to detect autoscale step changes.

### Availability check around incidents

Use `amgmcp_query_resource_metric` with `metricName: ServiceAvailability`, `aggregation: Average`, `interval: PT1H` around availability dip events.
