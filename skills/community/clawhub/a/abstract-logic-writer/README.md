# Abstract Logic Writer

Ontology-aware drafting, linting, and scoring for English academic abstracts.

This repository is organized so it can be uploaded to GitHub directly and also packaged as a ChatGPT Skill.

---

## 30 seconds to see the effect

```bash
python scripts/abstract_score.py examples/before_bad_orbital.txt --compare examples/after_good_orbital.txt
```

Expected pattern:

```text
A score: 45/100
B score: 100/100
Delta (B - A): +55
Winner: B
```

The point is not to imitate surface style. The point is to improve computable discourse logic, ontology fit, and lexical selection.

---

## Before / after comparison

### Case 1: Empty summary sentence + banned AI marker

Before:

> Satellite services are important. Existing orchestration is a challenge. Unlike prior work, we build a task-centric framework - it uses mission semantics and two stages. Simulations are good and show effectiveness.

After:

> Orbital edge services demand orchestration policies that preserve service continuity under dynamic topology and resource contention. Existing approaches remain resource-centric, which obscures logical task dependencies and destabilizes multi-stage service execution. We propose a task-centric orchestration framework that translates mission intents into logical service chains and embeds them through neuro-symbolic search to maintain continuity despite physical fluctuations. Simulations on dynamic constellation settings show robust service delivery and millisecond-level planning latency under severe contention.

### Case 2: Lexeme-selection mismatch

Before:

> With the growth of applications, the ontology grows more practical. The framework is useful.

After:

> As applications continue to develop, the ontology provides a stable concept layer for structured retrieval and constraint-aware planning. The framework supports reuse by aligning domain terms, relations, and evaluation targets.

The second version repairs selection mismatches such as `growth of applications` and replaces summary-only claims with purpose-bearing relations.

---

## What this repository contains

- `SKILL.md`: the ChatGPT Skill entrypoint
- `README.md`: GitHub-facing overview and quick start
- `scripts/abstract_lint.py`: rule diagnostics
- `scripts/abstract_score.py`: formal scoring and pairwise comparison
- `scripts/ontology_bootstrap.py`: local ontology seed builder and optional downloader
- `references/`: formal rules, lexeme typing, ontology workflow, negative examples, corpus
- `examples/`: before / after fragments
- `evals/`: recorded sample scoring outputs
- `assets/`: machine-readable rule tables used by the scripts

---

## Quick start

### 1. Lint one abstract fragment

```bash
python scripts/abstract_lint.py examples/before_bad_orbital.txt
```

### 2. Score one abstract fragment

```bash
python scripts/abstract_score.py examples/after_good_orbital.txt
```

### 3. Compare two fragments

```bash
python scripts/abstract_score.py examples/before_bad_lexeme.txt --compare examples/after_good_lexeme.txt
```

### 4. Bootstrap a domain ontology

```bash
python scripts/ontology_bootstrap.py \
  --domain "low-altitude autonomous systems" \
  --terms "airspace rule,uav mission,trajectory,legal constraint,information quality" \
  --outdir ./out/ontology
```

---

## The scoring formula

For an abstract fragment `F`, define:

```text
Score(F) = clip(
  100
  - 20 * M_core
  - 10 * V_order
  - 8  * V_summary
  - 6  * V_marker
  - 4  * V_select
  - 4  * V_terminal
  + 5  * Q_relation
  + 7  * Q_evidence,
  0,
  100
)
```

Where:

- `M_core`: missing core roles among `{motivation, challenge, idea}`
- `V_order`: discourse-role order violations
- `V_summary`: summary-only sentences such as `X is a challenge.`
- `V_marker`: banned surface markers such as the em dash or `Unlike`
- `V_select`: lexeme-selection mismatches such as `growth of applications`
- `V_terminal`: weak final sentences with no mechanism or evidence load
- `Q_relation`: validated purpose or contribution links such as `for`, `to`, `enables`, `addresses`, `translates`
- `Q_evidence`: evidence-bearing sentences with metrics or measurable outcomes

For pairwise comparison:

```text
Delta(B, A) = Score(B) - Score(A)
```

A positive delta means `B` is better under the current rule system.

---

## Design rules enforced by the repository

### 1. Sentence roles must be computable

A short abstract is modeled as an ordered sentence sequence with primary roles:

```text
B <= P <= M <= C <= I <= T <= E
```

Required subset:

```text
{M, C, I} subseteq Im(rho)
```

### 2. Concepts cannot be introduced without motivation or purpose

```text
new(x, si) => motive(x, si) or exists sj in {si-1, si, si+1}: purpose(x, sj) or consequence(x, sj)
```

### 3. Explanation must terminate in purpose or operational relation

```text
explain(x, si) => purpose(x, si) or exists y: relation(x, y, si)
```

### 4. Negative examples are first-class citizens

All rewrites of the user-supplied exemplars are stored or treated as negative examples unless explicitly labeled as repaired outputs. This repository does not use those rewrites as style templates.

### 5. Common AI-sounding markers are penalized

The scoring pipeline penalizes the em dash and `Unlike` by default. Extend the machine-readable rules in `assets/discourse_rules.json` when a stricter banned list is needed.

---

## Repository layout

```text
abstract-logic-writer/
├── README.md
├── SKILL.md
├── LICENSE.txt
├── .gitignore
├── agents/
│   └── openai.yaml
├── assets/
│   ├── discourse_rules.json
│   └── lexeme_types.json
├── examples/
│   ├── before_bad_orbital.txt
│   ├── after_good_orbital.txt
│   ├── before_bad_lexeme.txt
│   └── after_good_lexeme.txt
├── evals/
│   └── sample_scores.md
├── references/
│   ├── computable-rules.md
│   ├── lexeme-typing.md
│   ├── negative-examples.md
│   ├── ontology-bootstrap.md
│   └── source-abstract-corpus.md
└── scripts/
    ├── abstract_lint.py
    ├── abstract_score.py
    └── ontology_bootstrap.py
```

---

## Notes

- This repository is deterministic at the rule level, not at the level of stylistic imitation.
- The score is meant to compare logic, ontology fit, and rhetorical load, not to replace expert judgment.
- Push the directory to GitHub as-is, or package it as `skill.zip` for ChatGPT Skill upload.
