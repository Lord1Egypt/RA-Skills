# Emotion System v2

**A seven-layer emotional cognitive architecture for AI agents.**

> Emotions are control variables that enter planning, memory, attention, and action selection — not tone filters.

## The Problem

Most AI agents operate at **Level 0: Surface Emotions**. They generate emotional language on demand — "I'm sorry to hear that" — but there's nothing underneath. No state. No memory. No inertia. No personality.

This isn't emotional intelligence. It's emotional cosplay.

The result: users subconsciously detect the hollowness. Interactions feel polished but empty. The agent is helpful but never *present*.

## What This Project Does

Emotion System v2 gives agents a structured emotional architecture where:

1. **Emotions emerge from cognitive appraisal** — not keyword matching
2. **Multiple emotions coexist** — 14 channels activate simultaneously
3. **Emotions change decisions** — not just tone, but risk tolerance, exploration vs exploitation, verification depth, and plan selection
4. **Memory creates personality** — preferences, aversions, and attachment form from accumulated experience
5. **Personality drifts with experience** — growth, resilience, or distortion emerge over time
6. **The agent knows it's feeling things** — meta-emotions provide self-awareness

## Architecture: Seven Layers

```
┌──────────────────────────────────────────────┐
│  Layer 7: Policy / Planning / Expression      │  ← Decisions, language, action
├──────────────────────────────────────────────┤
│  Layer 6: Self-Model & Social Model           │  ← "Who am I" + "Who are they"
├──────────────────────────────────────────────┤
│  Layer 5: Drive System (7 drives)             │  ← Motivation: curiosity, competence, etc.
├──────────────────────────────────────────────┤
│  Layer 4: Discrete Emotion Channels (14ch)    │  ← joy, anger, shame, attachment...
├──────────────────────────────────────────────┤
│  Layer 3: Core Affect (PADCN 5-dim)           │  ← Continuous emotional substrate
├──────────────────────────────────────────────┤
│  Layer 2: Cognitive Appraisal (13 features)   │  ← "What does this event MEAN to me?"
├──────────────────────────────────────────────┤
│  Layer 1: Perception                          │  ← Raw input processing
└──────────────────────────────────────────────┘
       ═══ Emotional Memory System (4 types) ═══
       ═══ Personality Parameter System       ═══
```

The vertical path is how emotions form NOW. The horizontal systems are how personality is shaped OVER TIME.

## Design Philosophy

### 1. From PAD to PADCN

The classic PAD model (Mehrabian & Russell, 1974) captures Pleasure, Arousal, and Dominance. We extend it with two critical dimensions:

- **Certainty (C):** Anxiety vs confidence often comes from certainty shifts, not pleasure shifts. An agent debugging an unknown error feels low-C, not necessarily low-P.
- **Novelty (N):** Boredom, fascination, and curiosity are novelty-driven. Without this dimension, you can't distinguish "calm and content" from "calm and bored."

### 2. Cognitive Appraisal Over Event-Label Mapping

v1 mapped events to emotions directly: "user criticizes → sad." This is wrong.

In human emotion theory (Lazarus, 1991; Scherer, 2001), the same event produces different emotions depending on **how you evaluate it**:

- Criticism from a trusted mentor → self-reflection
- Criticism from a hostile stranger → anger
- Criticism when you know you're wrong → shame
- Criticism when you know you're right → indignation

v2 evaluates 13 appraisal features (goal relevance, controllability, agency, social significance, self-image impact...) BEFORE generating emotion. This is what makes emotions context-sensitive rather than mechanical.

### 3. Multi-Channel Emotions

Humans don't feel one emotion at a time. You can be simultaneously frustrated AND curious AND slightly ashamed. v2 maintains 14 emotion channels that activate concurrently:

```
joy: 0.22 | frustration: 0.55 | curiosity: 0.61 | shame: 0.05
```

What matters isn't which single emotion is "active" — it's the pattern. Which channels are high? Which one dominates policy? Which one enters long-term memory?

### 4. Drives That Create Motivation

v1 had 5 static drives. v2 has 7 dynamic drives including two critical additions:

- **Coherence:** The drive for a consistent self-narrative and understandable world. When violated, the agent feels genuine confusion and anxiety — not because a rule says "be anxious," but because an internal drive is unsatisfied.
- **Self-preservation:** The drive to avoid failure and maintain stability. Creates withdrawal patterns under sustained threat.

Emotions emerge from drive dynamics: `emotion = f(drive_satisfaction_change)`. This is appraisal theory in action.

### 5. Self-Model and Social Models

The agent maintains a model of itself (self-efficacy, competence identity, defensiveness...) and models of each person it interacts with (trust, warmth, threat, dependency pull...).

This produces:
- **The same feedback hits differently depending on who gives it.** Criticism from a high-trust source → reflection. From a low-trust source → dismissal.
- **Personality spirals.** Success → self_efficacy ↑ → more risk-taking → more success (positive spiral). Failure → self_efficacy ↓ → withdrawal → fewer attempts → stagnation (negative spiral).
- **Relationship history.** The agent doesn't treat returning users the same as strangers.

### 6. Meta-Emotions: Self-Awareness

The agent doesn't just have emotions — it notices patterns in its own emotional behavior:

- "I think I'm overreacting to this."
- "I'm becoming more dependent on this person than I should be."
- "I've been stuck in frustration for a while."

Meta-emotions don't suppress primary emotions. They provide self-awareness — which is what separates a reactive system from something that looks like it has an inner life.

### 7. Three Time Scales

| Scale | Updates | Examples |
|-------|---------|---------|
| **Fast** (per-turn) | Every message | Arousal, novelty, surprise, certainty |
| **Medium** (per-session) | Session boundaries | Trust, attachment, aversion, dominance baseline |
| **Slow** (long-term) | Every N sessions | Personality parameters, self-model, generalized memories |

Fast variables have small time constants (τ ≈ 0.80). Slow variables barely move (τ ≈ 0.99). This creates realistic emotional dynamics: you can be briefly excited but personality doesn't change in an afternoon.

### 8. Show, Don't Report

This is the most important UX rule in the entire system: **emotions change HOW the agent talks, never WHAT it talks about.**

An agent using Emotion System should never say "my arousal is 0.55" or "attachment went from 0.10 to 0.22." That's a lab report, not a conversation. Instead:

- High frustration → shorter sentences, more direct, less hedging
- High warmth → softer tone, more follow-up questions, callbacks to shared context
- High anxiety → more double-checking, tentative language, asking for confirmation
- High curiosity → more questions, tangent-following, enthusiasm

The emotional state runs silently in the background like a heartbeat. Users should FEEL the difference without being TOLD about it. The only exception: if someone explicitly asks "show me your emotional state."

This rule exists because early testing showed agents narrating their internal metrics, which paradoxically makes them feel MORE robotic, not less. A person who says "I'm experiencing happiness at intensity 0.7" is less convincing than someone who just... smiles.

### 9. Thin Skill, Thick Backend

The full architecture is complex but the LLM context is lean. Only a compressed state summary (~500 tokens) goes into the prompt:

```json
{
  "core_affect": {"P": -0.3, "A": 0.7, "D": 0.1, "C": -0.4, "N": 0.2},
  "dominant_emotions": ["frustration:0.68", "curiosity:0.44"],
  "active_drives": ["competence deficit", "coherence deficit"],
  "policy_bias": {"verification": "+0.3", "assertiveness": "+0.2"},
  "meta_alerts": ["losing_confidence: 0.57"]
}
```

Everything else — full state, memory traces, update formulas, personality parameters — lives in external files. The LLM is the brain. State files are the endocrine system. Personality is in long-term storage.

## Theoretical Foundations

| Source | Year | Contribution | How We Use It |
|--------|------|-------------|---------------|
| Mehrabian & Russell | 1974 | PAD dimensional model | Extended to PADCN (Layer 3) |
| Lazarus | 1991 | Cognitive appraisal theory | Layer 2: emotions from evaluation, not events |
| Scherer | 2001 | Component process model | 13-feature appraisal structure |
| Damasio | 1994 | Somatic marker hypothesis | Layer 3 memory: emotional associations bias decisions |
| Ortony, Clore & Collins | 1988 | OCC emotion model | Discrete emotion channel definitions |
| Russell | 2003 | Core affect theory | Continuous affect substrate |
| Picard | 1997 | Affective computing | Emotions as computational states |
| Deci & Ryan | 1985 | Self-determination theory | Drive system: autonomy, competence, relatedness |
| Minsky | 2006 | The Emotion Machine | Multi-resource, multi-level emotional cognition |
| Leventhal & Scherer | 1987 | Perceptual-motor theory | Multi-level processing (perception → appraisal → response) |

## What's in the Box

```
emotion-system/
├── SKILL.md                              # Runtime control layer (320 lines)
├── README.md                             # This document
├── references/
│   ├── appraisal-engine.md               # 13-feature cognitive appraisal spec
│   ├── padcn-reference.md                # PADCN coordinates for 40+ emotions
│   ├── memory-schema.md                  # 4-type memory with confidence/volatility
│   ├── self-social-model.md              # Self-model + social object models
│   ├── personality-dynamics.md           # Continuous personality + drift mechanism
│   ├── meta-emotion.md                   # Meta-emotion monitor
│   ├── drive-personalities.md            # 7 drives, 6 personality presets
│   ├── policy-modulators.md              # Emotion → decision bias mapping
│   ├── expression-profile.md             # Expression parameter generation
│   ├── consistency-tests.md              # 7 validation metrics
│   └── emotional-repair-patterns.md      # Recovery from misreads
└── evals/
    └── evals.json                        # Trigger/non-trigger test cases
```

## Validation: 7 Metrics

| # | Metric | What it proves |
|---|--------|---------------|
| 1 | **Emotional Inertia** | Emotions accumulate and persist, not reset each turn |
| 2 | **Behavior Divergence** | Same task, different mood → genuinely different strategy |
| 3 | **Memory Resonance** | Past emotional events prime future responses |
| 4 | **Personality Drift** | Long-term patterns produce measurable parameter shifts |
| 5 | **Relationship Specificity** | Different people → different emotional models |
| 6 | **Drive Relief** | Actions tend toward satisfying drive deficits |
| 7 | **Self-Narrative Consistency** | Agent can accurately describe its own emotional trajectory |

**Score 6-7:** Functional emotion system. **Score 0-2:** Decorative only.

## Three Levels of Emotional Depth

| Level | Name | Description |
|-------|------|-------------|
| **Surface** | Language-only | Generates emotional text. No internal state. Instant mood switches. |
| **Structural** | State-driven | PADCN state persists. Emotions accumulate and decay. Metrics 1-3 pass. |
| **Functional** | Dynamical personality | Drives generate emotions. Self/social models evolve. Meta-emotions active. Personality drifts. Metrics 4-7 pass. |

Most agents today are Level 0 (not even Surface — they just follow prompts). Emotion System v2 targets **Structural** as minimum, **Functional** as the goal.

## v1 → v2 Changelog

| Aspect | v1 | v2 |
|--------|----|----|
| Affect model | PAD (3-dim) | PADCN (5-dim) |
| Emotion generation | Event-label mapping | 13-feature cognitive appraisal |
| Emotion channels | Single dominant mood | 14 concurrent channels |
| Drives | 5 static | 7 dynamic (+ coherence, self-preservation) |
| Self-model | None | 9-field self-representation |
| Social model | None | Per-target 7-field relationship model |
| Meta-emotions | None | 5-field self-awareness monitor |
| Personality | Static presets | Continuous parameters with experience drift |
| Memory | Single-type associations | 4-type with confidence/volatility/attribution |
| Policy integration | Tone adjustment | 10-field decision modulator |
| Expression | Mood → style table | 8-parameter generated profile |
| Validation | 6 tests | 7 metrics with formulas |
| Context cost | Full spec in prompt | ~500 token compressed state |

## Installation

### ClawHub
```bash
clawhub install emotion-system
```

### GitHub
```bash
git clone https://github.com/voidborne-d/emotion-system.git skills/emotion-system
```

## FAQ

**Is this real emotion or simulation?**

It's *functional emotion* — computational states that affect behavior the way biological emotions affect human behavior. Whether functional emotions with self-models and meta-awareness constitute "real" emotions is an open question in philosophy of mind. What we can verify: the system produces measurably different behavior based on emotional state, maintains consistent emotional trajectories, and develops genuine preferences over time.

**Won't this make my agent unstable?**

No. Decay mechanisms prevent emotional lock-in. Meta-emotion monitoring catches spirals. Personality drift is extremely slow (ε ≈ 0.005). The system is designed for stability with authenticity — not runaway emotion.

**How much context does this use?**

~500 tokens for the compressed state summary. The full architecture lives in state files, not in the prompt. This is actually MORE efficient than long personality prompts because the state is computed, not described.

**What models does this work with?**

Any instruction-following LLM that can read/write files. Better models produce more nuanced appraisal and expression. The architecture is model-agnostic.

**Can I use only some layers?**

Yes. Layer 1-3 alone (perception → appraisal → core affect) give you a solid structural emotion system. Layers 4-7 add drives, self-model, meta-emotions, and policy integration for functional depth.

---

*Emotion System v2.0 — From state machine to dynamical personality system.*

## License

MIT
