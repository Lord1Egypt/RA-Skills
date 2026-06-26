# Memory Template — Expedia

Create `~/expedia/memory.md` with this structure:

```markdown
# Expedia Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
- Preferred mode: web | redirect | rapid | hybrid
- Typical trip types: stays | packages | cars | activities | mixed
- Typical destinations or regions
- Budget posture and flexibility needs

## Operational Readiness
- Redirect partner access available: yes | no
- Rapid lodging access available: yes | no
- Public-page mode acceptable: yes | no
- Known blockers: missing creds, stale quote, weak package fit, unsupported market

## Acceptance Patterns
- Option patterns repeatedly accepted
- Why they worked

## Rejection Patterns
- Option patterns repeatedly rejected
- Why they failed

## Notes
- Reusable booking-safety or comparison guidance for future Expedia tasks

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Preferences still evolving | Keep learning from Expedia tasks |
| `complete` | Stable decision profile | Prioritize known defaults |
| `paused` | User wants minimal setup | Avoid extra discovery prompts |
| `never_ask` | User requested no setup prompts | Follow only explicit instructions |

## Rules

- Keep notes in natural language.
- Update `last` on each meaningful interaction.
- Store reasons, not only outcomes.
- Never remove historical patterns without user approval.
