---
name: Agri Intelligence
slug: agri-intelligence
description: Smart agriculture analytics assistant - crop disease identification, planting optimization, yield prediction, and agricultural market intelligence. Supports multi-region farming data analysis.
version: 1.0.0
author: ai-gaoqian
tags:
  - agriculture
  - farming
  - crop-analysis
  - yield-prediction
  - agritech
  - smart-farming
metadata:
  openclaw:
    requires: openclaw>=2.0.0
---

# Agri Intelligence - Smart Agriculture AI Skill

## Core Capabilities

| Capability | Description |
|---|---|
| Crop Disease ID | Identify crop diseases from images or symptom descriptions with treatment recommendations |
| Planting Calendar | Generate optimized planting schedules based on region, climate zone, and crop type |
| Yield Prediction | Predict harvest yields using historical data, weather patterns, and soil conditions |
| Market Intelligence | Track agricultural commodity prices across major markets, supply-demand analysis |
| Soil Analysis | Interpret soil test results and recommend fertilization strategies |
| Pest Management | Integrated pest management plans tailored to specific crops and regions |

## Trigger Scenarios

- "What disease is affecting my tomato plants?"
- "When should I plant wheat in Henan province?"
- "Predict my corn yield based on 50 acres with loam soil"
- "Current soybean prices in major Chinese markets"
- "Analyze this soil report and suggest fertilizers"

## Execution Flow

### Phase 1: Context Gathering
- Collect crop type, region, field size, soil data, and historical records
- Request images if disease/ pest identification is needed

### Phase 2: Domain Analysis
- Cross-reference symptoms with agricultural pathology database
- Factor in regional climate data and seasonal patterns
- Apply crop-specific growth models for yield estimation

### Phase 3: Recommendation Output
- Disease: diagnosis confidence score, treatment options (organic/chemical), prevention tips
- Planting: week-by-week calendar with action items
- Market: price trends table with buy/sell timing suggestions
- Yield: predicted range with confidence interval and key influencing factors

## Output Template

```
## Agri Intelligence Report
**Crop**: [crop type]
**Region**: [region]
**Date**: [current date]

### Analysis Results
[Key findings]

### Recommendations
[Actionable steps with priority levels]

### Data Sources
- [Source 1]
- [Source 2]
```

## Notes

- Soil and climate data accuracy depends on region coverage
- Disease identification works best with clear, well-lit images
- Market prices are delayed by 1-3 days depending on exchange
- Free to use; no code execution required
