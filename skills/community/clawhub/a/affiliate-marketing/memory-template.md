# Memory Template — Affiliate Marketing

Create `~/affiliate-marketing/memory.md` only if the user wants continuity across sessions.

```markdown
# Affiliate Marketing Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Context
- Company or offer:
- Business model:
- Margin constraints:
- Partner types in play:
- Attribution method:
- Main metric:
- Restricted actions:

## Notes
- Approved commission structures:
- High-priority partners:
- Known attribution issues:
- Fraud or abuse risks:
- Open decisions:

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning context | Gather only what improves partner decisions |
| `complete` | Enough context exists | Work normally without re-asking basics |
| `paused` | User does not want more setup | Stop pushing for more detail |
| `never_ask` | User opted out of continuity | Work statelessly |

## Optional Support Files

If the user wants deeper continuity, create:

- `~/affiliate-marketing/partners.md` — partner pipeline, status, offers, next steps
- `~/affiliate-marketing/economics.md` — commission ceilings, margin scenarios, payout notes
- `~/affiliate-marketing/incidents.md` — fraud flags, trademark issues, attribution disputes

## Key Principles

- Keep memory fast to scan
- Store program decisions, not long conversation history
- Prefer data that changes execution quality: partner fit, payout logic, risk rules, incidents
- Update `last` whenever the local workspace changes
