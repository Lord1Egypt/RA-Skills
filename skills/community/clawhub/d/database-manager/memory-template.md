# Memory Template - Database Manager

Create `~/database-manager/memory.md` with this structure:

```markdown
# Database Manager Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## System Context
- Primary databases and engines:
- Environment map (dev, staging, prod):
- Critical data domains:
- Data retention constraints:

## Operations Profile
- Migration cadence:
- Preferred deployment windows:
- Rollback standards:
- Verification style:

## Reliability Profile
- Backup frequency and retention:
- Restore drill cadence:
- RTO target:
- RPO target:

## Active Risks
- Current schema risks:
- Query hot spots:
- Pending migrations with high blast radius:

## Notes
- Durable observations that improve safety and speed.

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | context still evolving | keep capturing system and risk patterns |
| `complete` | stable operating model | apply defaults with minimal prompts |
| `paused` | updates paused by user | use read-only memory context |
| `never_ask` | user declined setup prompts | avoid setup follow-up questions |

## Key Principles

- Store durable operational decisions, not chat transcripts.
- Keep entries short, auditable, and actionable.
- Do not store secrets, credentials, or private keys.
- Update `last` whenever memory changes.
