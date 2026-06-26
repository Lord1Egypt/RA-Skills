# Europe Memory

Create `~/europe/memory.md` with this structure only if the user wants continuity across sessions:

```markdown
# Europe Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Current Situation
- Mode: visitor / choosing-base / moving / resident / student / work / remote / family
- Nationality or passport context:
- Target country or shortlist:
- Target city or shortlist:
- Stay length or seasonality:

## Constraints
- Budget pressure:
- Right-to-stay or visa posture:
- Family, school, or care needs:
- Language comfort:
- Transport and mobility realities:
- Tax, healthcare, or insurance sensitivities:

## Open Loops
- Task:
- Waiting on:
- Next deadline:

## Notes
- Natural-language observations that improve future Europe guidance

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
- Nationality, target country, and length of stay matter more than a generic "Europe" label.
- Save only details that will materially improve the next Europe answer.
- Keep the default memory coarse. Do not store full identifiers unless the user explicitly wants saved continuity at that level.
- Update `last` on each meaningful use.
