---
name: agent-health-optimizer
description: "Audit and improve your OpenClaw setup with one skill. Scores agent health, audits memory hygiene, checks cron reliability, and compares installed skills against ClawHub — with conservative fixes instead of reckless auto-repair."
metadata:
  openclaw:
    requires:
      bins: ["openclaw", "python3"]
---

# Agent Health Optimizer

**Diagnose, score, and steadily improve your OpenClaw setup.**

This skill is an **audit toolkit**, not a magic self-healing system. It is good at surfacing likely problems, weak spots, and opportunities. Its `--fix` mode is intentionally conservative.

## Requirements

- **python3** (3.8+)
- **openclaw CLI**

## Quick Start

```bash
# Full diagnostic suite — one command
python3 scripts/self_optimize.py

# Individual tools
python3 scripts/health_score.py         # Health grade (A+ to F)
python3 scripts/memory_auditor.py       # Memory hygiene check
python3 scripts/cron_optimizer.py       # Cron analysis
python3 scripts/cron_optimizer.py --fix # Conservative auto-repair (backs up first)
python3 scripts/skill_comparator.py     # Adjacent/overlapping ClawHub skills
```

## What It Does

### 🏥 health_score.py — Agent Health Grade (0-100)

Scores 5 dimensions:

- **🧠 Memory (25pts)**: MEMORY.md completeness, daily log activity, working buffer, anti-poisoning hygiene, source tags
- **⏰ Cron (25pts)**: job health, schedule diversity, use of isolated sessions, suspicious delivery setups, selective stagger usage
- **📦 Skills (20pts)**: count, overlap hints, ClawHub management ratio, metadata completeness
- **🔒 Security (15pts)**: safety rules, anti-poisoning policy, WAL protocol, external action controls
- **🔄 Continuity (15pts)**: SOUL.md, USER.md, HEARTBEAT.md, IDENTITY.md, git tracking

### 🔍 memory_auditor.py — Memory Hygiene

Detects:
- Imperative rules that should be declarative facts
- Missing source tags on factual entries
- Stale entries >30 days with pending status
- External content stored as instructions
- Oversized files needing archival
- Daily log gaps

### ⏰ cron_optimizer.py — Cron Job Doctor

Detects:
- Error states with job names and error messages
- Time collisions (multiple jobs on same schedule)
- Missing stagger on **burst-prone recurring schedules**
- Suspicious announce setups (for example explicit channel without explicit `to`)
- Timeout mismatches
- Session target recommendations (isolated vs main)

`--fix` mode:
- creates `memory/cron-backup.json` before changes
- only auto-adds stagger to **recurring top-of-hour stampede-prone jobs**
- does **not** force delivery on jobs using `delivery=none`
- does **not** modify exact-time jobs just because they lack stagger

### 📦 skill_comparator.py — Skill Landscape Checker

Via ClawHub API (`https://clawhub.ai/api/v1/`):
- Fetches stars, downloads, installs for installed skills
- Lists top ClawHub skills you're missing
- Finds **adjacent / overlapping** skills with stronger community signals
- Category coverage analysis (what domains are missing?)

Important: these are **comparison hints**, not authoritative replacements.

### 🔄 self_optimize.py — Unified Runner

Runs all 4 tools and produces:
- Combined report with prioritized action items (HIGH/MED/LOW)
- Trend tracking vs prior run (📈/📉)
- JSON reports in `memory/` for historical review

## What It Reads & Writes

**Reads** (non-destructive):
- Workspace files: MEMORY.md, AGENTS.md, SOUL.md, USER.md, HEARTBEAT.md, IDENTITY.md
- Daily logs: `memory/*.md`
- Skill metadata: `skills/*/SKILL.md`
- Cron config: `openclaw cron list --json`
- ClawHub public API: `https://clawhub.ai/api/v1/skills/...`

**Writes** (reports only):
- `memory/health-score.json`
- `memory/memory-audit.json`
- `memory/cron-optimizer.json`
- `memory/skill-comparator.json`
- `memory/self-optimize-report.json`
- `memory/self-optimize-last.json`

**Modifies** (only with `--fix`):
- `cron_optimizer.py --fix` edits cron jobs via `openclaw cron edit`
- Always backs up to `memory/cron-backup.json` first

## Periodic Self-Optimization

Set up a weekly cron (read-only, no `--fix`):

```bash
openclaw cron add \
  --name "Agent Self-Optimize" \
  --cron "0 11 * * 0" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --stagger 2m \
  --no-deliver \
  --message "Run agent self-optimization:
python3 ~/.openclaw/workspace/skills/agent-health-optimizer/scripts/self_optimize.py

Report results. List HIGH priority issues first. Keep it brief if everything looks fine."
```

## Positioning

Use this skill when you want:
- a periodic audit
- a sanity check before changing agent architecture
- conservative recommendations
- a historical trend of agent health

Do **not** treat it as a substitute for human review on destructive or far-reaching changes.

## Credits

Diagnostic patterns informed by:
- **[proactive-agent](https://clawhub.ai/halthelobster/proactive-agent)** by halthelobster
- **[self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent)** by pskoett
- **Moltbook openclaw-explorers community** — cron jitter pattern (thoth-ix), heartbeat batching (pinchy_mcpinchface)

## License

This work is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt, with attribution and same-license requirement.
