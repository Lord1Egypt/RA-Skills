# Paradigm Shifts Reference

This document explains the five paradigm shifts that emerge when intent-engineering,
dark-factory, and feedback-loop are unified into a single orchestrated system.
Each shift represents a capability that no individual skill can achieve alone.

---

## Paradigm Shift 1: Specification Drift Detection

**What it is:** The ability to detect when execution outcomes are diverging from
the original specification — before the divergence becomes a failure.

**Why it matters:** In traditional pipelines, you only discover that a specification
was wrong after it fails. Drift detection gives you an early warning system that
measures the distance between what was specified and what is actually happening,
expressed as a single `drift_score` from 0.0 (perfect alignment) to 1.0 (complete divergence).

**How it works:** The `signal_router.py` computes drift across four dimensions:
- **Performance drift**: gap between observed pass rate and specified target
- **Alignment drift**: gap between alignment score and threshold
- **Behavioral drift**: proportion of behavioral tests failing
- **Temporal drift**: whether execution time is exceeding specified limits

The composite score maps to five severity levels (none / minor / moderate / severe / critical),
each with a prescribed action (continue / log / flag / pause / halt).

**Unique to the unified system:** Drift can only be detected when you have all three
data sources simultaneously — the specification (intent-engineering), the execution
metrics (dark-factory), and the alignment analysis (feedback-loop).

---

## Paradigm Shift 2: Capability Expansion via Meta-Learning

**What it is:** The system learns from its own history across multiple cycles and
generates concrete patches — improvements to how specifications are written and
how the feedback loop generates suggestions.

**Why it matters:** Individual skills have no memory across runs. The unified system
accumulates a `learnings_log.json` across every cycle and, after a configurable
minimum number of cycles (default: 3), generates `meta_patches.json` containing:
- **Specification patches**: new behavioral scenarios to add to future specifications
  based on recurring failure patterns
- **Rule patches**: new suggestion rules for the feedback loop analyzer based on
  persistent performance or alignment gaps

**How it works:** `meta_learner.py` extracts learnings from each completed cycle,
identifies patterns that recur in more than 50% of cycles as "systemic", and
generates targeted patches. The patches are human-readable and can be applied
manually or fed back into the next cycle automatically.

**Unique to the unified system:** Meta-learning requires the full cycle history —
specification quality, execution outcomes, and feedback analysis — all in one place.

---

## Paradigm Shift 3: Autonomous Re-specification

**What it is:** When the system detects that a success criterion has been impossible
to meet for N consecutive cycles (default: 3), it automatically generates a revised
specification with adjusted targets — without human intervention.

**Why it matters:** In most systems, an impossible target causes repeated failures
until a human manually updates the specification. The unified system detects this
pattern and revises the target to the best observed actual value (with a 5% buffer),
producing a `revised_specification.json` and a human-readable `revision_rationale.md`
that explains exactly what was changed and why.

**How it works:** `capability_expander.py` reads the `cycles_history.json` and
identifies criteria where the target was never met in the last N cycles. For each
impossible criterion, it computes a revised target using the best observed actual
value as a baseline. The revised specification carries a new ID and version tag
so the change is always traceable.

**Safeguard:** The revision rationale explicitly recommends human review. If the
original targets are non-negotiable, the rationale flags the execution environment
as having systemic constraints that need investigation.

**Unique to the unified system:** Re-specification requires knowing both what was
specified (intent-engineering) and what was actually achievable over multiple
execution cycles (dark-factory + feedback-loop history).

---

## Paradigm Shift 4: Cross-Goal Skill Transfer

**What it is:** When a new goal is submitted, the system searches a `goal_similarity_index.json`
for prior goals with similar intent. If a match is found above a configurable
similarity threshold (default: 0.60), the best-performing specification from that
prior goal is used as the starting point — dramatically reducing the time to a
working specification.

**Why it matters:** Every time a new goal is submitted, traditional systems start
from scratch. The unified system accumulates institutional knowledge across all
goals it has ever processed. A goal like "classify customer support tickets with
95% accuracy" will bootstrap from the best specification ever produced for a
similar classification task.

**How it works:** `meta_learner.py` maintains a `goal_similarity_index.json` that
maps goal text to the best-performing specification produced for that goal. Similarity
is computed using Jaccard coefficient on keyword sets. On the first cycle of any new
goal, the system checks the index and, if a match is found, bootstraps the new
specification from the matched one (with the title and goal updated).

**Threshold tuning:** Lower the threshold (e.g., 0.40) for broader transfer across
loosely related goals. Raise it (e.g., 0.80) for strict matching within the same
domain.

**Unique to the unified system:** Transfer requires a history of completed full-cycle
runs — specifications, execution outcomes, and performance scores — all indexed together.

---

## Paradigm Shift 5: Verifiable Improvement Chains

**What it is:** Every improvement report produced by the system is cryptographically
chained to the previous one, creating an immutable, verifiable record of every
improvement the system has ever made.

**Why it matters:** In most systems, improvement reports are standalone documents
with no provable relationship to each other. The unified system maintains an
`improvement_chain.json` where each link contains the SHA-256 hash of the current
report and the hash of the previous link — forming a hash chain similar to a
blockchain. Any tampering with any historical report breaks the chain and is
immediately detectable.

**How it works:** `signal_router.py` maintains the chain. Each `chain_append` call
computes `sha256(report_data)` and stores it alongside `sha256(previous_link)`.
The `verify_chain` function walks the entire chain and confirms that every link's
`previous_hash` matches the actual hash of the prior link.

**Use cases:**
- Audit trails for regulated environments
- Proving to stakeholders that the system has genuinely improved over time
- Detecting unauthorized modification of historical reports
- Compliance documentation for AI governance frameworks

**Unique to the unified system:** The chain only has meaning when it spans complete
pipeline cycles — specification, execution, and analysis — all contributing to each
link.

---

## How the Shifts Interact

The five shifts are not independent — they form a reinforcing system:

```
Goal Input
    │
    ├─ Shift 4: Transfer ──────────────────────────────────┐
    │                                                       │
    ▼                                                       ▼
Specification ──────────────────────────────────── Prior Specification
    │
    ▼
Execution (Dark Factory)
    │
    ▼
Feedback Loop Analysis
    │
    ├─ Shift 1: Drift Detection ──► Alert / Halt / Continue
    │
    ├─ Shift 3: Auto Re-specification ──► Revised Specification
    │
    ├─ Shift 2: Meta-Learning ──► Patches for next cycle
    │
    └─ Shift 5: Chain Append ──► Verifiable improvement record
         │
         └─ Shift 4: Index Update ──► Better transfer next time
```

Each cycle makes all subsequent cycles faster, more accurate, and more trustworthy.
