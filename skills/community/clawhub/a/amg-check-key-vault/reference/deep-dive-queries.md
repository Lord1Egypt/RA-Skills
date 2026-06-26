# Deep-Dive Queries

Run these only if the user asks for more detail or if initial results reveal issues worth investigating.

## Error Analysis

### Error requests by status code over time

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where httpStatusCode_d >= 400
| summarize count() by httpStatusCode_d, bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

### Top error operations

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where httpStatusCode_d >= 400
| summarize count() by OperationName, httpStatusCode_d, ResultSignature
| order by count_ desc
| take 30
```

### Throttled requests (429) over time

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where httpStatusCode_d == 429
| summarize count() by OperationName, bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

### Authentication failures detail

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where httpStatusCode_d in (401, 403)
| summarize count() by OperationName, CallerIPAddress, identity_claim_appid_g
| order by count_ desc
| take 20
```

### Not Found (404) requests — orphaned secret references

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where httpStatusCode_d == 404
| summarize count() by OperationName, id_s
| order by count_ desc
| take 20
```

## Latency Analysis

### Latency percentiles by operation

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where DurationMs > 0
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

### Slow operations (>500ms)

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where DurationMs > 500
| project TimeGenerated, OperationName, DurationMs, httpStatusCode_d, CallerIPAddress
| order by DurationMs desc
| take 50
```

### Latency trend over time

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where DurationMs > 0
| summarize
    AvgLatency=round(avg(DurationMs), 2),
    P95Latency=round(percentile(DurationMs, 95), 2),
    MaxLatency=max(DurationMs),
    Count=count()
    by bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

## Traffic Analysis

### Request volume trend

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize
    TotalRequests=count(),
    FailedRequests=countif(httpStatusCode_d >= 400),
    ThrottledRequests=countif(httpStatusCode_d == 429),
    AvgDurationMs=round(avg(DurationMs), 2)
    by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

### Request volume by operation type

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize Count=count(), FailedCount=countif(httpStatusCode_d >= 400) by OperationName
| order by Count desc
| take 20
```

### Top callers by IP

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize Count=count(), FailedCount=countif(httpStatusCode_d >= 400) by CallerIPAddress
| order by Count desc
| take 20
```

### Top calling applications

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize Count=count(), FailedCount=countif(httpStatusCode_d >= 400) by identity_claim_appid_g
| order by Count desc
| take 20
```

## Secret/Key Analysis

### Operations by secret/key type

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| extend ObjectType = case(
    OperationName has "Secret", "Secret",
    OperationName has "Key", "Key",
    OperationName has "Certificate", "Certificate",
    "Other")
| summarize Count=count(), Errors=countif(httpStatusCode_d >= 400) by ObjectType
| order by Count desc
```

### Most accessed secrets/keys

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where isnotempty(id_s)
| summarize Count=count(), Errors=countif(httpStatusCode_d >= 400) by id_s, OperationName
| order by Count desc
| take 20
```

### Failed secret/key accesses

```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where httpStatusCode_d >= 400
| where isnotempty(id_s)
| summarize count() by id_s, OperationName, httpStatusCode_d
| order by count_ desc
| take 20
```

## Metric Queries

### Fine-grained API latency around a spike

Use `amgmcp_query_resource_metric` with `metricName: ServiceApiLatency`, `aggregation: Average`, `interval: PT1H` and a 2-day window around the spike.

### Saturation trend

Use `amgmcp_query_resource_metric` with `metricName: SaturationShoebox`, `aggregation: Average`, `interval: PT1H` to get hourly saturation around high-usage periods.

### Availability check around incidents

Use `amgmcp_query_resource_metric` with `metricName: Availability`, `aggregation: Average`, `interval: PT1H` around availability drop events.
