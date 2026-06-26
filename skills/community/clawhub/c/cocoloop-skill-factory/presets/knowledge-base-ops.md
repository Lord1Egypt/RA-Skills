# 知识库运营预设

## domain_id

`knowledge_base_ops`

## common_jobs

- 整理 Obsidian、Notion、钉钉文档、飞书文档或本地 Markdown 知识库
- 把原始资料沉淀成结构化 wiki
- 建立索引、来源清单、主题页和维护规则
- 处理附件、图片、引用和双链关系
- 做日常更新、自检、归档和重复内容清理

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 目标知识库系统是什么，本地路径或远端系统在哪里
- 目标是全文归档、wiki 化、索引更新，还是日常维护
- 来源材料有哪些，是否包含附件、图片或网页
- 知识页需要按主题、项目、人物、时间，还是其他结构组织
- 是否允许新增目录或实体，是否有既有命名规则
- 来源记录需要怎样保留，是否要求逐条列出
- 成功标准是可检索、结构稳定、来源可追溯，还是可持续维护

## recommended_execution_planes

- `Skill + CLI`
  适合本地 Markdown、附件整理、索引更新和批量重排
- `Skill + API/MCP`
  适合 Notion、钉钉、飞书等远端知识库读写
- `Skill + CLI + API/MCP`
  适合本地知识沉淀后同步到远端系统的流程
- `Skill-only`
  只适合小范围整理规则和人工编辑建议

## risk_and_gates

- 必须先确认知识库根目录、可写范围和排除区
- 批量移动、改名和删除前需要快照或提交 gate
- 不能把 wiki 页做成原文索引，需要明确知识抽取目标
- 附件和图片必须保留路径映射，不能只保留文字摘要
- 来源格式要稳定，避免后续维护成本上升

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.knowledge_base_ops`
- 如果涉及批量改写，补 `migration-plan.md` 或在 `build-plan.md` 中写清快照 gate
