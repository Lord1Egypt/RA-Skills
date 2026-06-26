# Unified Orchestrator v2

**A meta-skill that unifies intent-engineering, dark-factory, and feedback-loop into a single self-evolving system — and unlocks five paradigm shifts that none of the three skills can achieve alone.**

---

## When to Use This Skill

Use this skill whenever you need to take a goal from raw language all the way to a verified, continuously improving implementation — in one command. It replaces the manual handoff between intent-engineering, dark-factory, and feedback-loop with a single pipeline that:

- Translates goals into machine-executable specifications
- Executes those specifications autonomously
- Measures outcomes against the original intent
- Generates regression tests from every failure
- Feeds improvements back into the next cycle automatically

Use individual skills when you need surgical control over a single stage. Use this skill when you want the full loop.

---

## The Five Paradigm Shifts

These are capabilities that emerge only when the three skills operate as a unified system. They are not features — they are new modes of operation.

### Paradigm Shift 1 — Specification Drift Detection

**What it is:** The system continuously compares what was *intended* (the specification produced by intent-engineering) against what was *executed* (the outcome report from dark-factory) and what was *observed* (the feedback loop analysis). Over multiple cycles, it builds a drift map: a quantified record of how far execution has wandered from original intent.

**Why it matters:** In isolated skill usage, drift is invisible. A specification can be perfectly written, execution can pass all tests, and the feedback loop can report healthy scores — while the system is quietly drifting away from the original goal. Only by holding all three artifacts simultaneously can the orchestrator detect semantic drift: the gap between what the goal *said* and what the system *does*.

**How it works:** `signal_router.py` computes a `drift_score` (0.0–1.0) by comparing the specification's `success_criteria` against the feedback loop's `alignment_score` and the dark-factory's `pass_rate`. A drift score above 0.15 triggers a re-specification cycle automatically.

---

### Paradigm Shift 2 — Capability Expansion via Meta-Learning

**What it is:** After each full pipeline cycle, `meta_learner.py` analyzes the complete history of specifications, outcomes, and improvement reports to identify *patterns* — recurring failure modes, consistently high-performing specification patterns, and improvement suggestions that were applied and worked. It then updates the skill registry and the shared intent framework with these learnings, making every future run smarter.

**Why it matters:** Individual skills improve within their own domain. The feedback loop makes the feedback loop better. Intent-engineering makes specifications better. But neither knows what the other learned. The meta-learner operates across all three domains simultaneously, compounding learnings: a failure pattern discovered in dark-factory execution informs how intent-engineering writes specifications, which changes what dark-factory executes, which changes what the feedback loop measures.

**How it works:** `meta_learner.py` maintains a `learnings_log.json` that accumulates cross-cycle patterns. After 3+ cycles on the same goal, it generates `specification_patches.json` — suggested improvements to the specification template itself — and `rule_patches.json` — new suggestion rules for the feedback loop analyzer.

---

### Paradigm Shift 3 — Autonomous Re-specification

**What it is:** When the system detects that a specification is no longer achievable given observed constraints (e.g. a success criterion of `duration_ms < 500` that has never been met in 5 cycles), it autonomously generates a revised specification with adjusted criteria, documents the revision rationale, and continues the pipeline — without human intervention.

**Why it matters:** Current AI systems fail silently or loop forever on impossible goals. This system detects impossibility, documents it, adjusts, and continues. The human gets a clear audit trail of what was attempted, what was impossible, and what was substituted — rather than a system that either crashes or silently lowers its own bar.

**How it works:** `pipeline.py` tracks `consecutive_failures` per success criterion. After a configurable threshold (default: 3), it calls `capability_expander.py` which generates a `revised_specification.json` with adjusted criteria and a `revision_rationale.md` explaining the change. The pipeline continues with the revised spec and flags the cycle as `auto_revised`.

---

### Paradigm Shift 4 — Cross-Goal Skill Transfer

**What it is:** When you run the unified orchestrator on a new goal, it first searches the `learnings_log.json` for similar past goals (by semantic similarity of the goal description). If a match is found above a configurable threshold, it bootstraps the new specification from the prior goal's best-performing specification version — skipping the cold-start problem entirely.

**Why it matters:** Every AI system starts from zero on every new task. This system starts from the closest thing it has already learned. A goal like "process customer support tickets with 98% accuracy" will bootstrap from any prior goal involving classification, accuracy thresholds, or text processing — not just identical goals. The system accumulates institutional knowledge across goals, not just within them.

**How it works:** `meta_learner.py` maintains a `goal_similarity_index.json`. On each new run, `pipeline.py` queries this index using keyword overlap and structural similarity. If a match scores above 0.6, the matched goal's `best_specification.json` is used as the starting template, with the new goal's specific criteria overlaid.

---

### Paradigm Shift 5 — Verifiable Improvement Chains

**What it is:** Every cycle produces a cryptographically signed improvement report. The unified orchestrator chains these reports together — each report contains the SHA-256 hash of the previous report — creating an immutable, independently verifiable improvement chain. Any external party can verify that improvement claim X was produced from observation Y, which was produced from specification Z, in cycle N.

**Why it matters:** AI systems routinely claim improvement without proof. This system produces a tamper-evident chain of evidence: you can prove to any stakeholder exactly what changed, when, why, and what effect it had. This is the foundation for auditable AI governance — not as a compliance afterthought, but as a first-class output of every run.

**How it works:** `pipeline.py` reads the `chain_tip` from `improvement_chain.json` (the hash of the last report) and includes it in the current report before signing. `signal_router.py` provides a `verify_chain` command that re-computes all hashes and confirms chain integrity.

---

## Architecture

```
unified-orchestrator-v2/
├── SKILL.md                                   ← this file
├── scripts/
│   ├── pipeline.py                            ← main entry point — runs the full loop
│   ├── meta_learner.py                        ← cross-cycle pattern learning and transfer
│   ├── capability_expander.py                 ← autonomous re-specification on impossible goals
│   └── signal_router.py                       ← drift detection, chain verification, routing
├── references/
│   ├── paradigm_shifts.md                     ← detailed design notes for all five shifts
│   ├── pipeline_config.json                   ← configurable thresholds and behavior
│   ├── learnings_log.json                     ← accumulated cross-cycle learnings (auto-updated)
│   ├── goal_similarity_index.json             ← cross-goal transfer index (auto-updated)
│   └── improvement_chain.json                 ← cryptographic improvement chain (auto-updated)
├── templates/
│   ├── pipeline_run_report_template.md        ← human-readable full pipeline report
│   └── revision_rationale_template.md         ← auto-revised specification rationale
└── examples/
    ├── example_goal_simple.json               ← simple standalone example
    ├── example_goal_triad.json                ← full triad example
    └── example_learnings_log.json             ← sample accumulated learnings
```

---

## Usage

### Quickstart — Any Goal, Any Input

```bash
# From a plain goal description (standalone — no other skills required)
python scripts/pipeline.py --goal "Process customer tickets with 98% accuracy in under 2 seconds"

# From an existing specification (skip intent-engineering)
python scripts/pipeline.py --spec specification.json

# Full triad — all three skills
python scripts/pipeline.py --spec specification.json --outcome outcome_report.json

# Continue a prior cycle (self-improving loop)
python scripts/pipeline.py --state pipeline_state.json

# Verify the improvement chain
python scripts/signal_router.py verify --chain references/improvement_chain.json
```

### Options

| Flag | Description |
| :--- | :--- |
| `--goal TEXT` | Plain language goal (required if no `--spec`) |
| `--spec PATH` | Path to intent-engineering `specification.json` |
| `--outcome PATH` | Path to dark-factory `outcome_report.json` |
| `--state PATH` | Path to prior `pipeline_state.json` (continue a cycle) |
| `--output-dir PATH` | Output directory (default: `./pipeline_output/`) |
| `--cycles N` | Run N cycles automatically (default: 1) |
| `--no-auto-revise` | Disable autonomous re-specification |
| `--no-transfer` | Disable cross-goal skill transfer |
| `--config PATH` | Path to custom `pipeline_config.json` |

### Running Multiple Cycles Automatically

```bash
# Run 5 cycles automatically, feeding each output back as input
python scripts/pipeline.py --goal "Achieve 98% pass rate on ticket classification" --cycles 5 --output-dir ./run_001/
```

### Verifying an Improvement Chain

```bash
python scripts/signal_router.py verify --chain ./run_001/improvement_chain.json
# Output: Chain verified: 5 links, all hashes valid. No tampering detected.
```

---

## Outputs

Every pipeline run produces the following in `--output-dir`:

| File | Description |
| :--- | :--- |
| `pipeline_run_report.json` | Full signed pipeline report with all five paradigm shift outputs |
| `pipeline_state.json` | State file for continuing the cycle |
| `improvement_chain.json` | Cryptographic improvement chain (appended each cycle) |
| `specification.json` | The specification used (or generated) this cycle |
| `revised_specification.json` | Auto-revised specification (if Paradigm Shift 3 triggered) |
| `revision_rationale.md` | Human-readable explanation of any auto-revision |
| `learnings_log.json` | Updated cross-cycle learnings (appended each cycle) |
| `goal_similarity_index.json` | Updated cross-goal transfer index |
| `observation.json` | Normalized observation (from feedback-loop observer) |
| `analysis.json` | Full analysis (from feedback-loop analyzer) |
| `improvement_report.json` | Signed improvement report (from feedback-loop orchestrator) |

---

## Integration with Individual Skills

The unified orchestrator is designed to work with the individual skills, not replace them. You can:

- Run `intent-engineering` independently to produce a specification, then pass it to the unified orchestrator with `--spec`.
- Run `dark-factory` independently to produce an outcome report, then pass it with `--outcome`.
- Run `feedback-loop` independently on any observation, then pass the analysis to the unified orchestrator with `--analysis`.
- Run the unified orchestrator end-to-end and then use the individual skills to drill into specific stages.

---

## Configuration

Edit `references/pipeline_config.json` to tune behavior:

```json
{
  "drift_threshold": 0.15,
  "auto_revise_after_n_failures": 3,
  "transfer_similarity_threshold": 0.60,
  "chain_enabled": true,
  "meta_learning_enabled": true,
  "min_cycles_for_meta_learning": 3
}
```

---

## The Self-Improving Loop

```
Cycle 1:
  goal → specification → execution → observation → analysis → improvement_report_1
                                                                      ↓
Cycle 2:                                                     pipeline_state.json
  pipeline_state → (transfer check) → specification_v2 → execution → observation
                                                                      ↓
                                                             improvement_report_2
                                                                      ↓
Cycle N:                                                     learnings_log grows
  meta_learner fires (after 3+ cycles) → specification_patches → rule_patches
  → all future specifications start smarter
  → all future feedback loop analyses use better rules
  → drift score stabilizes toward 0.0
  → improvement chain grows as verifiable evidence
```

---

## Dependency Map

This skill coordinates the following skills. Each is optional — the pipeline degrades gracefully:

| Skill | Required | Used For |
| :--- | :--- | :--- |
| `intent-engineering` | No | Specification generation from goal text |
| `dark-factory` | No | Autonomous execution and behavioral testing |
| `feedback-loop-v2` | No | Observation normalization, analysis, improvement reports |

When all three are absent, the unified orchestrator runs in **meta-only mode**: it accepts any JSON log or text description, runs the feedback-loop analysis internally, and produces a signed improvement report with cross-goal transfer and drift detection — using only its own embedded logic.
