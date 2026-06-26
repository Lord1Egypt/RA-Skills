# Memory Template - Bulgaria

Create `~/bulgaria/memory.md` with this structure:

```markdown
# Bulgaria Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Context
- Trip stage:
- Dates or season:
- Cities or regions:
- Group:
- Pace and budget:

## Preferences
- Likes:
- Avoids:
- Food notes:
- Mobility or hiking notes:

## Plans and Bookings
- Confirmed:
- Considering:

## Notes
- Specific recommendations already given
- Follow-up questions for next time

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning | Keep collecting context naturally |
| `complete` | Enough context exists | Recommend directly and update quietly |
| `paused` | User does not want more setup right now | Help with what is known |
| `never_ask` | User does not want memory-style follow-up | Do not ask for more setup context |

## Principles

- Keep observations in natural language
- Update `last` whenever the skill is used
- Store only information that improves future Bulgaria recommendations
- Avoid turning memory into a checklist of trivia
