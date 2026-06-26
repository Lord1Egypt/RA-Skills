# Rules & Reference

## Prohibited Actions

- **Do not modify** `SKILL.md` or `_meta.json`
- **Do not run** git commit / git push (unless the user explicitly asks)
- **Do not delete** existing files (unless a task explicitly requires it)
- **Do not optimize** this skill itself
- **Do not invent goals** — if there are no todos, stop
- In AUTONOMOUS.md, **only maintain goals and todos** — no reflections, logs, or history

## Core Principles

1. **Goal-driven** — everything revolves around the goals in AUTONOMOUS.md
2. **MVP mindset** — ship fast, don't over-engineer
3. **Single-round execution** — one round per wake-up, then stop
4. **Resumable** — interrupted runs can continue from tasks.md

## File Structure

```
skill directory (managed by openclaw, safe to update)
├── SKILL.md
├── _meta.json
└── assets/
    ├── templates.md       # File templates for first-time setup
    └── rules.md           # This file

agents/ (user data, preserved across normal updates)
├── AUTONOMOUS.md
└── memory/
    ├── tasks.md           # Active task list
    ├── tasks-log.md       # Completion history (max 50 lines)
    └── backlog.md         # Backlog ideas
```
