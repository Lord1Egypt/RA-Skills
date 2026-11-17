---
name: dr-checkpoint-implementation
description: Guide Codex through consequential multi-stage implementation work in small validated checkpoints. Use for production rollouts or mutations, external delivery, scheduled automation, secrets/permissions/billing/customer-data changes, destructive work, major dependency or rollback risk, or explicit step review. Avoid routine direct work.
---

# dr-checkpoint-implementation

Implement complex work in small validated checkpoints instead of one large change.

## Trigger Gate

Use checkpointed implementation only for:

- production rollouts or mutations;
- external delivery;
- scheduled automation;
- secrets, permissions, billing, or customer-data changes;
- destructive actions;
- major multi-stage changes with meaningful dependency or rollback risk; or
- explicit user-requested step review.

Do **not** use it merely because work is reporting-related, operational, an
integration, or may evolve. Explicit exclusions include questions, research,
drafts, reports, read-only checks, routine validation, and ordinary reversible
non-production local code or workspace changes.

## Core Rule

For a triggered task, do not perform consequential multi-stage implementation
as one big change. Break it into independently reviewable checkpoints, validate
each checkpoint, revise the remaining plan, and apply the approval policy before
continuing.

## Workflow

1. Restate the objective, constraints, and non-goals.
2. Break the work into small checkpoints.
3. Define acceptance criteria before coding each checkpoint.
4. Implement only the current checkpoint.
5. Run focused tests, validation, or dry-run evidence for that checkpoint.
6. Record the checkpoint using the template below at meaningful phase
   boundaries. Keep it internal unless user approval is required or the user
   requested progress updates.
7. Update the remaining plan if discovery changed anything.
8. Continue only when the current checkpoint is valid and the approval policy allows it.
9. Keep live rollout as a separate approval gate.

## Step Review Template

After every checkpoint, record:

- Implemented:
- Evidence:
- Learned:
- Remaining work:
- Plan changes:
- Approval decision: self-approved / needs user approval
- Reason:

For a triggered long-running task, persist checkpoint records in task-local
state and continue automatically when self-approved. Do not record
micro-steps. A user-facing reply is reserved for a required approval, a
concrete blocker, a requested update, or final completion.

## Approval Policy

Default to self-approval between checkpoints when:

- acceptance criteria are met
- focused tests or validation pass
- no new production risk or external side effect is introduced
- the remaining plan still matches the user's objective
- the user did not explicitly request manual review before continuing

For a bounded live change, use one decision point:

1. Run a read-only preflight or dry-run.
2. Obtain one confirmation from Daniel or an already-authorised requester
   acting within their approved scope.
3. Execute the approved batch once.
4. Immediately read back the result.

Do not request repeat approval unless the target, scope, method, or risk
materially changes.

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
