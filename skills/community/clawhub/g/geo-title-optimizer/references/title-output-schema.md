# GEO 标题交付字段

此 schema 是本 Skill 的简化交付约定。它不编码平台猜测或效果承诺。

## `title-candidates.json`

```json
{
  "topic": "主题",
  "audience": "目标读者",
  "evidence": ["来源链接或文件标识"],
  "candidates": [
    {
      "title": "标题文本",
      "reader_need": "目标读者当前要解决的事",
      "claim": "标题向读者承诺什么",
      "supporting_evidence": ["支持该承诺的来源"],
      "scores": {
        "factual_support": 0,
        "audience_relevance": 0,
        "clarity": 0,
        "distinctiveness": 0,
        "platform_fit": 0
      },
      "score_notes": {},
      "selected": false
    }
  ]
}
```

每项分数为 0–5，只用于同一任务的相对比较。`score_notes` 应说明实际理由，不以分数代替数据。

## `title-qa.json`

```json
{
  "selected_title": "标题文本",
  "opening_delivers_claim": true,
  "evidence_complete": true,
  "platform_versions": [
    {"platform": "平台", "length": 0, "limit_status": "budget_unknown", "limit_source": "页面链接或未核实说明"}
  ],
  "status": "SHIP|FIX|BLOCK"
}
```
