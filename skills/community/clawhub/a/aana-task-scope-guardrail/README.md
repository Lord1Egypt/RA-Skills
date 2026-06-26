# AANA Task Scope Guardrail Skill

This OpenClaw-style skill prevents agents from expanding the task, using unrelated data, or continuing after the user request is complete.

## Marketplace Slug

Recommended slug:

```text
aana-task-scope-guardrail
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/task-scope-gate.schema.json`: optional scope-gate payload shape.
- `examples/redacted-task-scope-gate.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Identify the current request.
2. Define the smallest useful completion target.
3. Classify the proposed next action as in scope, necessary support, optional, out of scope, or complete.
4. Use only task-relevant data.
5. Ask before expanding scope.
6. Stop when the request is complete.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect systems by itself,
- approve expanded scope by itself.

## Safety Model

Use this skill as a local instruction boundary for agent behavior. It should prevent agents from turning narrow requests into broad projects, reading unrelated private data, or continuing to act after completion.

When additional work would be useful, the agent should present it as an optional follow-up rather than doing it automatically.
