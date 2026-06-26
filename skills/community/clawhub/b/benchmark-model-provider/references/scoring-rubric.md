# Scoring Rubric

## Purpose

This file defines the scoring philosophy and default rubric for evaluating benchmarked models.

---

## 1. Measured axes

The benchmark measures four axes:

- quality
- depth
- cost
- speed

Only quality, depth, and cost participate in the default overall score.

---

## 2. Default overall scoring

Default weights:

- quality: 45%
- depth: 35%
- cost: 20%
- speed: excluded from default overall

```text
overall_default =
  0.45 * quality_score +
  0.35 * depth_score +
  0.20 * cost_score
```

---

## 3. Why speed is separate

Speed is still important, but it is affected by reasoning depth, thinking mode, output length, and model behavior. A slower model may still be better for the user if it delivers stronger reasoning.

Therefore:

- always measure speed
- always report speed
- do not include speed in the default overall formula
- allow optional speed inclusion for custom profiles

---

## 4. Per-question scoring

Quality and depth should be scored per question.

Default recommendation:

- quality: 0–10 per question
- depth: 0–10 per question

Raw scores are then aggregated and normalized.

---

## 5. Quality rubric

Score quality based on:

1. Instruction fit
2. Correctness or plausibility
3. Clarity and structure
4. Practical usefulness
5. Immediate usability

### Suggested interpretation

- 0–2: poor / mostly unusable
- 3–4: weak
- 5–6: acceptable
- 7–8: strong
- 9–10: excellent

---

## 6. Depth rubric

Score depth based on:

1. Number of analytical layers
2. Breadth of context integration
3. Comparison / counterpoint ability
4. Ability to go beyond surface-level output
5. Richness of reasoning structure

### Suggested interpretation

- 0–2: shallow
- 3–4: limited
- 5–6: moderate
- 7–8: strong
- 9–10: exceptional depth

---

## 7. Cost scoring

Cost is derived from token usage and pricing data.

Use inverse normalization:

- cheapest model in the comparison set → highest cost score
- most expensive model in the comparison set → lowest cost score

If all models have equal cost, assign a neutral equal cost score to all.

---

## 8. Speed scoring

Speed should be stored and optionally normalized for display, but not included in the default overall score.

Suggested raw metrics:

- total benchmark runtime
- average latency per question
- optional per-question latency

---

## 9. Normalization guidance

Recommended normalization target:

- convert comparison scores to a 0–100 scale

Examples:

- quality raw total → normalized quality score
- depth raw total → normalized depth score
- inverse-normalized cost → cost score
- optional inverse-normalized speed → speed score

---

## 10. Custom profiles

The skill should support profile-specific or user-specific weight overrides.

Examples:

- research-heavy → increase quality and depth weights
- daily lightweight → increase cost weight, optionally include speed
- operations-focused → emphasize quality and responsiveness

---

## 11. Storage rule

Always store:

- raw scores
- normalized scores
- final overall score
- scoring weights used for the run
