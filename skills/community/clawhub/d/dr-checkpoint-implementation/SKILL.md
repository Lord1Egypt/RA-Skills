---
name: dr-checkpoint-implementation
description: Guide Codex through complex or production-risk implementation work in small validated checkpoints. Use when a user asks for staged implementation, step review before proceeding, shadow/dry-run rollout, alerting, cron, data pipeline, monitoring, integration, reporting, operational tooling, or tasks where requirements may evolve after inspecting real code, APIs, tests, or data. Avoid for small one-file fixes, pure brainstorming, or quick direct changes.
---

# dr-checkpoint-implementation

Implement complex work in small validated checkpoints instead of one large change.

## Core Rule

Do not perform complex implementation as one big change. Break the work into independently reviewable checkpoints, validate each checkpoint, revise the remaining plan, and apply the approval policy before continuing.

## Workflow

1. Restate the objective, constraints, and non-goals.
2. Break the work into small checkpoints.
3. Define acceptance criteria before coding each checkpoint.
4. Implement only the current checkpoint.
5. Run focused tests, validation, or dry-run evidence for that checkpoint.
6. Review the checkpoint using the template below.
7. Update the remaining plan if discovery changed anything.
8. Continue only when the current checkpoint is valid and the approval policy allows it.
9. Keep live rollout as a separate approval gate.

## Step Review Template

After every checkpoint, report:

- Implemented:
- Evidence:
- Learned:
- Remaining work:
- Plan changes:
- Approval decision: self-approved / needs user approval
- Reason:

## Approval Policy

Default to self-approval between checkpoints when:

- acceptance criteria are met
- focused tests or validation pass
- no new production risk or external side effect is introduced
- the remaining plan still matches the user's objective
- the user did not explicitly request manual review before continuing

Stop for user approval when:

- the user explicitly asked to review each step before proceeding
- enabling live external side effects such as notifications, writes, cron delivery, emails, public posts, production mutations, or production data changes
- changing scope, architecture, data model, rollout strategy, or user-visible behavior materially
- validation is missing, weak, flaky, or contradicts the plan
- real-data calibration shows uncertain or risky behavior
- proceeding would touch secrets, permissions, billing, customer data, or production infrastructure

## Production Safety Gates

- Prefer read-only discovery before write behavior.
- Treat real-data runs as calibration, not proof, until evidence quality is confirmed.
- For alerts, notifications, or other side effects, build dry-run rendering and cooldown/suppression tests before enabling delivery.
- Do not enable external side effects until explicitly approved.
- If data is missing or confidence is low, report that clearly instead of forcing a decision.

## Testing Expectations

Run the smallest useful test after each checkpoint. If a test or run reveals a flawed assumption, fix the assumption and add regression coverage before proceeding.

Use focused validation for narrow changes. Broaden testing when a checkpoint touches shared behavior, cross-module contracts, data pipelines, monitoring, alerting, integrations, or production-facing workflows.

## Plan Adjustment Rules

Revise the remaining plan whenever discovery changes data shape, API behavior, risk, acceptance criteria, rollout approach, or user-visible behavior.

Keep unrelated dirty worktree changes untouched.

## Stop Conditions

Stop and ask for user approval when the approval policy requires it, when safety gates cannot be satisfied, when validation cannot be made meaningful, or when the next checkpoint would exceed the user's requested scope.

## Apply To Workspace

To make this procedure mandatory instead of advisory, apply the policy block in [`references/APPLY.md`](references/APPLY.md) to the workspace instructions.
