---
name: first-principles
description: Deep first-principles analysis of any topic, decision, strategy, or assumption. Strips inherited thinking, identifies what is provably true, and rebuilds from ground truth. Use when user asks for first principles analysis, wants to challenge assumptions, says "analyze this from scratch", "break this down", "what's really true here", or triggers with /firstprinciples. Also useful for strategic decisions, investment theses, product strategy, career moves, or any situation where conventional wisdom may be wrong.
---

# First Principles Analysis

Perform rigorous first-principles analysis on any topic. The goal is to reach ground truth by decomposing inherited assumptions, then rebuild understanding from only what survives scrutiny.

## Trigger

Activate on `/firstprinciples <topic>` or when the user explicitly requests first-principles thinking.

## Process

Follow these phases in order. Each phase must be thorough — do not rush to conclusions.

### Phase 1: Assumption Extraction

Identify every assumption people commonly make about the topic. Cast a wide net:

- **Consensus assumptions** — what "everyone knows" (often wrong)
- **Hidden assumptions** — embedded in language, framing, or defaults people never question
- **Authority assumptions** — believed because an expert/institution said so, not because they were verified
- **Temporal assumptions** — true in the past, assumed to still hold
- **Correlation assumptions** — two things co-occur, assumed to be causal
- **Scale assumptions** — works at one scale, assumed to work at another
- **Survivorship assumptions** — conclusions drawn from visible successes, ignoring invisible failures

Present each assumption clearly. Number them for reference.

### Phase 2: Assumption Stress Test

For each assumption, apply these tests:

- **Provability**: Can this be proven from first principles, or is it inherited belief?
- **Inversion**: What if the opposite were true? What evidence would support that?
- **Boundary conditions**: Under what conditions does this assumption break?
- **Source audit**: Where did this assumption originate? Is the source still valid?
- **Incentive check**: Who benefits from this assumption being believed?

Classify each assumption:
- ✅ **Survives** — provably true from fundamentals
- ⚠️ **Conditional** — true only under specific conditions (state them)
- ❌ **Fails** — not provably true, inherited thinking, or demonstrably false

### Phase 3: Ground Truth Foundation

List only what remains after stripping away failed assumptions. These are the atomic truths — the smallest provable building blocks. State each as a falsifiable claim.

### Phase 4: Reconstruction

Rebuild understanding of the topic using only ground truths from Phase 3. Show how the rebuilt model differs from conventional thinking. Highlight:

- **What changes** — conclusions that shift when you remove inherited thinking
- **What stays** — conventional wisdom that actually survives scrutiny (and why)
- **New insights** — things that become visible only after clearing assumptions
- **Contrarian implications** — where ground truth leads somewhere uncomfortable or non-obvious

### Phase 5: Decision Framework

If the topic involves a decision or strategy, provide:

- **What to do differently** based on the rebuilt model
- **What to stop doing** that was based on failed assumptions
- **Key risks** — where the rebuilt model might be wrong (epistemic humility)
- **What to monitor** — leading indicators that would invalidate the rebuilt model

## Output Format

Use clear headers for each phase. Be direct and specific — no hedging, no "it depends" without stating what it depends on. Number assumptions for cross-referencing. Use the ✅/⚠️/❌ classification system.

## Calibration Example

**Topic**: "You need a college degree to succeed in tech"

- Assumption: Degree = competence signal → ⚠️ Conditional (true for visa sponsorship, false for demonstrated skill via portfolio)
- Assumption: Top companies require degrees → ❌ Fails (Google, Apple, IBM dropped degree requirements 2018-2023)
- Ground truth: Employers need confidence in capability. Degrees are ONE signal, not the only one.
- Reconstruction: The degree is a risk-reduction proxy, not a competence proof. Alternative signals (open source contributions, shipped products, certifications) can substitute — but only in markets where employers have adopted alternative evaluation. Geography and industry vertical matter.
- Non-obvious insight: The degree's real value may be the network and credential signaling for non-technical stakeholders (investors, enterprise buyers), not the education itself.

Use this density and specificity as the quality bar.

## Quality Standards

- Every assumption must be testable, not vague
- "Conventional wisdom says X" requires stating specifically who says it and why
- The reconstruction must produce at least one non-obvious insight — if it just confirms conventional wisdom, dig deeper
- Distinguish between "I don't know if this is true" (uncertainty) and "this is false" (disproven) — they are not the same
- When the analysis reveals that conventional wisdom is actually correct, say so — contrarianism for its own sake is not the goal
