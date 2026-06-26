# Memory Template - Betting

Create `~/betting/memory.md` with this structure:

```markdown
# Betting Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
- Sports and leagues the user cares about
- Market types they trust or avoid
- Books, exchanges, or jurisdiction limits they mention

## Staking Style
- Whether they use units, flat stakes, or hard cash caps
- Any stated ceiling per event, day, or market

## Notes
- Repeated mistakes to warn about
- Review habits, language preferences, and triggers for stronger caution

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning | Capture context during real betting work |
| `complete` | Enough context exists | Use saved preferences without extra setup questions |
| `paused` | User does not want more tracking now | Work normally and avoid extra follow-up |
| `never_ask` | User does not want stored context | Stop gathering new long-term notes |

## Key Principles

- Keep notes short and useful
- Prefer natural language over rigid schemas
- Update `last` each time the skill is used
- Store constraints and habits, not secrets
