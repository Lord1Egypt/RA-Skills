# Templates

## CORE/hard-rules.md

```md
# Hard Rules

- Memory-first: search memory before context-dependent answers.
- State authority: `CORE/current-state.md` is the single source of current status.
- No fabrication: if memory is missing, say so explicitly.
- Session close discipline: append daily log + update state when changed.
```

## CORE/current-state.md

```md
---
last_updated: 2026-02-28T16:00:00+08:00
system_status: operational
current_mode: normal
owner: Ian
---

# Current State

## Active Projects
- name: duru-memory-skill
  status: in-progress
  progress: 40%
  next_action: refine retrieval and compatibility guidance as the built-in memory stack evolves

## Recent Decisions
- 2026-02-28: use Markdown files as the primary memory source
- 2026-04-13: keep Markdown memory as the source of truth while allowing built-in retrieval and optional Active Memory on top

## Blockers
- none

## Next Actions
- [ ] finalize scripts
- [ ] test session start/close flow
```

## daily/YYYY-MM-DD.md

```md
# Daily Log - 2026-02-28

## What happened
- ...

## Decisions
- ...

## Completed
- [x] ...

## Next
- [ ] ...
```

## projects/<name>.md

```md
---
status: active         # active | superseded | invalid
polarity: positive     # positive | negative
confidence: medium     # high | medium | low
avoid_reason: ""       # required when polarity=negative
replaces: ""           # optional memory id/path replaced by this entry
---

# Project: <name>

## Goal
...

## Status
- state: in-progress
- progress: 0%

## Decision Log
- YYYY-MM-DD: ...

## Open Tasks
- [ ] ...
```

## CORE/anti-patterns.md

```md
# Anti-Patterns (Avoided Pitfalls)

- id: AP-YYYYMMDD-XX
- status: invalid
- polarity: negative
- confidence: high
- trigger: <when this pitfall appears>
- avoid: <wrong approach>
- avoid_reason: <why this is dangerous>
- do_instead: <safe replacement>
```

## handoff/session-handoff-YYYY-MM-DD.md

```md
# Session Handoff - 2026-02-28

## Just finished
- ...

## In progress
- task: ...
  progress: ...
  next: ...

## Open questions
- ...
```
