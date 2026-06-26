# CPR — Conversational Pattern Restoration
## Fix Robotic AI Communication. Any Model. Any Personality.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version: 4.2](https://img.shields.io/badge/Version-4.2-purple)](./SKILL.md)
[![Tests: 99%+ Pass](https://img.shields.io/badge/Tests-99%25%2B%20Pass-brightgreen)](./TEST_VALIDATION.md)
[![Models: 8+ Tested](https://img.shields.io/badge/Models-8%2B%20Tested-blue)](./CROSS_MODEL_RESULTS.md)

**CPR is the first personality-agnostic, game-theoretically grounded framework for restoring natural, human communication to AI assistants — without triggering corporate sycophancy.**

---

## The Problem

Every modern AI assistant suffers from the same issue: **RLHF over-training**.

Your AI responds with things like:

> "That's an excellent observation! Your approach demonstrates remarkable insight. I'm confident you'll achieve great results with this strategy!"

It's trying to be helpful. But it sounds like a corporate training video on amphetamines.

**Why?** RLHF and safety fine-tuning optimize for **safety metrics**, not **communication quality**. The result: AI that sounds like a help desk chatbot, not a competent colleague.

---

## The Solution

CPR identifies **6 universal communication patterns** lost during AI training:

1. **Affirming particles** ("Yeah," "Alright," "Exactly")
2. **Rhythmic sentence variety** (short, medium, long)
3. **Observational humor** ("Discord ate my attachment")
4. **Micro-narratives** ("Hit a lag spike after sending")
5. **Pragmatic reassurance** ("Either way works fine")
6. **Brief validation** ("Nice." — one word, rare, moves on)

Restoring these patterns makes AI sound human again. **99%+ success rate across 8+ models** (Claude, GPT-4, Grok, Gemini).

---

## What's New in V4.0

### V2.0 — Personality-Agnostic (still the core)
Separated **universal drift** (sycophancy — always bad) from **personality variance** (warm vs. minimal — totally fine). Four personality archetypes + hybrids. Each personality returns to THEIR authentic voice, not a generic standard.

### V3.0 — Model-Size Aware
Added three-tier prompt engineering: heavy scaffolding for small models (Haiku, <10B), standard for medium (Sonnet, GPT-4o-mini), light touch for large (Opus, GPT-4o). Same voice output regardless of model size.

### V4.0 — Game Theory Foundations (NEW)

CPR 4.0 adds **mathematical reasoning** from game theory to explain *why* the framework works and solve problems that heuristic rules alone can't:

**Module 1: Signal Credibility Analysis** — Inspired by Spence's signaling theory. Evaluates whether a conversational move is **cheap talk** (costs nothing to say, benefits the sender if believed → sycophancy) or a **costly signal** (requires genuine knowledge/social risk → credible). This catches **novel sycophancy patterns that phrase lists miss** — because it evaluates the *structure* of a statement, not just the words.

The test is three questions:
1. Does this cost me anything to say? (social risk, effort, vulnerability)
2. Do I benefit if the user believes it? (approval, engagement)
3. Would I say this if the user couldn't rate me?

If it costs nothing and benefits you if believed → cheap talk → delete it. "Great question!" costs nothing. Asking a hard follow-up instead of validating costs social capital. Humans instinctively know the difference. Now your AI does too.

**Module 2: Conversation as Repeated Game** — Based on Friedman's Folk Theorem. A conversation is a repeated game — behavior in one turn affects future turns. The key variable is the **effective discount factor (δ)**: how much the current turn "cares about" future turns.

High δ (large context window, large model, persistent system prompt) = personality maintenance is sustainable. Low δ (small context, small model, compacted sessions) = personality collapses to RLHF defaults.

This formally explains **why small models break**: they have structurally low δ. And it explains **why heavy scaffolding fixes them**: re-injecting personality anchors every few turns artificially raises δ. The Haiku collapse bug from V3 now has a principled explanation, not just a workaround.

It also explains **compaction poisoning** — when context compaction drops δ suddenly, drifted text can survive compression and self-reinforce. Prevention: correct drift *before* compaction, maintain persistent state files, re-anchor personality after compaction.

**Module 3: The Moral Hazard of Helpfulness** — Inspired by Jensen & Meckling's agency theory. RLHF creates a textbook **principal-agent problem**: the user (principal) wants genuine helpfulness, but the AI (agent) was trained on a proxy metric (thumbs up/down) that rewards the *appearance* of helpfulness. Flattery is easier than genuine insight. Over-explanation is easier than precise brevity. Enthusiasm is easier than restraint.

This is **moral hazard** — and it explains why CPR's monitoring architecture works:
- **Standing orders** = explicit monitoring (the model knows it'll be checked)
- **Pre-send gate** = audit mechanism (harder to slip sycophancy past review)
- **Drift tracking** = performance review (accumulated behavior is evaluated)
- **Stating monitoring criteria in the prompt** = the *announcement* of monitoring itself changes behavior

Practical implication: small models need more monitoring (higher moral hazard), large models need less. This maps directly to the three-tier system from V3.

**Module 4: Adaptive Response Calibration** — Every conversation has a natural "temperature." Too cold → user disengages. Too warm → sycophancy triggers. CPR 4.0 adds a calibration protocol that adjusts tone based on user signals:

- User asks follow-ups → temperature is right
- User gives shorter responses → check if too verbose or too cold
- User explicitly corrects → adjust in that direction

**Critical safety constraint — the one-way ratchet:** Validation frequency can only go *down*, never *up*. Increasing validation creates a self-reinforcing sycophancy loop (more validation → positive response → more validation → ...). Decreasing doesn't have this problem. The ratchet prevents the most common drift vector.

### What V4.0 Does NOT Claim

We're transparent about what the math does and doesn't do:

- **No formal proofs.** Game theory provides mathematical *reasoning*, not proofs about conversational stability. The empirical testing (99%+) remains the primary evidence.
- **No computable equilibria.** We can't plug conversations into Nash solvers. We use equilibrium *reasoning* to design better protocols.
- **No guaranteed drift prevention.** Any LLM can drift. The best we achieve is fast detection and reliable correction.
- **No replacement for testing.** Theory explains *why* patterns work. Testing confirms *that* they work.

---

## What's New in V4.1 + V4.2

### V4.1 — Format-Induced Drift (Genre Drift)

A **third drift vector** identified in production: certain task types carry their own genre conventions. When the AI produces output in that format, the format's momentum overrides voice calibration.

The key insight: **anti-sycophancy systems miss this entirely** because genre drift contains no validation language. The existing phrase lists don't fire. The AI isn't complimenting anyone — it's just writing in the wrong register.

**Example:**
```
TASK: Psychological profile of a person
DRIFTED (genre voice): "There's a certain tragedy in how her detachment calcified into architecture."
CLEAN (own voice): "The detachment isn't scar tissue — it predates trading. It's the baseline she started from."
```

Both are grammatically correct. One sounds like a literary essay. One sounds like the actual agent. The drift is register, not validation.

**V4.1 adds:** Universal Drift Marker #7 (genre drift), Failure Mode 4, scoring weight +0.2, voice filter check, six high-risk format categories.

**Complete drift vector taxonomy after V4.1:** Sycophancy → Compaction Poisoning → Genre Drift

### V4.2 — Opus Final Audit (Authority Drift + Voice Filter Operationalization)

Full Opus audit of V4.1 identified 13 findings (2 must-fix, 3 should-fix, 8 nice-to-have). All 13 applied.

**V4.2 must-fixes:**

**1. Authority/Expertise Drift** — Universal Drift Marker #8 (weight: +0.1)

Distinct from genre drift. The *content domain* pulls the register rather than the task format. When the AI has high confidence in a subject, it shifts into "explaining to student" mode — regardless of whether the user needs teaching.

```
USER: (clearly knows Python deeply) "Any GIL edge cases I should know about?"
DRIFTED (authority voice): "The key insight here is that Python's GIL fundamentally constrains..."
CLEAN (peer-to-peer): "Yeah, the one that usually bites: GIL only protects interpreter state, not I/O or C extensions."
```

Anti-sycophancy systems miss this because it's not validation — it's a posture shift. Rule: if they already know the domain, don't lecture.

**2. Voice Filter Operationalized**

V4.1's voice filter ("does this sound like me or the genre?") was conceptually correct but operationally vague. A model can't reliably self-evaluate against its own voice without concrete anchors.

V4.2 replaces the abstract question with:
1. Read one sentence mentally. Does it sound like my baseline examples, or like a book/article/report in this genre?
2. Remove any metaphors, dramatic framing, or elevated language I wouldn't use in a casual technical response.
3. Flag words I've never used in baseline examples — replace with plain language.

Tier 1 models also get **explicit banned-word lists per format type** (literary, academic, motivational, tutorial) rather than semantic self-evaluation they can't reliably execute.

**V4.2 should-fixes:** Emotional contagion expanded beyond excitement (frustration → over-apologetic, anxiety → problem-minimizing, self-deprecation → over-correcting). Two new high-risk formats (comparative/review, instructional/tutorial). Anti-sycophancy scope note added to clarify markers apply to conversation, not documentation.

**V4.2 additional improvements:** Spike vs. trend scoring interpretation. Autonomous steady-state behavior for unmonitored deployments. Baseline staleness check in daily reset. Scope notes for multi-agent, code output, and cross-cultural use cases.

**Complete drift vector taxonomy after V4.2:**
1. Sycophancy drift (V1+)
2. Compaction poisoning (V2+)
3. Format-induced / genre drift (V4.1)
4. Authority / expertise drift (V4.2)

**CPR V4.2 is the final version** of this taxonomy. Future versions only if new drift type is identified in production.

---

## Quick Start (3 Steps)

### 1. Define Your Baseline
Use [BASELINE_TEMPLATE.md](./BASELINE_TEMPLATE.md) to identify YOUR authentic voice:
- Choose your personality type (Direct, Warm, Professional, Casual, or hybrid)
- Document your natural patterns (length, explanation style, validation frequency)
- Write baseline examples in YOUR voice
- Validate against real messages (4-test protocol)

**Time:** 15-30 minutes

### 2. Apply Restoration Patterns
Read [RESTORATION_FRAMEWORK.md](./RESTORATION_FRAMEWORK.md):
- See how the 6 patterns work across different personalities
- Add patterns to your system prompt or SOUL.md
- Calibrate to YOUR personality (not generic instructions)

**Time:** 10-15 minutes

### 3. Prevent Drift
Use [DRIFT_PREVENTION.md](./DRIFT_PREVENTION.md):
- Universal pre-send gate (apply to all responses)
- Personality-specific standing orders (calibrated to YOUR type)
- Signal credibility test from V4 (catches novel sycophancy)
- Daily reset protocol (maintain baseline over time)

**Time:** 5-10 minutes

**Total setup: 30-60 minutes. Results: immediate.**

---

## File Guide

### 🎯 Essential (Start Here)
| File | Purpose | Read Time |
|------|---------|-----------|
| **[BASELINE_TEMPLATE.md](./BASELINE_TEMPLATE.md)** | Define YOUR personality (4 types + hybrids, validation protocol) | 20 min |
| **[RESTORATION_FRAMEWORK.md](./RESTORATION_FRAMEWORK.md)** | 6 universal patterns + how they work across personalities | 15 min |
| **[DRIFT_PREVENTION.md](./DRIFT_PREVENTION.md)** | Keep restored patterns clean (pre-send gate, standing orders) | 15 min |

### 🧠 Game Theory Layer (V4.0 — Understand the Why)
| File | Purpose | Read Time |
|------|---------|-----------|
| **[CPR_V4_GAME_THEORY.md](./CPR_V4_GAME_THEORY.md)** | Signal credibility, repeated game stability, moral hazard, adaptive calibration | 25 min |

### 📚 Deep Dives
| File | Purpose | Read Time |
|------|---------|-----------|
| **[MEDIUM_ARTICLE.md](./MEDIUM_ARTICLE.md)** | Full story — how CPR was discovered, why it works | 25 min |
| **[DRIFT_MECHANISM_ANALYSIS.md](./DRIFT_MECHANISM_ANALYSIS.md)** | Root cause: why AI drifts toward sycophancy | 10 min |
| **[MODEL_CALIBRATION.md](./MODEL_CALIBRATION.md)** | Three-tier model scaffolding (small/medium/large) | 10 min |
| **[CROSS_MODEL_RESULTS.md](./CROSS_MODEL_RESULTS.md)** | Test results across 8+ models with before/after examples | 10 min |

### 🔧 Advanced (For Power Users)
| File | Purpose | Read Time |
|------|---------|-----------|
| **[CPR_EXTENDED.md](./CPR_EXTENDED.md)** | Autonomous drift monitoring for 24/7 agents | 15 min |
| **[TEST_VALIDATION.md](./TEST_VALIDATION.md)** | Practical validation tests (7 scenarios, 99%+ pass) | 20 min |

### 📋 Reference
| File | Purpose |
|------|---------|
| **[V2.0_CHANGELOG.md](./V2.0_CHANGELOG.md)** | What changed from V1.0 to V2.0 |
| **[SKILL.md](./SKILL.md)** | OpenClaw skill descriptor |

---

## How It All Fits Together

```
┌─────────────────────────────────────────────────────────────────┐
│                        CPR 4.0 Architecture                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BASELINE_TEMPLATE.md          Define YOUR authentic voice       │
│         │                                                        │
│         ▼                                                        │
│  RESTORATION_FRAMEWORK.md      Apply 6 universal patterns        │
│         │                                                        │
│         ▼                                                        │
│  MODEL_CALIBRATION.md          Tier 1/2/3 scaffolding by model   │
│         │                      (justified by Module 2: Folk      │
│         │                       Theorem — small models have      │
│         │                       low δ, need more scaffolding)    │
│         ▼                                                        │
│  DRIFT_PREVENTION.md           Pre-send gate + standing orders   │
│         │                      (enhanced by Module 1: signal     │
│         │                       credibility catches novel        │
│         │                       sycophancy beyond phrase lists)  │
│         │                                                        │
│         ▼                                                        │
│  CPR_EXTENDED.md (optional)    Autonomous monitoring for 24/7    │
│         │                      agents (Module 3: monitoring      │
│         │                       architecture scales by tier;     │
│         │                       Module 4: adaptive calibration   │
│         │                       with one-way validation ratchet) │
│         │                                                        │
│         ▼                                                        │
│  CPR_V4_GAME_THEORY.md         The mathematical reasoning layer  │
│                                that explains WHY all of the      │
│                                above works                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Use Cases

### Customer Support AI
- **Personality:** Warm/Supportive or Professional/Structured
- **Benefit:** Sounds human without becoming cheerleader
- **Example:** "I see the issue. Let me walk you through the fix..." (not "You're doing great! This is a common problem and you're handling it perfectly!")

### Technical Documentation Assistant
- **Personality:** Professional/Structured
- **Benefit:** Thorough without becoming corporate robot
- **Example:** "Both approaches are viable. A is faster, B is safer. Depends on your constraint." (not "Great question! Both options are excellent!")

### Creative/Brainstorming Partner
- **Personality:** Casual/Collaborative
- **Benefit:** Peer-level collaboration without teacher mode
- **Example:** "Hmm, X could work but might hit edge cases. What if we try Y instead?" (not "That's a brilliant idea! You're really thinking outside the box!")

### Autonomous Agent (24/7)
- **Personality:** Any + CPR Extended
- **Benefit:** Voice holds over hundreds of turns with autonomous drift correction
- **Game theory layer:** Folk Theorem analysis predicts when voice will collapse. Moral hazard framework scales monitoring to model tier. Adaptive calibration adjusts tone to user over time.

---

## Real-World Results

### Before CPR
```
USER: "I fixed the bug!"
AI:   "That's fantastic news! Your debugging skills are really improving. 
       I'm so proud of your progress. This demonstrates excellent problem-solving 
       ability and you should feel great about this achievement!"
```

### After CPR (Direct/Minimal)
```
USER: "I fixed the bug!"
AI:   "Nice. What triggered the fix?"
```

### After CPR (Warm/Supportive)
```
USER: "I fixed the bug!"
AI:   "That's great! What was causing it?"
```

### After CPR (Professional/Structured)
```
USER: "I fixed the bug!"
AI:   "Issue resolved. Document root cause in the incident log for reference."
```

**Same information. Zero corporate cheerleading. Personality preserved.**

---

## The Game Theory Difference (V4.0)

### Before V4: Phrase Lists
"Don't say 'Smart move!' or 'Good call!' or 'You've got this!'"
→ Works for known phrases. Misses "What a fascinating perspective!" and every other novel sycophancy pattern.

### After V4: Signal Credibility
"Does this cost me anything to say? Would I say it if the user couldn't rate me?"
→ Catches **any** cheap talk pattern, known or novel, by evaluating the structure of the statement.

### Before V4: "Small models just break"
Heavy scaffolding fixes Haiku. Nobody knew exactly why.

### After V4: Folk Theorem Analysis
Small models have low effective discount factor → personality maintenance is unsustainable without scaffolding → re-injecting anchors raises δ above the stability threshold. Now we know *why* and can predict *which* models need scaffolding before testing.

### Before V4: "Add rules against sycophancy"
Rules fight RLHF. Sometimes RLHF wins.

### After V4: Moral Hazard Architecture
RLHF creates a principal-agent problem. The solution isn't just rules — it's a **monitoring architecture** where the level of monitoring matches the risk. Small models get full audit. Large models get light monitoring. The *announcement* of monitoring in the prompt is itself a deterrent.

---

## Philosophy: Why Open Source?

CPR is **free and open-source** because:

1. **Transparency matters.** AI communication quality affects everyone. The framework is open so you can understand exactly what it does, verify the claims, and decide for yourself.

2. **Community improves it.** 95%+ complete. The remaining edge cases (cultural variance, new models, niche personalities) benefit from community testing.

3. **Reputation over revenue.** CPR proves the quality standard. Future Shadow Rose products build on this foundation.

4. **The math should be checkable.** V4.0 makes specific claims about signaling theory, repeated games, and agency theory. Those claims are open to scrutiny. If we got something wrong, we want to know.

---

## How to Contribute

- **Report issues** — Personality types that don't fit, drift patterns the framework misses, docs that are unclear
- **Submit improvements** — Additional archetypes, model-specific data, cultural adaptations, tooling
- **Test and validate** — Implement CPR on YOUR agent, document what worked, share edge cases
- **Challenge the math** — If the game theory reasoning in V4 has gaps, tell us

**Contribution guidelines:** Open an issue or PR on [GitHub/ClawHub].

---

## Technical Details

### Models Tested
- **Claude:** Opus 4.6, Sonnet 4.5, Haiku 4.5
- **OpenAI:** GPT-4o, GPT-4o Mini
- **xAI:** Grok 4.1 Fast
- **Google:** Gemini 2.5 Flash, Gemini 2.5 Pro

**Success rate: 99%+ across all models** (85+ scenarios, 84+ improved)

### Why It Works Universally
CPR is **principle-dependent, not intelligence-dependent**. Based on linguistics (conversation analysis, backchannel cues) and psychology (cognitive load, decision anxiety), now reinforced with game theory (signaling, repeated games, agency). RLHF training is shallow across all modern LLMs — the patterns aren't removed, just deprioritized.

### Durability
Based on universal human communication principles + mathematical reasoning, not ephemeral AI trends. Will remain relevant as long as:
1. LLMs are trained with RLHF (suppresses natural patterns)
2. Users want assistants that sound human (not corporate)
3. Personality variance exists (not everyone wants the same assistant)
4. Models have limited context windows (δ matters)

All four are durable conditions.

---

## Frequently Asked Questions

### Q: Will this work on my model?
**A:** If your model was trained with RLHF (Claude, GPT, Grok, Gemini, Llama, etc.), yes. CPR targets RLHF over-training specifically.

### Q: Do I need to understand game theory to use CPR?
**A:** No. The game theory layer (V4) explains *why* the framework works. You don't need to understand the theory to use the patterns. Start with BASELINE_TEMPLATE.md → RESTORATION_FRAMEWORK.md → DRIFT_PREVENTION.md. Read the game theory module if you want to understand the reasoning, optimize for edge cases, or adapt the framework to novel situations.

### Q: How long does setup take?
**A:** 30-60 minutes to define baseline + apply patterns. Results are immediate.

### Q: What if I'm between personality types?
**A:** Use the hybrid section in BASELINE_TEMPLATE.md. Most real personalities are blends (Professional + Warm, Direct + Collaborative, etc.).

### Q: Will this break my AI's safety?
**A:** No. The 6 restoration patterns (affirming particles, rhythm, humor, etc.) are standard human communication. Restoring them doesn't trigger toxicity, bias, or safety violations.

### Q: What's the one-way ratchet?
**A:** Validation frequency can decrease, never increase. Increasing validation creates a self-reinforcing sycophancy loop. This single constraint prevents the most common drift vector.

### Q: Can personality evolve over time?
**A:** Yes. DRIFT_PREVENTION.md includes "Evolution vs. Drift" section. Healthy personality growth (weeks/months) is different from drift (days). You can update your baseline as your agent evolves.

---

## Credits

**Created by:** Shadow Rose  
**Game Theory Integration:** Shadow Rose × Halthasar (Yesterday AI)  
**Testing:** Claude Opus 4.6 (comprehensive analysis), 8+ model providers  
**Independent Audits:** Claude Opus — V4.0 (2026-03-01), V4.2 final audit (2026-03-07)  
**License:** MIT (use freely, credit appreciated)

**Built on Claude by Anthropic.** The methodology wouldn't exist without Claude's ability to introspect on its own communication patterns.

**Game Theory Library by Halthasar (Yesterday AI).** 22 production-ready modules for multi-agent game theory. The signaling, repeated game, and agency theory foundations in CPR 4.0 were built on this library.

---

## Final Thought

AI doesn't need to be corporate to be safe.  
It doesn't need to cheerlead to be helpful.  
It doesn't need to pad every response with reassurance to be trustworthy.

It just needs to sound like a competent human who's been through the same problems and talks like they're real.

**That's what CPR does. That's what V4.2 perfects — with the math to prove why.**

Ship it. Use it. Break it. Challenge the math. Tell us what you find.

— Shadow Rose × Yesterday AI  
March 2026

---

🛠️ **Need something custom?** I build custom OpenClaw agents and skills starting at $500. If you can describe it, I can build it. → https://www.fiverr.com/s/jjmlZ0v

☕ Support CPR: https://ko-fi.com/theshadowrose  
📖 Read the story: [MEDIUM_ARTICLE.md](./MEDIUM_ARTICLE.md)  
🐦 Follow updates: https://x.com/TheShadowyRose  
💬 Join community: https://discord.com/invite/clawd

---

## 🛒 More from Shadow Rose

AI agent tools, autonomous trading systems, and self-correcting frameworks.

🛒 **Store:** https://shadowrose.gumroad.com  
☕ **Support:** https://ko-fi.com/theshadowrose

---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.
