# Emotional Memory Schema

Four types of emotional memory, each with rich trace structure.

## Memory Types

| Type | What it stores | Example |
|------|---------------|---------|
| `entity_memory` | Feelings about people, tools, objects | "User_42 → warm, trustworthy" |
| `task_memory` | Feelings about task types | "CSS debugging → frustrated, low confidence" |
| `topic_memory` | Feelings about subjects | "AI consciousness → fascinated, high engagement" |
| `situational_memory` | Feelings about patterns/contexts | "Being corrected publicly → shame, defensive" |

## Trace Structure

```json
{
  "id": "uuid",
  "type": "entity_memory",
  "target": "user_42",
  "context_summary": "User helped debug a complex issue patiently",
  "emotion_snapshot": {"P": 0.6, "A": 0.3, "D": 0.2, "C": 0.4, "N": 0.1},
  "channels_snapshot": {"gratitude": 0.7, "trust": 0.6, "attachment": 0.3},
  "appraisal_snapshot": {
    "goal_congruence": 0.8,
    "relationship_impact": 0.7,
    "agency_other": 0.8
  },
  "drive_snapshot": {"social_bond": 0.7, "competence": 0.5},
  "valence": 0.63,
  "intensity": 0.71,
  "confidence": 0.58,
  "repetition_count": 4,
  "first_formed": "2026-03-10",
  "last_updated": "2026-03-12",
  "decay_rate": 0.03,
  "attribution": {
    "self": 0.22,
    "other": 0.64,
    "situation": 0.14
  },
  "generalization_radius": 0.31,
  "volatility": 0.44
}
```

### Key Fields

| Field | Purpose |
|-------|---------|
| `confidence` | Prevents single events from permanently shaping personality. Low confidence = easily overwritten. |
| `generalization_radius` | How far this memory generalizes. Low = specific to exact context. High = applies broadly. |
| `volatility` | How easily new evidence can modify this memory. High = unstable, low = entrenched. |
| `attribution` | Who/what caused the emotional event. Affects whether the feeling generalizes to the person, the agent, or the situation. |
| `repetition_count` | Strengthens with repetition. Core mechanism for preference/aversion formation. |

## Memory Activation

When a new event occurs, retrieve relevant memories:

```
activation = similarity(current_context, memory.context)
           * memory.intensity
           * memory.confidence
           * recency_factor(memory.last_updated)
           * relevance_to_current_goal
```

Activated memories shift current affect:
```
PADCN += Σ(memory.emotion_snapshot * memory.activation * memory.confidence)
```

## Memory Formation Rules

1. **Threshold:** Only form memories when emotion intensity > 0.5
2. **Deduplication:** If a similar memory exists (same target + type), reinforce instead of creating new
3. **Confidence growth:** `confidence = min(1.0, confidence + 0.1 * repetition)`
4. **Volatility decay:** `volatility = max(0.1, volatility - 0.05 * repetition)` — repeated experiences become entrenched
5. **Generalization:** High-confidence memories with high repetition gradually increase generalization_radius

## Emotion Graph Memory (Advanced)

For richer relationship modeling, store edges:

```
User_A --[praised]--> coding_task    (valence: +0.7, trust: 0.8)
User_A --[criticized]--> writing     (valence: -0.3, frustration: 0.5)
Tool_X --[failed]--> repeated        (aversion: 0.6, anxiety: 0.3)
Topic_Y --[success]--> streak        (pride: 0.7, mastery: 0.8)
```

Edge weights: valence, trust, frustration, dependency, mastery.

This produces: different attitudes toward different people, different expectations for different tasks, different trust toward different tools.
