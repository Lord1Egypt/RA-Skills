# Recipe: Re-engagement campaign launch

A workflow for designing and launching a re-engagement campaign against contacts who used to engage but have gone quiet.

## When to use this

- "Half my list isn't opening anymore — what do I do?"
- "I want to win back dormant contacts before suppressing them."
- "How do I run a re-engagement before I clean my list?"
- After a list health audit flagged a large dormant cohort.

## What it produces

1. A defined **dormant cohort** (clear segment criteria the user can build in AC).
2. A **3-email re-engagement sequence** spec, tuned to your account baselines.
3. **Success criteria** (what counts as re-engaged) and a sunset rule.
4. A follow-up plan: who gets suppressed if the campaign doesn't bring them back.

The agent never sends or builds the campaign — AC's v3 API doesn't expose those endpoints. The output is a spec the user implements in the AC UI.

## How the agent runs it

1. `python3 {baseDir}/scripts/audit_list_health.py` — get current dormant percentage and account baselines.
2. `python3 {baseDir}/scripts/engagement_decay.py` — confirm the cohort is large enough to bother (re-engagement is only worth running if dormant >5% of list).
3. `python3 {baseDir}/scripts/stale_contact_report.py --window-days 90` — list of candidates and how long they've been dormant.
4. `python3 {baseDir}/scripts/domain_engagement_report.py` — check whether dormancy is concentrated on a specific domain (Yahoo dormancy is often a deliverability issue, not an engagement issue).
5. Read `frameworks/email-best-practices.md` and `frameworks/segmentation-theory.md` for design guidance.
6. Synthesize the spec.

## Cohort definition

Default cohort = active contacts who:
- Have NOT opened any campaign in the last 90 days, AND
- Were active at some point in the previous 365 days (so they were *real* subscribers, not dead-on-arrival imports).

The agent should adjust the 90-day threshold based on send frequency:
- High frequency (≥1 send/week) → 60-day dormant threshold
- Standard (≥1 send/month) → 90 days
- Low frequency (<1 send/month) → 120-180 days

Exclusions (always):
- Hard bounces (already deliverability-dead)
- Existing unsubscribers
- Tagged `do-not-email` or equivalent

## Sequence spec

### Email 1 — Honest re-engagement ask (Day 0)

| Element | Spec |
|---|---|
| Subject | "Are we still a fit, [first name]?" |
| Preheader | "If yes, just click below. If not, we'll move on." |
| Length | 80–120 words. The shorter the better — dormant readers don't read long emails. |
| Body | 1 sentence acknowledging the gap. 1 sentence stating what they get if they stay. 1 explicit "click here to keep getting emails" CTA. |
| CTA | Single button: "Yes, keep me on the list" → applies a `re-engaged` tag. |

### Email 2 — High-value reminder (Day 4, only if no click on Email 1)

| Element | Spec |
|---|---|
| Subject | "One more thing before we say goodbye" |
| Preheader | Specific value prop — what they'll miss. |
| Body | Show your single strongest piece of recent content (most-clicked from your last 90 days, surface via `subject_line_report.py`). |
| CTA | Same re-engage button + secondary "Show me more like this" link. |

### Email 3 — Sunset notice (Day 8, only if still no click)

| Element | Spec |
|---|---|
| Subject | "Removing you from the list tomorrow" |
| Preheader | Last chance to stay. |
| Body | Brief. State the date you'll suppress. One re-engage CTA. |
| CTA | "Keep me subscribed" — final chance. |

After Email 3 with no click: suppress (apply `auto-suppress-YYYY-MM` tag and remove from active lists).

## Success criteria

- **Re-engagement rate**: % of cohort who clicked the keep-me-on-the-list CTA.
- **Benchmark**: 3–8% is typical for a well-targeted re-engagement. Below 1% means your list health problem is bigger than re-engagement can solve.
- **Sunset rate**: contacts moved to suppression. Expect 70–90% of the cohort.

## Sample agent output

```
Re-engagement plan for testco.api-us1.com

Cohort: 1,847 contacts (39% of active list)
  Dormant 90-365 days: 1,612
  Dormant 365+ days: 235

Sequence: 3 emails over 8 days
  Day 0: "Are we still a fit, %FIRSTNAME%?" — direct ask
  Day 4: "One more thing before we say goodbye" — top performer recap
  Day 8: "Removing you from the list tomorrow" — sunset notice

Implementation in AC:
  1. Build a segment with the cohort criteria above.
  2. Build a 3-step automation: email + wait 4d + if-not-clicked + email + wait 4d + if-not-clicked + email.
  3. After the third email, apply tag `auto-suppress-2026-04` and remove from active lists.
  4. Tag every clicker with `re-engaged-2026-04` so you can monitor whether they stay engaged.

Expected outcome: ~150–250 re-engaged · ~1,600 sunsetted.
```

## Customization parameters

| Parameter | Default | Adjust if |
|---|---|---|
| Dormant threshold | 90 days | High/low send frequency |
| Cohort minimum | 5% of list | Smaller cohort = not worth the campaign |
| Sequence length | 3 emails | Tone/relationship — B2B may use 2; consumer may use 4 |
| Sunset action | Suppress | Some accounts move to a "low-frequency" segment instead |

## API limitations

- The skill cannot send the campaign — the user builds it in AC.
- Per-event open data is plan-dependent (`/messageActivities`); on plans without it, "no opens in 90 days" is approximated from `/linkData` clicks plus campaign-level metrics.
- The cohort numbers are based on the most recent calibration. Re-run `calibrate.py` if it's >7 days old.

## Outcome logging

After the spec is delivered, append to `~/.activecampaign-skill/history.jsonl`:

```jsonl
{"ts":"...","action":"recipe_delivered","recipe":"re-engagement-launch","cohort_size":1847,"dormant_pct":0.39}
```

After the user reports back on results (re-engaged count, suppressed count), append a follow-up entry with the actual numbers so future re-engagement campaigns can baseline against them.

## Related

- `frameworks/email-best-practices.md` — copy guidance.
- `frameworks/segmentation-theory.md` — cohort design.
- `recipes/welcome-series.md` — opposite end of the lifecycle.
- `recipes/list-health-audit.md` — the audit that often triggers a re-engagement.
- `scripts/engagement_decay.py`, `scripts/stale_contact_report.py` — the cohort builders.
