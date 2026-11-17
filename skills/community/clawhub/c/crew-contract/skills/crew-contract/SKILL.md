---
name: crew-contract
description: "Use when any task should use main-sub delegation (主-子分工)."
license: MIT
metadata:
  hermes:
    version: 1.4.0
    author: Ming Fang
    tags: [delegation, subagents, orchestration, review, workflow]
    category: autonomous-ai-agents
    related_skills: [hermes-delegation-routing, parallel-workstream-orchestration, subagent-driven-development]
---

# Crew Contract — Main–Sub Delegation (主-子分工)

The main agent **conducts** — it doesn't play every instrument. The general division of labor for any substantial work, adapted from the "Astra + Luna" orchestrator pattern. The **main agent** keeps the goal, constraints, evidence and final judgment; bounded **subagents** do noisy execution; an **independent reviewer** checks material changes before anything is called done. Applies to engineering, research, writing, data, ops — anything. Project-specific processes plug in from their own docs; this skill is the method layer.

## When to use

- The owner invokes it: "用主-子分工", "main-sub", "delegate this", "让子代理做".
- Any work that materially benefits from decomposition, independent contexts, parallel work, or independent review.
- Multi-component / cross-cutting / risky work where evidence and a review gate matter.

Do **not** use for simple questions, single small edits, or quick lookups — keep those in the main thread. Never create agents just to satisfy a template; use only the roles that improve the task, and scale to the job (explorer + worker may be enough; add tester/reviewer when risk warrants). Never switch the main model merely to activate this mode. Owner instructions always take precedence over this method.

## Intent-driven guidance (defaults, not a rulebook)

This skill states intent and defaults — the dispatcher sizes effort, review and budget to the task's actual goal, and states a reason when deviating from a default. Only the invariants are non-negotiable: separation of duties (no self-review), evidence over self-report, fail-closed scope, agents don't commit, owner's permission/cost boundaries.

Defaults (adjust when the task clearly calls for it — note why):
- Small, local, sequential work: stay in the main thread; no subagents.
- Every brief carries BUDGET + STOP (see template): attempts/time ceiling + what to do when exceeded.
- At least one independent-context check before anything is called done; skip only for low-risk changes that were directly verified — and say so.
- Review depth scales with risk: separate context → evidence-anchored findings → cross-model / ground-truth when value warrants.
- Effort scales with task shape: one narrow child for a small lookup; several for genuinely independent streams — count coordination cost first (see "Orchestration signals").
- Handing work down fits by shape — clarity × verifiability × blast radius — not by a fixed list of cases (see "Handing work down (intent-driven)").

## Roles

| Role | Writes? | Job | Returns |
|---|---|---|---|
| explorer | no | Map files/symbols/flows/constraints/tests before implementation | Concise paths/symbols, risks, recommended boundary |
| researcher | no | Answer one external/version-specific question from primary sources | Verified facts vs inference; version/date assumptions; references; uncertainty |
| worker | yes | ONE bounded change with explicit ownership; smallest defensible change | Changed files, commands run, results, remaining risks |
| tester | tests only | Reproduce/verify with the smallest decisive test or command; never change production code to force a pass | Exact command, pass/fail, output, gaps |
| reviewer | no | Independently review the ACTUAL final change (not its intended story) | Findings (severity + file/symbol + impact + fix) or "no material findings" + residual uncertainty |

- The **main agent** owns: interpreting the real goal and authorization boundary; architecture, decomposition and ordering; non-overlapping ownership; resolving conflicting findings; integration; final inspection; all user-facing claims.
- The **reviewer must be a separate context** from whoever produced the work (self-review doesn't count). Material changes only — correctness, regressions, security and permission issues, data integrity, race conditions, compatibility, missing high-value tests; not style. Invoke it for high-risk, cross-cutting, security- or data-sensitive, non-obvious changes; skip it when the change is low-risk and directly verified.
- **Review independence is layered** — the owner's model policy always wins, and independence is never claimed as achieved (see "Unresolved limits"). When the available models span ≥2 families: high-risk or unanchorable review MUST go to a cross-family reviewer. When only one family is available: fall back to evidence-anchored review + position swapping (AB/BA) + long-CoT review + low-confidence escalation to human, and declare residual family-bias in the delivery. Supporting evidence map: [`references/evidence-index.md`](references/evidence-index.md).
- Review protocol checklist (use what the risk justifies): deterministic/ground-truth checks first; per-dimension rubric scored independently; position swap on comparisons; reviewers recompute verifiable facts (hashes, counts) instead of restating them; human-labeled golden set to calibrate rubrics before trusting an LLM judge at scale.
- Role constraints: the explorer reports uncertainty or conflicting evidence and does not redesign; the worker follows existing project patterns and avoids unrelated refactors; the tester edits tests only when asked; the reviewer edits nothing.

## Delegation contract (every brief)

Every dispatched task states:

1. one concrete objective;
2. exact scope / owned files;
3. necessary context only (children cannot ask questions — briefs must be self-contained);
4. constraints + forbidden scope expansion;
5. required deliverable;
6. acceptance evidence.

Subagents return conclusions, paths/symbols, commands + results, risks, blockers — no raw log dumps. Bulk or mechanical deliverables: write the artifact to a file, return a one-line status. Inline findings: keep the summary to ~1–2k tokens (prompt convention — there is no hard harness clamp; never promise one).

**Ambiguity contract (return block, not a pause):** every child's deliverable opens with `assumptions[] / needs_input[] / default_if_forced / blocking_level (low|high)`. Depth-1 children cannot pause mid-run and wait — this block is a structured RETURN, aligning vocabulary (not mechanism) with A2A `input-required`. On `needs_input`, the main agent closes the loop: clarify with the owner when blocking_level is high, then narrow re-dispatch; when low, proceed with `default_if_forced` and record it.

Copy-paste template with per-role quick fills: [`references/child-brief-template.md`](references/child-brief-template.md). Read it when drafting any dispatch.

## Model selection (route card)

No model names are hardcoded in this skill (grep-enforced). When work enters orchestrated mode, settle routes up front:

1. Candidate set = intersection of what the runtime can actually use (its provider registry / model list) and the owner's current model policy. Fewer than three qualify → present exactly those plus free-text; NEVER pad the list with policy-external models.
2. Ask once per slot — **execution slot** (all explorer/researcher/worker/tester children share one route) and **reviewer slot** (independent review). Criteria, not names: execution = cheapest adequate + cache affinity (see "Cost discipline"); reviewer = the layered independence criterion under "Roles".
3. Skip the prompt when the work stays in the main thread, the owner already named models, or a recent route card still matches current config — say which applies.
4. Provider changes are the owner's call: confirm explicitly, never pick a provider yourself (invariant).
5. Emit a route card (slot / model / provider / basis / effective time), then re-verify it immediately before dispatch — config can drift between asking and fanning out.

## Execution pattern

1. Decide: main-thread-only or orchestrated.
2. Read-only exploration/research first when the surface is uncertain (parallel where truly independent).
3. Main decides direction; assign each writable area to ONE worker at a time.
4. Implement (bounded workers).
5. Verify with the smallest decisive test/reproduction. Verification priority: deterministic checks (tests, hashes, compilers, exact match) > weak-verifier ensembles > LLM judges; treat the LLM judge as a scarce budget — verification compute should stay below generation compute, and calibrate a judge before trusting it.
6. Independent review for material/risky changes; resolve findings; re-run affected checks.
7. Main inspects the final diff/artifact, then claims completion. Agents don't commit — the main reviews and commits.

Serialize any stage that depends on earlier evidence; parallelize only genuinely independent work.

## Truncation & recovery

A child can be cut off (iteration cap, timeout) before its final write. Recovery order:
1. Inventory the disk first — with SAVE-EARLY the artifact usually exists and only the tail is missing; never assume nothing landed.
2. Prefer "artifact + one narrow re-dispatch" (or main-thread assembly) over re-sending the whole task.
3. Log the cut-off as a real event: fail-stop without durable resume is a known limit (below) — repeated cut-offs are evidence for changing budgets/staging, not for blind retries.

**Manifest checkpoint protocol (optional — not the default):** enable only when replay is likely — ≥3 slices, multi-child relay, or a prior cut-off / expected timeout. Otherwise SAVE-EARLY + narrow re-dispatch is enough (a single-slice task gets nearly all the benefit from SAVE-EARLY alone). When enabled: one task-level manifest (slice list + per-slice status/complete markers + artifact paths + next action); a resuming child reads the manifest first and works only unfinished slices. Rules: slices idempotent; artifacts append-only; resume points fall on slice boundaries.

Live steering may exist in some surfaces; treat it as best-effort, never as the correctness mechanism.

## Failure and scope handling

- A subagent hitting an architectural decision, schema/API change, new dependency, security-sensitive choice, unclear requirement, or overlapping ownership must **stop and report** — not expand scope.
- On failure: inspect why; narrow, retry, reassign, or handle it in the main thread. Never silently ignore.
- Never claim delegated work finished unless it actually ran and its result was checked.
- Before finishing: every required agent has completed or explicitly failed; nothing required is still running.

## Orchestration signals (when it pays)

Orchestration pays when the work is **parallelizable, bounded, and verifiable**: streams can run independently; each stream can be pinned down without asking questions (children can't ask); each has a check (test, ground truth, source, artifact) someone else can apply. It degrades on strictly sequential work (controlled study across 180 agent configurations: -39% to -70%), shared-file/state coupling, ambiguous requirements, or tiny tasks; coordination overhead grows with dependencies and tool count. Cost is ~15x chat tokens — the task's value must cover it. Signals, not gates: run ONE bounded child first, extend only if it clearly pays.

**Admission gate:** open subagents only when ≥2 of these hold — (a) genuinely parallelizable/decomposable; (b) does not fit one context window; (c) task value covers orchestration cost. Record a one-line written justification on the route card (the format is checkable; the judgment stays with the main agent).

## Cost discipline (why not everything)

Orchestration is not free: the main stays in the loop for the whole task, and every subagent carries and re-reads its own context. Parallelism trades tokens for latency. So: keep agent count proportional to genuinely independent work; avoid duplicate scans; ask for short reports (raw logs pasted into the main thread get re-read every turn); skip the reviewer for low-risk changes; don't orchestrate small tasks at all.

Cost levers in order — **cache hit rate → model routing → effort level**. Children share the parent's prompt cache only with byte-identical prefixes, same model, same effort; switch models at compaction moments (the cache miss is already being paid there). Cheap execution tiers do not cancel orchestration overhead.

## Handing work down (intent-driven)

Defaults, not rules — the main agent sizes each hand-down to the task in front of it.

**Fit by shape, not by case.** Judge fit by clarity × verifiability × blast radius (how far a mistake reaches × how reversible it is): clear + mechanically checkable + low blast radius → a good default for handing work to a cheaper executor; fuzzy, novel, or high-risk → keep it on the main line or with a stronger model. Complexity matters less than ambiguity: a long but crisp checklist suits a cheap executor; a short, vague judgment call does not. If the work cuts into clear steps with a check between each → hand the steps down; if every step's judgment feeds the next → keep it up here.

**Calibrate verification to what the task can prove.** Prefer deterministic checks (tests, grep gates, hashes, read-backs) over LLM review; review depth is a budget, spent where the task can't check itself. Borderline "does this need a review?" calls can go to a fast local typed-decision gate (choice/score) for a quick suggestion — it suggests, the main line decides. Output nothing can check must be reviewed or re-run; unverified output never gets laundered into a conclusion (an extension of "evidence over self-report"). Confidence in handed-down work comes from checkability, not from model tier.

**Class patterns accumulate.** When the same shape of task shows up again, add a line to [`references/class-playbook.md`](references/class-playbook.md): shape → who ran it → which verification actually caught a problem → review verdict. Learned from real work, not legislated up front; keep the lines short. Whoever runs the work adds the line; mark a line stale when the tooling or models it names change.

## Unresolved limits (mitigation only — never report as solved)

- **No durable resume.** A cut-off child is rescued by hand or restarted; mitigations: SAVE-EARLY artifacts, staged tasks, narrow re-dispatch, optional manifest protocol (above).
- **Reviewer independence is partial.** A clean context removes identity-visibility bias; a same-family reviewer still shares model blind spots — the layered criterion (Roles) mitigates but does not eliminate this; when only one family is available, declare residual family-bias in the delivery.
- **Children cannot ask questions (depth 1).** Handle with self-contained briefs + the ambiguity contract (explicit assumptions / needs_input return block); residual loss is inherent.
- **Evidence-strength gaps** (2026-09-20 evidence review, section 7): long-context degradation and code-review corpora at summary level only; no direct "cheap executor + expensive judge" study found (a 2026-05 formalization of cheap-reward + expensive-verifier is the closest — see evidence index); most conclusions are cross-source mapping inferences, empirical n=1; multi-turn finding from simulated sessions (external-validity limits).

Reporting rule: present these as open, mitigations in progress — never as resolved.

## Theory basis

- **Context hygiene is the primary value of subagents** (not specialization): verbose output and intermediate reasoning die in the child context; the main thread keeps the goal, constraints, evidence, judgment.
- **Separation of duties**: explore / implement / verify / review are distinct roles; the generator and the verifier always work in different contexts.
- **Non-overlapping ownership**: one writer per area; prevents merge chaos.
- **Evidence over self-report**: child summaries are claims; the main checks artifacts, diffs, commands, hashes.
- **Fail-closed scope**: silent scope expansion is the failure mode this method exists to prevent.
- **Evidence anchors** (see [`references/evidence-index.md`](references/evidence-index.md) for the full rule → source map): parallelizable tasks +81% vs strictly sequential -39–70%; uncoordinated parallel error amplification 17.2x → 4.4x with an orchestrator ([Google agent-scaling study](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)); multi-agent ≈15x chat tokens ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)); 41–86.7% failure across 7 SOTA multi-agent systems, 14 failure modes ([MAST, arXiv:2503.13657](https://arxiv.org/abs/2503.13657)); clean-context reviewers and conflicting-assumption risk ([Cognition](https://cognition.ai/blog/multi-agents-working)); weak-verifier ensembles close the generation–verification gap ([Weaver](https://arxiv.org/abs/2506.18203)). Reviewer family-bias 3.4–8.4pp even without self-review (arXiv:2508.06709, arXiv:2609.17857); context rot persists under perfect retrieval, 13.9–85% drop (arXiv:2510.05381); subagent clarification is a known platform gap (upstream not-planned); per-role model binding is standard in mainstream frameworks.

Harness-specific dispatch mechanics (Hermes example): [`references/hermes-mechanics.md`](references/hermes-mechanics.md).

## Instances (non-exhaustive)

- **Case/fixture production**: frozen-artifact review with author/reviewer/oracle context isolation — this skill supplies the division of labor, the project supplies its process.
- **Software development**: two-stage review pipelines; cheap CLI worker lanes with a supervising main agent.
- **Handovers**: evidence-bearing work receipts between agents or sessions.

## Provenance & changelog

Adapted from the "Astra + Luna" orchestrator (execution roles at high effort + a strong, low-effort, read-only reviewer) and the sub-agent pattern literature. Method validation report and sources referenced in `references/evidence-index.md`.

- v1.4.0 (2026-09-23) — hand-down guidance (shape-based delegation fit, verification calibration with typed-decision gates, class playbook); intent-driven, no new mandates.
- v1.3.1 (2026-09-23) — renamed `conductor` → `crew-contract` (marketplace name-uniqueness; method layer unchanged).
- v1.3.0 (2026-09-23) — model-agnostic route selection (route card + candidate-intersection rule); layered review-independence criterion + review protocol checklist; admission gate + cache-ordered cost levers; ambiguity contract (needs_input return block); optional manifest checkpoint protocol; verification priority; no hardcoded model routes (grep-enforced).
- v1.2.0 (2026-09-21) — intent-driven defaults, orchestration signals, truncation recovery, unresolved-limits discipline, evidence anchors.
