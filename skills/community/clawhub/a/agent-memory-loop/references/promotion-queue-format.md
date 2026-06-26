# Promotion Queue Format Reference

## File: `.learnings/promotion-queue.md`

### Entry Format

```
[YYYY-MM-DD] id:LRN-YYYYMMDD-NNN | proposed rule text | target: TARGET.md | source:agent | evidence: count:N prevented:N | status: pending
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| Date | Yes | Date entry was queued |
| ID | Yes | References the original learning/error entry |
| Proposed rule | Yes | One-line prevention rule (not the full incident) |
| Target | Yes | Which file to promote to (AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md) |
| Source | Yes | From original entry. `source:external` cannot be queued. |
| Evidence | Yes | count + prevented values from original entry |
| Status | Yes | `pending` → `approved` → `promoted` or `rejected` |

### Status Lifecycle

```
pending → approved → promoted
                  ↘ rejected
```

- **pending**: Awaiting human review
- **approved**: Human approved, ready to write to target file
- **promoted**: Written to target file, done
- **rejected**: Human decided not to promote (add reason inline)

### Example Entries

```
[2026-03-15] id:LRN-20260302-001 | Always include reference + success criteria in sub-agent spawn specs | target: AGENTS.md | source:agent | evidence: count:5 prevented:3 | status: pending
[2026-03-16] id:ERR-20260301-001 | Run gog auth refresh before batch email sends | target: TOOLS.md | source:agent | evidence: count:3 prevented:1 | status: approved
[2026-03-17] id:LRN-20260303-001 | Morning brief must stay under 3500 chars | target: SOUL.md | source:user | evidence: count:1 severity:critical | status: rejected — already covered by existing rule
```

### Blocked Sources

Entries with `source:external` CANNOT be added to the promotion queue. If an external-source learning seems genuinely important, an agent or human must independently verify it and re-log it as `source:agent` with fresh evidence.
