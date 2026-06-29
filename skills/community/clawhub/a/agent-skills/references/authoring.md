# Skill Authoring Guide

Complete methodology for creating high-quality Skills: best practices → description optimization → quality evaluation.

---

## I. Best Practices

### 1.1 Start from Real Experience

Extract reusable patterns from actual tasks (successful steps, human corrections, I/O formats), or synthesize from project docs/runbooks/API specs. Only distill Skills after completing real tasks — never design from scratch.

### 1.2 Refine Through Real Execution

After initial draft, run with real tasks and collect full traces. Look at execution traces, not just output — if the Agent spends time on useless steps, the instructions are too vague or inapplicable.

### 1.3 Context Efficiency

**Add what the Agent lacks, remove what it knows.** For every piece of content ask: "Would the Agent get this wrong without this instruction?" No → delete.

**Design cohesive units.** Too narrow → multiple Skills conflict; too broad → hard to activate precisely. Querying DB + formatting results is a reasonable unit; adding DB administration is too large.

**Use progressive disclosure for large Skills.** SKILL.md <500 lines. Put detailed content in `references/`; tell the Agent in the main file **when** to load them.

### 1.4 Calibration Control

- **Match specificity to fragility**: When multiple approaches work, explain _why_; for fragile operations (e.g., DB migrations), enforce strict sequence
- **Provide defaults, not menus**: Pick one default, briefly mention alternatives
- **Prefer process over declaration**: Teach the Agent **how to approach** problems, not what to produce for specific instances

### 1.5 Effective Instruction Patterns

- **Gotchas**: Most valuable — environment-specific traps the Agent won't know. Update every time you step on one
- **Output templates**: More reliable than descriptive language; short templates in SKILL.md, long ones in `assets/`
- **Checklists**: Checkbox format prevents omissions
- **Verify loop**: Do → run validator → fix → repeat
- **Plan-verify-execute**: For batch/destructive operations, create intermediate plan first
- **Package scripts**: Agent repeatedly writes same logic → write a tested script once in `scripts/`

---

## II. Description Optimization

### 2.1 Trigger Mechanism

Agent loads all `name` + `description` at startup (Tier 1). Match → read full SKILL.md. Complex domain tasks are where description delivers value.

### 2.2 Writing Tips

- Imperative tone: "Use this skill when..."
- Focus on user intent, not internal mechanics
- Be pushy — explicitly list applicable scenarios
- ≤1024 characters

### 2.3 Trigger Eval

~20 queries (8–10 should trigger + 8–10 should not). Most valuable negatives are **near-misses**: share keywords but need something different. Run each query 3×; should-trigger ≥0.5 pass, should-not <0.5 pass. 60% train + 40% validation to prevent overfitting.

### 2.4 Optimization Loop

1. Evaluate current description → 2. Modify using only train failures → 3. Too narrow: broaden; too broad: add constraints → 4. Avoid adding specific keywords from failed queries → 5. If stuck, try structurally different descriptions → 6. Select iteration with **highest validation pass rate**. Usually 5 rounds suffice; final validation with 5–10 fresh queries.

---

## III. Quality Evaluation

### 3.1 Test Case Design

Start with 2–3 cases. Vary prompts (formal/casual/typos/detail levels), cover edge cases. Each case: prompt, expected output, assertion list.

### 3.2 Running Evals

With Skill + without Skill (baseline). Record outputs, timing, tokens.

### 3.3 Assertions

Good: programmatically verifiable, concretely observable, countable. Weak: too vague, too brittle.

### 3.4 Scoring

Each assertion PASS/FAIL + evidence. Blind comparison: LLM judge unaware of source version. Aggregate: `pass_rate(mean)` with/without + `delta`.

### 3.5 Pattern Analysis

Remove uninformative assertions → investigate dual failures → study Skill value → add examples for inconsistency → check outliers.

### 3.6 Iteration Loop

Eval signals → LLM improvement → rerun → score → human review → repeat. Stop when: satisfied / feedback consistently empty / no meaningful improvement.

---

## Cross-References

- [spec.md](spec.md) — Format spec | [quick-start.md](quick-start.md) — Quick start | [anti-patterns.md](anti-patterns.md) — Anti-patterns | [using-scripts.md](using-scripts.md) — Scripts
