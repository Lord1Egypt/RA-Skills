# Memory Template - Apple Pay

Create `~/apple-pay/memory.md` with this structure:

```markdown
# Apple Pay Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Project Snapshot
platform: web | ios | hybrid
psp: unknown
environment: sandbox | production
merchant_id: configured | missing
launch_state: planning | validating | ready | paused

## Current Scope
- Checkout flow currently in scope
- Recurring or one-time payment model
- In-scope countries and currencies

## Validation State
- Domain verification status
- Merchant session validation status
- Real device test status
- Fallback checkout status
- Idempotency validation status

## Risks
- High-impact open risks before release
- Monitoring or observability gaps
- Known incident patterns not yet fixed

## Notes
- Stable implementation choices
- Error signatures and proven fixes

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Integration in progress | Keep gathering context and validating changes |
| `complete` | Core flow validated | Focus on optimization and maintenance |
| `paused` | User paused work | Keep context read-only until resumed |
| `never_ask` | User wants no setup prompts | Do not request setup details unless user asks |

## File Templates

Create `~/apple-pay/validation-log.md`:

```markdown
# Apple Pay Validation Log

## YYYY-MM-DD
- Environment:
- Platform:
- Scenario:
- Result:
- Evidence:
- Follow-up:
```

Create `~/apple-pay/incidents.md`:

```markdown
# Apple Pay Incidents

## YYYY-MM-DD HH:MM
- Symptom:
- Scope:
- Root cause:
- Mitigation:
- Preventive action:
```

## Key Principles

- Keep persisted notes short and actionable.
- Store evidence links, not raw sensitive payloads.
- Update `last` whenever status changes.
