# Deep-Dive Queries

Run these only if the user asks for more detail or if initial results reveal issues worth investigating.

## Connection Analysis

### Connection rate per host (before vs during spike)

Replace `<START_BEFORE>`, `<END_BEFORE>`, `<START_DURING>`, `<END_DURING>` with appropriate timestamps.

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START_DURING>) .. datetime(<END_DURING>))
| where Category == "PostgreSQLLogs"
| where Message has "connection received"
| extend Host = extract("host=([^ ]+)", 1, Message)
| where Host != "127.0.0.1"
| summarize ConnCount=count() by bin(TimeGenerated, 1m), Host
| summarize AvgConnsPerHost=round(avg(ConnCount), 2), MaxConnsPerHost=max(ConnCount), DistinctHosts=dcount(Host) by bin(TimeGenerated, 1m)
| order by TimeGenerated asc
```

### Connection rate per database

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where Message has "connection authorized"
| extend DB = extract("database=(\\S+)", 1, Message)
| summarize count() by DB
| order by count_ desc
| take 30
```

### Session duration percentiles

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where Message has "disconnection"
| extend SessionSec = todouble(extract("session time: 0:00:([0-9]+\\.[0-9]+)", 1, Message))
| where SessionSec > 0
| summarize
    AvgSession=round(avg(SessionSec), 2),
    P50=round(percentile(SessionSec, 50), 2),
    P90=round(percentile(SessionSec, 90), 2),
    P99=round(percentile(SessionSec, 99), 2),
    MaxSession=max(SessionSec),
    Total=count()
```

### Databases with most timeouts

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where Message has "disconnection"
| extend SessionSec = todouble(extract("session time: 0:00:([0-9]+\\.[0-9]+)", 1, Message))
| extend DB = extract("database=(\\S+)", 1, Message)
| where SessionSec >= 29.0
| summarize TimeoutCount=count() by DB
| order by TimeoutCount desc
| take 20
```

### New vs existing databases during spike

Compares the set of databases connecting before vs during the spike.

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START_BEFORE>) .. datetime(<END_BEFORE>))
| where Category == "PostgreSQLLogs"
| where Message has "connection authorized"
| extend DB = extract("database=(\\S+)", 1, Message)
| summarize PreCount=count() by DB
| join kind=fullouter (
    AzureDiagnostics
    | where TimeGenerated between (datetime(<START_DURING>) .. datetime(<END_DURING>))
    | where Category == "PostgreSQLLogs"
    | where Message has "connection authorized"
    | extend DB = extract("database=(\\S+)", 1, Message)
    | summarize PostCount=count() by DB
) on DB
| extend Ratio = round(todouble(PostCount) / todouble(PreCount), 2)
| order by Ratio desc
| take 20
```

## Error Analysis

### Cancel request flood detection

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where Message has "cancel request did not match"
| summarize count() by bin(TimeGenerated, 1m)
| order by TimeGenerated asc
```

### Crash-related messages

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where Message has_any ("crash", "terminated", "server process", "postmaster", "aborting", "database system")
| project TimeGenerated, errorLevel_s, Message
| order by TimeGenerated asc
| take 50
```

### Provisioning retry activity

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where errorLevel_s == "ERROR"
| where Message has "already exists"
| extend Entity = extract("\"([^\"]+)\"", 1, Message)
| summarize count() by Entity
| order by count_ desc
| take 20
```

### Duplicate key / write contention

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where errorLevel_s == "ERROR"
| where Message has "duplicate key"
| extend Table = extract("unique constraint \"([^\"]+)\"", 1, Message)
| summarize count() by Table
| order by count_ desc
```

## Checkpoint and Vacuum Analysis

### Checkpoint frequency and duration

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where Message has "checkpoint"
| where Message has "complete" or Message has "starting"
| project TimeGenerated, Message
| order by TimeGenerated asc
```

### Autovacuum activity

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where Message has "autovacuum"
| project TimeGenerated, Message
| order by TimeGenerated asc
| take 30
```

## Metric Queries

### Fine-grained CPU around a spike

Use `amgmcp_query_resource_metric` with `interval: PT5M` and a 4-6 hour window around the spike.

### Active connections with fine granularity

Use `amgmcp_query_resource_metric` with `metricName: active_connections`, `interval: PT5M`.

### Database availability check

Use `amgmcp_query_resource_metric` with `metricName: is_db_alive`, `aggregation: Maximum`, `interval: PT5M` around crash/restart events.
