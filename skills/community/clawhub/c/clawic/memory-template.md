# Memory Template - Clawic CLI

Create `~/clawic/memory.md` with this structure:

```markdown
# Clawic Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- Activation cues, preferred runtime path, default install root -->
<!-- Example: "Use this when I ask for a Clawic skill or mention the clawic CLI." -->

## Registry Defaults
<!-- Default registry base URL or mirror notes -->
<!-- Example: "Stay on the public GitHub-backed registry unless I say otherwise." -->

## Install Defaults
<!-- Review posture, destination folders, overwrite policy -->
<!-- Example: "Always run show before install and keep vendor installs under ./skills." -->

## Notes
<!-- Stable observations that improve future command choices -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning defaults | Keep collecting explicit workflow choices |
| `complete` | Runtime and install habits are stable | Reuse saved defaults unless overridden |
| `paused` | User does not want continuity right now | Work only from the current request |
| `never_ask` | User does not want setup questions | Stop asking for persistent defaults |

## Key Principles

- Store reusable workflow defaults, not secrets.
- Keep notes in natural language, not config dumps.
- Save registry overrides only when the user intentionally uses one.
- Update `last` after meaningful `clawic` work.
