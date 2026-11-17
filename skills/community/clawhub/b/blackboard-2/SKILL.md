---
name: "blackboard"
description: "Typed multi-model workspace with kitchen-shift ownership, resource, hazard, protected-target, and next-action handovers."
---

# Blackboard

Use when several models or agents must hand off one task without collapsing observations, guesses, decisions, actions, and test evidence into a notes blob.

This is an external coordination workspace. J-space is an internal model mechanism; this skill borrows only the selective shared-workspace idea and makes handoffs persistent and auditable.

## Operating model: a working kitchen in shifts

Treat contributors as specialist kitchen staff working overlapping shifts. The board is the shared station state and handover sheet, not a transcript of everybody's internal monologue.

Every worker must be able to establish:

- what is completed;
- what remains outstanding;
- what is in progress and who owns it;
- what failed and should not be repeated blindly;
- what resource, quota, time, hop, storage, or context budget is running low;
- what is hazardous or requires verification;
- what is reserved or **DO NOT TOUCH**;
- the exact next bounded action.

Workers need the relevant shared state; they do not need every other worker's private reasoning. Router and supervisory layers may expose only the entries relevant to the assigned capability while preserving full provenance underneath.

## Core rule

Read blackboard → validate station state → claim one bounded job → attach receipts → update hazards/resources/protected state → request the next capability → unload.

Never rewrite another contributor's entry. Append corrections or verification.

## Start

Use `scripts/blackboard.py`; do not hand-edit a live board.

```bash
python scripts/blackboard.py init BOARD.json --goal "..." --model "provider/model" --max-hops 6
python scripts/blackboard.py show BOARD.json
```

The board owns `policy.max_hops`; later commands cannot override it. Mutations lock the board for the full load/validate/change/write transaction, increment `revision`, write atomically, and preserve a timestamped backup. Use `--expect-revision N` on mutations when the caller has read a particular revision.

Read `references/schema.md` before router integration.

## One-hop workflow

1. Run `validate`. Stop on schema, policy, state, route-loop, ownership, or provenance failure.
2. Read the goal, typed collections, `revision`, current `next`, unresolved questions, active ownership, constraints, hazards, and remaining limits.
3. Claim or confirm exactly one bounded job matching the assigned capability. Do not duplicate active work.
4. Keep contributions typed:
   - `facts`: directly observed or source-stated claims.
   - `inferences`: interpretations, hypotheses, conclusions.
   - `user_decisions`: authenticated user choices, approvals, and constraints.
   - `evidence`: receipt locators, hashes, excerpts, tool results.
   - `actions`: operations actually attempted or completed.
   - `test_results`: explicit `PASS:` or `FAIL:` outcomes.
   - `failed_attempts`: failed approaches and boundaries.
   - `open_questions`: unresolved questions.
5. Every entry carries writer, timestamp, provenance, verification state, and route/ownership identity where the schema supports it.
6. Before any action, run `guard --target ...`. Every recorded action also requires `--target` and repeats the constraint check.
7. Destructive actions additionally require `--destructive --approval-entry UUID`. Approval must be a user-provenance decision whose exact content is `APPROVE: <target>`; it is single-use.
8. Before routing, record material resource pressure, hazards, stale assumptions, and protected targets. Never silently hand over a nearly exhausted budget or an unverified dangerous state.
9. Set the smallest next capability and bounded instruction with `route`. Routing is allowed only from `active`.
10. End the model turn after handoff.

## Shift handover contract

A route, pause, lead-model change, or session close must leave a compact operational handover containing:

1. **Outcome / current state**
2. **Completed**, with receipt locators
3. **In progress / owner**
4. **Outstanding**
5. **Failures / do not repeat**
6. **Running low / limits**
7. **Hazards / must verify**
8. **Reserved / DO_NOT_TOUCH**
9. **Exact next action and required capability**
10. **Revision, route ID, locks, and rollback**

Use `none known` rather than leaving safety-critical categories ambiguous. Do not dump chain-of-thought. Preserve conclusions, evidence, decisions, failure boundaries, and state needed for continuation.

## User constraints and identity boundary

`DO_NOT_TOUCH: <target>` is the machine-readable equivalent of a reserved item in the walk-in. It is a hard constraint and blocks that exact target and descendants.

The helper requires every `user_decisions` entry to have a `user/*` writer identity and at least one `provenance.kind=user` source. A JSON file cannot authenticate a human by itself: the router or calling environment must bind `user/*` and user provenance to the authenticated inbound user, and must not expose those credentials as model-selectable strings.

## State

Allowed transitions are mechanically enforced:

- `active` → `needs_user`, `needs_verification`, `blocked`, or `completed`.
- `needs_user` → `active` only after a newer user decision.
- `needs_verification` → `active`, `blocked`, or `completed`.
- `blocked` and `completed` are terminal.

Completion requires a `PASS:` test written by a model that did not perform the tested non-route action, or a PASS entry independently verified by another model. Merely having a test-result entry is insufficient.

Raising `policy.max_hops` requires an unused user decision exactly matching `APPROVE_POLICY: max_hops OLD -> NEW`. Lowering it cannot go below the current hop count.

## Verification

A writer cannot verify its own entry. A verifier checks cited provenance, appends verification, and records a typed verdict.

Verification is the incoming shift checking the label and station rather than trusting that “done” was written. Critical, volatile, destructive, or recovery-sensitive claims must be rechecked before action.

```bash
python scripts/blackboard.py validate BOARD.json
```

Use `references/canary.md` for the three-model canary.
