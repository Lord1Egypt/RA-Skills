# AI Marketing + ActiveCampaign

[![tests](https://github.com/ji282h7/activecampaign-claw/actions/workflows/test.yml/badge.svg)](https://github.com/ji282h7/activecampaign-claw/actions/workflows/test.yml)
[![python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org)
[![license](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![release](https://img.shields.io/badge/release-1.0.17-orange)](CHANGELOG.md)
[![scripts](https://img.shields.io/badge/scripts-51-success)](#what-it-can-do)
[![tests](https://img.shields.io/badge/tests-493%20passing-brightgreen)](tests/)
[![ActiveCampaign](https://img.shields.io/badge/ActiveCampaign-v3%20API-blue)](https://developers.activecampaign.com/reference)

> Unlock ActiveCampaign's core capabilities — plus 50+ deeper diagnostics — through OpenClaw. Ask in plain English; get real reports on your live account data.

## Why this exists

ActiveCampaign is a deep platform. Every contact event, list movement, campaign metric, automation step, and pipeline interaction is captured and exposed through the v3 API. This skill makes all of that accessible the way you'd actually want to use it — by just asking.

Calibration scans your taxonomy and 90 days of campaign baselines once at install, so when you ask "find me my hottest leads" or "which subject lines actually work" or "are there dead tags I should clean up," the answer comes from your real data, formatted as a marker-friendly markdown report.

ActiveCampaign already covers the core capabilities — sends, automations, lead scoring, deals, segmentation. This skill adds the analytical layer on top (40+ reports) and wires it directly into the OpenClaw agent so the workflow is conversational rather than dashboard-driven.

## What it can do

### Performance analysis (you ask, it pulls)
- **Campaign postmortems** — every metric for one send, vs. your account baseline, with per-link CTR
- **Subject line analysis** — your top performers clustered by length, emoji, urgency, personalization, and ranked by lift
- **Send time optimization** — when your specific audience opens, by hour and day of week
- **Send frequency report** — who's getting fatigued (>8 sends/month) vs. who's been forgotten
- **Domain breakdown** — engagement by Gmail / Outlook / corporate; catches deliverability problems before they snowball
- **Engagement decay** — cohort retention plot; see when your list goes dead
- **From-name performance** — which sender name actually gets opened
- **Monthly trend** — opens/clicks/unsubs/bounces over time vs. baseline
- **Baseline drift detector** — pings you when a metric drops >1σ from calibrated normal

### List & contact health
- **List health audit** — bounces, role addresses, free-vs-corporate domains, suppressions to clean up
- **Duplicate finder** — case-insensitive emails, normalized phones, fuzzy name+company
- **Role address detector** — surfaces `info@`, `support@`, `noreply@` clutter
- **Field completeness** — which contacts have which fields populated, broken down by source
- **Stale contacts** — who hasn't engaged with anything in N months
- **New subscriber quality** — recent additions opening / bouncing / unsubscribing
- **List growth forecast** — linear projection of size N days out
- **Pre-import CSV validator** — catches bad emails, duplicates, role addresses *before* you import them

### Lead scoring & sales
- **Hot leads** — ranked by engagement signals (scores, recent activity, deal stage)
- **Slipping deals** — stale, overdue, or stuck in a stage too long *(needs Deals feature)*
- **MQL→SQL handoff** — who crossed the scoring threshold and got a deal vs. who didn't *(Deals)*
- **Win/loss by source** — which lists/tags/forms produce winning pipeline *(Deals)*
- **Pipeline audit** — per-stage health, value distribution, field completeness *(Deals)*
- **Tasks audit** — overdue tasks, completion rate per user, unassigned work *(needs Plus+)*
- **Sales rep performance** — per-rep scoreboard: deals open / won / lost, win rate, tasks open + overdue, notes activity score
- **Notes analysis** — action-item extraction across all contact + deal notes, stale-note flag for deals not touched recently
- **B2B accounts audit** — orphaned accounts, no-pipeline accounts, top accounts by deal/contact count, per-owner rollup *(needs Plus+)*
- **Saved-responses audit** — inventory + near-duplicate detection across sales-rep reply templates *(needs Plus+)*

### Marketing-content hygiene
- **Template audit** — unused campaign templates, stale templates, average open rate per template
- **Forms lead quality** — engagement / bounce / unsub rates per form, ranked by quality of leads each form produces

### Automation hygiene
- **Audit** — orphaned automations (active but enrolling no one), completion rates
- **Funnel** — per-step dropoff inside one automation
- **Overlap** — contacts in 3+ active automations (un-coordinated programs)
- **Stalled enrollments** — contacts whose step hasn't advanced in N days (broken Wait or If/Else)
- **Dependency map** — which automations enroll into which others
- **Broken-ref detector** — refs to deleted tags / fields / messages

### Tag, field, list & segment hygiene
- **Tag audit** — typo tags, dead tags (no automation/segment uses them), consolidation candidates that always co-occur
- **Custom field audit** — zombie fields, low-use fields, which are referenced in automations
- **Per-list audit** — size, last campaign sent, opt-in source
- **List overlap matrix** — which lists are subsets of others (probably duplicate-ish)
- **Segment audit** — empty segments, segments referencing deleted assets
- **Form audit** — quality of each form by downstream contact engagement

### Compliance & ops
- **Unsubscribe / opt-in audit** — every campaign has a working unsub link, every form mentions opt-in
- **Suppression export** — all unsubs + bounces with timestamps (for compliance audits, ESP migration)
- **per-contact data export** — full export of everything AC has on one contact
- **Webhook audit** — inventory + reachability probe of every configured webhook
- **Account snapshot** — full taxonomy export to JSON, versioned weekly via cron
- **Schema diff** — what changed between two snapshots (added/removed/renamed)

### Strategic advice (no API calls — domain knowledge)
- "Should this be a tag, custom field, or list?"
- "Why is my open rate dropping?"
- "What's a good RFM scoring model for a B2B account?"
- Welcome series / re-engagement / drip campaign **specs** that you build in the AC UI

## API scope

ActiveCampaign's v3 API is designed around records and integrations, not send/build operations. A few things to know about how this skill fits:

- **Campaigns and automations are built in the AC UI.** The v3 API focuses on reading and modifying records, so this skill produces clear specs you implement in AC's visual builders — which is where they belong anyway.
- **Spam complaint data is plan-tier dependent.** Engagement reports use bounce and unsub trends as solid proxies that work across all AC plans.
- **Per-event open data depends on your plan.** When `/messageActivities` returns 404, engagement reports automatically fall back to `/linkData` for click-by-domain breakdowns.
- **Deal time-in-stage** is computed from current state and recent activity windows; pipeline reports surface the most actionable view.
- **Deals-dependent reports** (`pipeline_audit`, `mql_to_sql_handoff`, `win_loss_report`) work on AC plans that include the Deals feature; they exit cleanly with a clear message otherwise.

## Performance & scale

Most reports scale freely with account size — they're bounded by taxonomy (lists, tags, fields, automations) or campaign count, not contact count. Calibration finishes in ~1 minute on accounts of any size because it reads counts from `meta.total` rather than scanning rows.

A handful of contact-scanning reports cap at 5k–20k by default to keep runtime reasonable: `dedupe_contacts`, `role_address_finder`, `free_vs_corporate_report`, `contact_completeness_report`, `stale_contact_report`. Raise the cap with `--max-contacts`, or scope to a single list / tag / segment first — most marketing questions are cohort-scoped anyway.

For accounts with 100k+ contacts, full-account scans are slow (roughly 1 hour per 150k contacts at AC's default 5 req/sec rate limit). See [SCALING.md](SCALING.md) for runtime math, memory profile, and recommended workflows.

## Quick start (5 minutes)

```bash
# 1. Install the skill
openclaw skills install ji282h7/activecampaign-claw

# 2. Get your AC API URL + token: https://help.activecampaign.com/hc/en-us/articles/207317590
#    Then set them
openclaw config set env.vars.AC_API_URL "https://YOURACCOUNT.api-us1.com"
openclaw config set env.vars.AC_API_TOKEN "YOUR-TOKEN"
openclaw gateway restart

# 3. Calibrate (one-time, ~1 minute)
python3 ~/.openclaw/skills/activecampaign/scripts/calibrate.py

# 4. Try it
#    In an OpenClaw session, ask: "Run a list health audit on my AC account"
```

Full instructions: [INSTALL.md](INSTALL.md)

## How it's organized

```
activecampaign/
├── SKILL.md                      ← agent's spec (decision tree, triggers, rules)
├── README.md                     ← you are here
├── INSTALL.md                    ← step-by-step setup
├── CHANGELOG.md
├── scripts/                      ← 50 executable scripts (run directly or via agent)
│   ├── calibrate.py              ← one-time account scan
│   ├── audit_list_health.py
│   ├── find_hot_leads.py
│   ├── find_slipping_deals.py
│   ├── campaign_postmortem.py
│   ├── tag_audit.py
│   ├── automation_funnel.py
│   ├── … 43 more …
│   └── _ac_client.py             ← shared HTTP client with rate-limit handling
├── recipes/                      ← agent-driven workflows
│   ├── daily-digest.md
│   ├── deal-hygiene.md
│   ├── list-health-audit.md
│   └── welcome-series.md
├── frameworks/                   ← embedded marketing knowledge
│   ├── email-best-practices.md
│   └── segmentation-theory.md
├── references/                   ← AC API endpoint docs
│   ├── contacts.md
│   ├── deals.md
│   └── custom-fields.md
└── tests/
```

## Examples

### Analysis — *"Find my hottest leads"*

The agent ranks contacts by a composite of AC lead score, recent engagement velocity, deal-stage progression, and content depth — not just raw score:

| Rank | Name | Score | Top signal | Action |
|---|---|---|---|---|
| 1 | Jane S. | 92 | Opened proposal email 3× yesterday + visited pricing page | Call today |
| 2 | Bob L. | 85 | Deal created 2 days ago, score jumped +18 in 7 days | Confirm BANT, send proposal |
| 3 | Priya S. | 78 | Trial signup + 4 page views, downloaded whitepaper | Welcome call, qualify use case |

The "top signal" column is what makes this useful — it's the *reason* the lead is hot, not just a number. You walk into the call already knowing what they care about.

### Maintenance — *"Merge my duplicate tags"*

The tag audit catches behavioral duplicates that string-similarity tools miss — pairs of tags applied to the same contacts with different names:

```
Tag audit — your account has 247 tags

Likely duplicates (95%+ co-occurrence)
• customer + Customer — co-occur on 1,847 contacts (case-mismatch)
• webinar-attendee + webinar_attendee — co-occur on 312 contacts (separator typo)
• vip + high-value-customer — co-occur on 89 contacts (semantic duplicate)

Over-saturated tags (>50% of contacts — bad for filtering)
• subscriber (96%)
• imported-2024 (62%)

Dead tags (not used in any automation or segment): 34
```

Then you can resolve any of them in the same conversation:

> **You:** Merge `customer` and `Customer` into the lowercase one.
>
> **Agent:** Here's the plan:
> 1. Apply `customer` to the 12 contacts that only have `Customer`
> 2. Remove `Customer` from all 1,847 affected contacts
> 3. Update 3 automation references (`Welcome Series`, `Renewal Nudge`, `NPS Follow-up`) to point at `customer`
> 4. Delete the `Customer` tag
>
> Total: 1 tag delete · 1,859 contact-tag updates · 3 automation patches. Confirm to proceed?

The destructive operations always require explicit confirmation — the agent shows the full plan first. The standalone script (`scripts/tag_merge.py`) follows the same contract: dry-run by default, `--confirm` required to execute, refuses to delete a tag that's still referenced by an automation or segment.

For more examples (subject-line lift analysis, list health audits, stalled-automation detection, re-engagement campaigns), browse the workflow recipes in [`recipes/`](recipes/).

## Where data lives

All data stays local on your machine:
- `~/.activecampaign-skill/state.json` — your calibrated taxonomy + baselines
- `~/.activecampaign-skill/history.jsonl` — record of recipes/scripts you've run
- `~/.activecampaign-skill/insights.md` — accumulated findings the agent surfaces back

Nothing is sent anywhere except your own AC account via your own token. No third-party gateways, no telemetry.

## Privacy & security

- Use a dedicated integration user when generating your token (tokens are scoped to the user that created them).
- Token storage: `~/.openclaw/openclaw.json` (file mode 0600). Be aware it's in plaintext on disk.
- Sanitization: API response data (contact names, deal titles, tag names) is sanitized before rendering to prevent markdown injection.
- The skill includes destructive operation guards: every `POST`/`PUT`/`DELETE` shows you the payload and waits for explicit confirmation before executing.

## License

MIT-0 (MIT No Attribution) — see [LICENSE](LICENSE).

## Contributing

Issues and PRs welcome at https://github.com/ji282h7/activecampaign-claw

## Credits

Built on top of [OpenClaw](https://openclaw.ai) skill framework. ActiveCampaign v3 API documentation: https://developers.activecampaign.com/reference
