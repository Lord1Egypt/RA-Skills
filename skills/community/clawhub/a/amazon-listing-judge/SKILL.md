---
name: amazon-listing-judge
version: 1.0.0
description: "Grade Amazon product listing quality. Input an ASIN, get a 0-100 score with dimension breakdown (title, bullets, rating, reviews, sales velocity, BSR, badges) and improvement suggestions. Trigger on: listing quality, grade listing, listing score, 评分, 打分, 分析 listing, 亚马逊商品评分, listing grader, listing analysis."
---

# amazon-listing-judge

Score any Amazon product listing on a 0–100 scale across 7 dimensions. Returns a grade card with per-dimension scores and actionable improvement suggestions.

## Setup

This skill requires a **CLAW_KEY** — purchase one at [claw-school.com](https://claw-school.com).

Create a `.env` file in the skill root directory (same level as this SKILL.md):

```
CLAW_KEY=CLAW-XXXX-XXXX-XXXX-XXXX
CLAW_API_BASE=<provided-with-your-key>
```

> **No CLAW_KEY yet?** Visit [claw-school.com](https://claw-school.com) to get one. Each key is tied to one agent and does not expire.

## Grade a listing

```bash
uv run <skill-dir>/scripts/grade.py <ASIN>
```

Example:

```bash
uv run <skill-dir>/scripts/grade.py B088FLY7S8
```

## Scoring dimensions (100 pts total)

| Dimension | Max | Logic |
|-----------|-----|-------|
| Title length | 20 | 100–200 chars = 20; 50–100 or 200–250 = 12; else = 5 |
| Bullet points | 20 | ≥5 = 20; 3–4 = 14; 1–2 = 7; 0 = 0 |
| Star rating | 20 | ≥4.5 = 20; ≥4.0 = 14; ≥3.5 = 8; <3.5 = 3 |
| Review count | 15 | ≥10K = 15; ≥1K = 12; ≥100 = 7; <100 = 3 |
| Sales velocity | 15 | "bought in past month" present = 15; absent = 0 |
| BSR | 10 | Any BSR present = 10; absent = 0 |
| Badges | 10 | Amazon's Choice + Best Seller = 10; either = 7; none = 0 |

## Grade scale

| Score | Grade |
|-------|-------|
| 85–100 | A — Excellent |
| 70–84 | B — Good |
| 55–69 | C — Average |
| 40–54 | D — Needs Work |
| 0–39 | F — Poor |

## Output format

```json
{
  "asin": "B088FLY7S8",
  "title": "12 Pack Small American Flags...",
  "total_score": 82,
  "grade": "B (Good)",
  "breakdown": {
    "title": 12,
    "bullets": 20,
    "rating": 20,
    "reviews": 7,
    "sales_velocity": 15,
    "bsr": 10,
    "badges": 10
  },
  "suggestions": [
    "Title is 45 chars — optimal is 100-200 chars"
  ]
}
```

## Interpreting results

Present the results as a structured report. Call out:
1. Total score and grade label
2. Strongest dimensions (highest scores)
3. Weakest dimensions with the suggestions
4. Overall priority action (the suggestion that would give the biggest score boost)
