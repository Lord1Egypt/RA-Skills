# Memory Template - Duolingo Learning OS

Create `~/duolingo/memory.md` with this structure:

```markdown
# Duolingo Learning OS Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Active Topics
<!-- List topic slugs currently enabled (english, cooking, etc.) -->
<!-- Mark priority and weekly target per topic -->

## Routing Policy
<!-- When this skill should auto-activate -->
<!-- Link to AGENTS routing decision and trigger phrasing -->

## Rotation Policy
<!-- Single-topic or multi-topic schedule -->
<!-- Examples: alternating days, weighted split, fixed daily stack -->

## Progress Snapshot
<!-- Streak, recent wins, recent misses, pending reviews -->

## Notes
<!-- Observations about motivation, friction, and adaptation choices -->

---
*Updated: YYYY-MM-DD*
```

## Topic Namespace Standard

Each topic uses this path: `~/duolingo/topics/<topic-slug>/`

Required files:
- `profile.md`
- `curriculum.md`
- `queue.md`
- `sessions.md`
- `checkpoints.md`

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Skill actively teaching | Continue lessons and reviews |
| `complete` | Main goals reached | Maintain with lighter reviews |
| `paused` | User paused learning | Keep state, stop proactive lessons |
| `never_ask` | User disabled this system | Do not reactivate unless asked |

## Key Principles

- Global memory coordinates topics; topic files hold lesson details.
- Keep router decisions explicit and easy to audit.
- Update `last` on every learning session.
