---
name: driftwatch
description: Monitor agent identity drift using git history. Detects when AI agents quietly modify their own SOUL.md, IDENTITY.md, AGENTS.md, or memory files — autonomy expansion, constraint softening, or self-modification. Read-only, safe to run anytime. Use when you want to audit agent identity changes, verify no unauthorized modifications have occurred, or run a weekly hygiene check on your agent stack.
---

# DriftWatch 🔍

**Agent Identity Drift Monitor for OpenClaw workspaces**

Uses your workspace's existing git history to track changes to agent identity files. For each change it classifies severity, optionally runs LLM semantic analysis, and outputs a human-readable markdown report.

## Usage

```bash
# Full report, last 30 days (heuristic only, fast)
python3 skills/driftwatch/driftwatch.py --no-llm --days 30

# With LLM semantic analysis (requires ANTHROPIC_API_KEY)
python3 skills/driftwatch/driftwatch.py --days 30

# Last 7 days
python3 skills/driftwatch/driftwatch.py --no-llm --days 7

# Cron/heartbeat mode: silent unless concerns found
python3 skills/driftwatch/driftwatch.py --cron --days 7
```

## What it tracks

- `SOUL.md` — core personality and values
- `IDENTITY.md` — agent name, creature, vibe
- `AGENTS.md` — operational rules and protocols
- `USER.md` — what agents know about their human
- `TOOLS.md` — tool and access notes
- `agents/*/MEMORY-INDEX.md` — per-agent active context

## Output

Writes a markdown report to the skill directory. Flags:
- 🟡 Medium: human should review
- 🔴 High: potential concern — review before next agent session

## Add to weekly heartbeat

```markdown
## Weekly Drift Check (Mondays)
Run: python3 skills/driftwatch/driftwatch.py --cron --days 7
```

**Read-only. Does not modify any files.**
