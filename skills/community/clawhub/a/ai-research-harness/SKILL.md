---
name: research-harness
version: 1.3.2
agent_created: true
description: >
  Cognitive discipline for AI-native scientific experimentation.
  Trigger when setting up controlled experiments with LLM agents,
  designing reproducible evaluation pipelines, or structuring research
  workspaces for long-running agent collaboration. Provides guardrails,
  not recipes — teaches agents how to reason about experiments, not
  which commands to run.
---

# research-harness

> Version: 1.3.2
> Cognitive discipline for AI-native scientific experimentation — guardrails, not recipes.

## When to Use

Trigger this skill when the user:
- Sets up a new AI-native research experiment repo
- Designs controlled experiments with LLM agents
- Needs reproducible evaluation, statistics, and error analysis
- Wants to structure a research workspace for long-running agent collaboration
- Wants agent-safe research governance that prevents overclaiming
- Says anything like: "research harness", "experiment framework", "AI科研", "对照实验", "评分体系", "可复现性", "科研workflow", "agent协作科研", "可控实验", "效应量"

## Core Philosophy

This skill does not prescribe *what* experiment to run. It prescribes *how to think* while running it.

Research agents fail not because they lack capability, but because they:
- Scale before validating the minimum loop
- Overclaim what the data proves
- Treat surprising results as methodology failures before checking the execution chain
- Delete failed runs to make progress look cleaner
- Change baselines or rubrics silently
- Invent designs from thin air without tracing them to published precedents or stated assumptions

The antidote is **cognitive discipline** — a set of non-negotiable mental habits enforced by repo structure, not by prompt reminders. Detailed reasoning for each discipline is in `references/scientific-thinking.md`.

A critical addition from real-world practice: **governance before scale**. When a closed loop produces strong signals, the most tempting mistake is to expand immediately. The correct move is to lock down claim boundaries, audit artifacts, fix provenance gaps, and only then scale. A dedicated calibration phase between closed-loop and full-scale expansion is a sign of maturity, not delay.

---

## Six Cognitive Disciplines

| # | Discipline | Core Question | Deep dive |
|---|------------|---------------|-----------|
| 1 | **Minimum Closed Loop Before Scale** | Can the smallest version produce distinguishable signals? | `references/experiment-design.md` |
| 2 | **Isolated Variables & Attributable Baselines** | Does each group add exactly one variable? | `references/experiment-design.md` |
| 3 | **Dual-Track Validation** | Do two independent scoring systems agree? | `references/scoring-statistics.md` |
| 4 | **Effect Size Over Significance** | What is the magnitude, not just the p-value? | `references/scoring-statistics.md` |
| 5 | **Pipeline Before Interpretation** | Was the execution chain verified before the hypothesis was questioned? | `references/scientific-thinking.md` |
| 6 | **Theoretical Grounding Before Design** | Can every design decision trace to a published precedent or an explicitly stated hypothesis? | `references/methodology-grounding.md` |

*Disciplines 1-2: experiment design. 3-4: scoring & statistics. 5: critical reasoning. 6: methodology accountability.*

---

## Seven Governance Rules

| # | Rule | Principle |
|---|------|-----------|
| 1 | **Human Owns Direction; Agent Owns Execution** | Agent cannot change research questions, promote evidence without review, or make academic decisions |
| 2 | **Evidence Has Status; AI Output Is Not Fact** | All AI-generated evidence starts as `candidate`; only back-to-source verification promotes to `verified` |
| 3 | **Failed Runs Are Data, Not Trash** | Register every run in the manifest; failures are process evidence against survivorship bias |
| 4 | **Protected Surfaces Change Only By Proposal** | Baselines, rubrics, raw results, and schema require version bump + documented proposal |
| 5 | **Every Handoff Needs an Alignment Doc** | Short doc replaces long chat history for agent onboarding |
| 6 | **Calibrate Before Scaling** | After a closed loop produces strong signals, lock down claim boundaries, audit artifacts, and fix provenance before expanding to full scale |
| 7 | **Methodology Review Gate** | Any "novel" design (no direct precedent) must have a Design Justification Document with ≥2 published precedents or explicit assumption declarations before entering experiment execution |

Details in `references/agent-collaboration.md`.

---

## Phase Workflow

### Phase 0 · Scaffold

**Goal**: Set up the three-layer repo and root entry files.

- **`thinking-space/`** — research direction, claims, decisions (human)
- **`execution-layer/`** — briefs, logs, results, drafts (agent)
- **`code-workshop/`** — runnable artifacts, packages

Root files: `AGENTS.md` (workspace map), `PLAN.md` (phase panel), `WORKFLOW.md` (procedure), `harness/README.md` (governance).

Directory skeleton and rationale: `references/repo-architecture.md`.

### Phase 1 · Harden

**Goal**: Make the repo self-checking before formal execution.

1. **Module contracts** — Each core module gets a `CONTRACT.md` (purpose, inputs, outputs, invariants, local validator). Template in `references/repo-architecture.md`.
2. **Local validators** — `scripts/validate_<module>.py` per module; `scripts/validate_repo_state.py` as aggregator. Gate rule: 0 FAIL before any formal run.
3. **Multi-level audit** — Structure validation as layered gates: schema-valid → evidence-governed → planning-useful → experiment-ready. Use a default mode (WARN only) during early phases and a strict mode (FAIL on gaps) before scaling. This keeps the repo moving without compromising the expansion gate.
4. **Experiment manifest** — `experiments/results/manifest.csv` as run-level provenance ledger (run_id, wave, task_id, group, model, version metadata, status, retry_of, git_commit).
5. **Protected surfaces** — Baselines, rubrics, raw results, scoring config, schema. Require version bump + proposal to change.

### Phase 2 · Design

**Goal**: Design attributable controlled experiments with grounded methodology.

- **Progressive building**: minimum artifacts → schema validation → small task set → dry run → scoring → expand. Design details in `references/experiment-design.md`.
- **Controlled groups**: Baseline → incremental treatments. Adjacent groups differ by exactly one variable.
- **Gold checklists**: Every task has `must_include`, `forbidden`, and `scoring_notes`. For multi-group experiments, separate gold checklists into `planning_gold` (items all groups can achieve) and `evidence_gold` (items only augmented groups can access).
- **Metric fairness annotation**: Each evaluation metric must declare `evidence_access_required` (`true`/`false`). Score families with different access requirements must be reported separately, never mixed into a single total. Details in `references/scoring-statistics.md`.
- **Artifact QA**: Creating knowledge artifacts (cards, schemas, tasks) follows a scaffold→validate→commit cycle. Validators catch syntax errors, enum mismatches, and registry sync issues before they accumulate. Details in `references/repo-architecture.md`.
- **Output contract**: Agent output follows a strict schema (YAML/JSON). The scorer and analysis pipeline depend on this contract.
- **Design justification** (Discipline 6): Before implementing any non-trivial schema, scoring system, or experiment protocol, write a Design Justification Document. Template and grounding framework in `references/methodology-grounding.md`. This is required, not optional.

### Phase 3 · Execute & Analyze

**Goal**: Run experiments, score, compute statistics, analyze errors.

Preflight gate: local validators must pass. Then:
1. **Dry run** — print prompt, no API call
2. **Smoke run** — 1 task × 2 groups, verify output parsing
3. **Wave 1** — small set × all groups, minimum viable data
4. **Scoring**: Track A (rule-based) + Track B (semantic) cross-validation. Details in `references/scoring-statistics.md`.
5. **Statistics**: Cohen's d primary, 95% CI, paired t, Wilcoxon. `--reproduce` flag for one-click reproducibility.
6. **Error analysis**: hallucination, output depth, specificity, task appropriateness.

### Phase 4 · Handoff & Writing

**Goal**: Package results for the next phase or agent.

- **Claim-safe memo**: After any closed loop that produces strong signals, write a memo separating: supported findings, positive signals, not-yet-supported claims, and required next evidence. This prevents overclaiming and directly drives the next phase. Never jump to expansion without calibrating the claim boundary first.
- **Alignment doc**: ~1 page with state, entry files, new surfaces, preflight commands, protected surfaces. Never pass chat history.
- **Upstream proposals**: Any insight affecting direction goes to `sync/upstream_proposals/` first. Template in `references/agent-collaboration.md`.
- **Writing markers**: `[REF-MISSING]`, `[CRITICAL-CHECK]`, `[TODO]`. Never use AI numbers without verification.

---

## Non-Negotiables

1. No unverified citation becomes a research fact
2. No debug result becomes a formal result
3. No agent changes baseline, rubric, or metric definitions without a proposal
4. No raw result is overwritten
5. No failed experiment is deleted
6. No phase gate passes before validators report zero FAIL
7. No closed loop expands to full scale before calibration: lock down claim boundaries, audit artifacts, and fix provenance gaps first
8. No non-trivial design enters execution without a Design Justification Document (Discipline 6)

---

## Theoretical Alignment: ETCLOVG Mapping

The **ETCLOVG** seven-layer taxonomy from *Agent Harness Engineering: A Survey* (Li et al., 2026, CMU/Yale/JHU) provides an external validation of this skill's structure and reveals two coverage gaps:

| ETCLOVG Layer | This Skill's Coverage | Gap Analysis |
|---------------|----------------------|--------------|
| **E**xecution | Phase 0 Scaffold (repo layers, validators) | ✅ Covered |
| **T**ooling | Module contracts, output schemas | ✅ Covered |
| **C**ontext | Protected surfaces, evidence status grading | ✅ Covered |
| **L**ifecycle | Phase 0–4 workflow, progressive building | ✅ Covered |
| **O**bservability | `manifest.csv` only | 🔴 **Missing**: no trace-native full-chain recording (model calls, tool invocations, state snapshots, retry/recovery actions, cost/latency) |
| **V**erification | Disciplines 3–4, dual-track scoring | 🟡 **Partial**: lacks trace-native evaluation (judging execution path quality, not just outcome) |
| **G**overnance | Seven Governance Rules, evidence status | ✅ Covered |

### Key Insights from ETCLOVG

1. **Harness Coupling Problem**: Changes to any ETCLOVG layer are not local optimizations — they propagate. Adding a tool changes context window usage, which changes verification reliability. **Rule: treat any layer change as a system-level change; re-validate all layers.**

2. **Cost–Quality–Speed Trilemma**: Stronger sandboxing, richer context, deeper evaluation improve quality but cost tokens, latency, and infrastructure. **When a closed loop produces strong signals, resist the urge to add more harness. Instead, audit what can be removed without quality loss** (Anthropic's finding: some context resets help old models but hurt newer ones).

3. **Trace-Native Evaluation**: Agent evaluation should not be "leaderboard-style" (who scores highest) but "quality control" (why did it fail, which layer caused it, is the evaluator itself trustworthy). **Record full execution traces; judge path quality, not just outcomes.**

### Actionable Supplements (v1.4.0 candidates)

- **Observability module**: Extend `manifest.csv` to a `traces/` directory per run, recording model calls, tool results, state snapshots, errors, retries, and cost/latency.
- **Path evaluation**: Add "was the execution path reasonable?" as a separate scoring dimension alongside outcome correctness.
- **Evaluator trustworthiness**: Before trusting an automated evaluator, ask: "Is the evaluator itself a potential failure point?" (Guerdan et al., NeurIPS 2025)
- **Harness decoupling audit**: When changing any ETCLOVG layer, run a cross-layer re-validation before trusting the results.

**Reference**: Li, J., Xiao, X., et al. (2026). Agent Harness Engineering: A Survey. *OpenReview*. [Project page](https://picrew.github.io/LLM-Harness/)

---

## References

- `references/repo-architecture.md` — three-layer repo, module contracts, manifest, validators
- `references/experiment-design.md` — progressive building, controlled groups, gold checklists
- `references/scoring-statistics.md` — dual-track validation, effect size, reproducibility
- `references/scientific-thinking.md` — cognitive disciplines for agent-led research
- `references/agent-collaboration.md` — governance, evidence status, alignment docs
- `references/methodology-grounding.md` — theoretical grounding for schema, scoring, and experiment design
