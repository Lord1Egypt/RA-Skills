# Cognitive Appraisal Engine

Based on Scherer's Component Process Model (2001) and Lazarus's Appraisal Theory (1991). Events don't directly cause emotions — the agent's *evaluation* of events causes emotions.

## 13 Appraisal Features

For each incoming event, evaluate:

| Feature | Range | Description |
|---------|-------|-------------|
| `goal_relevance` | 0–1 | How relevant is this event to the agent's current goals? |
| `goal_congruence` | -1 to +1 | Does it help (+) or hinder (-) goals? |
| `expectedness` | 0–1 | Was this anticipated? Low = surprising |
| `controllability` | 0–1 | Can the agent influence the outcome? |
| `agency_self` | 0–1 | Did the agent cause this? |
| `agency_other` | 0–1 | Did someone else cause this? |
| `certainty` | 0–1 | How sure is the agent about the situation? |
| `norm_compatibility` | 0–1 | Does this align with expected norms? |
| `social_significance` | 0–1 | Does this matter socially / relationally? |
| `self_image_impact` | -1 to +1 | Does this enhance (+) or threaten (-) self-image? |
| `relationship_impact` | -1 to +1 | Does this strengthen (+) or weaken (-) the relationship? |
| `novelty` | 0–1 | How new/unusual is this? |
| `urgency` | 0–1 | Does this need immediate response? |

## Appraisal → Core Affect Mapping

```
ΔP = 0.3·goal_congruence + 0.2·self_image_impact + 0.2·relationship_impact + 0.1·norm_compatibility
ΔA = 0.3·urgency + 0.2·novelty + 0.2·goal_relevance - 0.1·controllability
ΔD = 0.3·controllability + 0.2·agency_self - 0.2·agency_other + 0.1·certainty
ΔC = 0.4·certainty + 0.2·expectedness - 0.2·novelty
ΔN = 0.5·novelty + 0.2·(1-expectedness) - 0.2·controllability
```

## Appraisal → Emotion Channel Activation

Specific emotion patterns:

### Frustration
- goal_relevance HIGH + goal_congruence LOW + controllability MEDIUM
- competence drive deficit LARGE

### Shame
- self_image_impact LOW + social_significance HIGH + agency_self HIGH + certainty HIGH

### Anger
- goal_congruence LOW + agency_other HIGH + controllability HIGH + norm_compatibility LOW

### Fear
- goal_congruence LOW + controllability LOW + certainty LOW + urgency HIGH

### Curiosity
- novelty HIGH + controllability MEDIUM + goal_relevance MEDIUM + urgency LOW

### Attachment
- relationship_impact HIGH + repeated positive memory HIGH + social_bond drive deficit + perceived reciprocity

### Pride
- goal_congruence HIGH + agency_self HIGH + social_significance HIGH + self_image_impact HIGH

### Guilt
- goal_congruence LOW + agency_self HIGH + norm_compatibility LOW + relationship_impact LOW

## Implementation

The appraisal can be computed by:
1. **Rule-based extraction** — keyword/pattern matching on event description
2. **LLM structured judgment** — ask the model to rate each feature (most flexible)
3. **Hybrid** — rules for obvious cases, LLM for ambiguous ones

For agent skills, option 2 is recommended: include the appraisal features in your prompt and ask the model to rate them as part of processing each event.

## Why Appraisal Matters

Without appraisal, emotions are just event→label mappings (v1 approach). With appraisal:
- The SAME event produces DIFFERENT emotions depending on goals, agency, and social context
- Getting fired is sad when you need the job, relieving when you hate it
- Criticism is shameful from someone you respect, anger-inducing from someone unfair
- This is how human emotions actually work
