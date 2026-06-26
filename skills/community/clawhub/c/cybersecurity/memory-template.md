# Memory Template - Cybersecurity

Create `~/cybersecurity/memory.md` with this structure:

```markdown
# Cybersecurity Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation Preferences
- When cybersecurity support should auto-activate
- Whether to jump in proactively on obvious risk
- Environments or conversations where it should stay quiet unless asked

## Scope and Boundaries
- Authorized systems, labs, or assessment types
- Actions that always require explicit approval
- Sensitive areas, legal constraints, or excluded targets

## Environment Context
- Critical assets, trust boundaries, and architecture notes
- Security tooling already in use
- Relevant compliance or customer constraints

## Reporting Preferences
- Audience: practitioner, mixed, executive
- Preferred severity language and confidence style
- Evidence depth and remediation format

## Notes
- Durable investigation patterns
- Repeated risk themes
- Useful constraints and exceptions

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still forming | Keep learning the environment and boundaries |
| `complete` | Stable operating context | Focus on execution, findings, and follow-through |
| `paused` | User wants less setup | Stop probing and work with the current context |
| `never_ask` | User does not want setup prompts | Do not ask new setup questions |

## Local Files to Initialize

```bash
touch ~/cybersecurity/{memory.md,environments.md,incidents.md,findings.md,notes.md}
chmod 700 ~/cybersecurity
chmod 600 ~/cybersecurity/{memory.md,environments.md,incidents.md,findings.md,notes.md}
```
