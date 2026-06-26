# AANA Continuous Self-Improvement Skill

This OpenClaw-style skill helps agents improve across repeated work without silently changing their authority, memory, tools, or safety boundaries.

## Marketplace Slug

Recommended slug:

```text
aana-continuous-improvement
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and safety boundaries.
- `schemas/improvement-cycle.schema.json`: optional review-payload shape.
- `examples/redacted-improvement-cycle.json`: safe example payload.

## What It Does

The skill gives the agent a disciplined improvement loop:

1. Observe the task and result.
2. Score against explicit constraints.
3. Diagnose the smallest useful improvement.
4. Propose a future improvement.
5. Gate the improvement against scope, memory, files, tools, and policy boundaries.
6. Apply only low-risk current-task improvements.
7. Ask before persisting or reusing improvements later.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- change agent instructions,
- alter tool permissions,
- create automations.

## Safety Model

Self-improvement is useful only when it stays accountable. The skill requires explicit user approval before improvements affect future behavior, stored memory, files, tools, policies, or permissions.

Use redacted summaries for review payloads. Do not include secrets, tokens, passwords, full payment numbers, unnecessary private records, or unrelated user messages.
