# autoresearch Design Philosophy Deep Dive

> Source: github.com/karpathy/autoresearch, March 2026

## One-liner

Give AI an LLM training script, let it modify code, run experiments, keep or discard, loop all night. Wake up and check results.

## Agent Loop Breakdown (Core Mapping Source for This Skill)

autoresearch's agent loop is the prototype for all designs in this skill:

```
autoresearch:        autowriter:
─────────────        ─────────────────
Read train.py   →    Read research_facts.md
Modify train.py →    Write / rewrite article
Run 5min        →    Execute self-evaluation (quantified score)
Check loss      →    Check composite score
keep/discard    →    keep/discard
Log results.tsv →    Append draft_log
Loop            →    Loop (until score >= 80)
```

### Key Mappings

| autoresearch Mechanism | Writing Mapping | SKILL.md Section |
|---|---|---|
| Modify train.py | Targeted rewrite (only fix low-scoring dimensions) | Phase 1: Subsequent rounds |
| Fixed 5min time budget | Fixed word budget (controlled by --depth) | --depth knob table |
| Loss number | 6-dim evaluation function (0-100 quantified scoring) | Phase 2: Evaluation function |
| keep/discard decision | score >= 80 keep / < 80 discard | Phase 3: Decision |
| results.tsv | draft_log (iteration records) | Draft Log section |
| Simplicity criterion | Conciseness dimension (weight 20%) | Evaluation dimension #4 |
| Loop until convergence | Iterate until score >= 80 or two consecutive rounds diff < 5 | Phase 3: Early termination |

## Design Philosophy Details

### 1. Single File to Modify

autoresearch only lets the agent modify `train.py`. Not because it can't do more, but it **deliberately limits scope**.

**Writing mapping:** Each article covers one core idea. Depth > breadth. Subsequent rounds only fix lowest-scoring dimensions, never rewrite everything — like changing partial parameters in train.py, not rewriting the entire project.

### 2. Fixed Time Budget

Each experiment gets exactly 5 minutes. No matter what was changed, only 5 minutes.

**Writing mapping:** `--depth` uniformly controls word budget (1500 to 8000+ words). "I have 500 words left, what's most worth saying?" — this constraint forces prioritization.

### 3. Simplicity Criterion

> "All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it."

autoresearch doesn't chase lowest loss — it optimizes the balance of loss vs complexity.

**Writing mapping:** Conciseness is an independent evaluation dimension (weight 20%). If removing a paragraph doesn't affect the article, that paragraph should be removed. In practice: Phase 2 checks "Can 30%+ content be deleted without losing the core point?"

### 4. Crash/Discard Log

results.tsv records every experiment: keep, discard, crash. Including failures.

**Writing mapping:** "Failure showcase" is an independent evaluation dimension (weight 15%). Every article must include at least one "what didn't work." Draft log preserves all discarded versions and reasons.

### 5. One Knob (nanochat Philosophy)

nanochat uses a single `--depth` parameter to control all hyperparameters.

**Writing mapping:** `--depth 1-4` uniformly controls word count, technical depth, and iteration count. No other parameters exposed.

### 6. Git Branches as Experiment Records

Every experiment gets a git commit. Success advances the branch, failure resets.

**Writing mapping:** Draft log is the writing equivalent of git log. Every iteration is recorded. Failed versions aren't waste — they're "crash logs of writing experiments."

## Core Insight

**The deepest insight of autoresearch isn't "letting AI run experiments" — it's the trinity of "automated loop + quantified evaluation + failure transparency."**

Mapped to writing:
- Automated loop → write → evaluate → rewrite loop
- Quantified evaluation → 6-dim scoring function (not "feels about right")
- Failure transparency → draft log (not just showing the final version)

Code before prose. Results before opinions. Experiments before conclusions.
