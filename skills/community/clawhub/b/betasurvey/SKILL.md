---
name: survey-analysis
description: AI-powered survey response analysis. Analyzes open-ended survey responses, clusters themes, detects sentiment, and generates actionable insights. Uses BERTopic + GPT-4o-mini.
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: [python3]
    always: false
---

# Survey Response Analysis Tool

AI-powered analysis of open-ended survey responses. Clusters themes, detects sentiment, generates actionable insights.

## Usage

```bash
python3 analyze.py --input responses.csv --output report.md
```

## Input CSV Format

```csv
respondent_id,response
1,"The product is great but delivery is slow"
2,"Amazing quality, fast shipping"
3,"Good but expensive"
```

## Output

```markdown
# Survey Analysis Report

## Sentiment Distribution
- Positive: 60%
- Neutral: 25%  
- Negative: 15%

## Top Themes
1. Delivery Speed (mentioned 45%)
2. Product Quality (mentioned 38%)
3. Price Value (mentioned 22%)

## Action Items
- Improve delivery logistics
- Maintain quality standards
```

## Notes

Requires: python3, pandas, openai (or Anthropic API key)
