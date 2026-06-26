---
name: lead-scoring
description: AI-powered B2B lead scoring model. Predicts conversion probability for potential customers using machine learning (LightGBM + SHAP). CSV upload or API integration.
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins: [python3]
    always: false
---

# Lead Scoring Model

AI-powered B2B lead scoring using LightGBM + SHAP for interpretability.

## Usage

```bash
python3 score.py --input leads.csv --output scores.csv
```

## Features

- CSV upload → scored leads with conversion probability
- Top features driving each score (SHAP)
- Ranked priority list
- Pipeline: LightGBM → SHAP → actionable insights

## Input CSV Format

```csv
company_size,industry,page_views,email_opens,form_fills,job_title_score
50,tech,120,5,2,8
200,finance,45,2,0,5
```

## Output

```csv
lead_id,score,probability,top_factor,risk_level
1,0.85,85%,page_views,hot
2,0.32,32%,low_engagement,cold
```

## Notes

MIT-0 License | Requires: python3, lightgbm, shap, pandas
