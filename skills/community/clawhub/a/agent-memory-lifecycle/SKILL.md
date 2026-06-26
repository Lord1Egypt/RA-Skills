---
name: memory-lifecycle
description: Systematic memory management for long-running AI agents. Implements a five-tier lifecycle — heartbeat micro-attention, nightly consolidation, weekly reflection, monthly archiving, and yearly wisdom distillation. Use when setting up a new agent's memory system, improving an existing agent's memory quality, or when the agent's MEMORY.md is growing too large and context quality is degrading. Triggers on "set up memory", "memory management", "improve memory", "memory lifecycle", "nightly consolidation", "sleep cycle", "memory housekeeping".
---

# Memory Lifecycle

Structured memory management that makes agents smarter over time — not through code, but through disciplined capture, consolidation, and distillation of context.

## Philosophy

Memory management is not about saving tokens. It's about crafting **high-signal context** that makes a powerful LLM *more* effective.

**Core principles:**
1. **Distill, don't summarise.** Output should be *better* than raw input — structured, actionable, reasoning preserved
2. **Preserve decisions and reasoning.** "We chose X because Y" > "We did X"
3. **Never compress away specifics.** Phone numbers, dates, prices are facts, not fluff
4. **Daily files are immutable.** They're the audit trail — add headers, never edit content
5. **Each tier builds upward.** Raw → structured → refined → wisdom
6. **Archives are a library, not a bin.** Full narratives, not one-liners

## Setup

Run the setup script to scaffold memory files and create cron jobs:

```bash
python3 scripts/setup.py
```

The script will:
1. Create structured memory files (people.md, decisions.md, lessons.md, commitments.md)
2. Add a `## Recent` working memory buffer to MEMORY.md
3. Create four cron jobs (nightly, weekly, monthly, yearly)
4. Add memory micro-attention tasks to HEARTBEAT.md

Run with `--dry-run` to preview changes without applying them.
Run with `--agent <id>` to target a specific agent (default: main).

## The Five Tiers

### Tier 1: Heartbeat Micro-Attention (every ~30 min)

Added to the agent's HEARTBEAT.md. Quick focused pass — capture, promote, tag:

1. **Capture:** Ensure notable events are in today's `memory/YYYY-MM-DD.md`
2. **Promote:** Session-critical items (new appointment, key decision) → `MEMORY.md → ## Recent`
3. **Tag:** Mark daily file entries with `[decision]`, `[lesson]`, `[person]` for the nightly cycle
4. **Monitor:** Check nightly cycle health — if it errored, fix and re-run. Don't just report.

### Tier 2: Nightly "Sleep Cycle" (cron, ~2:00 AM local)

Read `references/nightly-prompt.md` for the full cron prompt.

- Read today's daily file end-to-end
- Write a 2-3 line "day essence" header
- Promote items to structured files (people → people.md, decisions → decisions.md, etc.)
- Update MEMORY.md if active project state changed
- Clear processed items from `## Recent`

**Rules:** Never edit daily file content. Never remove from MEMORY.md unless completed AND archived.

### Tier 3: Weekly Reflection (cron, Sunday ~3:00 AM local)

Read `references/weekly-prompt.md` for the full cron prompt.

- Read all 7 daily files from the past week
- Spot patterns: repeated topics, unresolved threads
- Refine MEMORY.md — improve structure and language (not strip content)
- Review commitments, contacts, decisions for staleness
- Write a "week in review" in Sunday's daily file

### Tier 4: Monthly Deep Clean (cron, 1st of month ~4:00 AM local)

Read `references/monthly-prompt.md` for the full cron prompt.

- Create `memory/archive/YYYY-MM.md` with **full narratives** of completed work
- Move completed items from MEMORY.md to archive
- Keep MEMORY.md under ~4000 words
- Consolidate related lessons into principles
- Personality check on SOUL.md

**Rules:** Archive entries must be self-contained. Active items never move to archive.

### Tier 5: Yearly Wisdom Distillation (cron, January 1)

Read `references/yearly-prompt.md` for the full cron prompt.

- Create `memory/wisdom/YYYY.md`
- Extract wisdom that transcends specific events
- Evolve SOUL.md based on a year's experience
- Flag SOUL.md changes to the human

## The "Recent" Buffer

A `## Recent` section at the top of MEMORY.md acts as working memory:

```markdown
## Recent
> Working memory — heartbeat promotes critical items here, nightly cycle processes them.
- **2026-03-23:** Viewing booked Thu 26 Mar 9am with estate agent
- **2026-03-23:** Server upgraded v2.3.13 → v2.3.22
```

- Heartbeats promote critical items here immediately
- Every new session sees it (MEMORY.md is loaded automatically)
- Nightly cycle processes items and clears them

This bridges the gap between raw daily capture and curated long-term memory.

## File Structure

After setup, the memory directory contains:

```
MEMORY.md                  ← Active long-term memory (loaded every session)
memory/
  YYYY-MM-DD.md            ← Daily raw notes (immutable)
  people.md                ← Contacts, relationships, dynamics
  decisions.md             ← Key choices with rationale
  lessons.md               ← Mistakes and learnings (grows, never shrinks)
  commitments.md           ← Deadlines and obligations
  archive/
    YYYY-MM.md             ← Monthly archives (full narratives)
  wisdom/
    YYYY.md                ← Yearly distilled wisdom
```

## Health Check

Run the health check to verify the memory system is working:

```bash
python3 scripts/health_check.py
```

Checks: nightly cron status, MEMORY.md size, Recent buffer staleness, structured file freshness.

## What Gets Archived vs What Stays

- **Archive:** Completed projects, resolved leads, past deadlines, finished work
- **Keep active:** Ongoing relationships, active projects, preferences, lessons learned
- **Never compress:** Phone numbers, addresses, credentials, family details, business structure
