# Florida Memory

Create `~/florida/memory.md` with this structure only if the user wants continuity across sessions:

```markdown
# Florida Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Current Situation
- Mode: visitor / moving / resident / business / seasonal
- Main region:
- City or suburb:
- County / ZIP / flood zone / district if known:

## Constraints
- Timeline or seasonality:
- Budget pressure:
- Family, school, or elder-care needs:
- Vehicle, toll, and commute realities:
- Insurance, storm, or health sensitivities:

## Open Loops
- Task:
- Waiting on:
- Next deadline:

## Notes
- Natural-language observations that improve future Florida advice

---
Updated: YYYY-MM-DD
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning context | Keep gathering high-signal details naturally |
| `complete` | Enough stable context exists | Reuse what is already known before asking |
| `paused` | User does not want more setup right now | Help with current task and avoid extra intake |
| `never_ask` | User does not want this tracked | Stop collecting new background unless asked |

## Key Principles

- Keep notes in natural language, not config-style keys.
- Region, county, flood zone, and district matter more than generic "Florida" labels.
- Save only details that will materially improve the next Florida answer.
- Keep the default memory coarse. Do not store full street addresses or sensitive identifiers unless the user explicitly asks for saved continuity at that level.
- Update `last` on each meaningful use.
