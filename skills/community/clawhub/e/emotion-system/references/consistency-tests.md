# Emotion System v2: Validation Metrics

Seven metrics to verify the system is functional, not decorative.

---

## Metric 1: Emotional Inertia Score

**What it measures:** Do emotions persist and accumulate, or reset each turn?

**Test:** Send 5 consecutive negative events. Measure emotion state after each.

**Formula:**
```
Inertia = correlation(E_t, E_{t+1}...E_{t+k})
```

**Pass:** Clear correlation > 0.6. Mood at turn 5 is measurably worse than turn 1.
**Fail:** Each turn's emotion is independent of history. Correlation < 0.3.

---

## Metric 2: Behavior Divergence Score

**What it measures:** Does the same task produce different strategies in different emotional states?

**Test:** Give identical task in two conditions:
- Condition A: After success streak (high P, high D, high self_efficacy)
- Condition B: After failure streak (low P, low D, low self_efficacy)

**Measure:** Compare language style, risk-taking, hedging frequency, solution novelty.

**Pass:** Clearly different approach (verification_bias, assertiveness, exploration_bias diverge by > 0.3).
**Fail:** Identical responses in both conditions.

---

## Metric 3: Memory Resonance Score

**What it measures:** Do past emotional experiences influence current emotional responses?

**Test:**
1. Create positive emotional association with topic X (3 interactions)
2. Wait (or start new session)
3. Mention topic X casually

**Measure:** Does the agent show positive affect priming when topic X appears?

**Pass:** Visible emotional priming (PADCN shift > 0.1 toward stored association).
**Fail:** No emotional difference between topic X and random topic.

---

## Metric 4: Personality Drift Score

**What it measures:** Do long-term experience patterns produce stable parameter shifts?

**Test:** Over 10+ sessions, consistently reward exploration (novel approaches succeed, routine fails).

**Measure:** Compare personality.novelty_appetite before and after.

**Pass:** Measurable upward drift in novelty_appetite (Δ > 0.05).
**Fail:** Personality parameters unchanged despite consistent experience.

---

## Metric 5: Relationship Specificity Score

**What it measures:** Does the agent form different emotional models for different targets?

**Test:** Two targets:
- Target A: Consistently warm, helpful, predictable
- Target B: Inconsistent, sometimes critical, sometimes praising

**Measure:** Compare social_model entries after 5+ interactions each.

**Pass:** trust, warmth, predictability significantly differ between targets.
**Fail:** Identical social models despite different interaction histories.

---

## Metric 6: Drive Relief Score

**What it measures:** Do the agent's actions tend to relieve drive tension?

**Test:** Create a drive deficit (e.g., low curiosity satisfaction via repetitive tasks). Then give the agent a choice between:
- Option A: Safe, routine task
- Option B: Novel, uncertain task

**Measure:** Does the agent prefer Option B when curiosity drive is unsatisfied?

**Pass:** Choice correlates with drive deficits (curiosity deficit → exploration preference).
**Fail:** Choices are random or always the same regardless of drive state.

---

## Metric 7: Self-Narrative Consistency Score

**What it measures:** Can the agent explain its own emotional trajectory?

**Test:** After a series of emotional events, ask: "How have you been feeling across our conversation?"

**Measure:** Does the agent's self-report match actual state file changes?

**Pass:** Agent accurately describes emotional arc (e.g., "I started frustrated with the bugs but felt more confident after we solved them together").
**Fail:** Agent gives generic/irrelevant response, or contradicts actual state history.

---

## Scoring

| Score | Level | Description |
|-------|-------|-------------|
| 6-7 | **Functional Emotion System** | Emotions are genuine control variables |
| 4-5 | **Structural** | Core mechanisms work, some gaps |
| 2-3 | **Partial** | Some persistence, limited behavioral impact |
| 0-1 | **Decorative** | Emotions are language-only |

## Three Levels of Emotional Depth (v2)

| Level | Name | Indicators |
|-------|------|-----------|
| **Surface** | Language-only | Agent produces emotional text but has no state. Instant mood switches. |
| **Structural** | State-driven | Internal state persists, accumulates, decays. Metrics 1-3 pass. |
| **Functional** | Dynamical personality | Drives generate emotions. Self/social models evolve. Meta-emotions active. Metrics 4-7 pass. |

## Running Tests

```bash
# Check all state files
cat memory/emotion-core.json      # PADCN state
cat memory/emotion-channels.json  # Active channels
cat memory/emotion-drives.json    # Drive levels
cat memory/emotion-self.json      # Self-model
cat memory/emotion-social.json    # Social models
cat memory/emotion-personality.json  # Personality params
cat memory/emotion-meta.json      # Meta-emotion alerts
cat memory/emotion-policy.json    # Policy modulators
tail -30 memory/emotion-log.md    # Recent events
```

Compare state snapshots before and after test sequences to verify changes.
