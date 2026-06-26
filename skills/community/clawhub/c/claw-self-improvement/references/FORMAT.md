# Format Reference

Canonical format rules, templates, and examples for the four `.learnings/` files used by `claw-self-improvement`.

## Table of Contents

- Files Covered
- ID Formats
- Common Raw Entry Fields
- Status Meanings for Raw Files
- LEARNINGS.md Template
- ERRORS.md Template
- FEATURE_REQUESTS.md Template
- PROMOTED.md Template
  - Categories
  - Statuses
  - Template
- Examples
  - Learning Marked as Promoted
  - Promoted Entry
  - Error Entry Example

## Files Covered

- `LEARNINGS.md`
- `ERRORS.md`
- `FEATURE_REQUESTS.md`
- `PROMOTED.md`

## ID Formats

- `LRN-YYYYMMDD-XXX` — learning
- `ERR-YYYYMMDD-XXX` — error
- `FEAT-YYYYMMDD-XXX` — feature request
- `PRM-YYYYMMDD-XXX` — promoted rule

`XXX` can be sequential (`001`) or short alphanumeric (`A3F`).

## Common Raw Entry Fields

These fields are common across `LEARNINGS.md`, `ERRORS.md`, and `FEATURE_REQUESTS.md` where relevant:

- `**Logged**:` ISO-8601 timestamp
- `**Priority**:` `low | medium | high | critical`
- `**Status**:` usually `pending | in_progress | resolved | wont_fix | promoted`
- `**Area**:` `frontend | backend | infra | tests | docs | config`
- `### Summary`
- `### Metadata`

Recommended metadata fields when useful:
- `Source`
- `Related Files`
- `Tags`
- `See Also`
- `Pattern-Key`
- recurrence notes such as `First-Seen`, `Last-Seen`, `Recurrence-Count`

## Status Meanings for Raw Files

| Status | Meaning |
|---|---|
| `pending` | Captured but not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Fixed or integrated into working knowledge |
| `wont_fix` | Intentionally not being addressed |
| `promoted` | Distilled into `.learnings/PROMOTED.md` |

When a raw entry is promoted, add these fields:

```markdown
**Status**: promoted
**Promoted**: .learnings/PROMOTED.md
**Promotion-ID**: PRM-YYYYMMDD-XXX
**Promotion-Category**: Behavioral Patterns | Workflow Improvements | Tool Gotchas | Durable Rules
```

## LEARNINGS.md Template

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description of what was learned.

### Details
What happened, what was wrong, and what is now understood.

### Suggested Action
What to do differently next time.

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-..., ERR-...
- Pattern-Key: optional stable dedupe key

---
```

## ERRORS.md Template

```markdown
## [ERR-YYYYMMDD-XXX] short_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
Brief description of what failed.

### Error
Actual error message or representative output.

### Context
- Command/operation attempted
- Input or parameters used
- Environment details if relevant

### Suggested Fix
If identifiable, what might resolve this.

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-...

---
```

## FEATURE_REQUESTS.md Template

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
What the user wanted to do.

### User Context
Why they needed it.

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built or extended.

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## PROMOTED.md Template

`PROMOTED.md` is for short, durable, reversible rules distilled out of raw learnings.

### Categories

- `Behavioral Patterns`
- `Workflow Improvements`
- `Tool Gotchas`
- `Durable Rules`

### Statuses

- `active`
- `superseded`
- `retired`

### Template

```markdown
## [PRM-YYYYMMDD-XXX] short-title

**Promoted**: ISO-8601 timestamp
**Status**: active
**Category**: Workflow Improvements
**Source IDs**: LRN-..., ERR-...

### Rule
One short durable rule.

### Apply When
Describe when this should be used.

### Why
What failure, confusion, or repeated waste this avoids.

### Notes
Optional example, caveat, or related files.

---
```

## Examples

### Learning Marked as Promoted

```markdown
## [LRN-20250115-003] best_practice

**Logged**: 2025-01-15T16:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: .learnings/PROMOTED.md
**Promotion-ID**: PRM-20250115-001
**Promotion-Category**: Durable Rules
**Area**: backend

### Summary
API responses must include correlation ID from request headers.

### Details
All API responses should echo back the X-Correlation-ID header from the request.
This is required for distributed tracing.

### Suggested Action
Always include correlation ID passthrough in API handlers.

### Metadata
- Source: user_feedback
- Related Files: src/middleware/correlation.ts
- Tags: api, observability, tracing

---
```

### Promoted Entry

```markdown
## [PRM-20250115-001] echo-correlation-id

**Promoted**: 2025-01-15T16:10:00Z
**Status**: active
**Category**: Durable Rules
**Source IDs**: LRN-20250115-003

### Rule
Echo the incoming `X-Correlation-ID` header in API responses.

### Apply When
When implementing or reviewing request/response handlers.

### Why
Keeps distributed tracing intact and avoids hard-to-debug observability gaps.

### Notes
Relevant files: src/middleware/correlation.ts

---
```

### Error Entry Example

```markdown
## [ERR-20250115-A3F] docker_build

**Logged**: 2025-01-15T09:15:00Z
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
Docker build fails on M1 Mac due to platform mismatch.

### Error
error: failed to solve: python:3.11-slim: no match for platform linux/arm64

### Context
- Command: `docker build -t myapp .`
- Dockerfile uses `FROM python:3.11-slim`
- Running on Apple Silicon (M1/M2)

### Suggested Fix
Add platform flag: `docker build --platform linux/amd64 -t myapp .`

### Metadata
- Reproducible: yes
- Related Files: Dockerfile

---
```
