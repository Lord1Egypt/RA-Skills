# Output Format

Present the health check report with the following sections in order.

---

## 1. Fleet Inventory

- Server count total and by region
- SKU tier breakdown (Burstable / General Purpose / Memory Optimized)
- Any servers not in "Ready" state, with activity log findings

## 2. CPU/Memory Scan Results

Table of **all** servers with peak CPU and memory over the scan period. Highlight abnormal servers.

| Server | Region | Peak CPU | Peak Memory | Status |
|--------|--------|----------|-------------|--------|
| server-name | eastus | 94% ⚠️ | 45% | WARNING |

Include the pulse check `scanSummary` (total scanned, total findings, severity counts).

## 3. Abnormal Server Deep Dive

For each abnormal server (from Phase 3):
- **Metric timeline**: CPU, memory, connections, IOPS, network I/O over the anomaly window
- **Anomaly characterization**: spike vs sustained, onset time, duration, recovery
- **Correlation analysis**: which metrics moved together (reference Phase 3 patterns)
- **Post-anomaly state**: did metrics return to baseline or settle at a new level

## 4. Resource Log Findings

For each abnormal server (from Phase 4):
- **Error/Warning summary**: top messages, crash indicators (FATAL/PANIC counts by hour), log volume anomalies
- **Connection patterns**: session duration distribution, timeout ratio, connection churn rates
- **Provisioning activity**: `already exists` errors indicate RP Worker retries

## 5. Known Issue Cross-Reference

Read `memory/amg-check-pg-flex/report.md`. For each documented bug, state:

| Bug ID | Server | Status | Change |
|--------|--------|--------|--------|
| BUG-001 | fleet-wide | Active | Count up 12% vs prior run |
| BUG-003 | wus-pgsql240828170101 | Resolved | 0 FATAL errors in last 7d |

Status options: **Still Active** / **Improving** / **Worsening** / **Resolved**

## 6. Action Items

Prioritized list grouped by severity:

- **Critical**: Servers currently down or sustained >90% CPU/memory
- **High**: Crash-restart cycles, sustained high utilization, connection storms
- **Medium**: Elevated error rates, timeout patterns, capacity concerns
- **Low**: Monitoring noise (missing functions, parameter mismatches, provisioning retries)

Each item should include: server name, the specific metric or log evidence, and recommended action.

## 7. Resource Inventory (Appendix)

Complete table of **all** discovered servers. Group by region (alphabetical), then name (alphabetical).

| Name | Resource ID | Region | SKU | State |
|------|-------------|--------|-----|-------|
| server-name | /subscriptions/.../flexibleServers/server-name | eastus | Standard_E8s_v3 | Ready |

Construct each Resource ID using:
`/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.DBforPostgreSQL/flexibleServers/{name}`

This appendix is the authoritative fleet reference and must be regenerated on every run.
