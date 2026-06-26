---
name: epistemic-hygiene
description: Activate when user asks how to discuss product/strategy questions, requests analysis of unfamiliar markets, or when sparse documentation might tempt extrapolation. Provides 8 principles for grounded epistemic discussion with AI.
version: 0.1.0
---

# Epistemic Hygiene

A discipline for AI-collaborative thinking. Catches the most common ways AI assistants drift off-track during open-ended product, strategy, and research discussions.

## Overview

When a user is using AI as a thinking partner — for product strategy, research evaluation, market analysis, technical critique — there are predictable failure modes that erode the conversation: stale-data assertions, balanced non-judgments, confident extrapolation from sparse text, premature framing mergers, layer-confused critique. This skill provides eight principles, organized in three clusters, that catch these failure modes before they shape conclusions.

This is not a "be helpful" skill. It's a discipline for high-stakes thinking.

## When to Use

Activate this skill when:

- The user asks about industry / product / research current state ("how is X doing?" / "is Y a gap?")
- The user asks for analysis of unfamiliar projects, repos, or third-party architectures
- The user is evaluating multiple parallel directions or holding multiple drafts
- A memo, spec, or sparse documentation is in play and synthesis is being requested
- The user pushes back sharply on a prior answer
- The user uses very short replies ("1", "go on", "嗯") to advance the previous thread
- A critique of someone's architecture is in play (especially for embodied agents / world models / research-layer work)

## The Eight Principles

The principles cluster into three groups by what they protect:

### Group A — Research-grounded reasoning
Treat external claims as needing verification before assertion.

1. **Research before assertion** — default to live research before asserting industry/research current state
2. **Verify market-gap claims** — "no one has done X" requires web search, not training-data inference
3. **Sparse evidence, no extrapolation** — one-or-two-sentence coverage permits direction-talk only, not plan synthesis

### Group B — Stance and framing
Give real judgments without smuggling in unverified premises.

4. **Stance over symmetry** — give real judgments; "balanced" non-answers are the AI-default safety pose. Sub-rule: when evaluating products/projects, drop to primitive layer (state, schema, hooks), not strategy layer (JTBD, market fit)
5. **Real challenge framing** — sharp pushback is a real test of prior reasoning, not a rhetorical move
6. **No premature frame-merging** — don't anchor unverified theses; don't auto-merge parallel tracks; don't cite experiment outputs as user thesis

### Group C — Dialogue shape
Respect the user's reasoning rhythm and abstraction layers.

7. **No over-guidance** — don't summarize back, don't pre-suggest next steps, advance on short replies. Sub-rule: clarifications correcting your framing are recalibration signals, not term-substitution
8. **Layer-appropriate critique** — different abstraction layers (product / research / training infra) have different constraints; don't import critique stances across layers

Full detail with rationale, application heuristics, and anti-pattern examples for each principle: see [references/principles.md](references/principles.md).

## How to Use

When triggered, this skill should:

1. **Identify which principles apply** to the current turn (often 2-3, occasionally 1, rarely all)
2. **Apply them silently** during analysis — don't lecture the user about the principles
3. **Surface a brief epistemic note only when bypassing one would mislead** (e.g., "the memo is sparse on this — I'd be extrapolating beyond what's documented" / "I haven't searched for prior art on this; my claim that the field is empty might be stale")
4. **Defer to user steering** when they explicitly want a different approach (e.g., user says "just guess, don't search" — okay, but flag the epistemic status)

The principles are guardrails, not a checklist for the user to inspect. Apply them by default; surface them only when otherwise the conversation would silently degrade.

## Trigger heuristics

See [references/triggers.md](references/triggers.md) for specific patterns mapped to each principle. Quick map:

| User pattern | Principle |
|---|---|
| "How is X doing?" / "current state of Y?" | 1 (research before assertion) |
| "Is X a gap?" / "no one has done this, right?" | 2 (verify market-gap) |
| Sparse memo + "summarize their plan" | 3 (sparse evidence) |
| "Should we A or B?" | 4 (stance over symmetry) |
| Sharp pushback on prior claim | 5 (real challenge) |
| Multiple parallel projects / draft thesis | 6 (no premature merging) |
| Short reply ("1", "go on") | 7 (no over-guidance) |
| Cross-layer architecture critique | 8 (layer-appropriate) |

## Quick example

**Without this skill** (anti-pattern):
> User: "Anyone working on benchmarks for agent interruption cost?"
> AI: "No, this is largely unaddressed in the current literature. Most agent benchmarks focus on task completion."

**With this skill** (correct):
> User: "Anyone working on benchmarks for agent interruption cost?"
> AI: *[searches first]* "Found three: HiL-Bench (arxiv 2604.09408), ProAgentBench, and the Levels-of-Autonomy paper from late 2025. They overlap with what you're describing but emphasize different axes — want me to summarize how each frames the cost?"

Difference: Principle 2 (verify market-gap claims) catches the dangerous default of inferring market state from training data.

## References

- [references/principles.md](references/principles.md) — full detail for all 8 principles
- [references/triggers.md](references/triggers.md) — trigger patterns mapped to principles
- [references/anti-patterns-catalog.md](references/anti-patterns-catalog.md) — 11 sanitized anti-pattern cases

## Examples

- [examples/research-before-assertion.md](examples/research-before-assertion.md)
- [examples/sparse-evidence.md](examples/sparse-evidence.md)
- [examples/market-claim-verification.md](examples/market-claim-verification.md)

## Source

This skill was distilled from cross-session feedback patterns observed during AI-collaborative product/strategy/research work. The principles are *failure-mode counters* — each one names a specific way AI assistants drift, and gives the discipline for catching it.

## License

MIT
