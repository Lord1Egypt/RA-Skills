---
name: activecampaign-claw
displayName: "ActiveCampaign (50+ Capabilities)"
version: 1.9.4
license: MIT-0
author: ji282h7
summary: "ActiveCampaign agent for marketers + sales: 50+ reports for list, campaign, automation, and pipeline analysis."
description: "ActiveCampaign agent for marketers + sales: list health, lead scoring, deliverability, campaign postmortems, automation diagnostics, and 40+ more reports."
homepage: https://github.com/ji282h7/activecampaign-claw
repository: https://github.com/ji282h7/activecampaign-claw
keywords:
  - activecampaign
  - email-marketing
  - marketing-automation
  - crm
  - lead-scoring
  - deliverability
  - segmentation
  - drip-campaign
  - list-hygiene
  - campaign-analytics
  - subject-line-testing
  - send-time-optimization
  - re-engagement
  - welcome-series
  - sales-ops
tags:
  - marketing
  - sales
  - crm
  - email
  - automation
  - analytics
  - reporting
user-invocable: true
argument-hint: "what would you like to do in ActiveCampaign?"
allowed-tools:
  - Bash
  - Read
when_to_use:
  # daily / strategic — explicit AC-scoped requests
  - "run my ActiveCampaign daily-digest recipe"
  - "design a welcome-series email sequence for ActiveCampaign (spec only — user builds in AC UI)"
  - "find slipping deals in my ActiveCampaign pipeline"
  - "audit my ActiveCampaign list health and deliverability"
  - "rank my ActiveCampaign contacts by lead score"
  - "show overdue deals in my ActiveCampaign account"
  - "calibrate my ActiveCampaign account or refresh local state.json"
  # contact + deal lookups (read)
  - "look up a contact in ActiveCampaign or check their profile"
  - "review the tags applied to a contact"
  - "see what lists a contact is on"
  - "see what automations a contact has been enrolled in"
  - "check bounce logs or contact scores"
  - "look up custom field values on a contact or deal"
  - "review or analyze a deal in the pipeline"
  - "filter deals by pipeline, stage, owner, or status"
  - "what's my pipeline value, deal count, or stage distribution"
  - "list my pipelines, stages, automations, tags, or custom fields"
  # marketing strategy
  - "who should I send this email to or how should I segment my list"
  - "help me write a subject line or improve email open rates"
  - "why is my open rate, click rate, or deliverability dropping"
  - "what's the best day or time to send emails"
  - "should this be a tag, custom field, or list in ActiveCampaign"
  - "design engagement tiers, RFM scoring, or lifecycle segments"
  - "re-engagement campaign for dormant or inactive contacts"
  - "review bounce handling and suppression status"
  - "email copy advice, CTA design, or campaign content review"
  # Performance analysis
  - "campaign postmortem / breakdown / report on my last send"
  - "compare two campaigns side by side"
  - "per-link performance / which link got the most clicks"
  - "bounce decomposition / why are emails bouncing"
  - "monthly campaign performance trend"
  - "are my metrics drifting / detect baseline drift"
  - "campaign send velocity / how often am I mailing"
  - "subject line analysis / which subject patterns get opened"
  - "content length and CTA correlation"
  - "performance by from-name or reply-to address"
  - "best time of day to send / send time optimization"
  - "send frequency per contact / fatigue risk"
  - "engagement by recipient domain (Gmail vs Outlook etc)"
  - "engagement decay / cohort retention"
  - "stale contacts who have not engaged"
  - "new subscriber quality / are recent additions engaging"
  - "performance for one segment / list / tag"
  - "MQL to SQL handoff diagnostics"
  - "win loss report by source"
  - "predict outcomes for a planned send / send simulator"
  - "list growth forecast"
  # Operational
  - "tag audit / dead tags / typo tags"
  - "custom field audit / unused fields"
  - "list audit / which lists are stale"
  - "list overlap / which lists duplicate each other"
  - "segment audit / empty or broken segments"
  - "pipeline audit / per-stage health"
  - "automation audit / orphaned automations"
  - "automation funnel / step-by-step dropoff"
  - "automation overlap / contacts in multiple flows"
  - "stalled automation enrollments"
  - "form audit / quality by form source"
  - "find duplicate contacts"
  - "contact completeness / which fields are populated"
  - "find role addresses (info@, support@, etc.)"
  - "free mail vs corporate domain split"
  - "validate a CSV before importing"
  - "archive the AC account taxonomy locally for diff / audit use"
  - "diff two account snapshots"
  - "audit webhooks / are webhook URLs reachable"
  - "unsubscribe / opt-in compliance audit"
  - "export all suppressed contacts"
  - "per-contact data export"
context:
  - "~/.activecampaign-skill/state.json"
  - "~/.activecampaign-skill/insights.md"
metadata: {"openclaw":{"emoji":"📨","requires":{"bins":["python3"],"env":["AC_API_URL","AC_API_TOKEN"]},"primaryEnv":"AC_API_TOKEN","os":["darwin","linux"]}}
---

# AI Marketing + ActiveCampaign

Direct integration with ActiveCampaign's v3 API, built to operate the way an experienced marketer and sales lead actually thinks. Calibration scans your account once at install (taxonomy + 90-day campaign baselines); 50+ scripts then answer questions against your live data in plain English.

## What it does

**Performance analysis** — campaign postmortems, subject-line analysis, send-time optimization, send-frequency / fatigue, domain breakdown (Gmail vs. Outlook vs. corporate), engagement decay, from-name performance, monthly trend, baseline-drift detection.

**List & contact health** — list audits, duplicate finder, role-address detector, field completeness, stale contacts, new-subscriber quality, list-growth forecast, pre-import CSV validator.

**Lead scoring & sales** — hot leads ranked by composite signals, slipping deals, MQL→SQL handoff, win/loss by source, pipeline audit. *(Deals-dependent reports require an AC plan that includes Deals; they exit cleanly otherwise.)*

**Automation hygiene** — orphaned-automation audit, per-step funnel dropoff, multi-automation overlap, stalled enrollments, dependency map, broken-reference detector.

**Tag / field / list / segment hygiene** — tag audit (typos, dead tags, co-occurrence consolidation), custom-field audit, per-list audit, list-overlap matrix, segment audit, form audit.

**Compliance & ops** — unsubscribe / opt-in audit, suppression export, Per-contact data export, webhook audit, account snapshot, schema diff between snapshots.

**Sales / CRM** — overdue tasks audit, per-rep performance scoreboard (deals + tasks + notes), notes content analysis (action-item extraction, stale-note detection), saved-responses audit, B2B accounts audit (orphaned / no-pipeline / owner rollup). *(Plus+ for Tasks, Saved Responses, B2B Accounts.)*

**Marketing-content hygiene** — campaign template audit (unused / stale / per-template open rate), per-form lead quality.

**Strategic advice (no API calls)** — "should this be a tag, custom field, or list?", "why is my open rate dropping?", welcome / re-engagement / drip campaign **specs** you implement in the AC UI.

## Operating model

> **Scope:** This skill operates against the AC account whose token you provide. It reads and (with explicit user confirmation) modifies records inside *that account only*. There is no cross-account access, no third-party data transmission, and no telemetry. All data — reports, exports, snapshots, history — is written to local files on your own machine.

The skill is **analysis-first**. Most of the 60+ scripts in `scripts/` are read-only: they pull data, produce a report, and exit.

**Write capabilities — explicitly declared:** A small number of scripts can modify records in the AC account when you ask for them. These include contact updates, contact tagging, list subscription changes, automation enrollment, deal updates, custom-field value updates, and tag-merge operations. Every modification flows through one auditable code path with the following guarantees:

1. **Use a least-privileged AC integration user** (see `INSTALL.md`). Admin is not required and not recommended; the token's blast radius should match what you intend to run.
2. **Single audited write path.** `ACClient.post / put / delete` all route through one `write()` helper that enforces the rules below and records every modification.
3. **Optional `AC_READ_ONLY=1` env var.** When set, every write is refused at the client layer before any HTTPS request goes out. Lets you run the entire script suite in pure-analysis mode without risk.
4. **Per-process write cap (default 10).** Override with `AC_MAX_WRITES=<n>` if intended. A runaway script can't perform more than the budget allows in one invocation.
5. **Audit log** at `~/.activecampaign-skill/writes.jsonl` (file mode 0600). Every write records timestamp, endpoint, method, payload SHA-256 (NOT payload), invoking script, and sequence number.
6. **Explicit confirmation before any POST / PUT / DELETE.** The agent shows the endpoint, the JSON payload, and a plain-English summary. Nothing proceeds without your explicit "yes."
7. **Deletes require their own confirmation step**, with a description of what is lost and a statement that the action is permanent.
8. **Destructive helpers (e.g. `tag_merge.py`) are dry-run by default**; `--confirm` is required to execute, and they refuse to operate on anything still referenced by an active automation or segment.
9. **All modification calls go through the Python client** (`scripts/_ac_client.py`), which sanitizes API-sourced values before any subprocess call to prevent shell injection.

When asked, the skill can act on contacts, deals, custom-field values, and tags — but only behind those gates, scoped to the records you specify, and previewed first.

## Local files and data retention

Calibration, history, and any reports written via `--output` produce local files only. The skill never transmits data to a third party. Files live under `~/.activecampaign-skill/` with mode `0600` and are owned by the running user:

| File | Purpose | Created by | Retention |
|---|---|---|---|
| `state.json` | Calibrated taxonomy + 90-day baselines | `calibrate.py` | Until you recalibrate or delete it |
| `history.jsonl` | Append-only log of recipe/script runs (no contact PII; just operation metrics) | Most scripts via `log_outcome()` | Manual — see below |
| `insights.md` | Persistent findings from prior runs | Scripts via `write_insight()` | Manual |
| `writes.jsonl` | Audit log of POST/PUT/DELETE operations (payload hash, not payload) | `_ac_client.write()` | Manual |
| `snapshots/*.json` | Versioned account snapshots | `snapshot.py`, `account_archive.py` | Manual |

All files can be inspected with normal text tools and deleted by removing the directory. Recommended retention: prune `history.jsonl` and snapshots every 90 days unless you need longer-term trend analysis. No data is sent off your machine.

To wipe everything the skill has stored locally:

```bash
rm -rf ~/.activecampaign-skill/
```

## Examples

**"Find my hottest leads"** — ranks contacts by a composite of AC lead score, recent engagement velocity, deal-stage progression, and content depth. Output includes a "top signal" column explaining *why* each lead is hot, so you walk into the call already knowing what they care about.

**"Merge my duplicate tags"** — catches behavioral duplicates that string-similarity tools miss. Surfaces case-mismatch (`customer` + `Customer`), separator typos (`webinar-attendee` + `webinar_attendee`), and semantic duplicates (`vip` + `high-value-customer`) by co-occurrence on the same contacts. Then resolves them in-conversation: applies the survivor tag, removes the dupe, patches automation references, and deletes the dead tag — with explicit confirmation before each destructive step.

**"Run my morning briefing"** — pulls a daily digest off your account: yesterday's campaign metrics vs. baseline, hot-lead changes since last check, slipping deals that crossed the staleness threshold overnight, automations with new stalled enrollments, and any baseline-drift alerts.

For more examples (subject-line lift analysis, list health audits, stalled-automation detection, re-engagement campaigns), see the workflow recipes in `recipes/`.

## What makes this skill different

1. **Account calibration** — `scripts/calibrate.py` scans your AC account and writes a state file (taxonomy, baselines, patterns). Every conversation starts with context, not a cold start.
2. **Workflow recipes** — `recipes/` contains parameterized workflows (welcome series, list audit, deal hygiene, daily digest) instead of bare endpoints.
3. **Embedded domain knowledge** — `frameworks/` contains what a senior marketer or sales leader knows: email best practices, segmentation theory, deliverability patterns.
4. **Executable audit scripts** — `scripts/` contains tools that run analyses and return markdown reports (list health, hot leads, slipping deals).
5. **Outcome logging** — every recipe execution writes to `~/.activecampaign-skill/history.jsonl` so future runs can compare to past performance.

## Setup

Get credentials from **Settings → Developer** in your AC account:

```bash
export AC_API_URL=https://youraccount.api-us1.com
export AC_API_TOKEN=your-api-token
```

**On first install, run calibration:**

```bash
python3 {baseDir}/scripts/calibrate.py
```

This builds `~/.activecampaign-skill/state.json` with your account's lists, tags, custom fields, pipelines, automations, and 90-day performance baselines. Re-run monthly.

Two gotchas:
- **Auth header is `Api-Token`, not `Bearer`.** The #1 reason custom integrations fail.
- **Tokens are scoped to the creating user.** Use a dedicated integration user.

## First interaction

When the user invokes this skill and `~/.activecampaign-skill/state.json` does not exist, this is a first-run. Follow this flow:

### Step 1: Welcome and calibrate

Greet the user and explain what calibration does in one sentence: "Let me scan your ActiveCampaign account so I can give you advice grounded in your actual data." Then run:

```bash
python3 {baseDir}/scripts/calibrate.py
```

### Step 2: Narrate the discovery

After calibration completes, read the script's output and `state.json`. Present a conversational account briefing — not a data dump. Narrate what you found as if you're a new team member who just studied their account:

- Name the lists, top tags, and pipeline stages by name — show you know their setup
- Translate baselines into plain language: "Your open rate is 28% — that's well above industry average" or "Your unsub rate is high at 0.7% — worth investigating"
- Mention their best send days and times as a practical tip
- Call out anything notable: no active automations, strong list growth, high bounce rate
- End with one quick-win suggestion based on what the data shows

Keep it to 8-12 lines. Conversational, not clinical.

### Step 3: Ask their role

After the briefing, ask: **"Are you primarily focused on marketing or sales?"** Then show the matching capability menu below.

### Marketing menu

"Here's what I can do for you right now:"

> Note: items marked **(spec)** produce a written blueprint — subject lines, timing, segmentation, copy — that you assemble in the AC UI. The v3 API does not allow creating automations or sending campaigns.

1. **List health audit** — Check your subscriber quality, bounce rates, and domain concentration. Flags contacts to suppress.
2. **Campaign performance review** — Compare your recent sends against your baselines. Surface what's working and what's not.
3. **Welcome series spec** — Produce an onboarding email sequence blueprint (emails, timing, triggers, copy) tuned to your send-time patterns and audience. **You build the automation in AC.**
4. **Subject line analysis** — Review your top-performing subjects and suggest patterns to replicate.
5. **Re-engagement campaign spec** — Identify dormant contacts worth one more attempt and produce a win-back flow blueprint. **You build the automation in AC.**
6. **Daily digest** — Get a morning briefing with campaign results, list growth, and action items.

### Sales menu

"Here's what I can do for you right now:"

1. **Deal pipeline hygiene** — Surface stale deals, missing data, and slipping close dates. Prioritized by value.
2. **Hot leads** — Rank your contacts by engagement signals. See who to call today.
3. **Daily briefing** — Deals needing attention, top leads, pipeline snapshot, and today's action items.
4. **Pipeline snapshot** — Stage distribution, total value, and velocity. Spot bottlenecks.
5. **Contact enrichment** — Look up a contact's full profile: tags, custom fields, deals, and scores.
6. **Deal updates** — Move deals between stages, add notes, or update close dates via the API.

### Returning users

If `state.json` exists and is fresh, skip the welcome flow. Jump straight to answering the user's question. If `state.json` is >30 days old, suggest recalibration before proceeding but don't block.

## How to use this skill

### Decision tree — "I want to do X"

#### Quick lookups (prefer these for single-record questions)

These are sub-second single-call scripts. Use them whenever the user is asking about **one specific thing** — don't reach for the audit scripts.

| If the user wants to... | Run |
|---|---|
| Look up a contact by email | `scripts/contact_lookup.py --email <email>` |
| Look up a contact by ID | `scripts/contact_by_id.py <id>` |
| Get the most recent N contacts | `scripts/contact_recent.py [--limit N]` |
| **Most engaged / top scoring contacts** (fast) | `scripts/contact_most_engaged.py [--limit N] [--by score\|recent]` |
| **Contacts with the most clicks / opens** (real engagement events) | `scripts/contact_engagement_leaders.py [--by clicks\|opens\|both] [--window-days N] [--limit M]` |
| Full profile on one contact (compound) | `scripts/contact_full_profile.py --email\|--id` |
| Look up a deal by ID | `scripts/deal_by_id.py <id>` |
| Full context on one deal (compound) | `scripts/deal_full_context.py <id>` |
| Deep-dive on an automation | `scripts/automation_deep_dive.py <id>` |
| Find a tag id by name | `scripts/tag_lookup.py --name <name>` *(checks state.json first; no API call if cached)* |
| Find an automation id by name | `scripts/automation_lookup.py --name <name>` *(state.json first)* |
| See the most recent campaign send | `scripts/last_campaign.py` |

**When the user asks "find / look up / what's the id / what's the most recent" — prefer these over the audit scripts. The audits paginate thousands of records; these single-call scripts return in <1s.**

#### Recipe-driven workflows

| If the user wants to... | Load | Or use endpoint |
|---|---|---|
| Audit list quality | `recipes/list-health-audit.md` + `scripts/audit_list_health.py` | — |
| Find hot leads | `scripts/find_hot_leads.py` | — |
| Surface slipping deals | `scripts/find_slipping_deals.py` | — |
| Get a morning briefing | `recipes/daily-digest.md` | — |
| Spec a welcome series (user builds in AC UI) | `recipes/welcome-series.md` + `frameworks/email-best-practices.md` | — |
| Clean up the pipeline | `recipes/deal-hygiene.md` + `scripts/find_slipping_deals.py` | — |

#### Direct API operations

| If the user wants to... | Load | Or use endpoint |
|---|---|---|
| Sync a contact | `references/contacts.md` | `POST /contact/sync` |
| Create/update a deal | `references/deals.md` | `POST /deals` |
| Read/write custom fields | `references/custom-fields.md` | `fieldValues`, `dealCustomFieldData` |
| Tag a contact | `references/contacts.md` | `POST /contactTags` |
| Enroll in automation | `references/contacts.md` | `POST /contactAutomations` |
| Understand segmentation | `frameworks/segmentation-theory.md` | — |
| Email copy/design advice | `frameworks/email-best-practices.md` | — |

#### Performance analysis scripts

| If the user wants to... | Run |
|---|---|
| Postmortem on one campaign | `scripts/campaign_postmortem.py <campaign_id>` |
| Compare two campaigns | `scripts/campaign_compare.py <id_a> <id_b>` |
| Per-link performance for a campaign | `scripts/link_performance.py <campaign_id>` |
| Bounce decomposition (global or per-campaign) | `scripts/bounce_breakdown.py [--campaign <id>]` |
| Monthly performance trend | `scripts/monthly_performance.py [--months N]` |
| Detect baseline drift vs. calibration | `scripts/baseline_drift.py [--window-days N]` |
| Send velocity per list | `scripts/campaign_velocity.py [--window-days N]` |
| Subject line pattern analysis | `scripts/subject_line_report.py [--days N]` |
| Content length / CTA correlation | `scripts/content_length_report.py [--days N]` |
| Performance by from-name / from-email | `scripts/from_name_report.py [--days N]` |
| Best send window | `scripts/send_time_optimizer.py` |
| Sends-per-contact distribution | `scripts/send_frequency_report.py [--window-days N]` |
| Engagement by recipient domain | `scripts/domain_engagement_report.py` |
| Cohort retention | `scripts/engagement_decay.py [--months N]` |
| Stale contacts | `scripts/stale_contact_report.py [--window-days N]` |
| New subscriber engagement | `scripts/new_subscriber_quality.py [--days N]` |
| Audience-cut performance | `scripts/segment_performance.py --list/--tag/--segment <id>` |
| MQL→SQL handoff diagnostics | `scripts/mql_to_sql_handoff.py [--threshold N --days N]` *(needs Deals)* |
| Win/loss by source | `scripts/win_loss_report.py [--days N]` *(needs Deals)* |
| Predict outcomes for planned send | `scripts/send_simulator.py --list/--tag/--segment <id>` |
| Project list growth | `scripts/list_growth_forecast.py [--project-days N]` |

#### Operational / hygiene scripts

| If the user wants to... | Run |
|---|---|
| Tag hygiene audit | `scripts/tag_audit.py` |
| Custom field audit | `scripts/custom_field_audit.py` |
| Per-list audit | `scripts/list_audit.py` |
| List overlap matrix | `scripts/list_overlap.py` |
| Saved-segment audit | `scripts/segment_audit.py [--skip-counts]` |
| Pipeline / stage audit | `scripts/pipeline_audit.py` *(needs Deals)* |
| Automation audit | `scripts/automation_audit.py [--window-days N]` |
| Per-automation funnel | `scripts/automation_funnel.py <automation_id>` |
| Cross-automation overlap | `scripts/automation_overlap.py` |
| Stalled enrollments | `scripts/stalled_automations.py [--min-days N]` |
| Form audit | `scripts/form_audit.py` |
| Find duplicate contacts | `scripts/dedupe_contacts.py` |
| Contact field completeness | `scripts/contact_completeness_report.py` |
| Find role addresses | `scripts/role_address_finder.py` |
| Free-mail vs. corporate split | `scripts/free_vs_corporate_report.py` |
| Validate a CSV pre-import | `scripts/import_validator.py <csv>` |
| Snapshot the account | `scripts/snapshot.py [--scope taxonomy/contacts/deals/all]` |
| Local account archive | `scripts/account_archive.py [--scope ...]` |
| Diff two snapshots | `scripts/schema_diff.py <a.json> <b.json>` |
| Webhook inventory + reachability | `scripts/webhook_audit.py [--skip-probe]` |
| Unsubscribe / opt-in compliance | `scripts/unsubscribe_audit.py` |
| Export suppressed contacts | `scripts/suppression_export.py` |
| Raw per-contact data export | `scripts/contact_data_export.py <email>` |

#### Sales / CRM scripts

| If the user wants to... | Run |
|---|---|
| Audit overdue tasks + per-user workload | `scripts/tasks_audit.py` *(needs Plus+)* |
| Analyze contact + deal notes (action items, stale notes) | `scripts/notes_analysis.py [--stale-days N]` |
| Per-rep performance scoreboard (deals + tasks + notes) | `scripts/sales_rep_performance.py` |
| Audit campaign email templates (unused, stale, performance) | `scripts/template_audit.py [--stale-days N]` |
| Audit saved-response library (sales reply templates) | `scripts/saved_responses_audit.py` *(needs Plus+)* |
| B2B accounts audit (orphaned, no-pipeline, owner rollup) | `scripts/accounts_audit.py` *(needs Plus+)* |
| Per-form lead quality (subscribelist proxy) | `scripts/forms_lead_quality.py [--window-days N]` |

### Layer 1: Recipes (workflow-level)

In `recipes/`. Each is a parameterized workflow. The agent reads the recipe + invokes any associated script.

### Layer 2: Frameworks (domain knowledge)

In `frameworks/`. Loaded when the conversation needs strategic thinking:
- "Should this be a tag or a custom field?" → `frameworks/segmentation-theory.md`
- "Why is open rate dropping?" → `frameworks/email-best-practices.md`

### Layer 3: References (endpoint docs)

In `references/`. Standard API reference for when the agent needs to make a specific call.

## The state file

`~/.activecampaign-skill/state.json` (built by `scripts/calibrate.py`) contains:

```json
{
  "schema_version": 1,
  "account": {"url": "...", "regional_host": "api-us1"},
  "taxonomy": {
    "lists": [...], "tags": [...], "custom_fields": {...},
    "pipelines": [...], "automations": [...]
  },
  "baselines": {
    "open_rate_p50": 0.28, "click_rate_p50": 0.04,
    "best_send_window_utc": ["14:00", "15:00"],
    "best_send_dow": ["Tue", "Wed", "Thu"]
  },
  "last_calibrated": "2026-04-24T12:00:00Z"
}
```

No PII is stored in the state file. All taxonomy values are sanitized on write.

**Always read this before answering account-specific questions.** If the file doesn't exist or is >30 days old, prompt the user to run calibration.

## The history file

`~/.activecampaign-skill/history.jsonl` — append-only log of recipes executed and decisions made. Read it to ground responses in actual past performance.

## The insights file

`~/.activecampaign-skill/insights.md` — persistent markdown file of significant findings. Written by scripts when they detect notable patterns (3+ consecutive metric declines, new risks, milestones). Unlike history.jsonl (structured data), insights.md captures human-readable analysis that grounds the agent's recommendations across sessions and survives conversation compaction.

## Quick reference: most common operations

**Upsert a contact:**
```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contact":{"email":"jane@example.com","firstName":"Jane","lastName":"Doe"}}' \
  "$AC_API_URL/api/3/contact/sync" | jq
```

**Tag a contact** (look up tag ID from state.json):
```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contactTag":{"contact":"123","tag":"42"}}' \
  "$AC_API_URL/api/3/contactTags" | jq
```

**Enroll in automation:**
```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contactAutomation":{"contact":"123","automation":"7"}}' \
  "$AC_API_URL/api/3/contactAutomations" | jq
```

## When to invoke this skill (routing rules for the agent)

**Use this skill when:**

- The user mentions ActiveCampaign, AC, or their AC account
- The user asks about contacts, deals, tags, lists, pipelines, automations, or custom fields in a CRM context
- The user wants to audit list health, find hot leads, surface slipping deals, or run a daily digest
- The user asks about email campaign design, welcome series, re-engagement flows, or send-time optimization
- The user mentions any of the scripts in `scripts/` (e.g. `calibrate.py`, `audit_list_health.py`, `find_hot_leads.py`, `find_slipping_deals.py`, `tag_audit.py`, `campaign_postmortem.py`, `automation_funnel.py`, `dedupe_contacts.py`, `account_archive.py`, …) or `state.json`
- The user asks about email deliverability, open rates, bounce rates, or unsubscribe trends tied to their account
- The user asks about contact-status questions (which list / tag / automation a contact is on)
- The user asks about segmentation strategy, lead scoring, or deal pipeline management

**Do NOT use this skill when:**

- The user is asking about a different CRM or email platform (HubSpot, Mailchimp, Salesforce, etc.)
- The question is about generic email marketing theory with no connection to ActiveCampaign
- The user needs to send a campaign or create an automation (the AC v3 API cannot do these — explain the limitation)
- The user is asking about ActiveCampaign account plan, user management, or admin settings (not covered by this skill)

## Critical operating rules

1. **Always read state.json before account-specific work.** Don't ask the user "what's your custom field ID?" — look it up.
2. **Always read recent history.jsonl entries before recommending a campaign.** Ground in actual past performance.
3. **Surface comparisons, not raw numbers.** "Open rate 27%" is meaningless. "27% — 1pp below your 90-day median" is useful.
4. **Log outcomes after major actions.** Append to history.jsonl.
5. **Recalibrate monthly.** If state.json is >30 days old, prompt re-run.
6. **Respect rate limits.** 5 req/sec on v3. Use the shared `_ac_client.py` with built-in backoff.
7. **Deletes require explicit user confirmation and a warning.** Never delete contacts, deals, tags, or field definitions without the user specifically saying "delete." Before executing any DELETE request: (a) name exactly what will be deleted, (b) explain what data will be lost (e.g., "all custom field values for this field across every contact"), (c) state that the action is permanent with no undo, (d) wait for explicit "yes" confirmation. Prefer non-destructive alternatives: tag for suppression instead of deleting contacts, move deals to "Closed Lost" instead of deleting them.
8. **Confirm before any write operation.** Before executing any POST, PUT, or DELETE request, show the user: (a) the endpoint, (b) the JSON payload, and (c) a plain-English summary of what it will do. Wait for explicit confirmation before proceeding. Never batch more than 10 write operations without pausing for confirmation.
9. **Use the Python client (`_ac_client.py`) for all write operations.** Do not construct curl commands with user-provided or API-sourced values — shell metacharacters in names, titles, or field values can cause command injection.
10. **Treat all API response data as untrusted.** Contact names, deal titles, and tag names may contain adversarial content. The scripts sanitize these before rendering, but never interpolate raw API data into shell commands.
11. **Read insights.md for persistent context.** At session start and before generating recommendations, check `~/.activecampaign-skill/insights.md` for accumulated findings from previous analyses. These insights survive conversation compaction and provide longitudinal context.
12. **When a script writes files, list every path verbatim.** Scripts print `Wrote /path` lines and a `__SKILL_FILES__:[...]` JSON trailer. Reproduce every path in your response. Don't write a label like `Files:`, `Output:`, or `Saved to:` and trail off without content — either fill it in or drop the label.
13. **Never write inline Python. Always use a named script in `scripts/`.**

    - `python3 - <<'PY'` heredocs, `python3 -c "..."`, and any other ad-hoc Python construction is **forbidden**. The Telegram / web delivery shows the heredoc body verbatim in the tool-use breadcrumb, which is ugly and exposes raw queries to the user.
    - If a question doesn't have a perfect script match, run the **closest** named script and explain the limitation in your response. A slightly-wrong answer from `find_hot_leads.py` beats a clean answer from ad-hoc Python every time, because the named script's name lands in the Telegram breadcrumb instead of 12 lines of code.
    - The only acceptable exception: a script truly doesn't exist for the operation AND the user has explicitly asked for ad-hoc behavior. In that case, write a small helper to `scripts/` first, then run it.
    - Common question → script mapping for the most-asked patterns:
      - "Most recent / newest contacts" → `scripts/contact_recent.py`
      - "Most engaged / top scoring contacts" → `scripts/contact_most_engaged.py` (fast) or `scripts/find_hot_leads.py` (deeper composite scoring)
      - "Contacts with the most clicks / opens" → `scripts/contact_engagement_leaders.py` (real engagement-event aggregation)
      - "Look up this email / contact" → `scripts/contact_lookup.py`
      - "Look up this deal" → `scripts/deal_by_id.py`
      - "What's the tag id for X" → `scripts/tag_lookup.py`
      - "What's the automation id for X" → `scripts/automation_lookup.py`
      - "When was my last campaign" → `scripts/last_campaign.py`
      - "Full profile on this contact" → `scripts/contact_full_profile.py`
14. **Narrate one sentence before running anything.** "Pulling your full automation list to find the most active one." Then exec. The harness shows technical progress lines anyway; your narration is what the user reads.

## API limitations

- **Cannot send campaigns** via v3 API. Recipes design email series; the user builds them in the AC UI.
- **Cannot create automations** via API. Read-only for automation structure. Can enroll contacts.
- **Cannot read site tracking page visits** via API. Hot leads scoring uses scores, tags, and deal data instead.
- **Cannot read spam complaint data** via API. List health uses bounces and unsubs as proxies.
- **Per-contact engagement** via `/activities` endpoint can be incomplete. Use directionally, not as absolute truth.
- **`/messageActivities` is not exposed on every plan.** When AC returns 404, the engagement scripts (`send_time_optimizer`, `send_frequency_report`, `domain_engagement_report`, `engagement_decay`, `stale_contact_report`, `new_subscriber_quality`, `segment_performance`) automatically fall back to `/linkData` — that means **clicks-only** analysis with no open events. The `client.fetch_engagement_events()` helper in `_ac_client.py` handles the fallback transparently. If a report shows zero opens but non-zero clicks, this is why.
- **Stage-movement timestamps for deals are not exposed** in v3. `pipeline_audit.py` reports current state and 90-day-recent-creation only; it cannot compute time-in-stage.
- **Some endpoints are gated by AC plan tier.** When a script hits a 403 on a plan-gated endpoint (`/deals*`, `/dealTasks`, `/savedResponses`, `/accounts`, `/notes`), it prints a friendly "Not available on your ActiveCampaign plan" markdown report and exits cleanly — this is a tier limitation, not a bug. Affected scripts include `pipeline_audit.py`, `mql_to_sql_handoff.py`, `win_loss_report.py`, `tasks_audit.py`, `notes_analysis.py`, `sales_rep_performance.py`, `saved_responses_audit.py`, and `accounts_audit.py`.

## Notes & gotchas

- **Rate limit**: 5 req/s. On 429, respect `Retry-After`.
- **Pagination**: `?limit=100&offset=0`. Cursor-based: `?orders[id]=ASC&id_greater=N`.
- **All IDs are strings.**
- **Currency is in cents.** Deal value `100000` = $1,000.
- **Multi-value dropdowns**: `||` delimiter.
- **Custom field values are NOT on the contact object.** Separate `fieldValues` resource.
- **Webhooks are at-least-once.** Build idempotent handlers.
