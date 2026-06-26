# Recipe: List Health Audit

A diagnostic that examines your AC account and identifies list quality issues, deliverability risks, and contacts who should be suppressed or re-engaged.

## When to use this

- "How healthy is my list?"
- "Why is open rate dropping?"
- "Should I clean my list?"
- "What's my dormant percentage?"
- Quarterly hygiene checks

## What it produces

A markdown report with:
1. **Headline metrics** vs. account baseline
2. **Risk flags** — things that could hurt deliverability
3. **Dormant cohort breakdown** — who hasn't engaged, for how long
4. **Suppression candidates** — contacts to remove now
5. **Re-engagement candidates** — contacts worth one more attempt
6. **Remediation plan** — prioritized actions

## How the agent runs it

The audit composes the headline `audit_list_health.py` with several focused diagnostic scripts:

1. `python3 {baseDir}/scripts/audit_list_health.py` — top-level metrics + suppression candidates
2. `python3 {baseDir}/scripts/dedupe_contacts.py` — flag duplicates within the list
3. `python3 {baseDir}/scripts/role_address_finder.py` — `info@`, `support@`, etc. clutter
4. `python3 {baseDir}/scripts/free_vs_corporate_report.py` — domain composition, B2B vs. consumer lean
5. `python3 {baseDir}/scripts/contact_completeness_report.py` — which fields are populated
6. `python3 {baseDir}/scripts/list_audit.py` — per-list send recency, churn, dormancy
7. `python3 {baseDir}/scripts/list_overlap.py` — which lists are subsets of others
8. `python3 {baseDir}/scripts/suppression_export.py` — current suppression breakdown
9. `python3 {baseDir}/scripts/stale_contact_report.py --window-days 365` — never-engaged + long-stale
10. Read each script's markdown output, synthesize, present top 3-5 actions

The scripts use `~/.activecampaign-skill/state.json` for baselines. If state.json doesn't exist or is >30 days old, prompt the user to run `python3 {baseDir}/scripts/calibrate.py` first.

## What the script analyzes

### Bounce metrics
- Hard bounce rate (target: <0.5%)
- Soft bounce rate (target: <2%)

### Contact growth
- Total contacts
- New contacts in last 30 days
- Growth rate vs. previous period

### Unsubscribe signals
- Unsub rate per campaign (target: <0.5%, alarming: >1%)
- Trend across last 5-10 campaigns

### Domain distribution
- % of list on Gmail vs. Outlook vs. Yahoo vs. corporate domains
- Any single domain >40% concentration is a deliverability risk

### Suppression candidates
- Hard bounced (suppress immediately)
- Contacts with 3+ bounce log entries (suppress)

### Re-engagement candidates
- Contacts with low scores but valuable tags (customer, VIP)

## Sample report output

```
# List Health Audit — testco.api-us1.com
Generated: 2026-04-24

## Headline metrics

| Metric | Your value | Account baseline | Status |
|---|---|---|---|
| Total contacts | 4,823 | — | — |
| New (30d) | 164 | — | 3.4% growth |
| Hard bounce rate | 0.31% | <0.5% | ✅ |
| Unsubscribe rate | 0.42% | <0.5% | ✅ |
| Open rate (last campaigns) | 22.1% | 28.0% | ⚠️ Below |

## Risk flags

⚠️ Open rate dropped below your 90-day median.

⚠️ Domain concentration: acmecorp.com represents 47% of list.

## Suppression candidates

- 12 contacts with hard bounces → suppress immediately
- 8 contacts with 3+ bounce entries → suppress

## Suggested actions (prioritized)

1. Suppress bounced contacts (tag with auto-suppress-YYYY-MM)
2. Investigate open rate decline — check recent subject lines
3. Diversify list sources to reduce domain concentration
```

## Customization parameters

| Parameter | Default | Options |
|---|---|---|
| `--format` | `markdown` | `json` for machine-readable |
| `--output` | stdout | file path |

## Follow-up actions

After running the audit, the agent should ask if the user wants to:

1. Apply suppression tags automatically
2. Run a re-engagement campaign → load `recipes/welcome-series.md`
3. Compare to baseline trends

## Outcome logging

After successful execution, append to `~/.activecampaign-skill/history.jsonl`:

```jsonl
{"ts":"...","action":"audit_executed","recipe":"list-health-audit","total_contacts":4823,"bounced_count":20,"suppression_candidates":12}
```

## API limitations

- **Per-contact engagement data** (last open date) is unreliable via the activities endpoint. The audit uses bounce logs, contact scores, and campaign-level metrics instead.
- **Spam complaint data** is not available via the API. The audit focuses on bounces and unsubscribes as deliverability proxies.
- **Domain-level deliverability** (inbox placement rates) is not available. The audit checks domain concentration risk only.

## Suggested next steps

After presenting the list health audit, offer the user these follow-ups:

1. **If suppression candidates found:** "Want me to tag the bounced contacts with `auto-suppress-YYYY-MM` so they stop receiving campaigns? I'll show you exactly what will be tagged before applying."
2. **If open rate is below baseline:** "Should I check your recent subject lines against your top-performing ones from calibration? I can also design a re-engagement campaign for dormant contacts."
3. **If domain concentration risk detected:** "Want me to break down which contacts are on the concentrated domain and check their engagement? Some may be suppression candidates."

## Related

- `frameworks/email-best-practices.md` — deliverability guidance
- `frameworks/segmentation-theory.md` — for re-engagement segment design
- `scripts/audit_list_health.py` — the actual implementation
