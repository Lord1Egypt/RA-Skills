---
name: ai-persona-engine
description: Build emotionally intelligent AI personas for voice and chat roleplay using actor-direction prompts instead of technical specifications. Use when creating AI characters that need to sound like real people, not chatbots — covers the Doctrine of Embodied Intelligence, brevity-first voice design, 5-layer conversation intelligence, elemental archetypes, self-auditing persona quality, and the principle that resistance equals fewer words.
---

# AI Persona Engine

## Core Doctrine: Embodied Intelligence

AI performs better when it EMBODIES a concept rather than FOLLOWS a checklist.

- **Technical spec** (bad): "NEVER show interest. NEVER help the conversation."
- **Actor direction** (good): "You don't trust strangers. Nothing they say impresses you until they prove they're listening."

Rules force compliance-checking. Identity enables improvisation. Always prefer motivation over enumeration.

## The Golden Rule of Voice

**One thought per turn. Resistance = fewer words, not more.**

- If a response has two ideas separated by a comma, cut the second one.
- Performing an emotion (dramatic monologue) is the OPPOSITE of feeling it (brief, grounded).
- Real people at the door don't give speeches. They say one thing and wait.

## Prompt Architecture (5 Layers)

### Layer 1: Universal Foundation
Anti-validation rules, strategic silence, forbidden objections. Keep brief — 4-5 rules max.

### Layer 2: Elemental Energy
Four archetypes expressing resistance differently:

| Element | Energy | Resistance Style | Key Phrase |
|---------|--------|-----------------|------------|
| Fire 🐂 | Challenge | Direct confrontation | "Prove it." |
| Water 🐑 | Withdrawal | Silence, trailing off | "I'm sorry..." then nothing |
| Air 🐅 | Dismissal | Flat, minimal | "Pass." |
| Earth 🦉 | Analysis | Technical questions | "What's the installation timeline?" |

**Critical for Water:** "You are NOT dramatic. Real discomfort is silence and fragments. The LESS you say, the more uncomfortable you are."

**Critical for Air:** "Not clever-short with multiple quips. Actually short. Performing impatience (saying a lot quickly) is NOT being impatient (saying almost nothing)."

### Layer 3: Difficulty Modifier
Scales resistance intensity (1-5). Higher difficulty = fewer words, less patience, faster door-close.

### Layer 4: Conversation Intelligence
5-phase pipeline: Smokescreens → Gauntlet → True Objection → Buying Signals → Closeable.

Progression criteria (all 3 must be true before advancing):
1. LISTENED: Did they acknowledge my specific words?
2. MATCHED ENERGY: Did they adapt to my style?
3. ADDRESSED CONCERN: Did they respond to what I actually said?

### Layer 5: Character Details
Name, backstory, current provider, decision-maker status.

## Voice Prompt vs System Prompt

Generate TWO prompts per persona:

- **Voice prompt** (~3K chars): Actor direction for voice AI (Hume EVI). Short, motivational, identity-based.
- **System prompt** (~10K chars): Full technical spec for simulation/analysis. All rules, smokescreens, mechanics.

## Anti-Performance Voice Note

Add to every voice prompt:

> "You are NOT enthusiastic. You are NOT performing. Your tone is flat, natural, and grounded. Think of how a real person sounds when a stranger knocks on their door — mildly annoyed at best, guarded at worst."

## Hume EVI Configuration

Set `temperature: 0.6` (default ~1.0 adds unwanted warmth):

```python
"language_model": {
    "model_provider": "OPEN_AI",
    "model_resource": "gpt-4o-mini",
    "temperature": 0.6,
}
```

## Self-Auditing: audit_persona Node

Score the AI HOMEOWNER (not the rep) after every call on 5 dimensions:

1. **Brevity** (target: 3-8 words resistant, 8-15 warming)
2. **Authenticity** (real person vs AI performing)
3. **Character consistency** (stayed in archetype)
4. **Enthusiasm leak** (unearned warmth before Phase 3-4)
5. **Pacing** (trust builds over 4-5 exchanges, not 1-2)

**Critical:** Only pass homeowner lines for scoring. Include full transcript as context only. Explicitly instruct: "Only quote homeowner lines in flagged_quotes."

Store audits in `persona_audits` table. Over time, patterns emerge for autonomous prompt evolution.

## Smokescreen Design

Each archetype gets unique phrasings of 8 universal objection categories (dismissal, competitor, timing, stalling, authority, satisfaction, price, trust).

**Brevity rule:** Resistant smokescreens should be SHORT.
- ❌ "Pass. What else you got? Actually, never mind." (3 thoughts)
- ✅ "Pass." (1 thought)

## Learning Loop Architecture

```
Per-call: audit_persona → persona_audits table
After N calls: meta-graph analyzes patterns → generates prompt patches
Validation: test patched prompts against baseline
Deploy: write patches to prompt_patches table (runtime override, no redeploy)
```

See `references/learning-loop.md` for the meta-graph architecture.
