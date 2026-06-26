---
name: auto-dream
description: Consolidate long-running agent memory with a 4-phase Orient → Gather → Merge → Prune pass. Use when memory/context is stale, duplicated, contradictory, too large, after long sessions, after daily reflection, before handoff, or when the user asks to “dream”, “consolidate memory”, “clean memory”, or “prune context”. Promotes durable facts, prunes noise, converts relative dates to absolute dates, resolves contradictions, and avoids storing secrets, customer data, or raw transcripts.
version: 1.0.2
license: MIT-0
metadata:
  openclaw:
    emoji: 🌙
    requires: {}
---

# Auto Dream — Memory Consolidation

Run a targeted memory consolidation pass. The goal is not to archive everything; it is to keep future sessions accurate, small, and useful.

## Use When

- Memory or context feels stale, duplicated, contradictory, or too large
- A long coding/research/ops session produced durable facts or decisions
- Daily reflection completed and durable items need promotion
- Before handing off work to another agent/session
- The user asks to dream, consolidate memory, clean memory, or prune context

## Core Rules

- Merge before creating: update existing topic files instead of making duplicates
- Preserve durable facts, decisions, preferences, project conventions, and recurring tool gotchas
- Remove or downgrade task progress, stale todos, solved bugs, and noisy session logs
- Convert relative dates like “yesterday” or “last week” to absolute dates
- Never store secrets, tokens, customer data, private raw transcripts, or full command output
- Make the pass idempotent: running twice should not create extra churn

## Four-Phase Workflow

### 1. Orient

Build a quick map of existing memory before editing.

Check, when present:
- `MEMORY.md` or workspace memory index
- `memory/YYYY-MM-DD.md` for today and yesterday
- project/topic memory files relevant to the current work
- `memory/morning-briefing.md` only as an index, not as source of truth

Do not exhaustively read transcripts. Search targeted keywords only when needed.

### 2. Gather Signal

Collect only durable signal:
- user corrections and stable preferences
- project decisions and architecture constraints
- solved recurring errors and tool quirks
- important security, auth, deployment, billing, or data-handling rules
- new source-of-truth paths or ownership changes

Discard:
- routine progress updates
- “we did X today” logs with no future value
- temporary todos
- duplicate phrasing of facts already stored
- private/customer data examples

### 3. Merge

For every useful item:
- update the closest existing file/section
- resolve contradictions by keeping the newer verified fact and removing stale wording
- compress to one clear line when possible
- move details out of the global index into topic/project files
- mark resolved items only if that state will matter later; otherwise remove them

`MEMORY.md` should stay an index, not a transcript dump:
- target: under ~200 lines and ~25 KB
- one fact per line when practical
- link or point to detail files instead of duplicating detail

### 4. Prune

Remove or shorten:
- completed one-off tasks
- stale debugging notes older than 30 days unless recurring
- duplicate project facts
- obsolete paths, credentials notes, setup commands, or ownership claims
- long entries that can become concise references

## Output

Return a short summary:

```text
🌙 Dream abgeschlossen
Merged: X durable facts into existing memory
Pruned: X stale/duplicate entries
Fixed: X contradictions
Memory size: before → after
Open questions: none | list
```

If nothing changed, say: `Memories are already tight — nothing to do.`

## Cron Trigger Heuristics

Run automatically when:
- today's daily memory exceeds ~100 lines
- global memory approaches its size/line budget
- a session longer than 30 minutes changed durable project state
- daily reflection produced new durable learnings
