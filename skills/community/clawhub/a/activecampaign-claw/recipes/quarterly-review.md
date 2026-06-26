# Recipe: Quarterly Marketing Review

A comprehensive rollup of the last 90 days of marketing performance, list health, automation efficacy, and pipeline activity. Designed to be the report a marketing lead presents to leadership.

## When to use this

- "Run my quarterly review"
- "End-of-quarter marketing report"
- "Comprehensive marketing audit"
- "Where did we land this quarter?"
- Before/after a major program change, to baseline the before-state

## What it produces

An end-to-end markdown report with eight sections:

1. **Executive summary** — 5 bullet headline numbers
2. **Campaign performance** — what was sent, what worked, what dropped
3. **Subject line + send time learnings** — patterns from the data
4. **Audience health** — list growth, engagement decay, dormancy
5. **Automation efficacy** — funnels, completion rates, orphans
6. **Tag / field / segment hygiene** — what to clean
7. **Pipeline contribution** *(if Deals enabled)* — win/loss, MQL→SQL handoff, attribution
8. **Recommendations** — prioritized actions for the next quarter

## How the agent runs it

This recipe runs ~12 scripts in sequence, each a small slice of the picture. The agent reads outputs and composes the report rather than dumping each section verbatim.

```bash
SKILL=~/.openclaw/skills/activecampaign/scripts

# 1. Section: Campaign performance (90-day window)
python3 $SKILL/monthly_performance.py --months 3
python3 $SKILL/baseline_drift.py --window-days 90
python3 $SKILL/campaign_velocity.py --window-days 90

# 2. Section: Content learnings
python3 $SKILL/subject_line_report.py --days 90
python3 $SKILL/from_name_report.py --days 90
python3 $SKILL/send_time_optimizer.py
python3 $SKILL/content_length_report.py --days 90

# 3. Section: Audience health
python3 $SKILL/list_audit.py
python3 $SKILL/engagement_decay.py --months 12
python3 $SKILL/new_subscriber_quality.py --days 90
python3 $SKILL/stale_contact_report.py --window-days 180
python3 $SKILL/domain_engagement_report.py
python3 $SKILL/send_frequency_report.py --window-days 30
python3 $SKILL/free_vs_corporate_report.py

# 4. Section: Automation efficacy
python3 $SKILL/automation_audit.py --window-days 90
python3 $SKILL/automation_overlap.py
python3 $SKILL/stalled_automations.py --min-days 14
python3 $SKILL/broken_automation_detector.py
# Optionally drill into the top 2-3 active automations:
# python3 $SKILL/automation_funnel.py <id>

# 5. Section: Hygiene candidates
python3 $SKILL/tag_audit.py
python3 $SKILL/custom_field_audit.py
python3 $SKILL/list_overlap.py
python3 $SKILL/segment_audit.py --skip-counts
python3 $SKILL/dedupe_contacts.py
python3 $SKILL/role_address_finder.py

# 6. Section: Pipeline (skipped if Deals not enabled)
python3 $SKILL/win_loss_report.py --days 90
python3 $SKILL/pipeline_audit.py
python3 $SKILL/mql_to_sql_handoff.py --threshold 50 --days 90

# 7. Snapshot + log
python3 $SKILL/snapshot.py --scope taxonomy
```

Total runtime on a medium account: ~5 minutes (mostly bound by AC's 5 req/s rate limit).

## Sample output structure

```
# Quarterly Marketing Review — Q1 2026

## Executive summary
- 47 campaigns sent to 312k recipient-events; open rate 26.4% (-0.8pp vs. baseline)
- List grew 8.4%; new-subscriber engagement is solid (62% opened ≥1 email)
- 3 automations completed >10k contacts; 2 are orphaned (no enrollments in 30 days)
- 14 zombie tags + 6 unused custom fields are safe to delete
- Pipeline closed $487k won / $112k lost; one source list has a 0% win rate

## Campaign performance
[monthly_performance + baseline_drift output, summarized]

## What's working in your content
- Subject lines with personalization tokens lift open rate +6.1pp
- Tuesday 2pm UTC sends outperform Wednesday by 3pp
- "Marketing Director" from-name beats "Acme Team" by +9pp
[from subject_line_report, send_time_optimizer, from_name_report]

## Audience health
- 12,438 active contacts; M+0 cohort retention shows Apr cohort at 41% open-anything
- Gmail and corporate domains driving most engagement; Yahoo lagging
- 1,847 contacts haven't engaged in 12+ months — re-engage or sunset
[from list_audit, engagement_decay, domain_engagement_report, stale_contact_report]

## Automation efficacy
- "Welcome Series" funnel: 100% start → 78% step 3 → 41% goal
- "Trial Nurture" stalled: 230 contacts stuck at the Wait-7-days step
- "Old Sales Outreach" hasn't enrolled anyone in 90 days — archive?
[from automation_audit, automation_funnel, stalled_automations]

## Hygiene candidates (estimated impact: 30 min cleanup, much cleaner reporting)
- Delete 14 zombie tags
- Delete 6 unused custom fields
- Consolidate "VIP" + "Premium" tags (95% co-occurrence)
- Suppress 47 role addresses
[from tag_audit, custom_field_audit, role_address_finder]

## Pipeline contribution
[win_loss_report + mql_to_sql_handoff if Deals enabled]

## Recommendations for Q2
1. Investigate Trial Nurture stall (230 contacts stuck)
2. Suppress role addresses + zombie tags before sending next campaign
3. A/B test personalized subject lines (current data shows +6.1pp lift)
4. Move Yahoo segment to bi-weekly cadence (lower engagement)
5. Build a sunset workflow for the 1,847 long-dormant contacts
```

## Customization parameters

| Parameter | Default | Description |
|---|---|---|
| `window_days` | 90 | Quarter length |
| `include_pipeline` | auto | Auto-detects Deals feature; can force off |
| `automation_drill_top` | 3 | How many top automations to run `automation_funnel` on |

## Outcome logging

```jsonl
{"ts":"...","action":"quarterly_review_generated","recipe":"quarterly-review","scripts_run":24,"window_days":90,"snapshot":"snapshot-...-taxonomy.json"}
```

## Variant: weekly pulse

For a lighter-weight weekly version, run only:
- `monthly_performance.py --months 1`
- `baseline_drift.py --window-days 7`
- `automation_audit.py --window-days 7`
- `tag_audit.py` (if it's been a few weeks)

## Related

- `recipes/daily-digest.md` — same-shape but daily, fewer sections
- `recipes/list-health-audit.md` — deep-dive just on audience health
- `recipes/deal-hygiene.md` — deep-dive just on the pipeline side
- `frameworks/email-best-practices.md` — context for the content learnings section
- `frameworks/segmentation-theory.md` — context for the hygiene recommendations
