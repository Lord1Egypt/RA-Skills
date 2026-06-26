# Distillation Guide

Detailed reference for the four-phase memory consolidation process.

## When to Distill

Trigger distillation when any of these conditions are met:
- 48+ hours since last consolidation AND 3+ unprocessed daily notes
- User explicitly requests it ("consolidate memory", "review notes")
- Weekly scheduled task fires

Check `memory/heartbeat-state.json` → `lastConsolidatedAt` to determine timing.

## Phase 1: Orient

Read `MEMORY.md` completely. Build a mental map of:
- What topics are already covered
- Which entries feel outdated
- Where gaps might exist

This prevents duplicating what's already captured.

## Phase 2: Gather

Read daily notes since the last consolidation date:
```bash
# Find unprocessed daily notes
ls memory/20*.md | sort
```

For each file, identify entries in these categories:
- **Systems**: New tools, automations, or infrastructure built
- **Lessons**: Mistakes made and their fixes, non-obvious knowledge gained
- **Decisions**: Choices with lasting impact and their reasoning
- **Environment**: Facts about the setup that won't change soon
- **Preferences**: User patterns, style choices, workflow habits

## Phase 3: Consolidate

Add gathered items to `MEMORY.md` under appropriate sections.

### Writing Style
- **Concise**: One line per fact when possible
- **Contextual**: Include *why*, not just *what*
- **Actionable**: Frame lessons as rules, not stories
- **Dated**: Add dates for time-sensitive entries

### Examples

❌ Too verbose:
```
On March 15th, we tried to use Library X for PDF processing but it turned out 
that the async API was broken in version 2.x and we had to upgrade to 3.x which 
fixed everything. This took about 2 hours to debug.
```

✅ Right level of detail:
```
- **Library X requires v3+** for async support (v2.x async API is broken) — 2026-03-15
```

❌ Too vague:
```
- Database stuff works now
```

✅ Specific and actionable:
```
- **SQLite over JSON** for datasets >100 records — JSON corruption risk + slow append
```

### Merging with Existing Entries

When new information relates to an existing MEMORY.md entry:
- **Update** the existing entry rather than adding a duplicate
- **Supersede** old info clearly (remove outdated version)
- **Add context** if the original entry was too terse

## Phase 4: Prune

Review all of `MEMORY.md` and remove:
- **Resolved blockers**: "Waiting for X" when X is done
- **Superseded entries**: Old info replaced by newer knowledge
- **Irrelevant details**: Context for completed one-off tasks
- **Over-specific entries**: Compress multiple related items into one

### Pruning Heuristic

For each entry, ask:
1. Would future-me need this? → Keep
2. Is this still accurate? → Keep if yes, remove/update if no
3. Could I re-derive this easily? → Remove (it's not worth the space)
4. Is this a one-time fact or a recurring pattern? → Keep patterns, prune one-offs

## After Distillation

Update the timestamp:
```json
{
  "lastConsolidatedAt": "2026-04-01T22:00:00+09:00"
}
```

Optionally note in today's daily file:
```markdown
## Maintenance
- Distilled daily notes from 03-28 through 04-01 into MEMORY.md
```
