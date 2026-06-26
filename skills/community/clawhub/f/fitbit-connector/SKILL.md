---
name: fitbit-connector
description: Fitbit data connector skill for OpenClaw. Exposes compact auth/fetch/store/quality tools; OpenClaw performs all coaching reasoning.
---

# Fitbit Connector Skill (Tool Provider)

Use this skill when OpenClaw needs Fitbit or unified health data.

This is the **canonical front door** for health / Fitbit retrieval in OpenClaw.
If a user asks for latest Fitbit numbers, recovery signals, readiness trends, sleep/HRV/resting-HR patterns, or recent health metrics for training interpretation, start here.

This skill is **data-plane only**:
- it authenticates,
- fetches Fitbit data,
- syncs/cache stores normalized metrics,
- returns compact JSON.

OpenClaw handles interpretation, decisions, and coaching language.

## Canonical usage rule

For ordinary question-answering, prefer this skill first.
Do **not** start by searching the workspace for Fitbit paths if this skill is available.
Do **not** prefer older opinionated helper scripts over this interface.

For training questions, combine this skill with `memory/training-continuity.md`:
- this skill = latest health/recovery data
- `memory/training-continuity.md` = training state, progression rules, recent workout context

## Setup

1. Create Fitbit developer app (type `Personal`).
2. Redirect URI: `http://127.0.0.1:8787/callback`.
3. Create `.env` from `references/env.example`.
4. Run auth bootstrap:
   - `python3 scripts/fitbit_auth.py auth-url`
   - approve in browser, copy `code` + returned `state`
   - `python3 scripts/fitbit_auth.py exchange --code <CODE> --state <STATE>`

## Primary front-door interface (recommended)

For most OpenClaw usage, call the narrow front door first:

- `node ../skills/health-training-frontdoor/scripts/request.js '{"action":"latest_recovery"}'`

This keeps retrieval typed and low-ambiguity.

## Backend tool interface (compact JSON)

Direct backend contract/schema:

- `python3 scripts/fitbit_tools.py schema`
- Auth status:
  - `python3 scripts/fitbit_tools.py auth-status`
- Endpoint catalog (broad API surface):
  - `python3 scripts/fitbit_tools.py catalog`
- Capability discovery across last N days (rate-limit aware):
  - `python3 scripts/fitbit_tools.py discover-capabilities --days 14 --sleep-ms 500 --stop-on-429`
- Direct Fitbit endpoint fetch (generic exposure):
  - `python3 scripts/fitbit_tools.py fetch-endpoint --path sleep/date/YYYY-MM-DD.json --normalize`
- Fetch API day payload:
  - `python3 scripts/fitbit_tools.py fetch-day --date YYYY-MM-DD`
  - add `--raw` for full Fitbit payload
- Fetch cached date range (field-filtered):
  - `python3 scripts/fitbit_tools.py fetch-range --start YYYY-MM-DD --end YYYY-MM-DD --metrics hrv_rmssd,resting_hr,sleep_minutes,data_quality`
  - add `--ensure-fresh` to auto-sync that range before reading
- Fetch latest N cached days:
  - `python3 scripts/fitbit_tools.py fetch-latest --days 5 --metrics hrv_rmssd,resting_hr,sleep_minutes,data_quality`
  - add `--ensure-fresh` to auto-sync the last N days before reading
- Sync one day from Fitbit API to cache:
  - `python3 scripts/fitbit_tools.py store-sync-day --date YYYY-MM-DD`
- Sync date range from Fitbit API to cache:
  - `python3 scripts/fitbit_tools.py store-sync-range --start YYYY-MM-DD --end YYYY-MM-DD`
- Query sync quality flags:
  - `python3 scripts/fitbit_tools.py quality-flags --days 7`
- Unified DB status (Apple + Fitbit):
  - `python3 scripts/fitbit_tools.py unified-status`
- Unified latest daily rows with source preference:
  - `python3 scripts/fitbit_tools.py unified-fetch-latest --days 14 --source best`

## Canonical QA patterns

### Latest Fitbit / recovery snapshot
For questions like:
- "What do my latest Fitbit numbers suggest?"
- "How does recovery look today?"
- "Give me my newest HRV / sleep / resting HR"

Prefer:
- `python3 scripts/fitbit_tools.py fetch-latest --days 3 --metrics hrv_rmssd,resting_hr,sleep_minutes,data_quality --ensure-fresh`

### Unified health snapshot
For questions that may blend Fitbit + Apple Health:
- `python3 scripts/fitbit_tools.py unified-fetch-latest --days 14 --source best`

### Trend / confidence checks
When freshness or quality confidence matters:
- `python3 scripts/fitbit_tools.py quality-flags --days 7`

### Training interpretation
For questions like:
- "Should I train today?"
- "How did yesterday compare to recovery?"
- "Has recovery improved since earlier this week?"

Use both:
1. this skill for current/recent health signals
2. `memory/training-continuity.md` for training rules, progression, and recent exercise context

## Notes

- Output contract: compact JSON (machine-optimized, minimal token usage).
- Prefer narrow `--metrics` lists to keep token usage low.
- SQLite cache is local reliability layer; Fitbit API remains source-of-truth.
- No medical diagnosis. This skill only provides data.

## Anti-patterns

If this skill is available, avoid these failure modes:
- searching the workspace first just to locate Fitbit functionality
- asking the user where the connector lives
- preferring `fitbit_query.py` over `fitbit_tools.py` for normal QA
- treating memory references as the primary source of live Fitbit data
- using orchestrator files as the first discovery surface for ordinary health questions

## Legacy scripts

Older opinionated scripts remain only for backward compatibility and should be treated as **non-canonical** for ordinary OpenClaw reasoning:
- `fitbit_query.py`
- `fitbit_coach_view.py`

If a normal user question can be answered through `fitbit_tools.py`, do that instead.
