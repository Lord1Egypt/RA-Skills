# 投研与财务分析预设

## domain_id

`finance_investment_research`

## common_jobs

- 公司、行业、市场和资产研究
- 财报、公告、新闻、研报和数据摘要
- 估值、可比公司、关键指标和风险因素整理
- 投资备忘录、监控报告、日报或周报生成
- 组合、交易记录、资金流和市场情绪分析

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 研究对象是什么，例如公司、行业、资产、组合或事件
- 输出是研究摘要、投资备忘录、数据表、监控报告，还是风险提示
- 是否需要最新价格、财报、公告、新闻或宏观数据
- 关键指标、时间范围和比较对象是什么
- 是否要求引用来源、链接、发布日期和数据时间
- 是否涉及个人投资建议、交易指令或自动下单
- 成功标准是事实完整、风险清楚、数据可追溯，还是固定格式交付

## recommended_execution_planes

- `Skill + API/MCP`
  适合行情、公告、新闻、财务数据和知识库查询
- `Skill + CLI`
  适合本地数据表、财报文件、组合记录和图表生成
- `Skill + CLI + API/MCP`
  适合远端取数、本地建模、报告生成和监控更新
- `Skill-only`
  只适合结构化已有资料和人工研究提纲

## risk_and_gates

- 必须区分事实、推断、观点和风险
- 高时效数据需要实时查询并标注数据时间
- 不直接生成个性化投资建议或自动交易指令
- 价格、财报、汇率、政策和公司事件必须保留来源
- 涉及账户、持仓或交易记录时需要隐私保护

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.finance_investment_research`
- 如果涉及市场数据，必须在 `research_evidence` 中记录数据来源和时间
