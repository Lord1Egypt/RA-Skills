# Handoff Format Specification

Handoffs are dense summaries written at session boundaries so the next session can resume without re-reading the full conversation history.

## File Location
`handoff.md` in the workspace root. Overwrite on each new handoff — only the latest matters.

## Format

```markdown
# Session Handoff
**Generated:** [YYYY-MM-DD HH:MM] [timezone]

## Current Task
[What was being worked on — 1–2 sentences max]

## Last Decision
[The last significant thing decided, completed, or changed]

## Open Items
- [Unfinished work or pending decisions]
- [Each item on its own line]

## Key Context
[1–3 facts the next session needs to avoid repeating work or making wrong assumptions]
```

## Rules
- **Max 20 lines.** Dense, not verbose.
- **No pleasantries.** Write for a cold-start agent, not a human reader.
- **Tense:** Past tense for completed work. Present tense for open items.
- **No opinions or summaries of the conversation.** Only actionable facts.

## When to Write a Handoff
- Query counter hits the configured threshold (default: 10)
- User says "BTW", "switching gears", "new topic", or starts a clearly unrelated task
- User explicitly requests `/handoff`

## When to Read a Handoff
- At session start — check if `handoff.md` exists and is < 3 hours old
- If recent: read, apply context, then delete the file

## Example

```markdown
# Session Handoff
**Generated:** 2026-04-16 09:30 CDT

## Current Task
Building context-manager skill for CertainLogic bundle.

## Last Decision
Decided on query-count (not timer) as primary bloat signal. 10-query default.

## Open Items
- Write SKILL.md body
- Package and test .skill file
- Add to ClawHub listing

## Key Context
- Skill is free, bundled with paid CertainLogic products
- Must reflect CertainLogic quality bar — it's a product advertisement
- Token math reference saved to references/token-math.md
```
