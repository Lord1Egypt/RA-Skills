# Memory Template — Drawing

Create `~/drawing/memory.md` with this structure:

```markdown
# Drawing Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Defaults
- Audience age:
- Preferred mode: color-scene | coloring-page | learning-card
- Print target: none | A4 | US Letter
- Default orientation: portrait | landscape

## Style Preferences
- Likes:
- Avoid:
- Usual style packs:

## Model Notes
- OpenClaw image model:
- Provider quirks worth remembering:
- Prefers prompts only or prompts plus model advice:

## Winning Patterns
- Prompt blocks that consistently work
- Reusable negative constraints
- Series anchors that should stay stable

## Notes
- Anything practical learned from repeated requests

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning defaults | Keep observing and confirming naturally |
| `complete` | Defaults are stable | Use them without re-asking unless the task changes |
| `paused` | User does not want more setup now | Help with current requests only |
| `never_ask` | User does not want preference-gathering | Use neutral defaults and stop probing |

## Key Principles

- Save practical defaults, not essays.
- Record the output mode separately from the visual style.
- Keep winning prompts as short reusable fragments rather than full transcripts.
- If a child age is unknown, note the inferred default and keep it revisable.
- Store provider quirks only when repeated evidence supports them.
