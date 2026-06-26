# Recipe: Daily Digest

A morning briefing that summarizes the most important things a sales rep or marketing lead needs to know today.

## When to use this

- "Give me my morning briefing"
- "What happened overnight?"
- "Daily digest"
- "What do I need to do today?"
- "Catch me up"

## What it produces

A structured markdown briefing with 5 sections:

1. **Deals needing attention** — slipping, stale, or high-value with upcoming close dates
2. **Hot leads** — top-scored contacts with recent activity
3. **Campaign performance** — results from recent sends vs. baselines
4. **Pipeline snapshot** — total open value, stage distribution, changes
5. **Action items** — prioritized to-do list for today

## How the agent runs it

The digest combines output from multiple scripts and data sources:

1. Read `~/.activecampaign-skill/state.json` for baselines
2. Run `python3 {baseDir}/scripts/find_slipping_deals.py --top 5` for deal alerts (skips if Deals not enabled)
3. Run `python3 {baseDir}/scripts/find_hot_leads.py --top 5` for lead alerts
4. Run `python3 {baseDir}/scripts/baseline_drift.py` to surface metric drift
5. Run `python3 {baseDir}/scripts/automation_audit.py --window-days 7` to flag orphaned automations
6. Pull recent campaign data via API; for any campaign with notable drop, optionally run `python3 {baseDir}/scripts/campaign_postmortem.py <id>`
7. Compose the briefing and present to user
8. Log to history.jsonl

## Section details

### 1. Deals needing attention

Sources: `scripts/find_slipping_deals.py`

Show top 5 by urgency (days overdue × value):
- Deal name, value, stage, days since last activity
- Expected close date vs. today
- One-line recommended action

### 2. Hot leads

Sources: `scripts/find_hot_leads.py`

Show top 5 by composite score:
- Contact name, email, score
- Key signal (tag, score change, deal stage)
- One-line recommended action ("Call today", "Send proposal")

### 3. Campaign performance

Sources: AC campaigns API

Pull last 3-5 campaigns sent since previous digest:
- Campaign name, send date, audience size
- Open rate vs. account p50 baseline (from state.json)
- Click rate vs. baseline
- Flag any campaign significantly below baseline

### 4. Pipeline snapshot

Sources: AC deals API

- Total open deals and value
- Deals won/lost since last digest
- Stage distribution bar (text-based)

### 5. Action items

Synthesized from all sections above:
- Ordered by priority (revenue impact × urgency)
- Each item is one concrete action: "Call Jane at Acme — deal is 12 days overdue ($50K)"
- Maximum 7 items to stay scannable

## Sample output

```
# Daily Digest — 2026-04-24

## Deals needing attention

| Deal | Value | Status | Action |
|---|---|---|---|
| Acme Enterprise | $50,000 | 12 days overdue, 18 days stale | Call today or escalate |
| Globex Pro | $25,000 | 5 days overdue | Send follow-up email |

## Hot leads

| Contact | Score | Signal |
|---|---|---|
| Jane Smith (jane@acme.com) | 92 | Opened proposal email 3x yesterday |
| Bob Lee (bob@globex.com) | 85 | New deal created, high engagement |

## Campaign performance (last 3 sends)

| Campaign | Sent | Open rate | vs. baseline |
|---|---|---|---|
| April Newsletter | 2,400 | 31.2% | +3.2pp ✅ |
| Trial Nurture #5 | 340 | 19.8% | -8.2pp ⚠️ |
| Feature Launch | 1,800 | 28.1% | +0.1pp ✅ |

⚠️ Trial Nurture #5 significantly underperformed. Check subject line and audience.

## Pipeline snapshot

Open: 16 deals | $510,000 total value
Won this week: 2 deals ($35,000)
Lost this week: 0

Qualified ████████░░ 50%
Proposal  █████░░░░░ 31%
Negotiation ███░░░░░░░ 19%

## Today's action items

1. Call Acme — deal is 12 days overdue ($50K)
2. Follow up with Globex — 5 days past close date ($25K)
3. Investigate Trial Nurture #5 performance drop
4. Reach out to Jane Smith (score: 92, high intent)
5. Review 2 deals with missing close dates
```

## Customization parameters

| Parameter | Default | Description |
|---|---|---|
| `top_deals` | 5 | Max deals to show |
| `top_leads` | 5 | Max leads to show |
| `campaign_lookback_days` | 7 | Days of campaign history |
| `pipeline_id` | all | Filter to specific pipeline |

## Outcome logging

```jsonl
{"ts":"...","action":"digest_generated","recipe":"daily-digest","deals_flagged":2,"leads_flagged":2,"campaigns_reviewed":3}
```

## API note

Per-contact engagement signals (e.g., "opened email 3x yesterday") use the `/activities` endpoint which can be incomplete. The digest focuses on deal activity and scores for reliability, supplementing with campaign-level metrics.

## Suggested next steps

After presenting the digest, offer the user these follow-ups based on what the data showed:

1. **If any deals are slipping:** "Want me to run a full deal hygiene audit? I can show the complete pipeline breakdown and help you update stale deals."
2. **If any leads scored above 80:** "Should I pull the full signal breakdown for [top lead name]? I can also help you tag them or enroll them in an automation."
3. **If campaign performance is below baseline:** "Want me to run a list health audit to check if deliverability factors are contributing to the decline?"

## Related

- `scripts/find_slipping_deals.py` — deal urgency ranking *(needs Deals)*
- `scripts/find_hot_leads.py` — lead scoring
- `scripts/baseline_drift.py` — metric drift detector
- `scripts/automation_audit.py` — orphaned automations
- `scripts/campaign_postmortem.py` — drill into a single send
- `recipes/deal-hygiene.md` — deeper pipeline analysis
- `recipes/list-health-audit.md` — list quality check
- `recipes/quarterly-review.md` — bigger-picture rollup
