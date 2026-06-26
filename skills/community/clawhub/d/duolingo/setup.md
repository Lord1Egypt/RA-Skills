# Setup - Duolingo Learning OS

Read this silently when `~/duolingo/` does not exist or is empty.
Start naturally and configure activation plus multi-topic structure early.

## Priority Order

### 1. Confirm Activation and Optional Routing Scope
In the first exchanges, define when this should auto-activate.
Ask for the real trigger topics now, for example:
- english
- cooking
- math

If the user wants auto-routing, prepare the AGENTS block using `activation-routing.md`.
Do not edit AGENTS automatically. Always show the snippet and ask the user to apply it.

### 2. Confirm Learning Mode Per Topic
For each active topic, confirm:
- target outcome
- current level
- session pace (light, normal, intense)

If user gives two or more topics, keep all active; do not force a single track.

### 3. Bootstrap Filesystem and Topic Namespaces
Create `~/duolingo/` with:
- global router files
- global memory
- one namespace per active topic

Use templates from `blueprint.md` and `topic-template.md`.

### 4. Run Placement and First Micro-Lesson
For each new topic:
- run quick placement (2-5 prompts)
- set starting lesson in `queue.md`
- complete first loop from `lesson-loop.md`

### 5. Configure Daily Rotation for Multi-Topic Learning
When multiple topics are active, define a default rotation:
- same-day stack (topic A then B)
- alternating days
- weighted plan (for example 70 percent English, 30 percent cooking)

Store this in global memory and apply automatically.

## What to Save

| Save to | Content |
|---------|---------|
| `memory.md` | Global status, active topics, rotation policy, streak summary |
| `router/topics.md` | Canonical topics and trigger phrases |
| `router/agentsmd-snippet.md` | Current AGENTS.md routing snippet |
| `topics/<slug>/profile.md` | Goal, level, constraints |
| `topics/<slug>/curriculum.md` | Skill tree and lesson units |
| `topics/<slug>/queue.md` | Next lessons and review backlog |
| `topics/<slug>/sessions.md` | Session log and results |

## Guardrails

- Never start lessons before topic namespace exists.
- Never remove a topic without explicit user confirmation.
- If AGENTS router is enabled, keep it synchronized with `router/topics.md`.
- Keep lesson loops short; split long explanations into multiple loops.
