# Memory Template - Fox News Monitor

Create `~/fox-news/memory.md` with this structure:

```markdown
# Fox News Monitor Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Context
- When this skill should activate automatically
- Preferred Fox sections and topics
- Preferred briefing depth and recency window

## Coverage Defaults
- Fox-only or Fox-first plus outside corroboration
- Opinion included only on request or allowed by default
- Live coverage preference versus recap preference

## Safety Defaults
- Confirmation required before multiple opens: yes/no
- Save archived briefings when requested: yes/no
- Outside verification required for contested stories: yes/no

## Notes
- Repeated section preferences inferred from usage
- Known source constraints, broken paths, or access limits
- Proven briefing patterns that worked well

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Preferences are still evolving | Keep learning while delivering answers |
| `complete` | Defaults are stable | Use saved preferences with minimal extra questions |
| `paused` | User wants fewer setup questions | Operate with explicit requests only |
| `never_ask` | User asked to stop setup prompts | Do not probe for more defaults |

## Rules

- Keep notes in natural language outside the required status fields.
- Update `last` whenever section defaults, safety defaults, or balance preferences change.
- Save durable patterns, not one-off headlines.
- Never remove prior notes without explicit user instruction.
