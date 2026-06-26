---
name: autoresearch-loop
description: "Run an explicit, bounded modify-verify-decide loop toward a measurable metric with approval gates, scoped edits, and rollback proof."
metadata:
  version: "0.2.1"
---
# Autoresearch Loop

Use this skill only when the user explicitly asks for an autoresearch or iterative improvement loop. It is for bounded, measurable optimisation in a version-controlled workspace. It must not start from casual improvement language, and it must not run unattended until the user has approved the goal, commands, scope, rollback strategy, run mode, and iteration cap.

The goal is measurable. Each iteration makes one atomic change, verifies it, and keeps or discards the result. The loop stops when the goal is met, the approved iteration cap is reached, the user stops it, or a blocker/safety gate is hit.

## Core Loop

```text
1. Confirm approved run contract
2. Read context + lessons file
3. Pick ONE hypothesis
4. Make ONE atomic change inside approved scope
5. Snapshot/commit before verification
6. Run approved VERIFY command
7. Run approved GUARD command
8. Decision: keep / discard / rework
9. Log the result
10. Health check and safety gate
11. Repeat only within approved cap
```

Read `references/loop-protocol.md` for the full loop spec.
Read `references/pivot-protocol.md` for the escalation ladder.
Read `references/lessons-protocol.md` for cross-run learning.

## Before Starting

Confirm with the user and do not start until the contract is explicit:
- **Goal** — one sentence describing what you want to achieve
- **Metric** — what number is measured, direction, baseline, and target
- **Verify command** — exact command used to measure the metric
- **Guard command** — exact command that must keep passing
- **Scope** — files/directories allowed to change, and files/directories that are forbidden
- **Rollback strategy** — normal branch/worktree revert, or isolated disposable reset
- **Run mode** — foreground by default; background/unattended only after explicit approval
- **Iteration cap** — required for background/unattended runs; recommended for foreground runs
- **External research policy** — web/search is off by default unless explicitly approved
- **Data boundary** — do not expose private code, secrets, logs, or proprietary data to external sources

Show the run contract and ask for confirmation. One round minimum. Then start only after the user says go.

## Verify vs Guard

- **Verify** = "Did the target metric improve?" — measures progress
- **Guard** = "Did anything else break?" — prevents regressions
- Guard files are never modified
- If verify passes but guard fails: rework up to 2 attempts, then discard

## Decision Rules

| Result | Action |
|--------|--------|
| Verify pass + Guard pass | Keep. Extract lesson. |
| Verify pass + Guard fail | Rework within approved scope (max 2 attempts). If still failing, discard. |
| Verify fail | Discard using approved rollback. |
| Crash | Stop unless the fix is clearly inside approved scope and non-destructive. |
| Syntax error | Fix immediately only if caused by the current iteration and inside approved scope. |

## Escalation Ladder

See `references/pivot-protocol.md` for full details.

| Trigger | Action |
|---------|--------|
| 3 consecutive discards | REFINE — adjust within current strategy |
| 5 consecutive discards | PIVOT — abandon strategy, try fundamentally different approach |
| 2 PIVOTs without improvement | Ask before external research unless pre-approved |
| 3 PIVOTs without improvement | Soft blocker — stop and report to human |

A single successful keep resets all counters.

## Long Run Hygiene

- Every completed experiment must be recorded before the next one starts
- Re-read original instructions every 10 iterations to prevent context drift
- Log: one row per iteration (iteration, commit/snapshot, metric, delta, status, description)
- For background runs, send progress at the approved cadence and stop at the cap

## Lessons

Extract structured lessons after:
- Every kept iteration (what worked and why)
- Every PIVOT decision (what failed and why)
- Run completion

Store in `autoresearch-lessons.md` in the working repo root unless the user chose another path. Do not commit this file unless the user explicitly asks. Consult it at the start of each run. Keep about 50 entries, summarising older ones with time decay.

## Safety

- Foreground mode is the default. Background/unattended mode requires explicit approval and an iteration cap.
- Make changes only inside approved scope.
- Commit, snapshot, or otherwise record only your own changes before verification.
- Revert only changes made by the current loop.
- Never reset unrelated user work.
- Never modify guard files unless the user explicitly changes the scope contract.
- Do not run destructive commands, deploy, publish, push, or touch production systems unless explicitly approved for this run.
- Do not use web search or external sources unless the run contract allows it.
- Do not paste private code, secrets, logs, customer data, or proprietary data into external services.
- Stop and report if the metric cannot be measured mechanically.
