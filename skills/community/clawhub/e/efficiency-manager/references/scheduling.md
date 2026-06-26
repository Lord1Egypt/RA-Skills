# Scheduling Heuristics

The current planner is lightweight.

Use these heuristics when generating day plans or recommending schedules:

## Planning Order

1. Respect hard constraints first.
2. Protect one focus block if possible.
3. Place deadline-sensitive work before flexible work.
4. Put cognitively heavy work into stronger time windows.
5. Group similar tasks to reduce switching cost.
6. Push shallow tasks into fragmented or lower-energy windows.
7. Stop planning when the day is full.

## Tradeoff Rules

- Prefer a smaller believable plan over an overloaded perfect-looking one.
- If a task pool does not fit, show overflow instead of pretending everything fits.
- If historical slot confidence is weak, keep recommendations light.
- If a user is already overloaded, recommend defer or drop, not only reorder.

## Output Shape

For a useful day plan, include:
- scheduled blocks
- deferred tasks
- one bottleneck
- one warning if the plan is too tight

## Current Command Caveat

The existing `plan` command is sequential and simple.

Use it as:
- a quick draft

Do not describe it as:
- full optimization
- conflict-aware scheduling
- calendar-grade planning
