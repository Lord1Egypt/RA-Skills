# Learnings Log

Corrections, knowledge gaps, best practices, and durable project conventions.

**Categories**: correction | knowledge_gap | best_practice | insight
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## When to log here

Use this file when a lesson should change future behaviour.

Examples:
- the user corrected a wrong assumption
- a project convention was discovered
- a workaround or prevention rule emerged from debugging
- a better workflow or tool usage pattern was identified

## Entry template

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line summary of the learning

### Details
What happened, what was wrong or surprising, and what is now known to be true

### Suggested Action
Specific prevention rule, fix, or workflow change

### Metadata
- Source: conversation | error | user_feedback | docs | simplify-and-harden
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20260313-001
- Pattern-Key: stable.pattern.key
- Recurrence-Count: 1
- First-Seen: 2026-03-13
- Last-Seen: 2026-03-13

---
```

## Promotion fields

When the learning becomes durable project memory:

```markdown
**Status**: promoted
**Promoted**: CLAUDE.md
```

When it becomes a reusable skill:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```
