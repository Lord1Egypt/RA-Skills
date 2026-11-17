---
name: aegis-structured-execution
description: 'Use when substantial project work needs execution control. USE FOR: "proof-heavy execution pass", "multi-phase drift control", "scope-proof-checkpoint coordination". DO NOT USE FOR: "tiny one-shot edit", "general brainstorming", "simple formatting".'
disable-model-invocation: true
---

# Aegis Structured Execution

Use this skill for broad, risky, multi-phase, or proof-heavy work where execution state can drift.

## Contract

1. Identify the deliverable, scope, non-goals, truth sources, and proof requirements.
2. Split work into phases only when trust boundaries, proof modes, or execution surfaces differ.
3. Keep final synthesis in the coordinator; helper agents may gather evidence but do not define final truth.
4. Separate current state, target state, validated proof, unresolved gaps, and drift.
5. Follow `aegis-html-ledger` throughout execution: record the active work before it begins and keep its actual state, plan changes, and exact resume point current in the local project ledger. Cloud copying is optional and requires authorization covering this project's records, the destination account and folder, and the content scope. Reuse valid existing authorization; selecting this skill alone does not grant it. With no such authorization, keep the ledger local, mark cloud sync as not enabled, and continue the work. Never copy credentials, private conversations, personal records, or restricted project content by implication.
6. Use completion messages through the established coordination route alongside the ledger to report the outcome and remaining work.
7. Report completion only at the strongest proven level: `implemented`, `code_proven`, `test_proven`, `runtime_proven`, or `end_to_end_proven`.

## Issue and PR structure

Establish whether the reported problem is real before creating its issue.
Determine early whether the fix needs one PR or several.

For a simple change, create the issue and PR in the same delivery phase and
link the PR to the issue, so discussion can also happen on the issue.

For a complex change, create an umbrella issue and the first PR, linked in the
same way. Organize the remaining PRs as a dependent stack for a multilayer
problem, or as parallel PRs when the work can proceed independently.

## Completion Criteria

The execution pass is complete only when the deliverable, proof level, unresolved gaps, and next safe action are explicit and do not contradict repo truth. The active ledger must preserve the current work and plan changes needed for another session to continue. When a handoff is selected, use this state as input while preserving the selected handoff skill's format, disclosure, delivery, and acceptance requirements.

## Red Flags

- The plan becomes generic ceremony.
- Helper output is treated as final authority.
- Proof is inflated by docs, HTML, or tracker status.
- A contradiction is smoothed over instead of marked as `drift` or `gated`.

## Boundary

Do not use this as a heavy wrapper for tiny one-shot tasks. Use `aegis-html-ledger` for ongoing project state. Add `aegis-communication-discipline` when its communication contract is relevant; it is not a mandatory companion for every task.
