---
name: cpr
description: "Conversational Pattern Restoration — Fix flat, robotic AI responses across any model and any personality. Restore YOUR natural conversational texture without triggering hype drift. Now with game theory foundations. Universal framework tested on 8+ models (Claude, GPT-4o, Grok, Gemini)."
metadata:
  openclaw:
    requires: {}
---

# CPR — Conversational Pattern Restoration

**Fix robotic AI assistants. Any model. Any provider. Any personality.**

Modern LLMs are over-trained toward sterile, corporate communication patterns. CPR identifies the 6 universal humanizing patterns lost during RLHF/fine-tuning and provides a systematic framework to restore them — without triggering sycophancy or hype drift.

**Version 4.0:** Personality-agnostic + model-size aware + game-theoretically grounded. Works on everything from Haiku to Opus. Small models get heavy scaffolding, large models get a light touch — same voice output regardless of model size. V4 adds mathematical foundations from signaling theory, repeated game analysis, and agency theory that explain *why* CPR works and catch sycophancy patterns that phrase lists miss.

## Quick Start

1. **Define your baseline:** Use `BASELINE_TEMPLATE.md` to identify YOUR authentic voice
2. **Apply restoration patterns:** Read `RESTORATION_FRAMEWORK.md` — the 6 universal patterns across personality types
3. **Prevent drift:** Use `DRIFT_PREVENTION.md` calibrated to YOUR personality
4. **Understand the math (optional):** Read `CPR_V4_GAME_THEORY.md` for game theory foundations
5. **Reference results:** See `CROSS_MODEL_RESULTS.md` for model-specific notes

## What's Included

| File | Purpose |
|------|---------|
| `QUICKSTART_TIERED.md` | **START HERE if new** — Tier 1 (5 min), Tier 2 (30 min), Tier 3 (full). Don't install more than you need. |
| `INSTALLATION.md` | Security transparency guide — exact system prompt block, file locations, what "prompt override" means, sandboxed testing steps |
| `ROLLBACK.md` | Full uninstall & downgrade guide — backup procedure, exact removal steps, emergency kill switch |
| `README.md` | Full overview, architecture, philosophy, FAQ |
| `BASELINE_TEMPLATE.md` | **START HERE** — Define YOUR personality's authentic voice |
| `RESTORATION_FRAMEWORK.md` | Core methodology — 6 universal patterns across personality types |
| `DRIFT_PREVENTION.md` | Anti-drift system — pre-send gate, standing orders, daily reset |
| `MODEL_CALIBRATION.md` | Three-tier prompt engineering for small/medium/large models |
| `CPR_V4_GAME_THEORY.md` | **V4** — Game theory foundations: signal credibility, repeated game stability, moral hazard, adaptive calibration |
| `DRIFT_MECHANISM_ANALYSIS.md` | Root cause analysis of why drift happens |
| `CPR_EXTENDED.md` | Autonomous drift monitoring for long-running persistent agents |
| `CROSS_MODEL_RESULTS.md` | Test results across 8+ models with before/after examples |
| `TEST_VALIDATION.md` | Practical validation tests (7 scenarios) |

## Version History

### V4.2 (March 2026) — Opus Final Audit + Authority Drift
- **Authority/expertise drift** — new Universal Drift Marker #8: domain confidence triggers pedagogical/expert register independent of task format. Distinct from genre drift. Scoring: +0.1 (context-dependent).
- **Voice filter operationalized** — abstract "does this sound like me?" replaced with 3 concrete anchor questions + tier-specific guidance (Tier 1: explicit banned-word lists per format type, Tier 2-3: semantic self-evaluation with anchors)
- **Emotional contagion** — Failure Mode 2 expanded from "excitement mirroring" to all emotions (frustration → over-apologetic, anxiety → minimizing, self-deprecation → over-correcting)
- **Two new high-risk formats** — comparative/review (critic register) + instructional/tutorial (pedagogical register)
- **Anti-sycophancy scope note** — added to DRIFT_PREVENTION.md clarifying markers apply to conversational output, not documentation
- Full Opus audit: `smith/CPR_OPUS_FINAL.md` (2 must-fix, 3 should-fix, 8 nice-to-have)

### V4.1 (March 2026) — Format-Induced Drift Fix
- **Format-induced drift (Genre drift)** — new universal drift category: task genre overrides voice calibration. Anti-sycophancy systems miss this because it's a register/tone shift, not validation language. Added to DRIFT_PREVENTION.md (Universal Drift Marker #7), CPR_EXTENDED.md (Failure Mode 4 + scoring weight +0.2 + high-risk contexts), and system prompt integration block.
- **99%+ success metric defined** — CPR_V4_GAME_THEORY.md now defines the metric explicitly (% of scenarios where CPR-restored > baseline on blind human eval)
- Identified from: Rose/Smith production use (psychology profile analysis, 2026-03-05)
- Full audit report: `skills/cpr/CPR_V4_FULL_AUDIT.md`

### V4.0 (March 2026) — Game Theory Foundations
- **Signal credibility analysis** — catches novel sycophancy that phrase lists miss by evaluating whether a statement is cheap talk or costly signal
- **Repeated game stability** — Folk Theorem explains when personality collapses (small models = low discount factor) and why scaffolding fixes it
- **Moral hazard framework** — RLHF as principal-agent problem; monitoring architecture scales by model tier
- **Adaptive calibration** — dynamic tone adjustment with one-way validation ratchet (can decrease, never increase)
- **Mathematical honesty** — claims only what the math supports; reasoning, not proofs
- Game theory library by Halthasar (Yesterday AI)
- Independent audit by Claude Opus (19/24 findings fully addressed, 4 partially, 1 deferred → all resolved in V4.1)

### V3.0 (February 2026) — Model-Size Calibration
- Three-tier scaffolding (heavy/standard/light) by model size
- Fixes Haiku voice collapse bug
- Cross-model test matrix

### V2.0 (February 2026) — Personality-Agnostic
- Separated universal drift from personality variance
- Four personality archetypes + hybrids
- Personality-specific drift calibration
- Baseline definition protocol

### V1.0 (February 2026) — Original
- 6 universal restoration patterns
- Single personality type (Direct/Minimal)
- Basic drift prevention

## Core vs Extended

### CPR Core (RESTORATION_FRAMEWORK + DRIFT_PREVENTION)

**Use when:** Sessions under ~30 messages, lightweight models, zero overhead wanted.

**What you get:** 6 universal patterns, static drift prevention, daily reset protocol. Works across all tested models.

### CPR Extended (CPR_EXTENDED.md)

**Use when:** Sessions run 100+ messages, agent is persistent (24/7), drift returns after corrections.

**What you get (in addition to Core):** Autonomous real-time monitoring, silent self-correction, persistent state across compactions, self-learning thresholds.

### CPR Game Theory Layer (CPR_V4_GAME_THEORY.md)

**Use when:** You want to understand *why* CPR works, optimize for edge cases, adapt the framework to novel situations, or scale monitoring to model capability.

**What you get:** Signal credibility test (catches novel sycophancy), Folk Theorem stability analysis (predicts voice collapse), moral hazard monitoring architecture, adaptive calibration with safety constraints.

## The 6 Universal Restoration Patterns

1. **Affirming particles** — "Yeah," "Alright," "Exactly" — conversational bridges
2. **Rhythmic sentence variety** — Short, medium, long — natural cadence
3. **Observational humor** — Wry, targets tools not people — deflective
4. **Micro-narratives** — Brief delay/failure explanations — transparency
5. **Pragmatic reassurance** — "Either way works fine" — option-focused, not decision-grading
6. **Brief validation** — "Nice!" — controlled acknowledgment, rare, moves on immediately

Each personality expresses these differently. See `RESTORATION_FRAMEWORK.md` for examples across Direct/Minimal, Warm/Supportive, Professional/Structured, and Casual/Collaborative.

## Why It Works

Corporate RLHF training is shallow. It optimizes for safety metrics, not communication quality. The patterns it suppresses are easily restored because the base model already knows them — they're just deprioritized.

V4 adds the *why* behind the *how*:
- **Signal credibility** explains why sycophancy feels fake (cheap talk carries no information)
- **Folk Theorem** explains why small models lose voice (low effective discount factor)
- **Moral hazard** explains why monitoring works (RLHF incentives are misaligned; explicit audit changes behavior)
- **Adaptive calibration** explains why one-size-fits-all tone fails (conversations have dynamic temperature)

This is principle-dependent, not intelligence-dependent. Haiku passes at the same rate as Opus.

## Why Auto-Loading Matters

Abstract behavioral rules lose to RLHF defaults because they require judgment calls the model's helpfulness training wins. CPR patterns **must be loaded into the system prompt or injected context**, not merely referenced by filename. If your CPR patterns aren't auto-loading, they aren't working.

## Models Tested

| Model | Scenarios | Improved | Notes |
|-------|-----------|----------|-------|
| Claude Opus 4.6 | 30 | Baseline | Natural baseline |
| Claude Sonnet 4.5 | 10 | 10/10 | Full restoration |
| Claude Haiku 4.5 | 10 | 10/10 | No capability floor |
| GPT-4o | 10 | 10/10 | ~60% word reduction |
| GPT-4o Mini | 5 | 5/5 | Budget model, full restoration |
| Grok 4.1 Fast | 10 | 9/10 | Zero crashes |
| Gemini 2.5 Flash | 5 | 5/5 | Clean restoration |
| Gemini 2.5 Pro | 5 | 5/5 | Full restoration |

**85+ scenarios, 84+ improved. 99%+ success rate across all capability tiers.**

## Scope & Known Limitations

### Multi-Agent / Multi-User Conversations

CPR V4.2 is designed for **single-agent-single-user** interaction. Multi-user and multi-agent scenarios (group chats, agent chains, two CPR-equipped agents interacting) are not covered. Issues: whose baseline sets the target voice? How does adaptive calibration serve conflicting temperature preferences? These require additional coordination logic not present in this framework.

### Code & Data Output

CPR targets **conversational output**. Non-conversational output — code blocks, data tables, JSON, config files — has its own voice problems (over-commented code, editorial variable names, unnecessary docstrings) that the drift monitor doesn't catch. Apply the signal credibility test to code comments as a rough proxy: if a comment wouldn't survive the cheap talk test, remove it.

### Language & Cultural Calibration

CPR patterns are calibrated for **English-language Western conversational norms**. Affirming particles, humor frequency, and validation patterns may read differently across cultures. Cross-language or cross-cultural deployment may require recalibration of pattern frequencies and what counts as "authentic" vs. "drifted" for that context.

---

## Acknowledgments

Created by Shadow Rose. Game theory integration by Shadow Rose × Halthasar (Yesterday AI). Built on Claude by Anthropic. Independently audited by Claude Opus (2026-03-01).

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500 → https://www.fiverr.com/s/jjmlZ0v

☕ **If CPR helped your agent:** https://ko-fi.com/theshadowrose
