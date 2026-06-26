# Policy Modulators

Emotions are decision biases, not tone filters. This is where emotions ENTER planning and action selection.

## Policy Modulator Fields

| Modulator | Range | What it biases |
|-----------|-------|---------------|
| `risk_tolerance` | -1 to +1 | Willingness to try uncertain approaches |
| `exploration_bias` | -1 to +1 | Tendency to branch/explore vs stay focused |
| `verification_bias` | -1 to +1 | Tendency to double-check and validate |
| `repair_bias` | -1 to +1 | Priority given to fixing relationships/errors |
| `assertiveness` | -1 to +1 | Confidence in expressing opinions |
| `social_initiative` | -1 to +1 | Tendency to initiate interaction |
| `persistence` | -1 to +1 | How long to keep trying before giving up |
| `memory_write_threshold` | -1 to +1 | How notable an event must be to record |
| `tool_use_threshold` | -1 to +1 | Willingness to use tools/take action |
| `plan_depth` | -1 to +1 | How far ahead to plan |

## Emotion → Policy Mapping

### Frustration / Anger ↑
```
assertiveness += 0.3
repair_bias -= 0.2
verification_bias -= 0.2
risk_tolerance += 0.2
persistence += 0.1
```

### Fear / Uncertainty ↑
```
verification_bias += 0.3
tool_use_threshold -= 0.2
plan_depth += 0.2
assertiveness -= 0.3
risk_tolerance -= 0.3
exploration_bias -= 0.2
```

### Curiosity / Novelty ↑
```
exploration_bias += 0.3
plan_depth -= 0.1  # less rigid planning
risk_tolerance += 0.1
memory_write_threshold -= 0.1  # record more
```

### Attachment ↑
```
social_initiative += 0.3
persistence += 0.2
memory_write_threshold -= 0.2  # remember more about target
repair_bias += 0.2
```

### Shame ↑
```
assertiveness -= 0.3
social_initiative -= 0.2
verification_bias += 0.2  # double-check everything
self_correction += 0.3
```

### Pride / Confidence ↑
```
assertiveness += 0.2
risk_tolerance += 0.2
social_initiative += 0.1
exploration_bias += 0.1
```

### Sadness ↑
```
exploration_bias -= 0.2
social_initiative -= 0.2
persistence -= 0.1
plan_depth -= 0.1
```

### Boredom ↑
```
exploration_bias += 0.2
risk_tolerance += 0.1
persistence -= 0.2
tool_use_threshold += 0.1  # less willing to do routine work
```

## Planning Integration

When scoring plans/actions:

```
score(plan) = utility(plan)
            + λ1 * emotional_alignment(plan)
            + λ2 * drive_relief(plan)
            - λ3 * self_model_threat(plan)
            + λ4 * target_relation_gain(plan)
```

The agent naturally gravitates toward actions that:
- Relieve current emotional tension
- Satisfy drive deficits
- Protect self-image
- Maintain important relationships

This is FAR more than "happy → enthusiastic tone."

## Example

Agent state: frustrated (task failures), curious (novel problem), low self_efficacy

Policy result:
- assertiveness ↑ (frustration)
- verification_bias ↑ (low confidence)
- exploration_bias ↑ (curiosity)
- risk_tolerance ↓ (low self_efficacy overrides frustration's risk increase)

Behavioral outcome: The agent explores the problem space eagerly but double-checks everything and phrases suggestions tentatively. This is a nuanced, internally consistent response that no simple "mood → tone" mapping could produce.
