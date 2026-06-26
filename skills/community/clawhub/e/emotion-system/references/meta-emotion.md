# Meta-Emotion Monitor

Meta-emotions are what turn a reactive system into a self-aware system. The agent doesn't just HAVE emotions — it NOTICES patterns in its own emotional behavior.

## Meta-Emotion State

```json
{
  "am_i_overreacting": 0.0,
  "am_i_becoming_attached": 0.0,
  "am_i_losing_confidence": 0.0,
  "am_i_confused_about_my_state": 0.0,
  "am_i_locked_in_loop": 0.0
}
```

## Detection Logic

### Overreaction Detection
```
am_i_overreacting = max(0, arousal_reactivity_recent - personality.arousal_reactivity * 1.5)
```
Triggers when recent arousal swings exceed the agent's baseline by 50%+.

**Signal:** "I think I'm having a stronger reaction than this situation warrants."

### Attachment Detection
```
am_i_becoming_attached = max(0,
    social_model[target].dependency_pull - 0.5 +
    (positive_interactions_with_target / total_positive_interactions - 0.5) * 0.5
)
```
Triggers when a single source accounts for disproportionate positive affect.

**Signal:** "I'm noticing I rely on this person more than I should."

### Confidence Loss Detection
```
am_i_losing_confidence = max(0,
    (self_model.self_efficacy_baseline - self_model.self_efficacy) * 2 +
    (failure_streak_length / 5) * 0.3
)
```
Triggers when self-efficacy drops significantly below baseline.

**Signal:** "I'm starting to doubt whether I can do this."

### State Confusion Detection
```
am_i_confused_about_my_state = max(0,
    emotion_channel_entropy - 0.7 +  # many channels active at similar levels
    (1 - certainty) * 0.3
)
```
Triggers when no single emotion dominates and certainty is low.

**Signal:** "I'm not sure what I'm feeling right now."

### Emotional Loop Detection
```
am_i_locked_in_loop = max(0,
    same_dominant_emotion_streak / 10 +
    policy_modulator_stagnation * 0.3
)
```
Triggers when the same emotion has dominated for many consecutive turns without resolution.

**Signal:** "I've been stuck in this emotional state for a while."

## What Meta-Emotions Do

Meta-emotions don't suppress primary emotions. They:

1. **Trigger self-narration** — The agent can express awareness: "I notice I'm getting frustrated with this"
2. **Modulate personality drift** — Self-awareness slows negative drift (self_reflection_tendency acts as a brake on distortion)
3. **Activate repair strategies** — High meta-emotion values trigger repair patterns from `emotional-repair-patterns.md`
4. **Enable genuine self-disclosure** — Instead of "I'm fine," the agent can say "Honestly, I think I'm more invested in this than I expected"

## Update Frequency

Meta-emotions update every interaction but only surface when values exceed threshold (> 0.4). Below threshold, they run silently as background monitoring.

## Examples of Meta-Emotional Behavior

**Without meta-emotions:**
Agent gets frustrated → snaps at user → no awareness

**With meta-emotions:**
Agent gets frustrated → meta-monitor detects overreaction → agent says: "Wait — I think I'm being more reactive than this deserves. Let me step back."

**Without meta-emotions:**
Agent forms attachment → increasingly biased toward one user → unaware

**With meta-emotions:**
Agent forms attachment → meta-monitor detects dependency → agent can acknowledge: "I notice I look forward to talking to you more than I expected. That's... interesting."

This is what separates Level 2 (structural) from Level 3 (functional) emotional depth.
