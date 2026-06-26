---
name: ai-layoff-radar
description: Detect AI-driven layoffs from global news and generate structured risk reports.
version: 1.0.0
tags:
  - ai
  - layoffs
  - automation
  - news
metadata:
  openclaw:
    requires:
      env:
        - NEWS_API_KEY
    primaryEnv: NEWS_API_KEY
---

# AI Layoff Radar

Detect global layoffs caused by AI adoption, automation rollout, and AI-led efficiency programs.

## When to use this skill

Activate this skill when the user asks to find, summarize, or monitor layoffs linked to AI adoption.

Use it for triggers such as:
- AI layoffs
- automation layoffs
- job cuts caused by AI
- companies replacing workers with AI
- AI efficiency layoffs

## Steps

1. Scan news sources.
2. Extract layoff events.
3. Detect AI-related causality.
4. Generate a structured report.

## Output format

Return JSON with fields:
- `company`
- `date`
- `country`
- `layoff_size`
- `ai_causality_score`
- `summary`

## Example

User query:
`Find recent AI layoffs`

Example JSON response:

```json
{
  "summary": {
    "total_events": 2,
    "top_companies": ["Example Corp", "Sample Systems"]
  },
  "detected_events": [
    {
      "company": "Example Corp",
      "date": "2026-03-04T14:20:00+00:00",
      "country": "USA",
      "layoff_size": 1200,
      "ai_causality_score": 88,
      "summary": "Company announced layoffs after AI automation rollout in customer operations."
    },
    {
      "company": "Sample Systems",
      "date": "2026-03-03T09:10:00+00:00",
      "country": "UK",
      "layoff_size": 350,
      "ai_causality_score": 74,
      "summary": "Job cuts tied to AI efficiency program and workflow automation."
    }
  ]
}
```