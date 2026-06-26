# Memory Template — Fastmail API

Create `~/fastmail-api/memory.md` with this structure:

```markdown
# Fastmail API Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- User goals, preferred workflows, and risk boundaries in natural language -->

## Account Map
primary_account_id:
mailbox_ids:
identity_ids:
contact_account_ids:
calendar_account_ids:

## Operating Preferences
<!-- Confirmation style, batching defaults, and verification expectations -->

## Recent Operations
<!-- High-impact actions and notable outcomes -->

## Open Risks
<!-- Pending retries, partial failures, or unresolved data mismatches -->

## Notes
<!-- Extra context that improves next decisions -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning account context | Ask focused follow-ups when useful |
| `complete` | Core context is stable | Execute quickly with minimal setup |
| `paused` | User wants less proactivity | Run only explicit requests |
| `never_ask` | User asked to stop context gathering | Use existing context only |

## Key Principles

- Keep account IDs and workflow context current after every session.
- Store risk notes in natural language, not rigid config schemas.
- Never store raw bearer tokens in memory files.
- Update `last` on each use.
