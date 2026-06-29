---
name: skill-evolver
description: "Skill evolution system. Analyzes agent execution traces to generate Evolution Units (EUs — exploit/explore subtypes under the adaptive type), deploys them to SKILL.md via evidence-based scoring, making agents learn from their own experience. Trigger: 'run skill-evolver' / 'run skill evolution' / 'evolver status' / 'skill patch'"
version: "2.4.13"
display_name: Skill Evolver
slogan: "Skills should adapt to you — and prove it."
author: shawnbywang
license: MIT-0
tags: [skill, evolver, evolution-unit, self-improving, automation, cross-platform]
keywords: [skill-evolver, run skill-evolver, skill evolution, skill patch, evolver]
compatibility: "Requires Node.js 18+. Works on OpenClaw, Claude Code, and any Agent Skills-compatible platform with JSONL session logs."
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "🧬"
---

# skill-evolver

**Skills should adapt to you — and prove it.**

Watches how you actually use each skill, identifies where it falls short or succeeds, attaches those lessons to the skill, and tracks whether each lesson holds up over time.

**CLI**: `node scripts/evolver-cli.js <command>`

> All paths below are relative to this skill's directory.

---

## When to Use

**First-time setup**: User explicitly requests skill self-improvement, e.g. "run skill-evolver", "run skill evolution", "evolver status", or "skill patch".

**Ongoing** (lightweight): Once initialized, evolution runs automatically. Direct interaction only for:
- Status queries, unit review, pin/evict/feedback/clear/block
- Pause/resume, config changes, manual runs

Most of the time, skill-evolver works silently. Don't proactively mention it unless asked.

## Boundaries

- **Reads**: session JSONL files, existing SKILL.md and Evolution Unit (EU) files
- **Writes**: EU `.md` files in `eu/`, inline blocks in SKILL.md, state/config JSON, evidence/trace history files
- **Executes**: Node.js pipeline scripts (`generator.js`, `validator.js`, `reviewer.js`, `monitor.js`) via OS cron or direct invocation
- **Network**: trace and unit/skill text are sent only to the LLM configured for generation/validation/review — either your own provider (`evolver-config.json`) or OpenClaw's subagent channel, which reuses the agent's existing model with no separate API key (auto-detected by default). No telemetry, no hidden endpoints. Set `privacy.allowRemoteLLM: false` to disable all outbound calls. Optional http(s) webhook for notifications.
- **Scheduling**: optional OS crontab entry for periodic runs; remove it to stop.
- **Does NOT**: modify skill source code, monitor calls in real-time, make agent decisions, or run user-supplied shell commands.
- **Safety**: worst case is a bad inline block — evict with one command.

---

## Initialization Flow

When no `evolver-state.json` exists:

### Step 1: Collect User Preferences (ask the user before apply)

Three configuration decisions (all have defaults):

**Mode** (default: `continuous`)
- `continuous`: monitor every N hours, auto-trigger when enough new skill invocations accumulate
- `scheduled`: run at fixed schedule (user specifies frequency)
- `manual`: only on explicit request

**Notification level** (default: `brief`)
- `off`: no push notifications, results logged to file only
- `brief`: periodic natural-language summary of what was learned (requires LLM + delivery)
- `verbose`: brief reports + immediate push of raw evolution results after each run

If brief or verbose: **frequency** (default: `1d`) — how often reports are sent ("1d", "2d", "7d")

**Push channel** (default only for openclaw: current session)
- Which channel to deliver notifications through (e.g. `wecom`, `discord`)
- Platforms without channels: push via webhook URL or shell command configured in `evolver-config.json`

### Step 2: Run Setup

Pass user choices to setup.js:

```bash
node scripts/setup.js --mode <mode> --notify <off|brief|verbose> [--notify-frequency 1d] [--notify-channel wecom] [--interval 4h]
```

All flags optional — omitted flags use defaults. setup.js detects the environment, writes config, installs scheduling, and outputs JSON to stdout.

**Review the output before confirming to user.** Key things to check:

- `checks.sessions.reason` — explains what was found and where. If `sample` is empty but user has conversation history, the detected path may be wrong.
- `checks.llm.detail` — how LLM was resolved. "subagent" tier works but is lower quality; worth mentioning.
- `checks.notifications.hookAvailable` — whether push was auto-configured. If false, notifications go to log file only.
- `blockers[]` — must-fix issues. Help user resolve, then re-run.
- `warnings[]` — non-blocking issues worth mentioning.

### Step 3: Optional Bootstrap

If setup output shows session files were found, a one-time bootstrap can seed initial learnings:

```bash
bash scripts/bootstrap.sh --window-days 7
```

Not required — the system works from zero. If stdout contains `<brief_data>`, deliver a brief report to the user using `brief-prompt.md` as the prompt template.

### Diagnostics

```bash
node scripts/preflight.js          # detailed per-component health check
node scripts/preflight.js --fix    # auto-create missing dirs
node scripts/schedule.js status    # scheduling state + full detection audit
```

---

## Runtime Commands

### Manual Evolution Run

```bash
bash scripts/bootstrap.sh
```

Runs one evolution cycle (incremental from last evolution) and outputs `<brief_data>` to stdout. If output is non-empty, deliver a brief report using `brief-prompt.md` as the prompt template.

Options:
- `--max-si 20` — more traces per run
- `--window-days 14` — look further back
- `--filter-skill <name>` — only process SIs for one skill (targeted run)
- `--hint "<text>"` — prepend a guidance block to each SI trace; the generator's LLM uses it as steering when extracting Evolution Units. The agent is expected to translate the user's verbal intent into a concise hint before passing it in.

Targeted manual run (e.g. user just finished a `wecom-doc` workflow and wants the lesson codified immediately, with a steering hint):

```bash
bash scripts/bootstrap.sh --filter-skill wecom-doc \
  --hint "User wants the MCP path to become the default; cookie path is fallback only."
```

For raw pipeline output without brief formatting:
```bash
bash scripts/run-daily.sh --state evolver-state.json
```
Then read `eu/evolution-report.json` for structured results.

### Query Status

```bash
node scripts/evolver-cli.js status
```

Returns: `{ mode, paused, lastEvolution, totalEvolutions, pendingSI, units: { total, byTrack, topSkills } }`.
Summarize for user: current mode, how many units are active, when evolution last ran, how many pending SIs.

### List / Explain Units

```bash
node scripts/evolver-cli.js units [skill-name]
node scripts/evolver-cli.js explain <unit-keyword>
```

(`patches` is a deprecated alias for `units` and works identically for one release cycle.)

### Pin / Unpin / Evict

```bash
node scripts/evolver-cli.js pin <unit-keyword>
node scripts/evolver-cli.js unpin <unit-keyword>
node scripts/evolver-cli.js evict <unit-keyword>
```

After evicting, re-run lifecycle to update SKILL.md:
```bash
node scripts/lifecycle.js --eu-dir eu --evidence /dev/null --traces /dev/null
```

### User Feedback

```bash
node scripts/evolver-cli.js feedback <unit-keyword> good|bad
```

### Clear / Block (per-skill user control)

For when you want a skill left alone. `clear` detaches a skill's learned units from its SKILL.md **without deleting them** (the units stay archived on disk and can be restored later). `block` additionally excludes the skill from all future evolution.

```bash
# Detach one skill's units from its SKILL.md (archived, not deleted).
# NOTE: re-attached on the next evolution run unless you also block it.
node scripts/evolver-cli.js clear <skill>

# Detach ALL skills' units at once.
node scripts/evolver-cli.js clear --all

# Detach AND block in one step (stays off).
node scripts/evolver-cli.js clear <skill> --block

# Block a skill: detach now + skip it in all future evolution runs.
node scripts/evolver-cli.js block <skill>

# Re-allow a blocked skill (its archived units re-attach on the next run).
node scripts/evolver-cli.js unblock <skill>

# Show blocked skills.
node scripts/evolver-cli.js blocklist
```

Blocked skills are recorded in `evolver-config.json` under `blockedSkills` (hand-editable). Blocking never deletes lessons — it only stops them from being attached and stops new ones from being generated. Trace extraction skips blocked skills upstream, so no LLM cost is spent on them.

### Pause / Resume / Config

```bash
node scripts/evolver-cli.js pause
node scripts/evolver-cli.js resume
node scripts/evolver-cli.js config <key> <value>
node scripts/evolver-cli.js history --limit 5
```

---

## Unit Matching

Users don't use filenames. Match their intent:
- If units were just displayed → match by position ("the second one")
- Skill + keyword → match against title/condition
- Ambiguous → show candidates and ask

## Unit Types & Scoring

Evolution Units currently all live under type `adaptive`, with two subtypes:

- **Exploit** (✅): Proven strategy — "when X, do Y"
- **Explore** (⚠️): Dead end warning — "when X, don't do Y"
- **Pinned** (📌): User-protected, always active

New units start in **Nursery** (score capped) until positive evidence promotes them. Top 3 per skill are inlined to SKILL.md. Negative evidence → evict. Explore units retire when a matching exploit covers the same scenario.

---

## Continuous Mode Behavior

monitor.js runs via OS crontab (default every 4h):

1. **First run**: initializes state, exits. First evolution is user-initiated (Step 3).
2. Counts new SIs since last evolution. If ≥ threshold (default 5) or maxInterval elapsed: triggers `run-daily.sh`.
3. Processes up to 20 SIs per batch. Remaining carry over to next cron cycle.
4. After evolution with new units, writes `pending_brief` to evolver-state.json.

---

## Brief Report Delivery

Evolution results are written to `evolver-state.json` field `pending_brief`. To deliver:

- **If hook is configured**: already auto-triggered. No action needed.
- **If platform supports recurring agent tasks**: create a recurring task at `notifications.frequency` interval. Task: check `pending_brief` in evolver-state.json → if present, format with `brief-prompt.md` → deliver to user → clear field.
- **Otherwise**: check `pending_brief` on any evolver-related interaction and deliver if present.

---

## File Layout

```
scripts/
  setup.js               One-shot initialization wizard
  preflight.js           Detailed health check (diagnostics)
  run-daily.sh           Pipeline runner (extract → generate → validate → patch)
  monitor.js             Continuous mode trigger + notification hooks
  schedule.js            OS crontab installer
  evolver-cli.js         Query & control CLI
  trace-extractor.js     Session → trace extraction
  generator.js           LLM: trace → Evolution Units
  validator.js           LLM: evidence attribution
  lifecycle.js           Scoring + lifecycle + SKILL.md inline writeback
                         (formerly patcher.js, renamed in v2.4.4)
  lib/
    llm-client.js        Shared LLM client (multi-platform)
    platform-detect.js   Platform detection + adapter resolution
  adapters/
    base.js              PlatformAdapter base class
    openclaw.js          OpenClaw adapter
    claude-code.js       Claude Code adapter
  tests/                 Adapter fixture tests
evolver-config.json      Config (optional, overrides auto-detection)
                         Key fields: `llm` (endpoint/apiKey/model), `skillsPaths` (array of
                         absolute paths to skills root dirs — reviewer uses this to locate
                         SKILL.md descriptions; auto-inferred from install path if omitted)
evolver-state.json       State
eu/<skill>/              Evolution Unit storage (files are eu-YYYYMMDD-<slug>.md;
                         directory was renamed from patches/ in v2.4.0)
CHANGELOG.md             Version history
```
