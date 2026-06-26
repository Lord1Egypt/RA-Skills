---
name: amg-check-pg-flex
description: Run only when the user explicitly asks for a fleet-wide PostgreSQL Flexible Server health check — scans CPU, memory, storage, IOPS, disk bandwidth, and connection metrics across all servers, then deep-dives into abnormal servers with resource logs and correlation analysis. Tracks known issues across sessions via persistent report. Uses AMG-MCP pulse check for Tier 1 triage, then batched Azure Monitor queries for Tier 2 investigation. On first run, auto-discovers datasource UID and prompts for subscription ID.
argument-hint: "[time-range, e.g. 7d] [subscription-id]"
disable-model-invocation: true
effort: max
allowed-tools: mcp__amg__amgmcp_pulse_check mcp__amg__amgmcp_query_resource_graph mcp__amg__amgmcp_query_resource_metric mcp__amg__amgmcp_query_resource_metric_definition mcp__amg__amgmcp_query_resource_log mcp__amg__amgmcp_datasource_list mcp__amg__amgmcp_query_activity_log Bash(node *) Glob Read Write Edit
---

<!-- Auto-generated for OpenClaw by pack-openclaw. Notes for OpenClaw users:
     - Claude Code dynamic expressions (!`...`) in this file are NOT evaluated by OpenClaw
       and appear as literal text. Run them manually at the start of the workflow.
     - Invoke this skill only via slash command (e.g. /amg-check-pg-flex). Auto-invocation is
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
- Config: !`cat memory/amg-check-pg-flex/config.md 2>/dev/null || echo "NOT_CONFIGURED"`
- Prior report: !`[ -f memory/amg-check-pg-flex/report.md ] && echo "exists ($(grep -c '^### BUG-' memory/amg-check-pg-flex/report.md) bugs documented)" || echo "not found"`
- Arguments: time-range=$0, subscription-override=$1

> **Known Issues**: Before presenting findings, cross-reference results against `memory/amg-check-pg-flex/report.md`.

# AMG PostgreSQL Flexible Server Health Check

## Critical Constraints

- **No subagents for MCP.** The Agent tool cannot access MCP tools — all MCP calls must be made from the main context.
- **Scan every resource.** No sampling or early stopping.
- **Time format**: ISO 8601 UTC with explicit `from`/`to` — NEVER use `timespan` (it causes errors).
- **Parallelism cap**: 30 concurrent MCP calls per batch. Reduce to 4-5 if rate-limited.
- **Result too large**: Save to temp file and parse outside the context window. Prefer `node -e "..."` if installed; otherwise fall back to `python -c "..."`, `jq`, or `pwsh -Command "..."`. Bash permission for the chosen interpreter will be prompted on first use.

## Progress Tracking

Update checkboxes as you complete each phase:

- [ ] Phase 1a: Datasource validated
- [ ] Phase 1b: Servers discovered (N=?)
- [ ] Phase 1c: Non-ready servers investigated (if any)
- [ ] Phase 2: Pulse check completed (N scanned, N findings)
- [ ] Phase 3: Deep metrics for abnormal servers
- [ ] Phase 4: Resource logs for abnormal servers
- [ ] Report presented
- [ ] Known issues updated in `memory/amg-check-pg-flex/report.md`

## Configuration

**If Config shows `NOT_CONFIGURED`**: Run [First-Run Setup](#first-run-setup) at the bottom of this file, then return here.

**If Config is populated**: Extract the datasource UID and subscription ID from the pre-loaded Runtime Context above and use them for all queries. Use `$1` as the subscription override if provided.

- **Datasource UID**: from `## Azure Monitor Datasource` > `UID`
- **Subscription ID**: from `## Subscription` (or `$1` if provided)
- **Resource Type**: `microsoft.dbforpostgresql/flexibleservers` (lowercase)
- **ARM ID template**: `/subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.DBforPostgreSQL/flexibleServers/{name}`

## Time Range

Default: 7 days for metrics, 24 hours for logs. Override with `$0` (e.g., `3d`). Keep log queries to 1-2 days to avoid timeouts.

---

## Workflow

### Phase 1a: Validate Datasource

Call `amgmcp_datasource_list` (no parameters). Find entry with `type == "grafana-azure-monitor-datasource"`.

- Matches configured UID → proceed.
- Different UID → update `memory/amg-check-pg-flex/config.md`, warn user, use new UID.
- Not found → abort with error.

### Phase 1b: Discover All PostgreSQL Flexible Servers

```
azureMonitorDatasourceUid: {DATASOURCE_UID}
query: |
  resources
  | where type == 'microsoft.dbforpostgresql/flexibleservers'
  | where subscriptionId == '{SUBSCRIPTION_ID}'
  | project name, resourceGroup, location, properties.state, sku.name, sku.tier
  | order by location asc, name asc
```

If multiple subscriptions are configured, query each separately and merge results. Derive region summary by counting servers per `location`. Flag servers not in "Ready" state. Stop if zero servers found.

### Phase 1c: Activity Log for Non-Ready Servers

If any servers are not in "Ready" state, query the activity log for up to 3 of them:

```
azureMonitorDatasourceUid: {DATASOURCE_UID}
scope: /subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.DBforPostgreSQL/flexibleServers/{name}
startTime: now-3d
endTime: now
select: eventTimestamp,operationName,status,caller,subStatus
```

If the response exceeds 500 KB, retry with `startTime: now-6h`. Summarize: operations performed, caller type (service principal vs human), success/in-progress status, likely cause.

### Phase 2: Tier 1 — Fleet-Wide Pulse Check

```
azureMonitorDatasourceUid: {DATASOURCE_UID}
pastDays: 7
scenarios: pg_flex
```

Scans all servers across 5 scenarios: `pg_flex_cpu`, `pg_flex_memory`, `pg_flex_storage`, `pg_flex_disk_iops`, `pg_flex_disk_bandwidth`.

**Before moving to Phase 3, verify:**
1. `scanSummary.totalResourcesScanned` matches Phase 1 server count.
2. All 5 scenarios show `status: "completed"` in `scenarioResults`.
3. If `errors` non-empty, retry affected scenarios individually (e.g., `scenarios: pg_flex_cpu`).
4. If >10% servers missing, fall back to batched `amgmcp_query_resource_metric` for unscanned servers.

**Severity thresholds (findings array):**

| Severity | CPU   | Memory | Storage | Disk IOPS | Disk BW |
|----------|-------|--------|---------|-----------|---------|
| Critical | >90%  | >90%   | >85%    | >90%      | >90%    |
| Warning  | >80%  | >80%   | >75%    | >80%      | >80%    |

### Phase 3: Tier 2 — Deep Metrics for Abnormal Servers

Read **[reference/phase3-deep-dive.md](${CLAUDE_SKILL_DIR}/reference/phase3-deep-dive.md)** before starting Phase 3. It contains:
- Core metrics table (always query) and secondary metrics table (query on anomaly)
- Batch strategy: up to 50 comma-separated resource IDs per call, up to 5 parallel metric calls
- Correlation analysis patterns (use ultrathink)

### Phase 4: Resource Logs for Abnormal Servers

Read **[reference/phase4-resource-logs.md](${CLAUDE_SKILL_DIR}/reference/phase4-resource-logs.md)** before starting Phase 4. It contains:
- 5 KQL query templates: error distribution, top errors, warning messages, log volume, session duration
- Time filter rules (always required to avoid timeouts)

---

## Output

Present the report using the structure in **[reference/output-format.md](${CLAUDE_SKILL_DIR}/reference/output-format.md)**.

**Classification:**

| Severity    | Criteria |
|-------------|----------|
| **CRITICAL** | `is_db_alive` sustained 0, OR CPU max >90%, OR Memory max >90%, OR Storage >85% |
| **WARNING**  | CPU avg >80%, Memory avg >85%, sustained >60% for 6h+, spike >30pp in 1h, Storage >70%, `connections_failed` >0, `deadlocks` >0, disk IOPS/BW >80%, transactionIDs >1B, longest query >300s, replication delay >30s |
| **HEALTHY**  | All metrics within normal ranges |

## Update Known Issues

After presenting findings, update `memory/amg-check-pg-flex/report.md`:

1. Read the current file.
2. Rebuild the Resource Inventory table at the end: every server, full ARM ID, region, SKU, state. Group by region, sorted alphabetically.
3. Update existing bug status from today's telemetry (resolved / improving / worsening / still active).
4. Add new bugs with: severity, server name, region, metric evidence, log evidence, root cause, recommended action.
5. Update the "Updated" date header.

Only add genuine issues: sustained high utilization, crash patterns, connection storms, persistent errors. Skip transient single-hour spikes or expected maintenance windows.

## Error Handling

See **[reference/error-handling.md](${CLAUDE_SKILL_DIR}/reference/error-handling.md)** for the full recovery table.

## Analysis Guidance

- Known patterns, signals, root causes: [reference/analysis-patterns.md](${CLAUDE_SKILL_DIR}/reference/analysis-patterns.md)
- Optional deep-dive KQL queries: [reference/deep-dive-queries.md](${CLAUDE_SKILL_DIR}/reference/deep-dive-queries.md)

---

## First-Run Setup

Run only when Config shows `NOT_CONFIGURED`. After completing, return to the [Workflow](#workflow) above.

**1. Discover Datasource UID**: Call `amgmcp_datasource_list`. Filter `type == "grafana-azure-monitor-datasource"`. Prefer `uid == "azure-monitor-oob"` if multiple match. Abort if zero match.

**2. Discover Subscription ID**: Run this Resource Graph query to list all subscriptions with PostgreSQL Flexible Servers, then present the results as a table and ask the user which subscription(s) to use:
```
resources
| where type == 'microsoft.dbforpostgresql/flexibleservers'
| join kind=inner (
    resourcecontainers
    | where type == 'microsoft.resources/subscriptions'
    | project subscriptionId, subscriptionName=name
) on subscriptionId
| summarize ServerCount=count() by subscriptionId, subscriptionName
| order by ServerCount desc
```

Present the results as a table with columns: **Subscription Name**, **Subscription ID**, **Server Count**. Then ask the user: *"Which subscription ID(s) should I configure for this health check?"*

**3. Write config**: Write `memory/amg-check-pg-flex/config.md`:
```markdown
# amg-check-pg-flex Configuration

User-specific values for the PostgreSQL Flexible Server health check skill.
This file is auto-generated on first run and can be edited manually.

## Azure Monitor Datasource
- **UID**: {discovered_uid}
- **Name**: {discovered_name}

## Subscription
- {subscription_id}
```

**4. Confirm**: Show the resolved config and ask for confirmation before proceeding.
