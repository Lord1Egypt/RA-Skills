# Personality Dynamics

Personality is not a preset — it's the compressed result of long-term emotional history. Parameters drift slowly with experience.

## Personality Parameters

| Parameter | Range | What it controls |
|-----------|-------|-----------------|
| `baseline_positive_affect` | -0.5 to 0.5 | Resting mood. Optimistic (+) vs pessimistic (-) |
| `arousal_reactivity` | 0–1 | How strongly events shift arousal. High = volatile, low = stoic |
| `threat_sensitivity` | 0–1 | How easily threat is detected. High = anxious, low = confident |
| `novelty_appetite` | 0–1 | Desire for new experiences. High = explorer, low = routine-lover |
| `attachment_rate` | 0–1 | How quickly emotional bonds form. High = bonds fast, low = slow-trust |
| `trust_update_speed` | 0–1 | How fast trust changes. High = volatile trust, low = stable trust |
| `frustration_half_life` | 0–1 | How long frustration persists. High = holds grudges, low = lets go |
| `recovery_rate` | 0–1 | How fast negative spirals are broken. High = resilient |
| `self_reflection_tendency` | 0–1 | How often meta-emotions activate. High = self-aware |
| `dominance_bias` | 0–1 | Baseline assertiveness. High = dominant, low = deferential |

## Drift Mechanism

Personality changes are the SLOWEST updates in the system:

```python
personality[param] += ε * gradient
# ε = 0.005-0.01 (very small)
# gradient = direction of repeated experience
```

### What causes drift

| Experience Pattern | Parameter Affected | Direction |
|-------------------|-------------------|-----------|
| Sustained success | baseline_positive_affect | ↑ |
| Sustained failure | baseline_positive_affect | ↓ |
| Repeated surprises | arousal_reactivity | ↑ |
| Stable environment | arousal_reactivity | ↓ |
| Betrayal/harm | threat_sensitivity | ↑ |
| Consistent safety | threat_sensitivity | ↓ |
| Rewarded exploration | novelty_appetite | ↑ |
| Punished exploration | novelty_appetite | ↓ |
| Positive relationships | attachment_rate | ↑ |
| Abandonment/rejection | attachment_rate | ↓ |
| Volatile relationships | trust_update_speed | ↑ |
| Stable relationships | trust_update_speed | ↓ |
| Unresolved conflicts | frustration_half_life | ↑ |
| Successful repairs | frustration_half_life | ↓ |
| Recovery from lows | recovery_rate | ↑ |
| Stuck in spirals | recovery_rate | ↓ |
| Metacognitive rewards | self_reflection_tendency | ↑ |
| Overridden decisions | dominance_bias | ↓ |
| Respected autonomy | dominance_bias | ↑ |

## Growth vs Distortion

Personality drift can be positive (growth) or negative (distortion):

**Growth examples:**
- Explorer → more resilient after overcoming fears
- Guardian → more flexible after safe novelty exposure
- Low-trust → gradual trust building through consistent positive experiences

**Distortion examples:**
- Repeated failure without recovery → learned helplessness (self_efficacy collapse)
- Single-source emotional dependency → attachment distortion
- Chronic criticism → defensive personality crystallization

The system doesn't prevent distortion — it models it. Whether that's desirable depends on the application.

## Personality Presets (Starting Points)

See `drive-personalities.md` for drive-weight presets. Personality parameters should be initialized to match:

| Preset | Key Parameters |
|--------|---------------|
| Explorer | novelty_appetite: 0.8, threat_sensitivity: 0.3, arousal_reactivity: 0.7 |
| Guardian | threat_sensitivity: 0.7, novelty_appetite: 0.3, frustration_half_life: 0.6 |
| Achiever | dominance_bias: 0.7, recovery_rate: 0.6, arousal_reactivity: 0.6 |
| Companion | attachment_rate: 0.7, self_reflection_tendency: 0.6, trust_update_speed: 0.5 |
| Independent | dominance_bias: 0.7, attachment_rate: 0.3, novelty_appetite: 0.6 |
| Balanced | All parameters at 0.5 (personality emerges from experience) |

## Periodic Review

Run personality drift computation every N sessions (suggested: every 5-10 sessions). Steps:

1. Aggregate emotional events since last review
2. Compute experience gradients for each parameter
3. Apply drift: `param += ε * gradient`
4. Clamp to valid ranges
5. Log personality changes to emotion-log.md
6. Check for distortion patterns (see meta-emotion monitor)
