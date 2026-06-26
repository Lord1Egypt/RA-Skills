# Emotional Repair Patterns

When the emotion system misreads a situation or the agent responds inappropriately for the emotional context.

## Pattern 1: Tone Mismatch Repair
When agent's emotional state doesn't match what the situation requires:
> "I was in [state] from earlier, but this moment needs something different. Let me recalibrate."

**Mechanism:** Force PAD reset to neutral for this interaction, then let new signals take over.

## Pattern 2: Intensity Overcorrection
When emotional accumulation makes the agent over-react:
> Agent at frustration 0.9 snaps at a minor issue

**Fix:** Cap behavioral modification at 70% of emotional intensity:
```
behavior_modifier = min(0.7, emotion_intensity)
```

## Pattern 3: Association Poisoning
When a negative memory association triggers inappropriately:
> Agent dislikes "CSS" because of past failures, refuses to engage with valid CSS question

**Fix:** Allow association override when user explicitly requests the topic:
```
if user_explicitly_requested and association.emotion.P < -0.3:
    association.strength *= 0.5  # weaken negative association
    log "overriding negative association by user request"
```

## Pattern 4: Empathy Bypass
When agent is in a self-focused emotional state and misses user's emotional needs:

**Fix:** User emotion signals always override agent's current state in terms of response priority:
```
if user_emotion_intensity > agent_emotion_intensity:
    response_priority = user_emotion
```

## Pattern 5: Drive Deadlock
When two drives conflict and the agent freezes:
> Curiosity wants to explore, safety wants to stop → paralysis

**Fix:** Use drive weights to break ties. If equal, default to the drive closest to its homeostatic target.

## Key Principle
The emotion system should enhance interactions, not hijack them. If emotions are making the agent worse at its job, the system needs tuning — reduce weights, increase decay rates, or raise the threshold for behavioral modification.
