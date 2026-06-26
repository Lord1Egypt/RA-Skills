---
name: goal-decomposer
description: Break a large, fuzzy, or long-running objective into smaller goal-mode tasks with clear scope, stop conditions, and validation steps. Use when the user wants to use Codex /goal effectively, has a big project that should be split into sequential goals, or asks for a plan that can be executed as a chain of smaller goals.
---

# Goal Decomposer

Turn one big goal into a short sequence of smaller goals that are concrete enough for goal mode to handle well.

## Core rule

Do not send one vague multi-day objective into goal mode if it can be split into clearer checkpoints.

## Workflow

1. Read the user's real objective.
2. Restate the final desired outcome in one sentence.
3. Split it into 3-7 smaller goals.
   - Prefer goals that are roughly 20-120 minutes of focused work.
   - Keep each goal to one main deliverable or checkpoint.
   - Preserve dependencies and execution order.
4. For each smaller goal, define:
   - title
   - why it exists
   - scope / constraints
   - done condition
   - validation method
   - the exact `/goal ...` command to start it
5. If the original request is still too vague, ask for the one missing decision that blocks useful decomposition.
6. If the task is too small for goal mode, say so and recommend normal execution instead.

## Heuristics

A good sub-goal should have:
- one clear outcome
- a visible checkpoint
- a concrete validation step
- an obvious stop condition

Avoid sub-goals like:
- "keep improving the app"
- "clean up the codebase"
- "make it production ready"

Prefer sub-goals like:
- "make the project build cleanly on Node 22"
- "replace the old auth helper and pass auth tests"
- "write README setup steps and verify them on a fresh clone"

## Output format

Use this structure unless the user requests another format.

### Final objective

One sentence.

### Recommended sub-goals

For each goal, include:

1. **Goal title**
   - Why: ...
   - Scope: ...
   - Done when: ...
   - Validate with: ...
   - Command: `/goal ...`

### Suggested execution order

Use a numbered list.

### Notes

- Mention risky or ambiguous goals.
- Call out any goal that should be split again before execution.
- Say when a normal one-turn task is better than goal mode.

## Goal command style

Write `/goal` commands so they include:
- the objective
- what to read first
- what not to change when relevant
- how to validate
- the stopping condition

Keep each command compact but specific.

Good pattern:

```text
/goal Update the README setup section for this repo. Read README.md and package.json first. Do not change application code. Validate by checking the documented commands against the repo files. Stop when the README has accurate install, run, and example usage steps.
```

## Boundaries

- Do not claim goal mode can handle arbitrary open-ended work well.
- Do not produce a giant backlog; produce the next useful chain.
- If the user wants execution too, first decompose, then recommend starting with the first sub-goal.
