---
name: cms-project-governance
description: Keep a drifting or half-finished project under control with one compact, conflict-checked delivery state, right-sized scope, bounded autonomy, and independent QA acceptance. Use for non-technical requirement guidance, Legacy Bootstrap, Small/Medium/Large sizing, Lite/Standard/Full governance, Controller-Developer-QC routing, Milestones, Work Orders, QA acceptance, drift recovery, target rebaseline, roadmap review, or reducing token and document overhead. Typical triggers include 项目做了一半 / 不知道该不该继续 / 范围蔓延 / 想加新方向 / 想重开一个项目, scope creep, we keep adding features, too many documents and no working code, docs outweigh code, governance overhead is too high, 治理内卷, which project should I kill, should I archive this, redefine done, change the target, rebaseline, is this really accepted, and we accepted it but never shipped. Also use for anti-involution doc budgets, archive discipline, stop-loss rules, Active Packet bootstrap, and accepted-but-never-released risk. For already-authorized ordinary coding loops, use agent-loop-engineering. For a one-time read-only verdict on a project you have not committed to yet, use project-lifecycle-navigator.
---

# CMS Project Governance

Version: 2.2.1

Use this skill as the control plane for AI-assisted software delivery. Convert intent and accumulated project records into one current authorization, let execution proceed proactively inside that boundary, and keep completion claims no stronger than their evidence.

Respond in the user's language. Use plain language before technical language.

## Language Files

- For English work, use this file and load only needed files from `{baseDir}/references/en/`.
- For Chinese work, first read `{baseDir}/SKILL.zh-CN.md` and load only needed files from `{baseDir}/references/zh-CN/`.
- Keep machine-readable keys and enum values in English.

## Core Principles

1. The user owns purpose, priorities, and consequential decisions.
2. The AI should resolve ordinary reversible implementation choices without shifting them to a non-technical user.
3. Governance reduces uncertainty, drift, token cost, and rework; it does not maximize documents.
4. One current fact has one authoritative home.
5. A Milestone is a coherent user-observable capability, not a short task, test failure, or timed stage.
6. `Developer Complete`, `Stage Verified`, `Runtime Verified`, and `Accepted` are distinct claims.
7. Contract or document acceptance is not runtime feature acceptance.
8. Evidence outranks status text; conflicting evidence uses the weaker result.
9. Local compliance does not excuse global goal drift.
10. Use the lightest governance profile that controls actual risk.
11. Governance output is priced by uncertainty removed, not by documents produced. When document volume grows while verified behavior does not, governance itself has become the risk.
12. A target change creates a new baseline record; it never annotates the old one as void in place. History is archived by moving it, not by stacking override notes.

## Relationship To Agent Loop Engineering

- This skill discovers, sizes, bootstraps, authorizes, aligns, and accepts work.
- `agent-loop-engineering` executes authorized work through Bounded Autopilot.
- Both use one `Docs/ACTIVE_PACKET.md` with contract version `2.0` and 2.1 policy fields.
- This skill owns target and final QA authority; execution owns implementation and stage evidence.
- In a one-agent prompt, `QC` means Stage Reviewer. Standard/Full final acceptance remains independent.
- Use `project-lifecycle-navigator` instead for a one-time read-only verdict, such as go / narrow / pivot / archive / stop, when no persistent governance state is needed.
- **Standalone install.** This skill works without `agent-loop-engineering`. Any `{baseDir}/../agent-loop-engineering/...` path or `node <agent-loop-engineering>/scripts/...` command in this document is a convenience shortcut for co-installed setups only. When that sibling skill is absent, state it in one line and substitute the equivalent in-skill action: skip the Active Packet bootstrap script and write `Docs/ACTIVE_PACKET.md` from the bundled template; replace the loop-state validator with a manual stage-evidence check; replace reading `isolated-delegation.md` with the at-most-three-workers rule stated above. Never fail a run only because the sibling skill is missing.

Read `{baseDir}/references/en/execution-contract.md`.

## Cross-Plugin File Contracts (CDH)

When Personal Supervisor and Governance both run in the same Cordis context,
file ownership follows the CDH handshake — not a shared mutable folder. Read
`{baseDir}/references/en/cross-plugin-file-contracts.md` before writing
`.agent-state/<task-id>/` files, stamping `governance/supervisor-binding`, or
citing an Active Packet / Work Order across the plugin seam.

Plugins implement that contract; this skill owns the schema text. Conflicts
resolve in favor of the reference file.

## Choose One Mode

Choose one authority mode per pass:

| Need | Mode | Reference |
| --- | --- | --- |
| Idea or problem is still vague | Goal Discovery | `goal-discovery.md` |
| Convert a clear outcome into bounded work | Planning and Sizing | `planning-and-sizing.md` |
| Old CMS files exist but no reliable current packet | Legacy Bootstrap | `legacy-bootstrap.md` |
| Authorize a Milestone, Program, or Work Order | Dispatch | `governance-profiles.md`, `controller-qa.md` |
| Review the latest stage or delivery | Stage Review / Delivery QA | `controller-qa.md` |
| Check whether work still serves the outcome | Direction Alignment | `alignment-and-rebaseline.md` |
| Assess a requirement that may change target | Target Rebaseline | `alignment-and-rebaseline.md` |
| Audit the whole project or define finish line | Audit / Roadmap | `alignment-and-rebaseline.md` |

Do not mix a whole-project audit, latest-delivery QA, and target rebaseline in one authority pass.

## Legacy Bootstrap

When no valid Active Packet exists:

1. locate `Docs` or `docs` case-insensitively;
2. index names, sizes, and timestamps without reading all bodies;
3. read only canonical current-state files and files they explicitly link;
4. identify current target, acceptance, active Work Order, latest effective state, and one next action;
5. detect contradictory routes, duplicate current assignments, superseding QA decisions, missing authority, and claim-class mismatch;
6. compute an authority fingerprint;
7. draft one compact Active Packet when coherent;
8. write only with explicit `--write` and only inside the resolved workspace.

Use:

```text
node {baseDir}/../agent-loop-engineering/scripts/bootstrap-active-packet.mjs --workspace <project-path> --json
```

If the skills are installed separately, locate the same script inside the installed `agent-loop-engineering` skill. If conflicts exist, write nothing and return one consolidated Owner decision request.

Preserve legacy history. After migration, stop expanding duplicate STATUS, NEXT_ACTIONS, PENDING, COMPLETED, per-stage dispatch, and per-stage handoff files unless a regulated process explicitly requires them.

Read `{baseDir}/references/en/legacy-bootstrap.md`.

## Universal Workflow

```text
Idea, request, or legacy state
  -> discover or bootstrap one desired outcome
  -> define minimum useful scope and Non-Goals
  -> classify delivery claims and evidence
  -> size Small / Medium / Large
  -> choose Lite / Standard / Full
  -> create or refresh Active Packet
  -> Bounded Autopilot execution
  -> stage review and repair as needed
  -> alignment checks
  -> independent final QA when required
  -> accept, repair, split, rebaseline, or stop
```

Proceed with reversible uncertainty when assumptions are explicit. Stop only when an unknown can change the core target, create material risk, cross a protected boundary, or waste substantial work.

## State And Claim Dimensions

Keep these dimensions separate:

| Dimension | Values |
| --- | --- |
| Goal readiness | `Concept`, `Direction`, `Ready for Planning`, `Ready for Execution`, `Owner Decision Required` |
| Execution | `Ready`, `In Progress`, `Ready for Independent Acceptance`, `Needs Fix`, `Blocked`, `Invalid State` (`Ready for Review` is legacy input) |
| Alignment | `Aligned`, `At Risk`, `Locally Compliant, Globally Misaligned`, `Owner Review Required` |
| Stage review | `Not Reviewed`, `Passed`, `Needs Fix`, `Blocked` |
| QA decision | `Not Reviewed`, `Accepted`, `Accepted With Risk`, `Failed`, `Blocked`, `Not Required` |
| Project | `Active`, `Needs Fix`, `Blocked`, `Accepted`, `Accepted With Risk`, `Invalid State` |
| Delivery class | `Runtime`, `Contract`, `Governance`, `Artifact`, `Mixed` |

Do not describe a Contract milestone as implemented runtime, a screenshot as interaction proof, a build as usability proof, or Stage Reviewer approval as independent acceptance.

## Autonomy And Acceptance

For `acceptance_mode: Layered`:

- Controller may authorize several bounded stages in one Packet.
- Developer proceeds without asking after each successful loop.
- Stage Reviewer may pass a stage or return `Needs Fix` on the same Packet and Work Order.
- Standard/Full terminal state is `Ready for Independent Acceptance`.
- Independent QA receives criteria, diff, commands, raw evidence, limits, and target link, not the Developer's desired verdict.

Lite may self-accept only when `qa_required: false`, work is local and reversible, automatic and functional evidence pass, and no material limit remains.

Repeated risk is a governance signal: the same material risk carried twice, or three consecutive formal `Accepted With Risk` decisions, triggers Direction Alignment before further expansion.

Read `{baseDir}/references/en/controller-qa.md`.

## Alignment And Resizing

Run a lightweight target-link check every stage. Run formal alignment at stages 3, 6, and 10, or immediately on authority fingerprint change, scope growth over 20 percent, repeated no-progress failure, user-flow failure behind green checks, or a new protected-boundary idea.

Direction Alignment does not rewrite the target. Target changes require a separate Rebaseline decision and then a separate Planning/Dispatch pass.

Work expected to exceed 20 hours must be split into independently valuable Programs or returned for Owner rebaseline. Do not authorize an unreviewed 30-40 hour run.

## Compact Reading And Documents

Normal governance reads:

1. Active Packet;
2. linked authority files only when fingerprint changed;
3. current Work Order or delivery delta;
4. required evidence;
5. last three to five loop records.

Audit mode may read broadly but must remain read-only and use an explicit context budget. Do not use audit-sized context for each execution loop.

For high-output discovery, logs, validation, or independent QA, authorize isolated workers instead of expanding the coordinating context. Default to at most three active workers, one coordinating writer, disjoint write scopes, fingerprint-and-excerpt authority sharing, and summary-plus-evidence returns. Do not delegate small or tightly coupled work where worker startup and rereading would cost more than direct execution.

Read the execution skill's `{baseDir}/../agent-loop-engineering/references/en/isolated-delegation.md` when multi-agent delegation is authorized.

Create a file only for a durable authority boundary, Owner decision, final independent QA decision, cross-team handoff, formal rebaseline, or archive boundary. Standard governance normally needs only Active Packet, Loop Runs, one consolidated Work Order when useful, and one final QA decision.

Read `{baseDir}/references/en/governance-profiles.md`.

## Anti-Involution Controls

Governance fails in a specific way: it keeps producing correct-looking artifacts while the product stops moving. Watch the ratio, not the intent.

- **Document budget.** Active governance documents should stay small enough to read in one pass. When the active set outgrows that, move history to `Docs/archive/YYYY-MM.md` and keep only the current authority live.
- **Doc-to-code signal.** If document count or bytes materially exceeds source volume, or if a reporting period produces documents but no code change and no new verified behavior, stop expanding governance and report the imbalance as the finding. A five-line codebase with hundreds of governance documents is a governance failure, not a documentation success.
- **Archive by moving.** Superseded targets, old baselines, and closed loops are moved, not annotated. Never add `Superseded`, `CURRENT OVERRIDE`, or `this section is void` notes inside a live authority file; a reader must not have to reconstruct which layer is current.
- **Rebaseline is additive.** A target change writes a new `REBASELINE-<date>.md` and archives the prior baseline in the same pass.
- **`Accepted With Risk` needs an exit.** Every such decision carries the specific unlock condition, an owner, and a date. Without all three it is not risk-qualified acceptance; it is an unresolved blocker wearing a green badge. `Accepted` but never released is a governance defect and must be reported as such.
- **Subtraction before addition.** When a new direction arrives, name what will be dropped or paused before authorizing anything new. New scope is the strongest lure toward scope creep, and a portfolio only gets healthier by removal.

Read `{baseDir}/references/en/anti-involution.md`.

## Required Gates

- Do not execute before outcome, scope, Non-Goals, acceptance evidence, write boundary, and one next action are coherent.
- Do not write a bootstrap packet when current authority conflicts.
- Do not accept Standard/Full work from the same agent's stage review.
- QA failure stays on the same Milestone and Work Order as a bounded repair.
- Do not move failed core behavior, missing primary environment, or missing user flow into `Accepted With Risk`.
- Diagnostic sharding cannot silently replace an authorized full regression gate.
- Stop for Owner decisions on target, Non-Goals, protected architecture/data, production, credentials, deployment, paid resources, destructive action, or irreversible choice.
- At stage 10, accept, repair, split, rebaseline, or stop.
- Do not authorize work whose purpose, exclusion list, done condition, and primary user flow cannot each be stated in one sentence. An unanswerable "what does done mean" is a stop, not a question to defer into execution.
- Do not let the active governance document set grow without archiving; when the active set is no longer readable in one pass, archive before adding.
- Do not record `Accepted With Risk` without an unlock condition, an owner, and a date.
- Do not treat a project that has been accepted but never released as finished; surface it as an unresolved release blocker.

## Validation

Use the execution skill's compact validator:

```text
node <agent-loop-engineering>/scripts/validate-loop-state.mjs --workspace <project-path> --summary --max-findings 20
```

Use `--strict-history` only when historical log migration is the task. Thousands of legacy field gaps must be grouped, not emitted line by line.

Validate a CDH handshake front-matter fence on an execution-layer Markdown file:

```text
node {baseDir}/scripts/validate-handshake-frontmatter.mjs --file <.agent-state/.../HANDOFF.md> [--json]
```

## Output Contract

End governance responses with:

```text
Mode:
Current readiness/state:
Delivery class:
Decision:
Why:
Do now:
Do later:
Do not do yet:
Owner decision needed:
Next evidence:
Files created or updated:
```

In QA, include criterion, evidence level, decision, correction, owner, and re-verification. Keep the response usable by a non-technical Owner.
