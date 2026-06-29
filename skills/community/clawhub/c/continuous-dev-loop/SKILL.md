---
name: "continuous-dev-loop"
description: "Governed loop with roadmap, budget, ledger, and understanding debt."
---

# Continuous Dev Loop

Use this skill when a code project must advance in repeated, bounded rounds and each round must leave a machine-readable continuation contract.

This skill is not for broad brainstorming. It is for turning an established development direction into small verified slices that can continue without chat memory.

## Trigger

Use this skill only when all of these are true:

- The work is repository development work.
- The work can be advanced one slice at a time.
- The next round must be restartable from durable state.
- The round result must decide continue, stop, or block explicitly.

Do not use this skill for open-ended product strategy, initial milestone invention, or unbounded exploration. If the long-term direction is unclear, establish or update roadmap state first, then run the loop.

## Layer Model

This skill has three layers:

- `core`: mandatory one-slice protocol and footer contract
- `precision`: optional profiles, tuning, review cadence, metrics, and advisory scoring
- `governance`: optional long-horizon control for roadmap, budget, observation ledger, understanding debt, and review gates

`precision` and `governance` MUST NOT replace or weaken `core`.

If optional layers are unavailable, the `core` layer MUST still run correctly.

## Planning Model

Long-term planning and short-term loops live at different levels.

- `Vision`: stable long-term direction; human-owned by default.
- `Roadmap`: 4-8 week themes with exit conditions; loop may suggest changes but should not silently rewrite it.
- `Loop`: one verified slice per round.
- `Ledger`: durable facts about what happened.
- `Review`: checkpoint deciding whether the loop should keep following the roadmap.

Recommended durable files when a repo lacks equivalents:

- `VISION.md`: long-term direction and non-goals.
- `ROADMAP.md`: current phases, exit criteria, and review cadence.
- `LOOP_STATE.json`: current phase, current slice, budget, status.
- `round-ledger.jsonl`: append-only round observations.

Do not create competing files when the repository already defines equivalent state.

## Core Rule

One round equals one slice.

A slice is valid only when all of these are true:

- It has one dominant behavior change.
- It has one smallest concrete proof.
- It can produce exactly one `NEXT_SLICE` when continuation is healthy.
- It does not require overlapping write ownership without a merge plan.

Long-running loops should shrink slice size as autonomy increases.

## Required Invariants

Every round MUST satisfy all of these rules:

- Continue from explicit repo evidence first.
- Execute exactly one slice.
- Use exactly one coordinator.
- Verify the slice with:
  - one build, typecheck, or equivalent structural check
  - one smallest behavior proof tied to the slice
- Write continuity into repo-native or supervisor-owned state.
- End with the required human summary sections.
- End with the required machine-readable footer.
- Publish exactly one continuation truth.

Automatic continuation MUST NOT rely on chat memory.

## Continuation Priority

When choosing what to do next, use this order:

1. Explicit user priority for the current turn.
2. Previous round `NEXT_SLICE`.
3. Repo-native continuation evidence.
4. Current roadmap phase and exit criteria.
5. Existing project mainline already established in the repo.

If these sources conflict, stop and report the conflict. Do not invent a merged priority silently.

## Governance Checks

When governance is enabled, evaluate these before allowing continuation:

- `budget`: token, wall-time, cost, round, or retry limits.
- `understanding`: whether the coordinator or human can still explain the changed area and mainline.
- `observability`: whether the round leaves enough evidence to audit or replay the decision.
- `churn`: whether repeated edits, failed proofs, or scope drift indicate the slice is too broad.
- `review cadence`: whether a human, reviewer agent, CI gate, or formal gate is due before continuing.
- `roadmap fit`: whether the next slice still advances the current phase.

Governance advice is advisory unless repo-local runtime policy explicitly makes a gate enforcing.

## Budget Rule

Budget is an engineering signal.

If token use, elapsed time, tool retries, or patch churn rises unexpectedly:

- first response: shrink the next slice
- second materially similar response: add review or investigation before more implementation
- third materially similar response: stop automatic continuation with an appropriate blocker bucket

A loop MUST NOT keep expanding context to compensate for unclear scope.

## Understanding Debt Rule

A successful round may still increase risk if it adds code the coordinator or human cannot explain.

Track understanding debt when governance is enabled:

- `none`: changed behavior and affected files are explainable.
- `low`: minor unfamiliar code touched, bounded follow-up available.
- `medium`: important code path changed without enough review; review gate should be due.
- `high`: mainline understanding is no longer trustworthy; stop or require human review.

Code that passes tests but increases understanding debt is not automatically healthy continuation.

## Observation Ledger Rule

A governed loop SHOULD append a structured round event to a repo-native or supervisor-owned ledger.

A useful ledger records trace id, input source, selected slice, context evidence, files touched, commands, verification result, budget, churn or retry signals, continuation decision, and next slice or stop reason.

The ledger is factual evidence. It is not a replacement for the required footer.

## Multi-Agent Rule

Multi-agent execution does not relax the single-slice rule.

Allowed roles:

- `coordinator`
- `implementer`
- `verifier`
- `investigator`
- `reviewer`

Hard rules:

- There MUST be exactly one coordinator.
- Helper scope MUST be bounded before work starts.
- Parallel read-only work is allowed.
- Parallel write work is allowed only with explicit non-overlapping ownership.
- If write ownership overlaps, the coordinator MUST serialize integration.
- Helper output is evidence. Helper output is not continuation truth.

Read detailed role and merge rules in `references/multi-agent-governance.md`.

## Execution Modes

Use exactly one execution mode for the integrated round:

- `single-agent`
- `multi-agent-read-heavy`
- `multi-agent-split-write`

If governance friction increases, downgrade execution mode before retrying the same shape.

## Round Workflow

1. Read repo-native continuation evidence.
2. Read roadmap or phase state when present.
3. Choose one slice.
4. Choose one execution mode.
5. Establish repo policy constraints.
6. If precision is enabled, load project profile and tuning state.
7. If governance is enabled, establish budget, ledger, and review cadence.
8. Develop the slice.
9. Verify the slice.
10. If precision is enabled, run configured precision checks.
11. If governance is enabled, record budget, churn, understanding debt, and ledger event.
12. Evaluate continuation health.
13. Write continuity state.
14. Emit the human summary.
15. Emit the machine-readable footer.

## Repo Policy Profiles

A repository MAY declare one or more of these policy labels:

- `strict-clean`
- `warning-dirty`
- `commit-required`
- `push-required`
- `local-proof-heavy`
- `human-review-required`
- `budget-capped`
- `ledger-required`

Profile semantics are defined in `references/repo-policy-profiles.md`. If the repository already defines equivalent policy, use it as source of truth.

## Stop Rules

Stop automatic continuation when any of these are true:

- Required verification is missing or failed.
- Repo state is not trustworthy enough to continue.
- The same blocker recurs with materially unchanged evidence for three rounds.
- The current mainline no longer yields a credible next tiny slice.
- Human clarification, review, or permission is required.
- The loop contract is stale or incompatible with the supervisor.
- Budget policy says stop.
- Understanding debt reaches `high`.
- The next slice no longer fits the current roadmap phase.

Stop governance is defined in `references/stop-governance.md`.

## Human Summary Shape

End every round with these top-level sections in this exact order:

`Done`
- what changed

`Verified`
- exact checks and what they proved

`Risks`
- remaining uncertainty, blocker notes, proof limits, budget notes, or understanding debt

`Next`
- one next slice only, or `none`

If helper agents were used, add:

`Agents`
- coordinator role and helper roles used
- serialized write boundary or integration note when applicable

If governance was used, add:

`Governance`
- budget advice, ledger path, review gate, and understanding debt

## Required Footer

After the human summary, emit the exact core footer defined in `references/footer-contract.md`.

The core footer is mandatory.

Optional precision/governance fields MAY follow the core footer, but MUST NOT change the meaning of core fields.

Suggested governance footer fields:

```text
TRACE_ID: <id-or-none>
INPUT_SOURCE: <user|cron|github_issue|next_slice|monitor|manual|none>
CONTEXT_BOM: <path-or-none>
BUDGET_USED: <tokens/time/cost-or-none>
BUDGET_ADVICE: <continue|shrink|pause_review|stop|none>
UNDERSTANDING_DEBT: <none|low|medium|high|unknown>
CHURN_LEVEL: <none|low|medium|high|unknown>
REVIEW_GATE: <none|human|agent|ci|formal>
OBSERVABILITY_LEDGER: <path-or-none>
POLICY_DECISION: <continue|continue_with_warning|stop|none>
ROADMAP_PHASE: <phase-or-none>
```

## Precision Layer

The `precision` layer is optional.

It MAY add project-specific defaults, runtime tuning, advisory review scheduling, metrics, advisory scoring, and bounded hook execution.

The `precision` layer MUST NOT replace the footer contract, replace core stop rules, silently change continuation priority, imply automatic push or deploy, stop a loop by itself, or apply unscoped heuristics.

Read precision behavior in `references/precision-overview.md`.

## Governance Layer

The `governance` layer is optional.

It MAY add roadmap state, budget policy, observation ledger, understanding debt tracking, churn tracking, review checkpoints, and deterministic gates beyond the minimum proof.

The `governance` layer MUST NOT auto-rewrite long-term vision, treat continuation as default, expand authorization boundaries, merge/push/deploy/change product direction without explicit permission, mix raw ledger facts with distilled memory, or replace the core footer.

## Continuity State

A loop MUST write durable state into repo-native or supervisor-owned files.

Approved continuity surfaces include tasklists, progress logs, loop state docs, `LOOP_STATE.json`, `round-ledger.jsonl`, `.claude-orchestrator/current-next.txt`, `.claude-orchestrator/current-round.json`, deterministic verification scripts, and round ledgers.

If the repository already has a clear continuity surface, reuse it. Do not create competing state files.

If precision or governance is enabled, additional state MAY be written through templates.

## Out Of Scope

The core layer does not define scoring formulas, coverage heuristics, dashboards, automatic routing by score, automatic push behavior, repository-specific architecture heuristics, or long-term product direction as automatic loop output.

Those concerns require explicit precision support, governance support, repo-specific policy, or human direction.

## Anti-Patterns

Do not do any of these:

- treat a broad milestone as one slice
- let the loop invent long-term direction because `NEXT_SLICE` is empty
- emit multiple incompatible next steps
- continue silently after broken verification
- continue silently after repo drift, roadmap drift, or contract drift
- continue because budget exists when value is unclear
- let helper agents publish final continuation truth
- use a fake tiny slice to hide mainline exhaustion
- let default hooks commit unrelated changes
- let precision or governance output masquerade as core protocol
- treat passing tests as proof that understanding debt is acceptable
