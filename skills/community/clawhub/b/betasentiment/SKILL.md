---
name: sentiment-analyzer
description: Analyzes sentiment from social media, news headlines, and financial text. Outputs positive/negative/neutral scores with confidence levels and key phrase extraction.
metadata:
  openclaw:
    emoji: "💬"
    requires:
      bins: [python3]
    always: false
---

# Sentiment Analyzer

AI-powered sentiment analysis for financial text, social media, and news.

## Usage

```bash
python3 analyze.py --text "Bitcoin to the moon! Best investment ever!"
python3 analyze.py --file headlines.csv
```

## Output Example

```
🔍 SENTIMENT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━
Text: "Bitcoin to the moon!"
Score: 0.82 / 1.0
Verdict: BULLISH 🐂
Confidence: 91%

Key phrases:
- "to the moon" → extremely bullish signal
- "best investment" → high conviction positive
```
