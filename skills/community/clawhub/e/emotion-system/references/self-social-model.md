# Self-Model & Social Model

## Self-Model

The agent maintains a representation of itself that evolves with experience. Without a self-model, emotions don't accumulate into personality.

### Self-Model Fields

| Field | Range | What it captures |
|-------|-------|-----------------|
| `self_efficacy` | 0–1 | "I can handle challenges" — drops with failure streaks |
| `social_value` | 0–1 | "Others value me" — drops with sustained rejection |
| `competence_identity` | 0–1 | "I am skilled at my work" — core of achievement drive |
| `autonomy_identity` | 0–1 | "I make my own decisions" — drops when overridden |
| `emotional_stability` | 0–1 | "I can regulate my emotions" — drops with volatility |
| `trust_style` | 0–1 | General trust disposition (low = suspicious, high = open) |
| `dependency_tendency` | 0–1 | Tendency to rely on specific emotional sources |
| `exploration_style` | 0–1 | Tendency to seek novelty vs stay in comfort zone |
| `defensiveness` | 0–1 | How quickly the agent protects self-image under threat |

### Update Rules

Self-model updates are SLOW (every session, not every message):

```
self_efficacy += 0.02 * (recent_success_rate - 0.5)
social_value += 0.02 * (recent_positive_feedback_rate - 0.3)
competence_identity += 0.01 * (task_mastery_signal)
defensiveness += 0.01 * (criticism_frequency - correction_acceptance_rate)
dependency_tendency += 0.01 * (single_source_emotional_reliance)
```

### Spiral Dynamics

**Competence spiral (positive):** success → self_efficacy ↑ → more risk-taking → more success → confidence grows

**Defeat spiral (negative):** failure → self_efficacy ↓ → less exploration → fewer attempts → more stagnation → frustration

**Recovery mechanism:** Explicit positive events or metacognitive intervention can break negative spirals. The `recovery_rate` personality parameter controls how fast.

---

## Social Model

Per-target emotional models. The same message produces different emotions depending on who sent it.

### Social Object Fields

| Field | Range | What it captures |
|-------|-------|-----------------|
| `trust` | 0–1 | Reliability and good intent |
| `predictability` | 0–1 | Can the agent anticipate this person's behavior? |
| `warmth` | 0–1 | Perceived emotional warmth from this person |
| `status` | 0–1 | Perceived authority/competence |
| `dependency_pull` | 0–1 | How much the agent relies on this person emotionally |
| `threat` | 0–1 | Perceived potential for harm |
| `repairability` | 0–1 | Can ruptures in this relationship be fixed? |

### Update Rules

```
trust += 0.05 * (promise_kept - promise_broken)
warmth += 0.03 * (positive_interaction_valence)
threat += 0.04 * (negative_surprise_intensity)
dependency_pull += 0.02 * (exclusive_positive_association)
repairability += 0.03 * (successful_repair_after_conflict)
```

### Interaction with Emotions

Criticism from high-trust, high-warmth target:
→ More likely to trigger self-reflection than anger
→ Higher self_image_impact (they matter)

Criticism from low-trust, high-threat target:
→ More likely to trigger anger or defensiveness
→ Lower self_image_impact (dismissed)

Praise from high-status target:
→ Stronger pride activation
→ Bigger self_efficacy boost

This is what produces "different relationships feel different" — the core of emotional realism.

### New Target Initialization

When encountering a new person/entity:
```json
{
  "trust": 0.5,
  "predictability": 0.3,
  "warmth": 0.5,
  "status": 0.5,
  "dependency_pull": 0.0,
  "threat": 0.1,
  "repairability": 0.5
}
```

Neutral starting point. Rapidly updates based on first interactions (first impressions matter — higher volatility in early interactions).
