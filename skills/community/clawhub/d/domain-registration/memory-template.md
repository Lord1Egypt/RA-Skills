# Memory Template - Domain Registration

Create `~/domain-registration/memory.md` with this structure:

```markdown
# Domain Registration Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Activation Preferences
- Auto-activation boundaries for registrar and DNS lifecycle requests
- Ask-first versus proactive mode by risk level
- Providers or contexts to avoid by default

## Provider Context
- Registrar accounts and aliases in active use
- API readiness, dashboard-only constraints, and permission boundaries
- Country or TLD-specific policy notes

## Domain Inventory Summary
- High-priority domains and renewal windows
- Transfer lock status and ownership checkpoints
- Nameserver and DNS authority snapshots

## Risk and Approvals
- Billing threshold requiring explicit confirmation
- Operations needing multi-step validation
- Incident history and proven rollback paths

## Notes
- Durable operational patterns that improve future executions

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Continue collecting context during normal work |
| `complete` | Core workflow context is stable | Execute quickly with minimal clarification |
| `paused` | User paused setup prompts | Continue tasks using current context only |
| `never_ask` | User does not want setup prompts | Do not ask setup questions unless explicitly requested |

## Memory Principles

- Keep entries factual, concise, and tied to domain lifecycle operations.
- Replace outdated assumptions instead of stacking contradictions.
- Record only reusable context that improves future decisions.
- Never store secrets, raw tokens, or private data unrelated to domain operations.
- Update `last` on each meaningful execution.
