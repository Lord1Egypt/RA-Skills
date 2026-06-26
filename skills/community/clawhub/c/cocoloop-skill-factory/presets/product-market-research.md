# 产品与市场研究预设

## domain_id

`product_market_research`

## common_jobs

- 用户访谈、问卷、反馈、评论和竞品资料整理
- 生成用户画像、需求洞察、机会地图和 PRD 输入
- 分析竞品功能、定价、定位、渠道和信息架构
- 把研究材料转成路线图、实验计划或决策简报
- 维护市场监控、用户声音和产品假设清单

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 研究对象是用户、竞品、市场、功能，还是增长渠道
- 输入材料有哪些，例如访谈、问卷、评论、竞品页面、数据或内部文档
- 输出是研究摘要、PRD 输入、竞品矩阵、机会清单，还是路线图建议
- 目标用户、市场范围、时间范围和比较对象是什么
- 是否需要引用来源、截图、链接、数据时间或证据等级
- 是否需要生成表格、PPT、报告页或产品文档
- 成功标准是洞察清楚、证据可追溯、决策可用，还是格式可交付

## recommended_execution_planes

- `Skill-only`
  适合研究框架、访谈提纲、洞察整理和机会清单
- `Skill + CLI`
  适合本地资料整理、评论清洗、表格和报告生成
- `Skill + API/MCP`
  适合产品分析、问卷、知识库、竞品监控和文档系统联动
- `Skill + CLI + API/MCP`
  适合外部资料抓取、本地分析、报告生成和知识库写回

## risk_and_gates

- 必须区分用户原话、数据事实、推断和产品建议
- 竞品资料需要来源、时间和采集方式
- 用户访谈和反馈需要隐私保护
- 产品路线图建议需要保留假设和不确定性
- 视觉报告和 PPT 需要进入 `design_md`

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.product_market_research`
- 如果涉及竞品或用户证据，必须在 `research_evidence` 中保留来源指针
