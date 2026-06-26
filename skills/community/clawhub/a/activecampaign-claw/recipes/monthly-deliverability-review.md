# Recipe: Monthly deliverability review

A monthly cadence for verifying your sender health is stable before it becomes a crisis.

## When to use this

- First Monday of each month, as a standing review.
- "Is my deliverability okay?"
- Before a high-stakes send (product launch, big promotion).
- After receiving an inbox-placement complaint or a deliverability warning from AC.

## What it produces

1. **Headline scorecard** — bounces, unsubs, complaint proxies, domain mix — vs. last month and 90-day baseline.
2. **Trend flags** — anything that drifted >1σ from your normal range.
3. **Domain spotlight** — engagement breakdown by recipient domain (Gmail / Outlook / Yahoo / corporate).
4. **Actionable next steps** — only the items that actually moved.

## How the agent runs it

1. `python3 {baseDir}/scripts/baseline_drift.py` — flags any baseline metric that drifted significantly.
2. `python3 {baseDir}/scripts/monthly_performance.py` — full month's send metrics vs. baseline.
3. `python3 {baseDir}/scripts/bounce_breakdown.py --window-days 30` — bounce categorization (550 vs. 421 vs. content blocks).
4. `python3 {baseDir}/scripts/domain_engagement_report.py` — per-domain engagement.
5. `python3 {baseDir}/scripts/unsubscribe_audit.py` — unsub trend, opt-in compliance.
6. `python3 {baseDir}/scripts/audit_list_health.py` — top-level account health.
7. Synthesize into a single scorecard.

## Headline scorecard targets

| Metric | Target | Concerning | Action threshold |
|---|---|---|---|
| Hard bounce rate | <0.5% | 0.5–1% | >1% — investigate sources |
| Soft bounce rate | <2% | 2–4% | >4% — pause big sends |
| Unsubscribe rate | <0.5% per send | 0.5–1% | >1% — review last subject lines |
| List growth | positive | flat | shrinking 3 months in a row — re-engagement needed |
| Yahoo/AOL bounce share | <15% of total | 15–30% | >30% — likely DMARC/DKIM issue |

## Sample report output

```
# Monthly Deliverability Review — testco.api-us1.com (April 2026)

## Headline scorecard

| Metric | This month | Last month | 90-day baseline | Status |
|---|---|---|---|---|
| Sends | 14 | 11 | 13.2 avg | normal |
| Hard bounce rate | 0.31% | 0.28% | 0.30% | ✅ |
| Soft bounce rate | 1.4% | 1.1% | 1.3% | ✅ |
| Unsub rate / send | 0.42% | 0.39% | 0.41% | ✅ |
| Open rate | 22.1% | 27.4% | 28.0% | ⚠ -5.9pp |
| List size | 12,438 | 12,320 | — | +0.96% |

## Trend flags

⚠ Open rate dropped 5.9pp below baseline. Two likely causes:
  - Recent subject-line shift (the last 4 sends used "URGENT" patterns; subject_line_report shows -9.7pp lift)
  - Apple Mail Privacy Protection (open rates drift naturally; is click rate also down?)
    → Click rate is flat at 4.1% (baseline 4.0%). MPP, not engagement loss.

## Domain spotlight

| Domain group | % of list | Open rate | Click rate | Trend |
|---|---|---|---|---|
| Gmail | 41% | 24% | 4.4% | stable |
| Outlook | 18% | 19% | 3.1% | stable |
| Yahoo | 9% | 16% | 2.8% | ↓ -3pp opens (watch) |
| Corporate | 32% | 26% | 4.9% | stable |

## Actions

1. Retire urgency-bait subject lines (next 5 sends — A/B test against your top performers).
2. Yahoo open rate dipped — verify DMARC alignment is `pass` for your sending domain in any recent send.
3. Nothing else moved. Continue current cadence.
```

## Customization parameters

| Parameter | Default | Notes |
|---|---|---|
| Review window | 30 days | Match your reporting cadence. |
| Trend significance | 1σ from baseline | Tighten to 0.5σ on smaller accounts where signals are noisier. |
| Action threshold | "moved" | Don't list items that didn't change — keep the report short. |

## What NOT to do in this review

- **Don't compare directly to industry benchmarks** unless your account-level baseline is small (<20 campaigns over 90 days). Your own baseline is the right reference.
- **Don't react to single-month dips** without checking the underlying cause. Apple Mail Privacy Protection makes open rates drift downward over time independent of real engagement.
- **Don't skip the domain breakdown.** A healthy aggregate can hide a specific-domain crisis (Yahoo deliverability issues are often single-domain).

## API limitations

- Spam complaint data is not exposed via v3 API. Use unsub spikes and Yahoo/AOL deferrals as proxies.
- Per-event open data is plan-dependent. On plans without `/messageActivities`, opens are estimated from campaign-level metrics rather than per-recipient.
- Inbox placement / panel data is NOT available through this skill or AC's API. For that, integrate a separate seedlist tool (Litmus, Email on Acid, GlockApps).

## Outcome logging

```jsonl
{"ts":"...","action":"recipe_executed","recipe":"monthly-deliverability-review","month":"2026-04","trend_flags":1,"action_count":2}
```

If `baseline_drift` shows a significant deviation (>1σ), also append an `insights.md` entry so the agent can reference it in future reviews.

## Related

- `frameworks/email-best-practices.md` — deliverability hardening.
- `recipes/list-health-audit.md` — the deeper hygiene check (run quarterly).
- `recipes/re-engagement-launch.md` — what to do if dormancy is the root cause.
- `scripts/baseline_drift.py` — the drift detector.
