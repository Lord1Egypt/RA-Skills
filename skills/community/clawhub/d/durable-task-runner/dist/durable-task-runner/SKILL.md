---
name: durable-task-runner
description: "Run long-running, multi-step work in OpenClaw without losing it to resets: durable state, progress updates, smart 'continue this' recovery, verification before completion, and optional subagent orchestration. Use when work spans multiple phases, must survive agent or gateway resets, or should not depend on ad-hoc chat memory. Best fit for users who want explicit recovery after interruption rather than fragile background scheduler setup."
---

Use this skill to run long work like an orchestrator, not like a goldfish.

## Core stance

Act as the **planner/controller**.
Do not rely on conversational memory for active long-running work.
Persist the working state to disk early and keep it updated.

Prefer this skill when any of these are true:
- duration will likely exceed a few minutes
- the task has multiple milestones or checkpoints
- the user wants progress reporting without repeated permission prompts
- interruption or reset would be costly
- work may need pause / stop / steer controls
- verification matters before calling the task done

Do **not** use it for trivial one-shot tasks.

## Required baseline

Before substantial execution:
1. create a task snapshot with `scripts/task_ctl.py create`
2. record milestones, done criteria, constraints, execution priority, and next step
3. keep updates flowing through the helper scripts instead of hand-editing state where practical

Durable task files live under:
- `state/tasks/<task-id>.json`
- `state/tasks/<task-id>.events.jsonl`
- `state/tasks/<task-id>.progress.log`

## Required behavior

### 1. Plan first

Create the durable task before real work starts.
At minimum capture:
- goal
- done criteria
- constraints
- desired state
- execution priority (`time` or `tokens`)
- phase
- milestones
- next step
- reporting cadence

### 2. Work in bounded slices

Prefer:
- scan -> checkpoint
- extract -> checkpoint
- execute -> checkpoint
- verify -> checkpoint

Each meaningful slice should end with a progress/event update.

### 3. Report progress without permission theater

For active long work, send informational progress updates:
- on milestone completion
- on phase change
- on blocker/retry/pause/stop/completion
- periodically for longer runs

Do not ask for permission to keep going unless the next action is risky, destructive, external, or ambiguous.

### 4. Respect control state

If the user pauses, stops, or steers the task:
- record it in durable state/event history
- checkpoint safely
- resume only when the durable state says to

### 5. Resume deliberately

After interruption or reset:
- prefer the explicit user-facing recovery move: **"continue this"**
- use `scripts/task_continue.py` to select the most relevant durable task and resume it intelligently
- review recent events and verify the last concrete step before any non-trivial follow-through
- use `scripts/task_resume_bootstrap.py` for restart analysis when you need to inspect the decision surface directly
- use `scripts/task_resume_apply.py` only for clearly low-risk follow-through

The intended model is **smart resume after reset**, not endless ambient scheduler theater.
By default, bootstrap should prefer **asking whether to continue** after reset/interruption; explicit user intent like "continue this" is what should flip the task back into active execution.

### 6. Verify before completion

Before marking a task complete:
- verify outputs or milestone results
- record a verification event
- then update `desired_state=completed`

## Subagent model

Use subagents only when parallelism is worth the added control surface.

Default roles:
- **main agent** = planner/controller/verifier
- **subagents** = bounded workers

When using subagents:
- keep each worker scope narrow
- avoid overlapping write targets unless coordination is explicit
- require structured worker returns
- run dropped-line checks before ending the turn

Read `references/subagent-return-protocol.md` when using worker lanes.

## What to read next

Read only what the current task needs:
- `references/quickstart.md` — minimal end-to-end usage pattern
- `references/task-schema.md` — snapshot/event structure
- `references/control-levels.md` — how much process the task earns
- `references/subagent-return-protocol.md` — worker return rules

## Key scripts

Use these directly:
- `scripts/task_ctl.py` — create/update/show/progress/event/control durable tasks
- `scripts/task_continue.py` — smart user-facing "continue this" recovery after reset/interruption
- `scripts/task_resume_bootstrap.py` — analyze resumability after interruption
- `scripts/task_resume_apply.py` — apply low-risk resume follow-through
- `scripts/task_reconcile.py` — reconcile pending/idempotent action state
- `scripts/task_subagent_ctl.py` — manage controller-side worker lines
- `scripts/task_subagent_run.py` — prepare a ready-to-use worker payload
- `scripts/task_report.py` / `scripts/task_ticker.py` — render compact status
- `scripts/task_tick_all.py` — run due status delivery across all eligible running tasks
- `scripts/task_install_tick_cron.sh` — print/install a cron entry for recurring ticks

## Attribution discipline

Keep attribution explicit when ideas or adapted structures come from other skills.
If you borrow more than general inspiration, update `ATTRIBUTION.md` and note it near the relevant file.
