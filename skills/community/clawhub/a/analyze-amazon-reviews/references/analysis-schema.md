# Semantic analysis JSON contract

## Contents

- Output location
- Final object
- Evidence rules
- Batch partials
- Validation

## Output location

Write the completed semantic analysis to:

```text
RUN_DIR/analysis/final-analysis.json
```

Start from `RUN_DIR/analysis/final-analysis.template.json`. Keep all required arrays even when empty.

## Final object

```json
{
  "schema_version": 1,
  "language": "zh-CN",
  "report_title": "Amazon 评论分析：B08N5KWB9H",
  "executive_summary": [
    {
      "title": "核心结论标题",
      "finding": "只基于评论证据的简洁结论",
      "confidence": "中等",
      "review_ids": ["REVIEW_ID"]
    }
  ],
  "themes": [
    {
      "id": "durability",
      "name": "耐用性",
      "category": "quality",
      "summary": "主题的证据化说明",
      "severity": 4,
      "opportunity_score": 82,
      "review_ids": ["REVIEW_ID"],
      "positive_review_ids": [],
      "negative_review_ids": ["REVIEW_ID"],
      "mixed_review_ids": [],
      "neutral_review_ids": [],
      "evidence": [
        {
          "review_id": "REVIEW_ID",
          "quote": "Exact contiguous source quote",
          "interpretation": "该原文为什么能支持主题"
        }
      ],
      "recommendation": "具体且可验证的改进动作"
    }
  ],
  "pain_points": [
    {
      "title": "痛点名称",
      "finding": "表现、影响和边界",
      "review_ids": ["REVIEW_ID"]
    }
  ],
  "positive_drivers": [
    {
      "title": "购买驱动",
      "finding": "用户重视的收益",
      "review_ids": ["REVIEW_ID"]
    }
  ],
  "use_cases": [
    {
      "name": "使用场景",
      "description": "用户、任务和期望结果",
      "review_ids": ["REVIEW_ID"]
    }
  ],
  "listing_gaps": [
    {
      "title": "信息差",
      "finding": "当前预期与实际体验之间的差距",
      "review_ids": ["REVIEW_ID"]
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "owner": "产品 / Listing / 质检 / 客服",
      "action": "动作标题",
      "rationale": "为什么做，以及如何验证",
      "review_ids": ["REVIEW_ID"]
    }
  ],
  "competitor_comparison": [],
  "limitations": [
    "本报告基于有限、定向抽取的评论样本。"
  ]
}
```

Allowed optional fields may add useful structured detail, but do not remove required fields.

## Evidence rules

- Every `review_id` and every entry in a key ending `_review_ids` must exist in `reviews.jsonl`.
- `themes[].review_ids` must contain every unique review supporting that theme.
- Sentiment ID lists must be subsets of `themes[].review_ids`.
- Never duplicate IDs to inflate mention count.
- Every object containing `quote` must also contain `review_id`.
- `quote` must be a continuous, exact substring of that review's title or content after whitespace and curly-quote normalization.
- Put translations and interpretations outside `quote`.
- Use `severity` only from 1 through 5.
- Use `opportunity_score` only from 0 through 100.
- Use theme IDs matching `[a-z0-9][a-z0-9-]{0,63}` and keep them stable across reports.

## Batch partials

For large runs, save one compact partial per prepared batch under `RUN_DIR/analysis/partials/`. A partial may use the same arrays as the final object but should contain only findings supported by that batch. Include `batch_id` at the top level.

Do not copy full review records into partials. Store IDs, exact short quotes, theme assignments, and concise candidate insights. The final synthesis must merge aliases, deduplicate IDs, and resolve contradictory evidence.

## Validation

Run:

```bash
python3 "$SKILL_DIR/scripts/review_pipeline.py" validate-analysis --run-dir RUN_DIR
```

Validation checks:

- required top-level fields and types;
- unique valid theme IDs;
- valid evidence IDs;
- sentiment-subset integrity;
- severity and opportunity-score ranges;
- exact-quote grounding.

Fix every error before rendering. Review warnings and disclose unavoidable gaps in `limitations`.

