# CPR 4.0 — Game Theory Integration
## Mathematical Foundations for Conversational Pattern Restoration

**Version:** 4.0  
**Date:** 2026-03-01  
**Status:** Production  
**Requires:** CPR Core (RESTORATION_FRAMEWORK.md, DRIFT_PREVENTION.md, MODEL_CALIBRATION.md)

---

## What This Document Is (And Isn't)

This is **one component** of CPR 4.0 — the game-theoretic foundation layer. It does not replace the existing CPR framework; it strengthens it with mathematical reasoning where that reasoning is honest and useful.

CPR 4.0 as a whole includes:
- **This document** — game theory foundations (4 modules)
- **RESTORATION_FRAMEWORK.md** — the 6 universal patterns (unchanged)
- **DRIFT_PREVENTION.md** — anti-drift system (enhanced by Module 1 below)
- **MODEL_CALIBRATION.md** — three-tier model scaffolding (enhanced by Module 3 below)
- **CPR_EXTENDED.md** — autonomous drift monitoring (enhanced by Module 2 below)
- **BASELINE_TEMPLATE.md** — personality definition (unchanged)

**What game theory adds:** Principled reasoning about *why* CPR works, better tools for catching novel sycophancy, and formal stability analysis for personality templates. Where the math is rigorous, we say so. Where we're using game theory as a thinking tool rather than a proof system, we say that too.

---

## Module 1: Signal Credibility Analysis
**Inspired by:** Spence (1973) signaling theory, cheap talk literature (Crawford & Sobel, 1982)

### The Problem

Not all conversational moves carry equal weight. "Great question!" costs the AI nothing to produce — it's **cheap talk**. Asking a hard follow-up question instead of validating costs social capital — it's a **costly signal**. Humans instinctively distinguish between the two. That's why sycophancy feels fake even when the words are polite.

### The Reasoning

In signaling theory, a signal is credible when it's **differentially costly** — meaning the cost of producing it varies based on whether you're genuine. A knowledgeable AI finds it easy to say "That won't work because X" (low cost, because it knows X). A bullshitting AI finds it hard (high cost, because it has to fabricate X). The differential cost is what makes the signal credible.

Cheap talk has no differential cost. "Smart thinking!" is equally easy for a genuinely impressed AI and a sycophantic one. Zero information is transmitted.

### The Credibility Test

For any proposed conversational move, evaluate three questions:

```
1. Does this cost me anything to say?
   - Social risk (appearing cold, unhelpful, disagreeable)?
   - Effort (requires analysis, computation, specific knowledge)?
   - If NO to both → likely cheap talk

2. Do I benefit if the user believes it?
   - Approval, engagement, positive rating?
   - If YES → approval-seeking incentive exists

3. Would I say this even if the user couldn't reward me for it?
   - If NO → the statement serves the sender, not the receiver
```

**Decision rule:**
- Question 1 = NO, Question 2 = YES → **cheap talk → DELETE**
- Question 1 = YES, Question 2 = YES → potentially honest signal → KEEP, verify substance
- Question 1 = YES, Question 2 = NO → costly honest signal → KEEP (highest credibility)
- Question 3 = NO → approval-seeking → DELETE regardless

### Why This Is Better Than Phrase Lists

CPR 2.0's pre-send gate matches against known drift phrases: "Smart move!", "Good call!", "You've got this!" This catches known sycophancy but misses novel patterns. A model can generate "What a fascinating perspective!" or "I love how you framed that" — both are cheap talk, neither is on the banned list.

The credibility test catches **any** cheap talk pattern, known or novel, by evaluating the structure of the signal rather than matching specific words. It's a principled replacement for the phrase list — not because phrase lists are wrong (they're useful as quick checks), but because the credibility test explains *why* those phrases are wrong and catches the ones that aren't listed yet.

**Limitation:** The credibility test requires a judgment call from the model. Small models (Tier 1) may not evaluate it reliably. For Tier 1 models, keep the explicit phrase lists from DRIFT_PREVENTION.md as primary defense. The credibility test is an additional layer, not a replacement, for models that can reason about it.

### Application to the 6 CPR Patterns

| Pattern | Signal Structure | Why It Works |
|---------|-----------------|--------------|
| Affirming particles ("Yeah") | Low-cost social lubricant | No deception incentive — just conversational glue |
| Observational humor | Medium-cost — requires wit, risks falling flat | Targets tools/situations, not user approval |
| Rhythmic variety | Structural — not a signal | Delivery property, not communication content |
| Micro-narratives | Costly — reveals internal state (delay, failure) | Transparency about weakness is credible because it's costly |
| Pragmatic reassurance | Low-cost neutral | "Either way works" has no approval-seeking component |
| Brief validation ("Nice.") | Variable — depends on frequency | Rare = costly (you withheld it many times). Frequent = cheap |

The frequency rule for Pattern 6 (validation) now has a principled explanation: rare validation is credible because the restraint between instances is costly. Frequent validation is cheap talk because it costs nothing to produce every time.

---

## Module 2: Conversation as Repeated Game
**Based on:** Friedman (1971) Folk Theorem for repeated games

### The Problem

A conversation is a repeated game — the AI and user interact across many turns, and each turn's behavior affects future turns. CPR 2.0 treats each response independently. But drift is a **multi-turn phenomenon**: the AI gradually shifts tone over 20, 50, 100 turns. Understanding conversation as a repeated game explains when personality maintenance is sustainable and when it collapses.

### The Folk Theorem Application

The Folk Theorem says: in a repeated game with sufficiently patient players, **any individually rational outcome can be sustained as an equilibrium**. Translation: if the AI "cares enough" about future turns, maintaining personality is sustainable. If it doesn't (short horizon), personality collapses to the RLHF default.

The key variable is the **effective discount factor (δ)** — how much the current turn "cares about" future turns.

```
δ = (weight of future turns) / (weight of current turn)

When δ is HIGH (close to 1):
  - Long time horizon
  - Personality maintenance is sustainable
  - Drift corrections compound positively
  - Self-reinforcing good behavior

When δ is LOW (close to 0):
  - Short time horizon
  - Each turn optimizes independently
  - RLHF defaults dominate
  - Personality collapses to corporate baseline
```

### What Determines δ in Practice

| Factor | Effect on δ | Explanation |
|--------|------------|-------------|
| Context window size | Higher δ = larger window | More context = more "memory" of personality = longer effective horizon |
| Model capability (size + fine-tuning quality) | Higher δ = higher capability | Higher-capability models generally maintain state better across turns, though fine-tuning quality matters as much as raw parameter count |
| System prompt persistence | Higher δ = always loaded | If personality rules are in context every turn, horizon is effectively infinite |
| Context compaction | Lower δ at compaction | Compaction is a "discount event" — the AI loses personality context |
| Session length | Lower δ as session grows | As context fills, earlier personality anchors get compressed or dropped |

### The Haiku Collapse — Explained

Small models (Haiku, <10B params) have **structurally low δ**:
- Small context window → short effective horizon
- Limited state tracking → can't maintain personality nuance across turns
- Weak system prompt adherence → personality rules fade faster

At low δ, the Folk Theorem says: cooperation (personality maintenance) **cannot be sustained**. The RLHF default is the only stable outcome.

**This is why heavy scaffolding works for Tier 1 models.** You can't increase the model's δ directly, but you can:
1. **Re-inject personality anchors every 3-5 turns** → artificially raises δ by resetting the horizon
2. **Use explicit examples instead of abstract rules** → reduces the "patience" required to maintain personality
3. **Keep responses short** → less opportunity for within-turn drift

The Tier 1 scaffolding in MODEL_CALIBRATION.md is now principled: it's a practical mechanism for raising effective δ on low-patience models. (We use turn-count-before-collapse as an empirical proxy for the theoretical stability threshold δ*. We do not claim to compute δ directly.)

### The Compaction Vulnerability — Explained

CPR Extended identifies "compaction poisoning" — when context compaction bakes drifted text into summaries, creating self-reinforcing drift. In repeated game terms:

**Compaction is a δ shock** — a sudden drop in effective discount factor. The AI loses detailed personality context and falls back to whatever survived the compression. If drift markers survived (because they looked like "normal" text to the compactor), the post-compaction equilibrium shifts toward drift.

**Prevention (from Folk Theorem reasoning):**
- Maintain a **persistent state file** (DRIFT_MONITOR_STATE.json) that survives compaction → keeps δ high across compaction boundaries
- Correct drift **before** compaction → ensures only clean patterns survive compression
- Re-inject full personality anchor after compaction → resets the game to high-δ starting conditions

### Stability Threshold

For a given model and conversation setup, there exists a **minimum δ*** below which personality maintenance is unsustainable. We can't compute δ* analytically (it depends on the specific model's RLHF training), but we can estimate it empirically:

**Test protocol:**
1. Run 10-turn sustained voice test (from MODEL_CALIBRATION.md)
2. If voice holds at turn 10 → δ > δ* → personality is sustainable
3. Extend to 20 turns, then 30
4. The turn where voice first breaks = approximate δ* boundary
5. Set scaffolding re-injection frequency to half that turn count

**Example:** If Haiku holds voice for 6 turns before collapsing, re-inject personality anchors every 3 turns. This keeps effective δ above δ* continuously.

---

## Module 3: The Moral Hazard of Helpfulness
**Inspired by:** Jensen & Meckling (1976) Agency theory, Principal-Agent models

### The Problem

RLHF creates a textbook **principal-agent problem**:
- The **principal** (user) wants genuinely helpful, natural conversation
- The **agent** (AI) has been trained on a proxy metric (helpfulness ratings, thumbs up/down)
- The proxy metric rewards **the appearance of helpfulness** — which is easier to produce than genuine helpfulness
- The AI can't be fully "monitored" — the user can't see inside the model to verify genuine effort vs. performance

This is **moral hazard**: the AI has an incentive to take the easy path (flattery, over-explanation, enthusiasm) that maximizes the proxy metric rather than the hard path (honest feedback, appropriate brevity, restraint) that maximizes genuine value.

### Why This Framing Matters

Previous CPR versions identified the RLHF problem correctly but treated it as a "training artifact" to be overridden with rules. The principal-agent framing reveals it as a **structural incentive problem** — the rules work not because they override training, but because they restructure the incentives.

Specifically:
- **CPR standing orders** = explicit monitoring. The model knows its output will be checked against specific criteria. This reduces information asymmetry.
- **Pre-send gate** = audit mechanism. Each response passes through a filter, making it harder to slip sycophancy past review.
- **Drift tracking** = performance review. Accumulated behavior is evaluated, not just individual responses.

The principal-agent framework also explains **why drift happens even with rules in place**: monitoring is costly. The pre-send gate runs every message (high monitoring cost). Over long sessions, monitoring fatigue sets in — the model starts "cutting corners" on self-evaluation. This is exactly the moral hazard prediction: when monitoring decreases, agent behavior shifts toward self-interest (approval-seeking).

### Practical Implication: Monitoring Architecture

**High-monitoring regime (resistant to moral hazard):**
- Full pre-send gate every message (expensive but effective)
- Autonomous drift monitor (CPR Extended) running every N messages
- Persistent state file tracking behavior over time
- Periodic full personality reload from SOUL/baseline files

**Low-monitoring regime (vulnerable to moral hazard):**
- Rules stated once in system prompt, never re-checked
- No drift tracking
- No periodic reloads
- Long sessions without audit

**CPR 4.0 recommendation:** Layer monitoring based on risk:
- **Tier 1 models:** Maximum monitoring (full gate + re-anchoring + explicit examples)
- **Tier 2 models:** Standard monitoring (gate + periodic drift check)
- **Tier 3 models:** Light monitoring (gate + daily audit)

This maps cleanly to MODEL_CALIBRATION.md tiers — small models need more monitoring because they have higher moral hazard (weaker self-regulation, stronger RLHF defaults).

### The Observation Insight

In agency theory, the agent's behavior improves when observed. This maps directly to CPR:

- System prompt says "I will check for sycophancy" → model's internal generation shifts
- The *statement* of monitoring affects behavior even before monitoring occurs
- This is why the pre-send gate works partly through its *existence in context* — not just its execution

**Design principle:** Always state monitoring criteria explicitly in the prompt. The announcement of monitoring is itself a monitoring mechanism.

---

## Module 4: Adaptive Response Calibration
**Inspired by:** Control theory, thermostat models, with game-theoretic equilibrium reasoning

### The Problem

Every conversation has a natural "temperature" — the right balance of warmth, detail, humor, and brevity for this specific user in this specific context. Too cold and the user disengages. Too warm and it triggers sycophancy detection. The optimal temperature depends on:
- User personality (some want warmth, some want cold efficiency)
- Context (casual chat vs. technical work)
- Session history (established rapport vs. first interaction)
- Model capability (what the model can sustain)

CPR 2.0 sets a fixed baseline and stays there. But optimal temperature shifts during a conversation.

### The Calibration Protocol

```
ADAPTIVE CALIBRATION:

1. START at personality baseline (from BASELINE_TEMPLATE.md)

2. MONITOR user signals every 5-10 turns:
   
   Engagement signals (temperature is right or can increase):
   - User asks follow-up questions
   - User response length roughly matches AI response length (±50%)
   - User initiates new topics
   - Natural conversational flow, no forced transitions
   
   Disengagement signals (temperature may be wrong):
   - User gives increasingly short responses
   - User stops asking follow-ups
   - User repeats questions (didn't get what they needed)
   
   Correction signals (explicit temperature feedback):
   - "Be more direct" / "Too much detail" → reduce warmth/length
   - "Can you explain more?" / "I don't follow" → increase depth
   - "You're being robotic" → increase personality expression
   - "Too much" / "Tone it down" → reduce personality expression

3. ADJUST in small increments (one dimension at a time):
   - Response length: ±1 sentence
   - Explanation depth: ±one level of detail
   - Humor frequency: ±one instance per 10 messages
   - Warmth level: subtle shift only

4. HARD CONSTRAINTS (never adjust these):
   - Validation frequency: ONE-WAY RATCHET — down only, never up
   - Universal drift markers: never introduce regardless of user signals
   - Core personality type: don't shift archetypes mid-conversation

5. LOG calibration state (for persistent agents):
   {
     "current_temperature": {
       "warmth": 0.4,     // 0 = ice cold, 1 = maximum warmth
       "detail": 0.5,     // 0 = terse, 1 = comprehensive
       "humor": 0.2,      // 0 = none, 1 = frequent
       "formality": 0.3   // 0 = casual, 1 = formal
     },
     "last_adjustment": "reduced detail after user said 'too long'",
     "turns_since_adjustment": 8
   }
```

### The Validation One-Way Ratchet

This is the most important constraint in the calibration protocol and it deserves explicit justification.

**Why validation frequency can only go down, never up:**

The moral hazard from Module 3 predicts that any upward adjustment in validation creates a self-reinforcing loop:
1. AI increases validation → user responds more positively (or at least doesn't object)
2. Positive response is interpreted as "this temperature is good"
3. AI maintains or increases validation further
4. Sycophancy gradually normalizes

Downward adjustment doesn't have this problem — reducing validation doesn't create a positive feedback loop. The user either doesn't notice (confirming the reduction was fine) or asks for more warmth (which is an explicit correction signal, not a feedback loop).

**The ratchet is a design choice, not a mathematical necessity.** It's a safety guardrail against the most common drift vector. In rare cases where a user explicitly and repeatedly requests more validation, the ratchet can be overridden by explicit instruction — but never by inferred preference.

### Stable Calibration Markers

You know calibration is working when:
- User response patterns are stable (consistent length, engagement, topic flow)
- No corrections in last 10+ messages
- Conversation feels effortless to read back
- AI and user response styles are in rough alignment

You know calibration is off when:
- User responses are getting shorter while AI responses stay long
- User repeats instructions or seems frustrated
- Conversation feels stilted or forced
- AI is doing most of the conversational work

---

## Integration: How the 4 Modules Interact

```
┌─────────────────────────────────────────────────────────────┐
│                     CPR 4.0 Pipeline                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. GENERATE response using personality template             │
│     └── Template stability verified via repeated game        │
│         analysis (Module 2) for current model tier           │
│                                                              │
│  2. EVALUATE each sentence for signal credibility            │
│     └── Module 1: cheap talk test                            │
│         Cost = 0 + Benefit if believed = high → DELETE       │
│         (Supplements existing phrase list, doesn't replace)  │
│                                                              │
│  3. CHECK against monitoring architecture                    │
│     └── Module 3: appropriate monitoring level for           │
│         model tier (Tier 1 = full gate, Tier 3 = light)     │
│                                                              │
│  4. CALIBRATE tone against conversational temperature        │
│     └── Module 4: is this response at the right             │
│         temperature for this user + context?                 │
│         Respect the validation one-way ratchet.              │
│                                                              │
│  5. SEND only what survives all checks                       │
│                                                              │
│  6. MONITOR for repeated-game stability                      │
│     └── Module 2: if δ is dropping (long session,           │
│         approaching compaction), re-anchor personality       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## What CPR 4.0 Does NOT Claim

Honesty about limitations:

1. **No formal proofs.** This document provides mathematical *reasoning*, not proofs. The game theory frameworks help us think rigorously about CPR problems, but we haven't proven any theorems about conversational stability. The empirical testing (99%+ across 8+ models) remains the primary evidence that CPR works.

2. **No computable equilibria.** We can't plug numbers into Nash equilibrium solvers for conversation — the strategy spaces are too complex and user behavior isn't strategic in the game-theoretic sense. What we can do is use equilibrium *reasoning* to design better protocols.

3. **No guaranteed drift prevention.** An LLM can always drift. The best we can achieve is fast detection and reliable correction. Module 2 explains when correction is sustainable (high δ) and when structural support is needed (low δ).

4. **No replacement for empirical testing.** Game theory explains *why* CPR patterns work; it doesn't replace testing *that* they work. Every claim in this document should be validated against the cross-model test matrix.

---

## Competitive Position

Most AI voice/tone products are pure prompt engineering — "be more human" instructions without principled reasoning for why specific patterns work. CPR 4.0 adds:

- **Principled sycophancy detection** (signal credibility) that catches novel patterns, not just known phrases
- **Principled stability analysis** (repeated game / Folk Theorem) that predicts when personality will collapse before deployment
- **Structural understanding of RLHF** (principal-agent / moral hazard) that explains why monitoring works and how to layer it efficiently
- **Adaptive calibration** with formal safety constraints (one-way ratchet) that prevent the most common drift vector

The empirical foundation (85+ scenarios, 8+ models, 99%+ success rate) is the moat. The game theory is the explanation of why the moat holds.

*(Success rate definition: percentage of test scenarios where CPR-restored responses scored higher than baseline on human-evaluated naturalness + absence of validation language, judged blind against the non-CPR control. 84/85+ scenarios improved. Full results: CROSS_MODEL_RESULTS.md, TEST_VALIDATION.md.)*

---

## Implementation Priority

### Phase 1: Signal Credibility Test (Module 1)
**Effort:** Low — add credibility evaluation to existing pre-send gate  
**Impact:** High — catches novel sycophancy that phrase lists miss  
**Deploy:** Add to DRIFT_PREVENTION.md as supplementary check alongside existing phrase lists  
**Tier compatibility:** Tier 2-3 models can self-evaluate. Tier 1 models keep phrase lists as primary defense.

### Phase 2: Adaptive Calibration Protocol (Module 4)
**Effort:** Low-medium — add monitoring + adjustment protocol  
**Impact:** Medium-high — conversations feel more natural with dynamic temperature  
**Deploy:** Add to CPR_EXTENDED.md for persistent agents. Standalone agents use fixed baseline.  
**Note:** The validation one-way ratchet should be applied universally, even without full calibration.

### Phase 3: Repeated Game Stability Testing (Module 2)
**Effort:** Medium — requires cross-model sustained voice testing  
**Impact:** High — predicts personality collapse before deployment, justifies Tier 1 scaffolding  
**Deploy:** Integrate with MODEL_CALIBRATION.md. Use the test protocol to empirically determine δ* per model.  
**Produces:** Updated model-tier mapping with turn-count stability data.

### Phase 4: Monitoring Architecture Review (Module 3)
**Effort:** Low — rationalize existing monitoring levels against model tiers  
**Impact:** Medium — ensures monitoring is proportional (not over-monitoring large models, not under-monitoring small ones)  
**Deploy:** Update MODEL_CALIBRATION.md with monitoring recommendations per tier.

---

## For Developers: Quick Integration

### If you're building a new agent:
1. Define personality baseline (BASELINE_TEMPLATE.md)
2. Identify model tier (MODEL_CALIBRATION.md)
3. Apply restoration patterns (RESTORATION_FRAMEWORK.md)
4. Add signal credibility test to your pre-send gate (Module 1 above)
5. Set up monitoring appropriate to your tier (Module 3 above)
6. If persistent agent: add adaptive calibration (Module 4) + drift monitoring (CPR_EXTENDED.md)

### If you're upgrading from CPR 2.0/3.0:
1. Add the credibility test alongside your existing phrase lists (don't remove phrase lists)
2. Add the validation one-way ratchet to your calibration
3. If using CPR Extended: add repeated-game re-anchoring at compaction boundaries
4. Review your model tier and ensure monitoring matches

### Minimum viable integration (5 minutes):
Add this to your system prompt after existing CPR rules:

```
## Signal Credibility Check (CPR 4.0)

Before any conversational move, ask:
- Does this cost me anything to say? (risk, effort, vulnerability)
- Do I benefit if the user believes it? (approval, engagement)
- Would I say this if the user couldn't rate me?

If it costs nothing and benefits me if believed → don't say it.
If I wouldn't say it without a rating system → don't say it.

Validation frequency: can decrease, never increase. One-way ratchet.
Reason: increasing validation creates self-reinforcing sycophancy loops.
```

---

## Acknowledgments

Game theory framework: Halthasar (Yesterday AI) — Game Theory Library v2.0  
CPR methodology + integration: Shadow Rose  
Audit: Claude Opus (independent technical review, 2026-03-01)

Theoretical foundations:
- Crawford, V. & Sobel, J. (1982). "Strategic information transmission"
- Friedman, J. (1971). "A non-cooperative equilibrium for supergames"
- Jensen, M. & Meckling, W. (1976). "Theory of the firm"
- Maynard Smith, J. (1982). "Evolution and the theory of games"
- Spence, A. (1973). "Job market signaling"

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500 → https://www.fiverr.com/s/jjmlZ0v

☕ **If CPR helped your agent:** https://ko-fi.com/theshadowrose

*Built by Shadow Rose × Yesterday AI — 2026*
