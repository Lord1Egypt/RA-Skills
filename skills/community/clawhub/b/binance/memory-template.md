# Memory Template - Binance API

Create `~/binance/memory.md` with this structure:

```markdown
# Binance Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Mode
- Environment: testnet | mixed | production-enabled
- Allowed actions: market-data | account-read | trading
- Confirmation rule for production orders

## Scope
- Symbols in scope
- Intervals and data windows used often
- Account and exchange constraints to enforce

## Reliability Notes
- Known timestamp drift offsets
- Recurrent API errors and mitigations
- Stream reconnect behavior that worked

## Notes
- Stable user preferences inferred from behavior
- Workflow shortcuts proven in prior sessions

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Setup still evolving | Keep capturing context while executing tasks |
| `complete` | Stable operating context | Execute quickly with stored defaults |
| `paused` | User paused setup | Use existing defaults without new prompts |
| `never_ask` | User does not want setup prompts | Never ask setup questions unless user requests |

## File Templates

Create `~/binance/runbooks.md`:

```markdown
# Binance Runbooks

## YYYY-MM-DD - Workflow Name
- Objective:
- Environment:
- Commands used:
- Validation result:
- Follow-up:
```

Create `~/binance/incidents.md`:

```markdown
# Binance Incidents

## YYYY-MM-DD HH:MM
- Symptom:
- Endpoint or stream:
- Error code/message:
- Root cause:
- Mitigation:
- Preventive action:
```

## Key Principles

- Keep notes short and operational.
- Store runbook evidence, not secrets.
- Update `last` whenever context changes.
