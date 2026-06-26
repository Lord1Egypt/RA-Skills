---
name: memory-manager
description: Upgrade your agent's memory from basic notes to a 3-layer production system with nightly consolidation. Based on patterns from running 7 AI bots in production for 30+ days.
---

# memory-manager

**Upgrade your agent's memory from basic notes to a 3-layer production system with nightly consolidation. Based on patterns from running 7 AI bots in production for 30+ days.**

---

## Overview

Every AI agent has the same problem: it wakes up fresh every session with no memory of what happened before. The naive fix is a single `MEMORY.md` file — but that doesn't scale. After a few weeks, it's either a wall of text the agent ignores, or so curated it's missing operational context.

This skill installs a **3-layer memory architecture** that mirrors how humans actually store knowledge:

| Layer | File | What goes here |
|-------|------|----------------|
| 1 — Long-term | `MEMORY.md` | Curated wisdom, architecture decisions, hard-won lessons |
| 2 — Operational | `memory/YYYY-MM-DD.md` | What happened today, active project state, raw context |
| 3 — Tacit | `USER.md` | How your human works, preferences, frustrations, patterns |

Plus a **nightly consolidation cron** that reviews recent sessions and promotes important context up the layers automatically.

---

## When to Use This Skill

Activate this skill when the user asks you to:
- Set up memory for their agent
- Upgrade from a basic `MEMORY.md` system
- Add nightly consolidation or memory cron
- Improve agent continuity between sessions
- Track active projects across agent restarts
- Set up the memory-manager skill

---

## Setup Instructions

### Step 1: Run the Setup Script

```bash
bash ~/.openclaw/skills/memory-manager/scripts/setup.sh
```

This creates the `memory/` directory, copies templates into place, and prints next steps.

### Step 2: Customize the Templates

After setup, edit these files in your agent's workspace:

1. **`MEMORY.md`** — Add your agent's existing long-term context
2. **`USER.md`** — Fill in who the human is, how they work, what frustrates them
3. **`AGENTS.md`** — Review the startup sequence (already wired for 3-layer loading)
4. **`HEARTBEAT.md`** — Configure which projects to monitor

### Step 3: Configure the Startup Sequence

Your agent's `AGENTS.md` must include this memory loading sequence at the top of "Every Session":

```markdown
## Every Session

Before doing anything else:
1. Read `SOUL.md` — identity and persona
2. Read `USER.md` — who you're helping and how they work  
3. Read `memory/YYYY-MM-DD.md` (today) — what happened today
4. Read `memory/YYYY-MM-DD.md` (yesterday) — recent context bridge
5. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`
```

> **Why read yesterday too?** Sessions started after midnight won't have today's file yet. Yesterday bridges the gap. This prevented context loss in our production fleet during late-night sessions.

### Step 4: Set Up Nightly Consolidation

Add a cron job to consolidate memory each night at 2 AM:

```
0 2 * * * openclaw cron run memory-consolidation --model anthropic/claude-opus-4-5 --channel <your-main-channel-id>
```

The consolidation prompt to configure in OpenClaw cron:

```
You are performing nightly memory consolidation for this agent.

Tasks:
1. Read memory/YYYY-MM-DD.md files from the last 7 days
2. Read the current MEMORY.md
3. Identify: significant decisions, lessons learned, architecture changes, resolved issues, evolving patterns
4. Update MEMORY.md with distilled insights (add new, update stale, remove obsolete)
5. Check USER.md — update any new preferences or patterns you observed
6. Write a brief summary of what you consolidated to memory/consolidation-log.md

Be selective. MEMORY.md should stay under 500 lines. Quality over quantity.
Signal completion: reply "CONSOLIDATION_COMPLETE" to the channel when done.
```

> **Why 2 AM?** Low activity period. The consolidation model has full context of the day's events. Running nightly (not weekly) means no single consolidation is overwhelming.

---

## Memory Loading Rules

### In Main Session (direct human chat)
Load all three layers:
```
SOUL.md → USER.md → memory/today.md → memory/yesterday.md → MEMORY.md
```

### In Group Chats / Shared Channels
Load only layers 2 and 3 (no MEMORY.md):
```
SOUL.md → USER.md → memory/today.md → memory/yesterday.md
```

> **Why skip MEMORY.md in group chats?** Long-term memory often contains personal context — private preferences, health info, financial details — that shouldn't leak into conversations with strangers. Daily operational notes are usually safe.

### In Subagent / Worker Sessions
Load only today's notes:
```
memory/today.md (if relevant to task)
```

Subagents are ephemeral. Don't load full memory — it wastes tokens and context.

---

## Daily Notes Format

Each `memory/YYYY-MM-DD.md` file follows this structure:

```markdown
# YYYY-MM-DD

## Sessions

### [Time] — Session summary
- What happened
- Decisions made
- Tasks completed / in progress

## Active Projects

### Project Name
- **Status:** In Progress / Blocked / Complete
- **Last action:** What was done last
- **Next:** What needs to happen next
- **Blockers:** Anything blocking progress

## Context for Next Session

Key things future-me needs to know to pick up without re-explaining:
- [item 1]
- [item 2]

## Raw Log

(Less curated — dump things here that might matter)
```

> **The "Context for Next Session" section is the most important.** Agents often end sessions mid-task. Without this section, the next session has to reconstruct state from scratch. Write it as if briefing a colleague who just joined the project.

---

## Active Project Tracking

Projects move through these states in daily notes:

```
PLANNING → IN_PROGRESS → BLOCKED → REVIEW → COMPLETE
```

The heartbeat integration (see `HEARTBEAT.md`) checks active projects and surfaces blockers automatically.

---

## MEMORY.md Curation Rules

Long-term memory should be:
- **Curated, not comprehensive** — the distilled essence, not raw logs
- **Actionable** — things that change future decisions
- **Evergreen** — not "what I did Tuesday" but "lesson learned from the Tuesday incident"
- **Organized by topic** — architecture, lessons, human preferences, recurring patterns

Things that belong in MEMORY.md:
- Architecture decisions and the reasoning behind them
- Lessons learned from failures
- Patterns in how the human works / thinks
- Important context about key projects
- Things you've been told to always/never do

Things that do NOT belong in MEMORY.md:
- One-off task completions
- Information that will be stale in a week
- Raw conversation transcripts
- Things already captured in USER.md

---

## Heartbeat Integration

Add to your `HEARTBEAT.md` to enable project monitoring:

```markdown
## Active Project Check

For each project in active_projects.json (if it exists):
1. Check last updated timestamp
2. If project hasn't been touched in >48h, surface it: "⚠️ [Project] hasn't been updated in X days"
3. If status is BLOCKED, surface blocker to human
4. If status is COMPLETE but not archived, prompt to archive

## Memory Health Check (weekly, Sundays)

1. Check MEMORY.md line count — if >500 lines, flag for pruning
2. Check memory/ folder — if daily files >30 days old exist, flag for archiving
3. Report: X daily files, MEMORY.md is X lines, last consolidation: [date]
```

---

## File Reference

| File | Location | Purpose |
|------|----------|---------|
| SKILL.md | `~/.openclaw/skills/memory-manager/` | This file |
| setup.sh | `scripts/setup.sh` | One-command installer |
| templates/MEMORY.md | `templates/` | Long-term memory template |
| templates/AGENTS.md | `templates/` | Startup sequence template |
| templates/USER.md | `templates/` | User profile template |
| templates/HEARTBEAT.md | `templates/` | Heartbeat config template |
