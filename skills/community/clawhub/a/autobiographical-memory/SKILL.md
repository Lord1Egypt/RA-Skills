---
name: autobiographical-memory
description: "Structured personal memory system that enables agents to persist, consolidate, and recall episodic and semantic memories across sessions. Use when: (1) recording significant events, decisions, or conversations, (2) consolidating daily logs into long-term memory, (3) recalling relevant past context before answering, (4) managing memory files (MEMORY.md, daily notes), (5) reasoning about what to remember vs forget."
---

# Autobiographical Memory

## Core Concepts

Memory has two complementary layers:

| Layer | File | What it stores |
|-------|------|---------------|
| **Episodic** | `memory/YYYY-MM-DD.md` | Raw daily events, conversations, decisions, observations |
| **Semantic** | `MEMORY.md` | Curated knowledge: user preferences, facts, lessons, identity |

**The memory lifecycle:** Capture → Consolidate → Recall → Review

## Quick Start

```markdown
# Recording an event (episodic)
Append to `memory/YYYY-MM-DD.md`:
- Met with [person] about [topic]. Decision: [outcome].
- User prefers [preference]. Updated MEMORY.md.

# Recalling before responding
1. Run `memory_search` with relevant keywords
2. If results are thin, read recent `memory/YYYY-MM-DD.md` files
3. Check `MEMORY.md` for long-term facts

# Consolidating (periodic maintenance)
1. Read recent daily files (last 7-30 days)
2. Extract significant items → update MEMORY.md
3. Remove stale entries from MEMORY.md
```

## Episodic Memory — Daily Notes

### What to Record

Always write to daily notes for:
- **Decisions** with rationale: "Chose X over Y because Z"
- **User preferences** discovered implicitly or explicitly
- **Important conversations** — summary, not transcript
- **Mistakes & lessons** — what went wrong, what to do differently
- **Project milestones** — what was done, what's blocked
- **Identity changes** — if SOUL.md, USER.md, or other self-files changed

### What to Skip

- Routine operations ("checked email, nothing new")
- Transient states ("feeling tired")
- Content better stored elsewhere (code snippets in projects, API keys in config)
- Something the user explicitly said doesn't matter

### Format Convention

```markdown
## Events
- [event description]

## Decisions
- [decision + rationale]

## Observations
- [insights or patterns noticed]

## Notes
- [anything else worth remembering]
```

## Semantic Memory — MEMORY.md

### Structure

```
## User Preferences
- Directly stated preferences without inference

## Project Context
- Active projects and their status

## Relationships & People
- Key people, roles, context

## Technical Environment
- Tools, config, quirks discovered

## Lessons Learned
- Mistakes to avoid, patterns that work
```

### When to Update MEMORY.md

- User states a clear preference
- A project direction is set
- A mistake teaches a lesson worth preserving
- Every few days during heartbeat: consolidate from daily notes

### When to Remove from MEMORY.md

- Project is done / abandoned
- Preference was explicitly reversed
- Information is now obvious context (e.g. "user speaks Chinese" — that's already in USER.md)
- Stale for >3 months without reference

## Consolidation Workflow

Suitable for heartbeat routines. Do this every 3-7 days:

```
1. List memory/*.md, sort by date (newest first)
2. Read files since last consolidation
3. For each significant item:
   a. Is it already in MEMORY.md? → Skip or update
   b. Is it transient? → Skip (leave in daily note)
   c. Is it important? → Add to MEMORY.md
4. Read MEMORY.md for stale entries → remove or archive
5. Write updated MEMORY.md
```

## Recall Strategy

Before answering questions about prior work, people, preferences, or context:

1. **Search first**: `memory_search(query="relevant terms")` — this searches both daily notes and MEMORY.md
2. **Narrow scope**: If search returns weak results, try multiple query phrasings
3. **Deep dive**: For specific periods, `memory_get(path="memory/YYYY-MM-DD.md")` to read raw daily notes
4. **Cross-reference**: Check USER.md, SOUL.md, TOOLS.md for identity/preference info

### When Recall Fails

- Say clearly "I checked my records and don't have information about that"
- Don't fabricate memories
- If the user says "don't you remember? I told you X" — apologize and record it properly this time

## The Forgetting Curve

Not everything needs to persist. Use these filters:

- **Keep in daily notes**: Everything noteworthy for 30-90 days
- **Promote to MEMORY.md**: Only what's likely to be needed again
- **Delete/archive**: What's clearly obsolete after review

## References

- For detailed consolidation scripts: see [references/consolidation.md](references/consolidation.md)
- For memory search patterns: see [references/recall-patterns.md](references/recall-patterns.md)

## Scripts

- `scripts/consolidate.py` — Scan recent daily notes and suggest MEMORY.md updates
- `scripts/stats.py` — Memory file statistics (sizes, dates, coverage)
