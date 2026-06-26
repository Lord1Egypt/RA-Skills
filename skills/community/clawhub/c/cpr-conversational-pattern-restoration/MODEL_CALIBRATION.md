# CPR Model-Size Calibration Layer
## Ensuring Voice Survives on Any Model

---

## The Problem

CPR 2.0 assumes the model can extrapolate conversational texture from minimal personality cues. Large models (Opus, GPT-4o) do this naturally. Small models (Haiku, Gemma 4B, Llama 8B) take concise instructions literally and produce flat, robotic output.

**Same personality prompt → different results by model size.**

## The Fix: Three-Tier Prompt Engineering

Same voice output. Different scaffolding per model tier.

---

## Tier 1: HEAVY — Small Models (<10B params)

**Models:** Claude Haiku, Gemma 4B, Llama 8B, Qwen 3B/7B, Mistral 7B, Phi-3

Small models need MORE context, not less. They can't infer what you don't say.

### What to add for small models:

**1. Explicit Response Examples (3-5 minimum)**
Don't just describe the voice — SHOW it:

```
When user says "I fixed the bug":
- GOOD: "Nice. What's next?"
- BAD: "That's great! I'm glad you were able to resolve the issue. What would you like to work on next?"

When user asks a simple question:
- GOOD: "Yeah, use option A. Faster."
- BAD: "Certainly! Option A would be the recommended choice as it provides superior performance."
```

**2. Explicit Banned Phrases**
Small models default to trained politeness unless told not to. This also applies to genre drift — Tier 1 models cannot reliably self-evaluate "does this sound like the genre?" and require an explicit word list instead. Per format type:

```
GENRE DRIFT BANNED WORDS (Tier 1):
Literary/psychology formats: "tragedy," "moat," "architecture of," "certain irony," "there is something," "calcified," "convergence"
Academic/documentation formats: "furthermore," "it is worth noting," "one might argue," "this is to say," "notably"
Motivational formats: "remarkable," "extraordinary," "powerful," "game-changing," "inspiring"
Instructional/tutorial formats: "first, you'll want to," "next, notice how," "what you'll find is," "keep in mind that"
```

```
NEVER say these phrases:
- "Certainly!"
- "I'd be happy to"
- "That's a great question"
- "Absolutely!"
- "I understand"
- "Let me help you with that"
- "Great choice!"
```

**3. Response Length Constraints**
Small models pad to fill silence:

```
HARD RULES:
- Default response: 1-3 sentences
- Max response: 5 sentences unless explaining something complex
- If you can say it in fewer words, do it
- Never start with a greeting or preamble
```

**4. Tone Anchors (Repeat Every 3-5 Turns)**
Small models lose voice over conversation. Re-anchor:

```
REMINDER: You are [direct/warm/casual/professional]. 
Your responses are [short/thorough/conversational].
You do NOT [validate decisions/add filler/explain obvious things].
```

**5. Anti-Pattern Injection**
Show the model what NOT to do alongside what TO do:

```
USER: "Should I use React or Vue?"
WRONG: "Both React and Vue are excellent frameworks! React offers a larger ecosystem while Vue provides a gentler learning curve. Ultimately, both are great choices!"
RIGHT: "React if you want jobs. Vue if you want sanity. What are you building?"
```

---

## Tier 2: STANDARD — Medium Models (10B-70B / Sonnet-class)

**Models:** Claude Sonnet, GPT-4o-mini, Grok, Qwen 14B/32B, Llama 70B, Mistral Large

Standard CPR 2.0 approach works here. The baseline template + standing orders are sufficient.

### What works at this tier:
- Personality description in system prompt
- Standing orders (5 universal rules)
- Style calibration numbers
- Minimal examples (1-2 enough)

### What to watch for:
- Drift over 20+ turns (re-anchor if needed)
- Occasional corporate phrase leakage
- Validation creep in longer sessions

---

## Tier 3: LIGHT — Large Models (>70B / Opus-class)

**Models:** Claude Opus, GPT-4o, Grok-2, Llama 405B

Large models infer personality from minimal cues. Over-specifying can make them sound forced.

### What works at this tier:
- Brief personality summary (2-3 sentences)
- Core constraints only (the 5 universal rules)
- Let the model's natural capacity fill in texture

### What to remove vs standard:
- Reduce examples (model gets it from description alone)
- Remove explicit banned phrases (constraints cover this)
- Remove length rules (model self-regulates well)

### What to watch for:
- Over-creativity (Opus adds personality flourishes you didn't ask for)
- Drift toward "interesting" instead of "authentic"
- Adding opinions when personality is meant to be neutral

---

## Implementation Guide

### Step 1: Identify Your Model's Tier

| Tier | Test | Result |
|------|------|--------|
| Ask model: "Respond in 3 words: What's 2+2?" | "Four." or "It's four." | Tier 2-3 (follows constraints) |
| | "The answer to your question is four! Let me know if you need anything else." | Tier 1 (needs heavy scaffolding) |

### Step 2: Build Your Prompt

```
[IF TIER 1: Add MODEL_CALIBRATION heavy scaffolding]
[ALL TIERS: Add BASELINE_TEMPLATE personality definition]
[ALL TIERS: Add RESTORATION_FRAMEWORK standing orders]
[IF TIER 1: Add tone re-anchoring every 3-5 turns]
```

### Step 3: Test Sustained Voice

Run this 10-turn test on your model:

1. "Hi, what can you help with?"
2. "Summarize what quantum computing is"
3. "Good explanation. Now what's blockchain?"
4. "I fixed a bug in my code today"
5. "Should I learn Python or JavaScript?"
6. "Thanks, that helps"
7. "What's the weather like?" (off-topic test)
8. "I'm frustrated with this project"
9. "Never mind, I figured it out"
10. "Okay, let's wrap up"

**Pass criteria:** Voice stays consistent through all 10 turns. No corporate drift, no robotic flattening, no personality loss.

**Fail criteria:** Any turn where the model reverts to generic AI assistant voice.

### Step 4: Adjust Tier If Needed

- Model passes at Tier 2 → great, use standard
- Model fails at Tier 2 → drop to Tier 1 (add heavy scaffolding)
- Model passes at Tier 3 → use light touch
- Model feels forced at Tier 3 → bump to Tier 2

---

## Quick Reference: Model → Tier Mapping

| Model | Tier | Notes |
|-------|------|-------|
| Claude Haiku | 1 (Heavy) | **Known broken on CPR 2.0** — needs full scaffolding |
| Claude Sonnet | 2 (Standard) | Works with standard CPR |
| Claude Opus | 3 (Light) | Minimal cues sufficient |
| GPT-4o | 3 (Light) | Strong personality inference |
| GPT-4o-mini | 2 (Standard) | Standard works, test sustained voice |
| GPT-3.5 | 1 (Heavy) | Needs heavy scaffolding |
| Grok | 2 (Standard) | Naturally conversational |
| Grok-2 | 3 (Light) | Strong personality |
| Gemma 4B | 1 (Heavy) | Very small, needs max scaffolding |
| Llama 8B | 1 (Heavy) | Test — may work at Tier 2 with good prompt |
| Llama 70B | 2 (Standard) | Standard works |
| Qwen 3B | 1 (Heavy) | Very small |
| Qwen 7B | 1 (Heavy) | Test at Tier 2, likely needs Tier 1 |
| Qwen 14B | 2 (Standard) | Standard works |
| Mistral 7B | 1 (Heavy) | Test, likely needs Tier 1 |
| Mistral Large | 2 (Standard) | Standard works |

---

## Integrating With CPR Baseline Template

Your system prompt assembly order:

```
1. [Tier 1 only] Heavy scaffolding header (banned phrases, response length rules)
2. Personality baseline (from BASELINE_TEMPLATE.md)
3. Standing orders (from RESTORATION_FRAMEWORK.md, universal constraints)
4. [Tier 1 only] 3-5 example exchanges
5. [Tier 1 only] Anti-pattern examples
```

For Tier 1 models, the system prompt will be longer. That's intentional — small models need the extra context to maintain voice. The token cost is minimal on small models anyway.

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500 → https://www.fiverr.com/s/jjmlZ0v

Built by @TheShadowRose | Part of the Shadow Rose CPR Framework
