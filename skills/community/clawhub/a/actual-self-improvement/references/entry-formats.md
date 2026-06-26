# Entry formats

Use the bundled scripts when possible. These templates are the manual fallback.

## Learning entry

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: 2026-03-13T12:00:00Z
**Priority**: medium
**Status**: pending
**Area**: backend

### Summary
One-line summary of the lesson

### Details
Explain the wrong assumption, the evidence, and the corrected understanding.

### Suggested Action
Turn the lesson into a prevention rule.

### Metadata
- Source: conversation | error | user_feedback | docs | simplify-and-harden
- Related Files: src/example.ts
- Tags: api, auth
- See Also: LRN-20260312-001
- Pattern-Key: api.auth.header
- Recurrence-Count: 1
- First-Seen: 2026-03-13
- Last-Seen: 2026-03-13

---
```

## Error entry

```markdown
## [ERR-YYYYMMDD-XXX] error-name

**Logged**: 2026-03-13T12:00:00Z
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
One-line description of the failure

### Error
```
Representative error text
```

### Context
Command, tool, API, or environment details

### Suggested Fix
Most likely remediation or prevention rule

### Metadata
- Reproducible: yes | no | unknown
- Related Files: Dockerfile
- See Also: ERR-20260310-001

---
```

## Feature request entry

```markdown
## [FEAT-YYYYMMDD-XXX] capability-name

**Logged**: 2026-03-13T12:00:00Z
**Priority**: medium
**Status**: pending
**Area**: backend

### Requested Capability
What is missing

### Summary
One-line summary

### User Context
Why it matters

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
Concrete first implementation idea

### Metadata
- Frequency: first_time | recurring
- Related Features: existing-feature-name

---
```

## Status guidance

- `pending` — captured, not yet addressed
- `in_progress` — being worked on now
- `resolved` — issue fixed or lesson integrated
- `wont_fix` — intentionally not addressing it
- `promoted` — distilled into project memory
- `promoted_to_skill` — extracted into a reusable skill
