---
name: amg-check-storage-account
description: Run only when the user explicitly asks for a fleet-wide Azure Storage Account health check — pulse check for availability, latency, transactions, and error rates across all accounts, then deep-dives into the top 7 most interesting accounts with metrics (E2E latency, server latency, capacity, ingress/egress) and resource logs. Tracks known issues across sessions via persistent report. On first run, auto-discovers datasource UID and prompts for subscription ID.
argument-hint: "[time-range, e.g. 7d, 1d, 3d] [subscription-id]"
disable-model-invocation: true
effort: max
allowed-tools: mcp__amg__amgmcp_pulse_check mcp__amg__amgmcp_query_resource_graph mcp__amg__amgmcp_query_resource_metric mcp__amg__amgmcp_query_resource_metric_definition mcp__amg__amgmcp_query_resource_log mcp__amg__amgmcp_datasource_list mcp__amg__amgmcp_query_activity_log Bash(node *) Glob Read Write Edit
---

<!-- Auto-generated for OpenClaw by pack-openclaw. Notes for OpenClaw users:
     - Claude Code dynamic expressions (!`...`) in this file are NOT evaluated by OpenClaw
       and appear as literal text. Run them manually at the start of the workflow.
     - Invoke this skill only via slash command (e.g. /amg-check-storage-account). Auto-invocation is
       disabled on Claude Code but not on OpenClaw. -->

## OpenClaw Setup (one-time)

This skill calls MCP tools prefixed with `mcp__amg__*`, so OpenClaw must have an MCP server registered under the exact name **`amg`**. Run this once per workspace before invoking the skill:

```bash
openclaw mcp set amg '{"url":"https://<your-grafana-instance>/api/azure-mcp","transport":"streamable-http","headers":{"Authorization":"Bearer <your-token>"}}'
```

Replace `<your-grafana-instance>` with your Azure Managed Grafana endpoint and `<your-token>` with a valid Grafana service-account token (starts with `glsa_`). The server name **must** be `amg` — the skill's `allowed-tools` reference `mcp__amg__*` and will not find tools under any other name.

Verify the server is registered:

```bash
openclaw mcp list
```

> Official skill source: https://github.com/Azure/amg-skills

## Runtime Context
- Current UTC time: !`date -u +%Y-%m-%dT%H:%M:%SZ`
- Config: !`cat memory/amg-check-storage-account/config.md 2>/dev/null || echo "NOT_CONFIGURED"`
- Prior report: !`[ -f memory/amg-check-storage-account/report.md ] && echo "exists ($(grep -c '^### SA-' memory/amg-check-storage-account/report.md) bugs documented)" || echo "not found"`
- Arguments: time-range=$0, subscription-override=$1

> **Known Issues**: Before presenting findings, cross-reference results against `memory/amg-check-storage-account/report.md`.

# Azure Storage Account Health Check

Analyze Azure Storage Account health using a **two-phase approach**: a single `amgmcp_pulse_check` call for fleet-wide summary, followed by targeted deep dives into the **top 7 most interesting accounts** only.

## Critical Constraints

- **Do NOT use subagents (Agent tool) for MCP queries.** Subagents do not have access to MCP tools. All MCP tool calls must be made directly from the main conversation context.
- **Deep dive limit: at most 7 accounts.** Select the most interesting accounts from pulse check results. Do not deep-dive the entire fleet.
- **Time format**: ISO 8601 UTC with explicit `from`/`to` — NEVER use `timespan` (it causes errors).
- **UsedCapacity** only supports interval `PT1H` — do NOT use `PT6H` or `P1D` for this metric.
- **Parallelism cap**: 30 concurrent MCP calls per batch. Reduce to 4-5 if rate-limited.

## Prerequisites

- An AMG-MCP server must be connected (the `allowed-tools` frontmatter references the MCP server name — update it if your server has a different name)
- The MCP server's Grafana service account token environment variable must be set

## Configuration

**If Config shows `NOT_CONFIGURED`**: Run [First-Run Setup](#first-run-setup) at the bottom of this file, then return here.

**If Config is populated**: Extract the datasource UID and subscription ID(s) from the pre-loaded Runtime Context above and use them for all queries. Use `$1` as the subscription override if provided.

- **Datasource UID**: from `## Azure Monitor Datasource` > `UID`
- **Subscription ID(s)**: from `## Subscriptions` (or `$1` if provided)
- **Resource Type**: `microsoft.storage/storageaccounts` (lowercase)
- **ARM ID template**: `/subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.Storage/storageAccounts/{name}`

## Time Range

Default is 7 days (`pastDays: 7`) for pulse check and deep-dive metrics, 24 hours for resource logs. If the user specifies a different range via `$ARGUMENTS[0]` (e.g., `/amg-check-storage-account 3d`), adjust accordingly. For resource log queries, keep the range narrow (1-2 days) to avoid timeouts.

---

## Workflow

### Phase 1: Validate Datasource & Discover Accounts

**Step 1a: Validate Datasource**

Call `amgmcp_datasource_list` with no parameters.

Search the results for a datasource with `type` equal to `grafana-azure-monitor-datasource`. Extract its `uid`.

- If it matches the configured UID, proceed.
- If it differs, update `memory/amg-check-storage-account/config.md`, warn the user, and use the new UID.
- If no Azure Monitor datasource is found, abort with a clear error.

**Step 1b: Discover All Storage Accounts**

Call `amgmcp_query_resource_graph` once using the configured datasource UID and subscription ID(s):

```
azureMonitorDatasourceUid: {DATASOURCE_UID}
query: |
  resources
  | where type == 'microsoft.storage/storageaccounts'
  | where subscriptionId in ({SUBSCRIPTION_IDS})
  | project name, resourceGroup, location, subscriptionId, properties.provisioningState
  | order by location asc, name asc
```

Replace `{SUBSCRIPTION_IDS}` with the configured subscription IDs formatted as comma-separated quoted strings (e.g., `'sub-id-1', 'sub-id-2'`).

**Constructing the ARM resource ID**: Use subscriptionId from each row:

```
/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Storage/storageAccounts/{name}
```

**Region summary**: Derive from the account list by counting accounts per unique `location` value.

Note any accounts not in "Succeeded" provisioning state — flag them immediately.

If zero accounts are found, report "No Storage Accounts found" and stop.

### Phase 2: Fleet-Wide Pulse Check

Call `amgmcp_pulse_check` once to get a summary across all storage accounts:

```
azureMonitorDatasourceUid: {DATASOURCE_UID}
pastDays: 7
scenarios: storage_summary
```

If `$1` provides a subscription ID, add `subscriptionId` to scope the scan. Otherwise, if the config has a single subscription, pass it.

**After the pulse check, verify:**
1. The number of scanned resources is close to the Phase 1 account count.
2. The scenario shows `status: "completed"`.
3. If errors occurred, retry once. If still failing, note the failure in the report.

**Cross-reference pulse check results with Phase 1 inventory** to enrich each account with its resource group and region from the Resource Graph data.

### Phase 3: Top 7 Deep Dive

From the pulse check results, **select at most 7 accounts** for detailed investigation. Prioritize accounts with the most interesting signals:

1. **Availability drops** — any account below 99.9% availability
2. **Highest error transaction counts** — accounts with the most non-Success responses
3. **Highest latency** — accounts with the highest average E2E latency
4. **Unusual capacity or traffic patterns** — sudden capacity jumps, abnormally high ingress/egress
5. **Diversity** — prefer selecting accounts from different regions to maximize coverage

If the pulse check shows fewer than 7 accounts with notable signals, only deep-dive those that have something worth investigating. Do not pad to 7.

If the pulse check shows the entire fleet is healthy with no notable signals, skip Phase 3 entirely and report the fleet as healthy.

#### Step 3a: Deep Metrics

For each selected account, query these metrics **in parallel** using `amgmcp_query_resource_metric`. Compute `from` (matching `pastDays` from Phase 2) and `to` (now) in ISO 8601 UTC.

| Metric Name | Aggregation | Interval | Purpose |
|-------------|-------------|----------|---------|
| `Availability` | `Average` | PT6H | Availability trend |
| `SuccessE2ELatency` | `Average` | PT6H | Client-perceived latency |
| `SuccessE2ELatency` | `Maximum` | PT6H | Tail latency spikes |
| `SuccessServerLatency` | `Average` | PT6H | Storage backend latency |
| `Transactions` | `Total` | PT6H | Total volume (no filter) |
| `Transactions` (errors) | `Total` | PT6H | Error count (`filter: ResponseType ne 'Success'`) |
| `UsedCapacity` | `Average` | **PT1H** | Current capacity (use last data point) |
| `Ingress` | `Total` | PT6H | Data volume in |
| `Egress` | `Total` | PT6H | Data volume out |

All 7 accounts can be queried in parallel (7 accounts x 9 metrics = 63 calls, within the 30-call batch cap when split into 3 batches).

**Correlation analysis** — when analyzing metrics together:
- **High E2E latency + low server latency** = network issue, not storage
- **High E2E latency + high server latency** = storage backend issue (throttling, overloaded partition)
- **High error transactions + normal latency** = client errors (auth, not-found), not performance
- **High error transactions + high latency** = throttling (503) or backend degradation
- **Availability drop + high error transactions** = sustained storage issue
- **High ingress + high latency** = large writes saturating bandwidth
- **Dormant (all empty)** = no traffic, investigate if expected or orphaned

#### Step 3b: Resource Logs

For each selected account, query Storage resource logs using `amgmcp_query_resource_log`. Keep time range to 1-2 days.

**Log Query 1: Failed requests by status code**
```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where StatusCode >= 400
| summarize count() by StatusCode, StatusText, bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

**Log Query 2: High latency operations**
```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where ServerLatencyMs > 100
| summarize count(), avg(ServerLatencyMs), max(ServerLatencyMs) by OperationName
| order by count_ desc
| take 20
```

**Log Query 3: Error distribution by operation**
```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where StatusCode >= 400
| summarize count() by OperationName, StatusCode, StatusText
| order by count_ desc
| take 30
```

**Log Query 4: Request volume trend**
```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize
    TotalRequests=count(),
    FailedRequests=countif(StatusCode >= 400),
    ThrottledRequests=countif(StatusCode == 503),
    AvgLatencyMs=round(avg(ServerLatencyMs), 2)
    by bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

**Log Query 5: Authentication failures**
```kql
StorageBlobLogs
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where StatusCode == 403
| summarize count() by AuthenticationType, CallerIpAddress, UserAgentHeader
| order by count_ desc
| take 20
```

> **Note**: If `StorageBlobLogs` returns no data, diagnostic settings may not be configured. Try `StorageTableLogs` or `StorageQueueLogs`. If none return data, note it and skip logs for that account.

---

## Classification

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | Availability avg < 99.0% |
| **WARNING** | Availability avg < 99.9%, OR SuccessE2ELatency avg > 50ms, OR sustained latency > 20ms for 6+ hours, OR sustained error transactions across multiple time windows |
| **DORMANT** | All metrics return empty timeSeries (no traffic in scan period) |
| **HEALTHY** | All metrics within normal ranges |

---

## Analysis Guidance

For known patterns, deep-dive queries, and correlation techniques, see [reference/analysis-patterns.md](${CLAUDE_SKILL_DIR}/reference/analysis-patterns.md).

For optional deep-dive queries, see [reference/deep-dive-queries.md](${CLAUDE_SKILL_DIR}/reference/deep-dive-queries.md).

---

## Output Format

Present a summary report with these sections:

### 1. Fleet Inventory

Account count by region and subscription. Flag any accounts not in "Succeeded" provisioning state.

### 2. Pulse Check Summary

Fleet-wide summary from the `storage_summary` pulse check:
- Total accounts scanned and scan status
- Key fleet-wide metrics (availability, latency, error counts, capacity)
- Breakdown by health status (healthy / warning / critical / dormant)
- Which accounts were selected for deep dive and why each was chosen

### 3. Deep Dive Findings (Top 7)

For each selected account:
- **Metric timeline**: Availability, E2E latency, server latency, transactions over the scan window
- **Anomaly characterization**: spike vs sustained, onset time, duration, recovery
- **Correlation analysis**: which metrics moved together
- **Error rate**: error transactions / total transactions percentage

### 4. Resource Log Findings

For each deep-dived account:
- **Error summary**: top error status codes, affected operations, throttling timeline
- **Latency analysis**: slow operations by type, server vs E2E latency comparison
- **Authentication failures**: if any, source IPs and user agents

### 5. Known Issue Cross-Reference

Compare findings against `memory/amg-check-storage-account/report.md`. For each known bug, state: still active / improving / worsening / resolved.

### 6. Action Items

Prioritized list:
- **Critical**: accounts with availability < 99.0%
- **High**: accounts with sustained error transactions, high latency, or throttling
- **Medium**: accounts with elevated latency, intermittent errors, or capacity concerns
- **Low**: dormant accounts (investigate if orphaned), informational items

---

## Update Known Issues

After presenting findings, update `memory/amg-check-storage-account/report.md`:

1. **Read the current file** (create if it doesn't exist).
2. **Update status** of existing bugs based on today's telemetry.
3. **Add new bugs** with: severity, account name, region, metric evidence, log evidence, root cause, recommended action.
4. **Update the "Updated" date** in the header.

Only add genuine issues: sustained availability drops, persistent throttling, high error rates, or latency degradation.

---

## Error Handling

See **[${CLAUDE_SKILL_DIR}/reference/error-handling.md](${CLAUDE_SKILL_DIR}/reference/error-handling.md)** for the full recovery table.

---

## Reference

- Storage resource type: `Microsoft.Storage/storageAccounts`
- ARM ID template: `/subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.Storage/storageAccounts/{name}`
- Resource log tables: `StorageBlobLogs` (primary), `StorageTableLogs`, `StorageQueueLogs` (alternatives)
- Key status codes: `503` (throttling), `403` (auth failure), `404` (not found), `409` (conflict)
- UsedCapacity: `PT1H` interval only
- Known issues: `memory/amg-check-storage-account/report.md`
- Configuration: `memory/amg-check-storage-account/config.md`

---

## First-Run Setup

Run only when Config shows `NOT_CONFIGURED`. After completing, return to the [Workflow](#workflow) above.

**1. Discover Datasource UID**: Call `amgmcp_datasource_list`. Filter `type == "grafana-azure-monitor-datasource"`. Prefer `uid == "azure-monitor-oob"` if multiple match. Abort if zero match.

**2. Discover Subscription ID(s)**: Run this Resource Graph query to list all subscriptions with storage accounts, then present the results as a table and ask the user which subscription(s) to use:
```
resources
| where type == 'microsoft.storage/storageaccounts'
| join kind=inner (
    resourcecontainers
    | where type == 'microsoft.resources/subscriptions'
    | project subscriptionId, subscriptionName=name
) on subscriptionId
| summarize StorageAccounts=count() by subscriptionId, subscriptionName
| order by StorageAccounts desc
```

Present the results as a table with columns: **Subscription Name**, **Subscription ID**, **Storage Accounts**. Then ask the user: *"Which subscription ID(s) should I configure for this health check?"*

**3. Write config**: Write `memory/amg-check-storage-account/config.md`:
```markdown
# amg-check-storage-account Configuration

User-specific values for the Storage Account health check skill.
This file is auto-generated on first run and can be edited manually.

## Azure Monitor Datasource
- **UID**: {discovered_uid}
- **Name**: {discovered_name}

## Subscriptions
- {subscription_id_1}
- {subscription_id_2}
```

**4. Confirm**: Show the resolved config and ask for confirmation before proceeding.
