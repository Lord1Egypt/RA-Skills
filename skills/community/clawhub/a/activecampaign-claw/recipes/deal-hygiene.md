# Recipe: Deal Hygiene

A pipeline health check that surfaces stale deals, missing data, and action items for sales reps and managers.

## When to use this

- "Which deals are stale?"
- "Clean up my pipeline"
- "What's slipping this quarter?"
- "Weekly pipeline review"
- "Show me deals that need attention"

## What it produces

A markdown report with:
1. **Pipeline summary** — deal count and value by stage
2. **Slipping deals** — past expected close date with no recent activity
3. **Stale deals** — no activity in N days
4. **Data quality issues** — missing close date, value, or owner
5. **Stage distribution** — is everything bunched at the top?
6. **Recommended actions** — prioritized by deal value and urgency

## How the agent runs it

Combines several deal-side scripts (all require the Deals feature on the AC account):

1. `python3 {baseDir}/scripts/find_slipping_deals.py` — overdue / stale by value × urgency
2. `python3 {baseDir}/scripts/pipeline_audit.py` — per-stage health, deal-field completeness, stages with no recent activity
3. `python3 {baseDir}/scripts/win_loss_report.py --days 90` — what's been closing in the window
4. `python3 {baseDir}/scripts/mql_to_sql_handoff.py --days 7` — scoring crossings with no deal (sales miss) and deals with no scoring (rep off-script)
5. Read each markdown output and present a synthesized priority list
6. Offer to update specific deals via the API (with the standard pre-write confirmation flow)

## What the script analyzes

### Slipping deals
- `nextdate` (expected close) is in the past
- Ranked by: (days overdue × deal value) to surface highest-impact slips first

### Stale deals
- `mdate` (last modified) is older than threshold (default: 14 days)
- No recent deal activities (notes, stage changes, tasks)

### Data quality
- Missing `nextdate` (no expected close date set)
- Missing `value` or value = 0
- Missing `owner` (unassigned deals)
- Missing `contact` (orphan deals)

### Stage distribution
- Percentage of open deals in each stage
- Healthy pipeline: roughly decreasing from top to bottom
- Warning: >60% in first stage = not enough progression
- Warning: >30% in last pre-close stage = bottleneck

### Pipeline velocity
- Average days per stage (computed from deal `cdate` and `mdate`)
- Deals taking >2x average for their current stage

## Actions the agent can take

After showing the report, the agent can update deals via API:

```bash
# Move deal to a different stage
curl -s -X PUT -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"deal":{"stage":"3"}}' \
  "$AC_API_URL/api/3/deals/{id}" | jq

# Add a note
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"note":{"note":"Flagged as stale — 21 days without activity. Follow up required."}}' \
  "$AC_API_URL/api/3/deals/{id}/notes" | jq

# Update expected close date
curl -s -X PUT -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"deal":{"nextdate":"2026-05-15"}}' \
  "$AC_API_URL/api/3/deals/{id}" | jq
```

## Sample report output

```
# Deal Hygiene Report — Sales Pipeline
Generated: 2026-04-24

## Pipeline summary

| Stage | Deals | Total value | Avg age |
|---|---|---|---|
| Qualified | 8 | $120,000 | 12 days |
| Proposal | 5 | $210,000 | 18 days |
| Negotiation | 3 | $180,000 | 25 days |
| **Total open** | **16** | **$510,000** | — |

## Slipping deals (3)

| Deal | Value | Days overdue | Last activity |
|---|---|---|---|
| Acme Corp — Enterprise | $50,000 | 12 days | 18 days ago |
| Globex — Pro Plan | $25,000 | 5 days | 22 days ago |
| Initech — Annual | $15,000 | 3 days | 8 days ago |

## Stale deals — no activity in 14+ days (4)

| Deal | Value | Stage | Days since activity |
|---|---|---|---|
| Acme Corp — Enterprise | $50,000 | Negotiation | 18 days |
| Globex — Pro Plan | $25,000 | Proposal | 22 days |
| Widget Co — Starter | $5,000 | Qualified | 35 days |
| BigCo — Trial | $10,000 | Qualified | 16 days |

## Data quality issues

- 2 deals missing expected close date
- 1 deal with $0 value
- 0 unassigned deals

## Recommended actions

1. **Acme Corp**: 18 days stale + 12 days overdue. Call today or move to Lost.
2. **Globex**: 22 days stale. Send follow-up or reassign.
3. **Widget Co**: 35 days stale in Qualified. Likely dead — confirm or close.
```

## Customization parameters

| Parameter | Default | Description |
|---|---|---|
| `--stale-days` | 14 | Days without activity to flag as stale |
| `--pipeline` | all | Filter to specific pipeline ID |
| `--format` | markdown | `json` for machine-readable |
| `--output` | stdout | File path |

## Outcome logging

```jsonl
{"ts":"...","action":"audit_executed","recipe":"deal-hygiene","open_deals":16,"slipping":3,"stale":4,"total_value":510000}
```

## Suggested next steps

After presenting the deal hygiene report, offer the user these follow-ups:

1. **If stale deals exist:** "Want me to add a follow-up note to these stale deals? I can draft the note and update the expected close dates."
2. **If data quality issues found:** "Should I fix the missing data? I can update close dates, assign owners, or set deal values for the flagged deals."
3. **If pipeline is top-heavy (>60% in first stage):** "Your pipeline looks top-heavy. Want me to find hot leads that could help fill later stages, or review which qualified deals are ready to advance?"

## Related

- `scripts/find_slipping_deals.py` — the implementation
- `references/deals.md` — deal API reference
- `recipes/daily-digest.md` — includes deal hygiene in the daily briefing
