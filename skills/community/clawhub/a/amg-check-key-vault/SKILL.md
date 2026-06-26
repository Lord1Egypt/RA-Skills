---
name: amg-check-key-vault
description: Run only when the user explicitly asks for a fleet-wide Azure Key Vault health check — pulse check for availability, API latency, throttling (429s), auth failures (401/403), and vault saturation across all vaults, then deep-dives into the top 7 most interesting vaults with metrics and resource logs. Tracks known issues across sessions via persistent report. On first run, auto-discovers datasource UID and prompts for subscription ID.
argument-hint: "[time-range, e.g. 7d, 1d, 3d] [subscription-id]"
disable-model-invocation: true
effort: max
allowed-tools: mcp__amg__amgmcp_pulse_check mcp__amg__amgmcp_query_resource_graph mcp__amg__amgmcp_query_resource_metric mcp__amg__amgmcp_query_resource_metric_definition mcp__amg__amgmcp_query_resource_log mcp__amg__amgmcp_datasource_list mcp__amg__amgmcp_query_activity_log Bash(node *) Glob Read Write Edit
---

<!-- Auto-generated for OpenClaw by pack-openclaw. Notes for OpenClaw users:
     - Claude Code dynamic expressions (!`...`) in this file are NOT evaluated by OpenClaw
       and appear as literal text. Run them manually at the start of the workflow.
     - Invoke this skill only via slash command (e.g. /amg-check-key-vault). Auto-invocation is
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
- Config: !`cat memory/amg-check-key-vault/config.md 2>/dev/null || echo "NOT_CONFIGURED"`
- Prior report: !`[ -f memory/amg-check-key-vault/report.md ] && echo "exists ($(grep -c '^### KV-' memory/amg-check-key-vault/report.md) bugs documented)" || echo "not found"`
- Arguments: time-range=$0, subscription-override=$1

> **Known Issues**: Before presenting findings, cross-reference results against `memory/amg-check-key-vault/report.md`.

# Azure Key Vault Health Check

Analyze Azure Key Vault health using a **two-phase approach**: a single `amgmcp_pulse_check` call for fleet-wide summary, followed by targeted deep dives into the **top 7 most interesting vaults** only.

## Critical Constraints

- **Do NOT use subagents (Agent tool) for MCP queries.** Subagents do not have access to MCP tools. All MCP tool calls must be made directly from the main conversation context.
- **Deep dive limit: at most 7 vaults.** Select the most interesting vaults from pulse check results. Do not deep-dive the entire fleet.
- **Time format**: ISO 8601 UTC with explicit `from`/`to` — NEVER use `timespan` (it causes errors).
- **Parallelism cap**: 30 concurrent MCP calls per batch. Reduce to 4-5 if rate-limited.

## Prerequisites

- An AMG-MCP server must be connected (the `allowed-tools` frontmatter references the MCP server name — update it if your server has a different name)
- The MCP server's Grafana service account token environment variable must be set

## Configuration

**If Config shows `NOT_CONFIGURED`**: Run [First-Run Setup](#first-run-setup) at the bottom of this file, then return here.

**If Config is populated**: Extract the datasource UID and subscription ID(s) from the pre-loaded Runtime Context above and use them for all queries. Use `$1` as the subscription override if provided.

- **Datasource UID**: from `## Azure Monitor Datasource` > `UID`
- **Subscription ID(s)**: from `## Subscriptions` (or `$1` if provided)
- **Resource Type**: `microsoft.keyvault/vaults` (lowercase)
- **ARM ID template**: `/subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.KeyVault/vaults/{name}`

## Time Range

Default is 7 days (`pastDays: 7`) for pulse check and deep-dive metrics, 24 hours for resource logs. If the user specifies a different range via `$ARGUMENTS[0]` (e.g., `/amg-check-key-vault 3d`), adjust accordingly. For resource log queries, keep the range narrow (1-2 days) to avoid timeouts.

---

## Workflow

### Phase 1: Validate Datasource & Discover Vaults

**Step 1a: Validate Datasource**

Call `amgmcp_datasource_list` with no parameters.

Search the results for a datasource with `type` equal to `grafana-azure-monitor-datasource`. Extract its `uid`.

- If it matches the configured UID, proceed.
- If it differs, update `memory/amg-check-key-vault/config.md`, warn the user, and use the new UID.
- If no Azure Monitor datasource is found, abort with a clear error.

**Step 1b: Discover All Key Vaults**

Call `amgmcp_query_resource_graph` once using the configured datasource UID and subscription ID(s):

```
azureMonitorDatasourceUid: {DATASOURCE_UID}
query: |
  resources
  | where type == 'microsoft.keyvault/vaults'
  | where subscriptionId in ({SUBSCRIPTION_IDS})
  | project name, resourceGroup, location, subscriptionId, sku=properties.sku.name, enableSoftDelete=properties.enableSoftDelete, enablePurgeProtection=properties.enablePurgeProtection, provisioningState=properties.provisioningState
  | order by location asc, name asc
```

Replace `{SUBSCRIPTION_IDS}` with the configured subscription IDs formatted as comma-separated quoted strings (e.g., `'sub-id-1', 'sub-id-2'`).

**Constructing the ARM resource ID**: Use subscriptionId from each row:

```
/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.KeyVault/vaults/{name}
```

**Region summary**: Derive from the vault list by counting vaults per unique `location` value.

**SKU summary**: Count vaults by `sku` (standard vs premium).

Note any vaults not in "Succeeded" provisioning state — flag them immediately.

If zero vaults are found, report "No Key Vaults found" and stop.

### Phase 2: Fleet-Wide Pulse Check

Call `amgmcp_pulse_check` once to get a summary across all key vaults:

```
azureMonitorDatasourceUid: {DATASOURCE_UID}
pastDays: 7
scenarios: keyvault_summary
```

If `$1` provides a subscription ID, add `subscriptionId` to scope the scan. Otherwise, if the config has a single subscription, pass it.

**After the pulse check, verify:**
1. The number of scanned resources is close to the Phase 1 vault count.
2. The scenario shows `status: "completed"`.
3. If errors occurred, retry once. If still failing, note the failure in the report.

**Cross-reference pulse check results with Phase 1 inventory** to enrich each vault with its resource group, region, and SKU from the Resource Graph data.

### Phase 3: Top 7 Deep Dive

From the pulse check results, **select at most 7 vaults** for detailed investigation. Prioritize vaults with the most interesting signals:

1. **Availability drops** — any vault below 99.9% availability
2. **Highest error counts** — vaults with the most non-Success responses (especially 401, 403, 429)
3. **Highest latency** — vaults with the highest average API latency
4. **Throttling (429)** — vaults showing rate-limiting responses
5. **Diversity** — prefer selecting vaults from different regions to maximize coverage

If the pulse check shows fewer than 7 vaults with notable signals, only deep-dive those that have something worth investigating. Do not pad to 7.

If the pulse check shows the entire fleet is healthy with no notable signals, skip Phase 3 entirely and report the fleet as healthy.

#### Step 3a: Deep Metrics

For each selected vault, query these metrics **in parallel** using `amgmcp_query_resource_metric`. Compute `from` (matching `pastDays` from Phase 2) and `to` (now) in ISO 8601 UTC.

| Metric Name | Aggregation | Interval | Purpose |
|-------------|-------------|----------|---------|
| `Availability` | `Average` | PT6H | Availability trend |
| `ServiceApiLatency` | `Average` | PT6H | Average API latency |
| `ServiceApiLatency` | `Maximum` | PT6H | Tail latency spikes |
| `ServiceApiHit` | `Total` | PT6H | Total API call volume |
| `ServiceApiResult` (errors) | `Total` | PT6H | Error count (`filter: StatusCode ne '200'`) |
| `ServiceApiResult` (throttled) | `Total` | PT6H | Throttling count (`filter: StatusCode eq '429'`) |
| `ServiceApiResult` (auth failures) | `Total` | PT6H | Auth errors (`filter: StatusCode eq '401' or StatusCode eq '403'`) |
| `SaturationShoebox` | `Average` | PT6H | Vault capacity saturation |

All 7 vaults can be queried in parallel (7 vaults x 8 metrics = 56 calls, within the 30-call batch cap when split into 2 batches).

**Correlation analysis** — when analyzing metrics together:
- **High latency + high API hits** = vault under load, possibly approaching throttle limits
- **High latency + throttling (429)** = vault is being rate-limited, clients retrying
- **High errors + normal latency** = client-side issues (bad auth, missing secrets)
- **High 401/403 + specific time window** = key rotation event or misconfigured client
- **Availability drop + high errors** = sustained vault issue
- **High saturation + high API hits** = vault approaching transaction limits
- **Dormant (all empty)** = no traffic, investigate if orphaned

#### Step 3b: Resource Logs

For each selected vault, query Key Vault resource logs using `amgmcp_query_resource_log`. Keep time range to 1-2 days.

**Log Query 1: Failed requests by status code**
```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where httpStatusCode_d >= 400
| summarize count() by httpStatusCode_d, OperationName, bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

**Log Query 2: Top error operations**
```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where httpStatusCode_d >= 400
| summarize count() by OperationName, httpStatusCode_d, ResultSignature
| order by count_ desc
| take 30
```

**Log Query 3: Throttled requests (429) over time**
```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where httpStatusCode_d == 429
| summarize count() by OperationName, bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

**Log Query 4: Request volume trend**
```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| summarize
    TotalRequests=count(),
    FailedRequests=countif(httpStatusCode_d >= 400),
    ThrottledRequests=countif(httpStatusCode_d == 429),
    AvgDurationMs=round(avg(DurationMs), 2)
    by bin(TimeGenerated, 1h)
| order by TimeGenerated asc
```

**Log Query 5: Authentication failures**
```kql
AzureDiagnostics
| where ResourceType == "VAULTS"
| where TimeGenerated between (datetime(<START>) .. datetime(<END>))
| where httpStatusCode_d in (401, 403)
| summarize count() by OperationName, CallerIPAddress, identity_claim_appid_g
| order by count_ desc
| take 20
```

> **Note**: If `AzureDiagnostics` with `ResourceType == "VAULTS"` returns no data, diagnostic settings may not be configured. Note it and skip logs for that vault.

---

## Classification

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | Availability avg < 99.0%, OR SaturationShoebox avg > 75% |
| **WARNING** | Availability avg < 99.9%, OR ServiceApiLatency avg > 200ms, OR sustained 429 throttling across multiple time windows, OR sustained 401/403 errors |
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

Vault count by region, subscription, and SKU. Flag any vaults not in "Succeeded" provisioning state. Note soft-delete and purge-protection status.

### 2. Pulse Check Summary

Fleet-wide summary from the `keyvault_summary` pulse check:
- Total vaults scanned and scan status
- Key fleet-wide metrics (availability, latency, API hits, error counts)
- Breakdown by health status (healthy / warning / critical / dormant)
- Which vaults were selected for deep dive and why each was chosen

### 3. Deep Dive Findings (Top 7)

For each selected vault:
- **Metric timeline**: Availability, API latency, API hits, saturation over the scan window
- **Anomaly characterization**: spike vs sustained, onset time, duration, recovery
- **Correlation analysis**: which metrics moved together
- **Error rate**: error results / total API hits percentage

### 4. Resource Log Findings

For each deep-dived vault:
- **Error summary**: top error status codes, affected operations, throttling timeline
- **Latency analysis**: slow operations by type
- **Authentication failures**: if any, source IPs and application IDs

### 5. Known Issue Cross-Reference

Compare findings against `memory/amg-check-key-vault/report.md`. For each known bug, state: still active / improving / worsening / resolved.

### 6. Action Items

Prioritized list:
- **Critical**: vaults with availability < 99.0% or saturation > 75%
- **High**: vaults with sustained throttling (429), high latency, or auth failures
- **Medium**: vaults with elevated latency, intermittent errors, or approaching saturation
- **Low**: dormant vaults (investigate if orphaned), informational items

---

## Update Known Issues

After presenting findings, update `memory/amg-check-key-vault/report.md`:

1. **Read the current file** (create if it doesn't exist).
2. **Update status** of existing bugs based on today's telemetry.
3. **Add new bugs** with: severity, vault name, region, metric evidence, log evidence, root cause, recommended action.
4. **Update the "Updated" date** in the header.

Only add genuine issues: sustained availability drops, persistent throttling, high error rates, or latency degradation.

---

## Error Handling

See **[${CLAUDE_SKILL_DIR}/reference/error-handling.md](${CLAUDE_SKILL_DIR}/reference/error-handling.md)** for the full recovery table.

---

## Reference

- Key Vault resource type: `Microsoft.KeyVault/vaults`
- ARM ID template: `/subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.KeyVault/vaults/{name}`
- Resource log table: `AzureDiagnostics` (with `ResourceType == "VAULTS"`)
- Key status codes: `429` (throttled), `401` (unauthorized), `403` (forbidden), `404` (not found)
- Key metrics: `Availability`, `ServiceApiHit`, `ServiceApiLatency`, `ServiceApiResult`, `SaturationShoebox`
- Known issues: `memory/amg-check-key-vault/report.md`
- Configuration: `memory/amg-check-key-vault/config.md`

---

## First-Run Setup

Run only when Config shows `NOT_CONFIGURED`. After completing, return to the [Workflow](#workflow) above.

**1. Discover Datasource UID**: Call `amgmcp_datasource_list`. Filter `type == "grafana-azure-monitor-datasource"`. Prefer `uid == "azure-monitor-oob"` if multiple match. Abort if zero match.

**2. Discover Subscription ID(s)**: Run this Resource Graph query to list all subscriptions with key vaults, then present the results as a table and ask the user which subscription(s) to use:
```
resources
| where type == 'microsoft.keyvault/vaults'
| join kind=inner (
    resourcecontainers
    | where type == 'microsoft.resources/subscriptions'
    | project subscriptionId, subscriptionName=name
) on subscriptionId
| summarize KeyVaults=count() by subscriptionId, subscriptionName
| order by KeyVaults desc
```

Present the results as a table with columns: **Subscription Name**, **Subscription ID**, **Key Vaults**. Then ask the user: *"Which subscription ID(s) should I configure for this health check?"*

**3. Write config**: Write `memory/amg-check-key-vault/config.md`:
```markdown
# amg-check-key-vault Configuration

User-specific values for the Key Vault health check skill.
This file is auto-generated on first run and can be edited manually.

## Azure Monitor Datasource
- **UID**: {discovered_uid}
- **Name**: {discovered_name}

## Subscriptions
- {subscription_id_1}
- {subscription_id_2}
```

**4. Confirm**: Show the resolved config and ask for confirmation before proceeding.
