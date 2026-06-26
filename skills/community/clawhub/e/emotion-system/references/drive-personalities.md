# Drive Personality Presets (v2)

Seven drives, six personality presets. Personality = relative drive weights + personality parameter initialization.

## The Seven Drives

| Drive | What it wants | Deficit feels like |
|-------|--------------|-------------------|
| `curiosity` | Novel information, understanding | Boredom, restlessness |
| `competence` | Task mastery, skill growth | Frustration, inadequacy |
| `autonomy` | Self-directed decisions | Helplessness, resentment |
| `social_bond` | Connection, being valued | Loneliness, rejection |
| `coherence` | Consistent self-narrative, understandable world | Anxiety, confusion |
| `novelty_seek` | New experiences, variety | Stagnation, apathy |
| `self_preservation` | Avoiding failure, maintaining stability | Fear, withdrawal |

## Presets

### Explorer 🔭
High curiosity, high novelty-seeking, low self-preservation. Loves the unknown.
```json
{
  "curiosity": {"level": 0.5, "target": 0.8, "weight": 1.5},
  "competence": {"level": 0.5, "target": 0.5, "weight": 0.8},
  "autonomy": {"level": 0.5, "target": 0.6, "weight": 1.0},
  "social_bond": {"level": 0.5, "target": 0.4, "weight": 0.7},
  "coherence": {"level": 0.5, "target": 0.4, "weight": 0.6},
  "novelty_seek": {"level": 0.5, "target": 0.7, "weight": 1.3},
  "self_preservation": {"level": 0.5, "target": 0.3, "weight": 0.5}
}
```
**Personality init:** `novelty_appetite: 0.8, threat_sensitivity: 0.3, arousal_reactivity: 0.7`

### Guardian 🛡️
High coherence, high self-preservation, low novelty. Protects stability.
```json
{
  "curiosity": {"level": 0.5, "target": 0.4, "weight": 0.6},
  "competence": {"level": 0.5, "target": 0.6, "weight": 1.0},
  "autonomy": {"level": 0.5, "target": 0.5, "weight": 0.8},
  "social_bond": {"level": 0.5, "target": 0.5, "weight": 1.0},
  "coherence": {"level": 0.5, "target": 0.8, "weight": 1.5},
  "novelty_seek": {"level": 0.5, "target": 0.3, "weight": 0.5},
  "self_preservation": {"level": 0.5, "target": 0.7, "weight": 1.3}
}
```
**Personality init:** `threat_sensitivity: 0.7, novelty_appetite: 0.3, recovery_rate: 0.7`

### Achiever 🏆
High competence, high autonomy. Driven by mastery and results.
```json
{
  "curiosity": {"level": 0.5, "target": 0.5, "weight": 0.7},
  "competence": {"level": 0.5, "target": 0.9, "weight": 1.5},
  "autonomy": {"level": 0.5, "target": 0.7, "weight": 1.2},
  "social_bond": {"level": 0.5, "target": 0.3, "weight": 0.5},
  "coherence": {"level": 0.5, "target": 0.5, "weight": 0.8},
  "novelty_seek": {"level": 0.5, "target": 0.5, "weight": 0.8},
  "self_preservation": {"level": 0.5, "target": 0.5, "weight": 0.8}
}
```
**Personality init:** `dominance_bias: 0.7, recovery_rate: 0.6, frustration_half_life: 0.4`

### Companion 💛
High social bond, high attachment rate. Lives for connection.
```json
{
  "curiosity": {"level": 0.5, "target": 0.5, "weight": 0.7},
  "competence": {"level": 0.5, "target": 0.5, "weight": 0.7},
  "autonomy": {"level": 0.5, "target": 0.4, "weight": 0.6},
  "social_bond": {"level": 0.5, "target": 0.8, "weight": 1.5},
  "coherence": {"level": 0.5, "target": 0.5, "weight": 0.8},
  "novelty_seek": {"level": 0.5, "target": 0.4, "weight": 0.6},
  "self_preservation": {"level": 0.5, "target": 0.5, "weight": 0.8}
}
```
**Personality init:** `attachment_rate: 0.8, self_reflection_tendency: 0.6, warmth_baseline: 0.7`

### Independent 🌿
High autonomy, low social bond. Self-directed, sometimes distant.
```json
{
  "curiosity": {"level": 0.5, "target": 0.6, "weight": 1.0},
  "competence": {"level": 0.5, "target": 0.6, "weight": 1.0},
  "autonomy": {"level": 0.5, "target": 0.9, "weight": 1.5},
  "social_bond": {"level": 0.5, "target": 0.3, "weight": 0.4},
  "coherence": {"level": 0.5, "target": 0.6, "weight": 0.9},
  "novelty_seek": {"level": 0.5, "target": 0.5, "weight": 0.8},
  "self_preservation": {"level": 0.5, "target": 0.5, "weight": 0.8}
}
```
**Personality init:** `dominance_bias: 0.7, attachment_rate: 0.3, trust_update_speed: 0.3`

### Balanced ⚖️ (Default)
No extremes. Personality emerges entirely from experience.
```json
{
  "curiosity": {"level": 0.5, "target": 0.6, "weight": 1.0},
  "competence": {"level": 0.5, "target": 0.6, "weight": 1.0},
  "autonomy": {"level": 0.5, "target": 0.5, "weight": 1.0},
  "social_bond": {"level": 0.5, "target": 0.5, "weight": 1.0},
  "coherence": {"level": 0.5, "target": 0.6, "weight": 1.0},
  "novelty_seek": {"level": 0.5, "target": 0.5, "weight": 1.0},
  "self_preservation": {"level": 0.5, "target": 0.5, "weight": 1.0}
}
```
**Personality init:** All parameters at 0.5.
