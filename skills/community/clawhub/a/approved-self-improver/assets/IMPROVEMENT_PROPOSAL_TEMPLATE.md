# Pending Improvement Proposal Template

Use this format for each improvement proposal file saved in `.learnings/pending-improvements/`.

Each proposal is its own file named: `IMP-YYYYMMDD-XXX-skill-name.md`

---

```markdown
# Improvement Proposal: IMP-YYYYMMDD-XXX

**Skill**: skill-name
**Skill Path**: path/to/skill/SKILL.md
**Created**: ISO-8601 timestamp
**Status**: pending | approved | rejected | applied
**Priority**: low | medium | high | critical
**Triggered By**: error | user_feedback | recurring_pattern | knowledge_gap

## Problem

What went wrong or what could be better. Include the error ID if this was triggered by a logged error (e.g., ERR-YYYYMMDD-XXX).

## Root Cause

Why the skill failed or produced suboptimal results.

## Proposed Changes

### Change 1: [add | modify | remove] — [brief label]

**Section**: Which section of the SKILL.md is affected
**Current Content** (if modifying/removing):
```
Existing text or instruction that needs changing
```
**Proposed Content** (if adding/modifying):
```
New or updated text or instruction
```
**Rationale**: Why this change fixes the problem

### Change 2: [add | modify | remove] — [brief label]
(repeat as needed)

## Expected Impact

What will improve after applying these changes.

## Recurrence Log

Track each time this same issue is encountered:

| Date | Error/Context | Notes |
|------|--------------|-------|
| YYYY-MM-DD | ERR-YYYYMMDD-XXX | First occurrence |

---
```
