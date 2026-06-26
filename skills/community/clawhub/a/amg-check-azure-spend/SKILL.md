---
name: amg-check-azure-spend
description: Run only when the user explicitly asks for a monthly Azure subscription cost analysis — lists all accessible subscriptions, lets the user choose which to analyze, then queries last billing month's cost breakdown by resource type, region, and service category for each subscription. Queries subscriptions sequentially with 1-minute waits between calls to avoid billing API rate limits (429). On first run, auto-discovers datasource UID.
argument-hint: "[subscription-id-1,subscription-id-2,...] (optional, comma-separated)"
disable-model-invocation: true
effort: max
allowed-tools: mcp__amg__amgmcp_cost_analysis mcp__amg__amgmcp_query_azure_subscriptions mcp__amg__amgmcp_datasource_list Bash(sleep *) Glob Read Write Edit
---

<!-- Auto-generated for OpenClaw by pack-openclaw. Notes for OpenClaw users:
     - Claude Code dynamic expressions (!`...`) in this file are NOT evaluated by OpenClaw
       and appear as literal text. Run them manually at the start of the workflow.
     - Invoke this skill only via slash command (e.g. /amg-check-azure-spend). Auto-invocation is
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
- Config: !`cat memory/amg-check-azure-spend/config.md 2>/dev/null || echo "NOT_CONFIGURED"`
- Arguments: subscription-ids=$ARGUMENTS

# Azure Subscription Cost Analysis

Analyze Azure subscription costs for the **last full billing month** using `amgmcp_cost_analysis`. Queries each subscription individually with mandatory waits between calls to respect the billing API rate limit.

## Critical Constraints

- **No subagents for MCP.** The Agent tool cannot access MCP tools — all MCP calls must be made from the main context.
- **Sequential queries only.** Query one subscription at a time. **Never** query multiple subscriptions in parallel.
- **Mandatory 1-minute wait.** After each `amgmcp_cost_analysis` call, run `sleep 60` via Bash before the next call. This is non-negotiable — the billing API has a tight rate limit.
- **Recommend 5 subscriptions per run.** The billing API has tight throttling — each subscription takes 1-3 minutes (wait time + potential 429 retries). Warn the user if they select more than 5 that the run will be slow, but allow it if they confirm.
- **429 backoff.** If you receive a 429 (Too Many Requests), wait 2 minutes (`sleep 120`), then retry. If 429 persists, wait 5 minutes (`sleep 300`) and retry once more. If still failing, skip that subscription and note it in the report.

## Progress Tracking

Update checkboxes as you complete each phase:

- [ ] Phase 1a: Datasource validated
- [ ] Phase 1b: Subscriptions listed
- [ ] Phase 1c: Subscriptions selected
- [ ] Phase 2: Cost queries completed (0/N)
- [ ] Report presented
- [ ] Report saved to `memory/amg-check-azure-spend/report.md`

## Configuration

**If Config shows `NOT_CONFIGURED`**: Run [First-Run Setup](#first-run-setup) at the bottom of this file, then return here.

**If Config is populated**: Extract the datasource UID from the pre-loaded Runtime Context above.

- **Datasource UID**: from `## Azure Monitor Datasource` > `UID`

## Time Range

Always use the **last full billing month** boundaries. Compute them from the "Current UTC time" in the Runtime Context above:
- **startTime**: first day of the *previous* month at `00:00:00.000Z` (e.g., if current UTC time is `2026-04-16T...`, startTime = `2026-03-01T00:00:00.000Z`)
- **endTime**: first day of the *current* month at `00:00:00.000Z` (e.g., if current UTC time is `2026-04-16T...`, endTime = `2026-04-01T00:00:00.000Z`)

Do NOT use relative expressions like `now-30d` — billing months have variable lengths.

---

## Workflow

### Phase 1a: Validate Datasource

Call `amgmcp_datasource_list` (no parameters). Find entry with `type == "grafana-azure-monitor-datasource"`.

- Matches configured UID -> proceed.
- Different UID -> update `memory/amg-check-azure-spend/config.md`, warn user, use new UID.
- Not found -> abort with error.

### Phase 1b: List All Subscriptions

Call `amgmcp_query_azure_subscriptions` with the validated datasource UID.

Present the full list as a table:

| # | Subscription Name | Subscription ID |
|---|-------------------|-----------------|
| 1 | ...               | ...             |

### Phase 1c: Select Subscriptions

**If `$ARGUMENTS` provides subscription IDs** (comma-separated): Use those directly. Validate they appear in the Phase 1b list.

**If 5 or fewer subscriptions exist**: Use all of them.

**If more than 5 subscriptions exist**: Present the list to the user and ask them to choose. Suggest a default selection of ~5 based on name (e.g., production subscriptions first). Example prompt:

> *"Found N subscriptions. I recommend selecting around 5 — the billing API has tight rate limits, so each subscription takes 1-3 minutes (mandatory waits + potential 429 retries). You can select more, but the run will be slow. Which subscription numbers would you like to analyze? (e.g., `1,3,5`) Or press Enter to use my suggested selection: [list]."*

**If the user selects more than 5**: Warn them about the expected duration (roughly 2-3 minutes per subscription due to mandatory waits and 429 backoffs), then proceed if they confirm.

### Phase 2: Query Cost for Each Subscription

For each selected subscription, **one at a time**:

1. Call `amgmcp_cost_analysis` with:
   ```
   azureMonitorDatasourceUid: {DATASOURCE_UID}
   subscriptionId: {SUBSCRIPTION_ID}
   startTime: {BILLING_MONTH_START}
   endTime: {BILLING_MONTH_END}
   ```

2. Record the cost breakdown from the response:
   - Total cost for the subscription
   - Top cost drivers by resource type (MeterCategory)
   - Cost by region
   - Any notable cost spikes or anomalies

3. **Wait 1 minute before the next query:**
   ```bash
   sleep 60
   ```

4. If you receive a **429 (Too Many Requests)**:
   - Wait 2 minutes: `sleep 120`
   - Retry the same subscription
   - If 429 again, wait 5 minutes: `sleep 300` and retry once more
   - If still 429, skip this subscription and note "Rate-limited — skipped" in the report

Repeat for each subscription. Do NOT proceed to the next subscription without the 1-minute wait.

---

## Output Format

Present a cost report with these sections:

### 1. Billing Period

State the exact billing month analyzed (e.g., "March 2026: 2026-03-01 to 2026-04-01").

### 2. Cost Summary Table

| Subscription | Total Cost | Top Resource Type | Top Region | Status |
|-------------|------------|-------------------|------------|--------|
| sub-name-1  | $X,XXX.XX  | Virtual Machines  | East US    | OK     |
| sub-name-2  | $X,XXX.XX  | Storage           | West US 2  | OK     |

### 3. Per-Subscription Breakdown

For each subscription:
- **Total cost** for the billing month
- **Top 10 cost drivers** by MeterCategory (resource type) with amounts and percentages
- **Cost by region** — table showing spend per Azure region
- **Notable observations** — any unusually high costs, unexpected resource types, or potential optimization opportunities

### 4. Cross-Subscription Comparison

- Which subscription has the highest spend
- Common cost drivers across subscriptions
- Regional distribution of spend across all queried subscriptions

### 5. Cost Optimization Suggestions

Based on the data, flag:
- Subscriptions with disproportionately high costs in a single category
- Resource types that dominate spend (potential right-sizing candidates)
- Regions with unexpectedly high costs

---

## Save Report

After presenting findings, save the report to `memory/amg-check-azure-spend/report.md`:

1. Read the current file (if it exists).
2. Overwrite with the full cost report from this run, including:
   - Billing period and generation date
   - Cost summary table across all queried subscriptions
   - Per-subscription breakdowns (top services, regions, resource types)
   - Cross-subscription comparison
   - Cost optimization suggestions
   - Any skipped subscriptions (rate-limited) noted with reason
3. Update the "Generated" date header to today's date.

This file provides a baseline for future runs to compare month-over-month trends.

---

## Error Handling

See **[${CLAUDE_SKILL_DIR}/reference/error-handling.md](${CLAUDE_SKILL_DIR}/reference/error-handling.md)** for the full recovery table.

---

## First-Run Setup

Run only when Config shows `NOT_CONFIGURED`. After completing, return to the [Workflow](#workflow) above.

**1. Discover Datasource UID**: Call `amgmcp_datasource_list`. Filter `type == "grafana-azure-monitor-datasource"`. Prefer `uid == "azure-monitor-oob"` if multiple match. Abort if zero match.

**2. Write config**: Write `memory/amg-check-azure-spend/config.md`:
```markdown
# amg-check-azure-spend Configuration

User-specific values for the Azure spend analysis skill.
This file is auto-generated on first run and can be edited manually.

## Azure Monitor Datasource
- **UID**: {discovered_uid}
- **Name**: {discovered_name}
```

**3. Confirm**: Show the resolved config and ask for confirmation before proceeding.
