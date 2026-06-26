# 文档检索与研究预设

## domain_id

`docs_research`

## common_jobs

- 查询官方文档
- 整理产品或 API 资料
- 输出带引用的研究摘要
- 形成知识沉淀或 Notion 型资料

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 当前问题是否强依赖最新资料
- 是否必须优先官方来源
- 是否需要引用、链接或证据指针
- 是一次性回答，还是要形成可复用研究产物
- 是否已有固定知识库或外部文档系统

## recommended_execution_planes

- `Skill + Docs MCP/API`
  适合官方文档、SDK、标准和规范查询
- `Skill + 搜索 + 文档产物`
  适合形成研究摘要和参考分析
- `Skill-only`
  只适合收口已有资料，不适合时效性研究

## risk_and_gates

- 时效性问题必须优先官方来源
- 需要引用时不能只给结论
- 搜索受限时必须把缺口写进 `open_gaps`
- 要区分事实结论和推断结论

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须保留 `research_evidence`
