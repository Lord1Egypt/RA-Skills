# Design Decisions

Design rationale for the debate-research skill. Not loaded during execution;
kept here for human readers and future reviewers.

## Pipeline Overview

Structured multi-agent debate: Pre-flight → 3 debate stages
(stance / rebuttal / judgment) → report assembly, with optional evidence
audit. Fixed-round pipeline produces a Markdown consensus report.

## Key Design Decisions

1. **Fixed rounds, no dynamic convergence** — predictable cost, reproducible output. Industry approaches (MAD, AutoGen) favor dynamic iteration until convergence, but result predictability is low. Our 3-stage pipeline (stance → rebuttal → judgment) is a dialectical closed loop: linear, controllable, and optimized for generating formal consensus documents.

2. **Socratic element in Phase 2** — "attack weakest premise" forces higher-quality rebuttals. Instead of surface-level point-by-point counters, agents must identify the single weakest assumption and challenge it, inspired by Socratic Multi-Agent Reasoning approaches.

3. **Confidence + source tagging** — judge weighs by evidence quality, not just rhetoric. Each argument carries a confidence score (0.0-1.0) and source type tag, preventing the debate from devolving into pure language-game wheel-spinning.

4. **Phase 2 web_search disabled** — prevents information drift: rebuttals must challenge the opponent's logic on the fixed Phase 1 evidence base. Allowing search here lets agents patch weak arguments with freshly found sources instead of engaging the actual logic — and shifts the shared evidence base that Phase 3 judges on, invalidating confidence scores and source tags.

5. **Default two-sided, extensible** — default Proponent + Opponent covers most debates; expand to 2-4 roles when multi-dimensional analysis is needed (e.g., cost expert, security expert, feasibility expert).
