# Output Format

Present the health check report with the following sections in order.

---

## 1. Fleet Inventory

- Account count total and by region/subscription
- Any accounts not in "Succeeded" provisioning state, with activity log findings
- Autoscale vs manual throughput split
- Provisioned RU/s range across the fleet

## 2. RU/Availability/Latency Scan Results

Table of **all** accounts with peak NormalizedRU, avg latency, and availability over the scan period. Highlight abnormal accounts with the threshold they exceeded.

| Account | Region | Prov. RU/s | Peak NormalizedRU | Avg Latency (ms) | Availability | 429 Count | Status |
|---------|--------|------------|-------------------|-------------------|-------------|-----------|--------|
| acct-name | eastus | 1,600 | 100% | 2.5 | 100% | 307 | CRITICAL |

Include the pulse check `scanSummary` (total scanned, total findings, severity counts).

## 3. Abnormal Account Deep Dive

For each abnormal account (from Phase 4):
- **Metric timeline**: NormalizedRU, latency, availability, request volume over the anomaly window
- **Anomaly characterization**: spike vs sustained, onset time, duration, recovery
- **Correlation analysis**: which metrics moved together (reference Phase 4 patterns)
- **Throughput context**: provisioned RU/s, autoscale status, RU consumption relative to limit

## 4. Resource Log Findings

For each abnormal account (from Phase 5):
- **Throttling summary**: 429 error rate, affected databases/collections, throttling timeline
- **High-latency operations**: top slow operations by RU cost and latency
- **Error distribution**: error codes, affected operations
- **Diagnostic settings status**: note if resource logs are unavailable

## 5. Known Issue Cross-Reference

Read `memory/amg-check-cosmosdb-mongo-ru/report.md`. For each documented bug, state:

| Bug ID | Account | Status | Change |
|--------|---------|--------|--------|
| BUG-COSMO-001 | wus2-db | Active | Still sustained 100% RU |
| BUG-COSMO-003 | eno-db | Resolved | Availability 100% for last 7d |

Status options: **Still Active** / **Improving** / **Worsening** / **Resolved**

## 6. Action Items

Prioritized list grouped by severity:

- **Critical**: Accounts with sustained 100% RU or availability < 99.9%
- **High**: Accounts with frequent RU spikes >85%, replication lag >1s
- **Medium**: Accounts with elevated latency, sustained moderate RU consumption, throttling
- **Low**: Informational items (autoscale candidates, capacity planning, diagnostic settings)

Each item should include: account name, specific metric or log evidence, and recommended action.

## 7. Resource Inventory (Appendix)

Complete table of **all** discovered Cosmos DB for MongoDB (RU) accounts. Group by region (alphabetical), then name (alphabetical).

| Name | Resource ID | Region | Subscription | State |
|------|-------------|--------|--------------|-------|
| account-name | /subscriptions/.../databaseAccounts/account-name | eastus | sub-id | Succeeded |

This appendix is the authoritative fleet reference and must be regenerated on every run.
