---
name: focus-tracker
description: Maintain persistent focus on active work across compactions and session restarts. Use when starting a multi-step project, when resuming after compaction, when the user says "we're working on X", or when you notice you've lost track of what was being done. Also use proactively at session start to check if there's unfinished work. Prevents the agent from forgetting mid-project context, drifting between topics, or asking "what were we doing?" after a compaction.
version: 1.0.0
---

# Focus Tracker

Maintain a `FOCUS.md` file in the workspace root as persistent working state.

## When to Read FOCUS.md

- **Every session start** (before responding to first message)
- **After every compaction** (if context feels thin, read it)
- **When the user asks about current work** ("what are we doing?", "where were we?")

## When to Write/Update FOCUS.md

- **When starting a new focused project** — create or replace the active focus
- **When a sub-task completes** — check off items, update status
- **When priorities shift** — user redirects, update immediately
- **When work is DONE** — archive to `FOCUS-LOG.md` and clear FOCUS.md
- **Before compaction memory flushes** — ensure FOCUS.md reflects current state

## FOCUS.md Format

```markdown
# FOCUS — [Project Name]
**Started:** YYYY-MM-DD HH:MM UTC
**Status:** active | paused | blocked
**Context:** One-line summary of WHY we're doing this

## Objective
What we're trying to accomplish (1-3 sentences max)

## Plan
Numbered steps. Check off as completed.
- [x] Step 1 — done
- [ ] Step 2 — in progress (note current state)
- [ ] Step 3 — next

## Active State
What's happening RIGHT NOW. What was the last thing done, what's the next action.
This is the most important section — it's the "resume point" after compaction.

## Blockers
Anything waiting on the user, external systems, or decisions.

## Sub-Agents
Any spawned sub-agents and their status.
- `label` — task description — status (running/done/failed)
```

## Rules

1. **One focus at a time.** If the user pivots, archive the old focus first.
2. **Keep it short.** FOCUS.md should be <50 lines. It's a resume point, not a journal.
3. **Active State is sacred.** Always update it before stopping work. Future-you reads this first.
4. **Don't duplicate memory files.** FOCUS.md tracks *what we're doing now*. Daily memory files track *what happened*. Different jobs.
5. **Archive when done.** Append completed focuses to `FOCUS-LOG.md` with completion date and outcome, then clear FOCUS.md.
6. **Read it, don't ask.** If FOCUS.md exists, read it and resume. Don't ask "what were we working on?" when the answer is in the file.

## FOCUS-LOG.md Format

Append-only log of completed focuses:

```markdown
## [Project Name] — COMPLETED YYYY-MM-DD
**Duration:** X hours/days
**Outcome:** One-line result
```

## Integration with AGENTS.md

Add to your session-start routine, after reading SOUL.md and USER.md:
- Read `FOCUS.md` if it exists → resume work or acknowledge status
- If no FOCUS.md exists → no active project, proceed normally
