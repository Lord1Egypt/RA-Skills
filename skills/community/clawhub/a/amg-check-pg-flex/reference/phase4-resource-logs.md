# Phase 4: Resource Logs for Abnormal Servers

Query PostgreSQL resource logs using `amgmcp_query_resource_log` with the server's ARM resource ID.

**IMPORTANT**: Always include tight time filters. Never use `union *` without a time filter. Keep the range to 1-2 days.

Replace `<START>` and `<END>` with ISO 8601 UTC timestamps (e.g., `2026-04-09T00:00:00Z`).

---

## Query 1: Error Level Distribution

Hourly count by severity — reveals crash events (FATAL/PANIC) and sustained error storms.

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where errorLevel_s in ("ERROR", "WARNING", "FATAL", "PANIC")
| summarize count() by errorLevel_s, bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

## Query 2: Top Error Messages

Identifies the dominant error pattern (e.g., write contention, provisioning retries, missing functions).

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where errorLevel_s == "ERROR"
| extend MsgTrunc = substring(Message, 30, 150)
| summarize count() by MsgTrunc
| order by count_ desc
| take 20
```

## Query 3: Warning Messages (Crash Indicators)

Look for `terminating connection because of crash` — indicates a backend crash forced all connections to disconnect.

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where errorLevel_s == "WARNING"
| extend MsgTrunc = substring(Message, 30, 150)
| summarize count() by MsgTrunc
| order by count_ desc
| take 20
```

## Query 4: Log Volume Trend

5-minute buckets — a sudden 3-5x increase in log volume indicates a connection storm or crash event.

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| summarize count() by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

## Query 5: Session Duration Analysis

Detects timeout patterns. Sessions clustering at ~30s indicate Grafana query timeouts (30-second timeout is the default).

```kql
AzureDiagnostics
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where Category == "PostgreSQLLogs"
| where Message has "disconnection"
| extend SessionSec = todouble(extract("session time: 0:00:([0-9]+\\.[0-9]+)", 1, Message))
| where SessionSec > 0
| summarize
    Total=count(),
    FastSessions=countif(SessionSec < 1),
    TimeoutSessions=countif(SessionSec >= 29)
    by bin(TimeGenerated, 5m)
| extend TimeoutPct=round(100.0*TimeoutSessions/Total, 1)
| order by TimeGenerated asc
```

---

## What to Report

For each abnormal server:
- **Error/Warning summary**: top error messages, crash indicators (FATAL/PANIC counts), log volume spikes
- **Connection patterns**: session duration distribution, timeout ratio (`TimeoutPct`), connection churn
- **Provisioning activity**: `already exists` errors indicate RP Worker retries (low severity, but flag if frequent)
