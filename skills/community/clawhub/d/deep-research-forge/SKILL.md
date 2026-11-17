---
name: deep-research-forge
archetype: general
description: 深度研究与决策分析 skill。用于系统研究一个产品、公司、人物、概念、技术、赛道或文化现象，先选择研究方法论组合，再建立研究问题、证据账本、正式状态层级和结论级引用映射，动态组合时间轴、竞品截面、用户选择、生态地图、因果机制、反方证据、场景推演和决策模块；复杂研究可启用多 Agent 并行执行，把来源搜证、时间线、竞品截面、反方证据和决策综合拆成并行研究小队，最后输出研究报告、决策简报、复盘评分或可复用研究资产。用户会说“研究一下”“深度分析”“竞品分析”“帮我搞懂”“横纵分析”“做个 deep research”“多 agent 并行研究”“这个公司/产品/概念是什么来头”“值不值得关注/投入/学习/跟进”等。
---

# Deep Research Forge

这是一个面向 `方法论驱动研究 / 深度研究 / 竞品分析 / 概念溯源 / 决策简报 / 多 Agent 并行研究` 的 skill。

它先建立研究问题和证据账本，再沿时间追踪来路、在当下截面比较同类，并把因果机制、反事实和未来剧本整理成可复用、可更新、可转交的研究资产。

核心原则：方法论决定研究路径，模板只是最后的承载形状。不要先套模板再找内容。

## 核心边界

- 负责：
  - 产品、公司、人物、概念、技术、赛道、文化现象的深度研究
  - 时间轴溯源、竞争截面、同类比较、因果机制、未来剧本
  - 证据账本、来源分级、事实/推测/判断分离
  - 方法论路由、动态输出组合、可插拔研究模块
  - 来源策略、矛盾证据处理、置信度、反转条件和监控清单
  - 政策、标准、考试和认证研究中的正式状态层级判断
  - 复杂课题的多 Agent 并行拆解、角色分工、证据合并与冲突复核
  - 输出研究报告、决策简报、竞品矩阵、学习路线或资料包
  - 对真实调研输出做反向评估、质量评分和 ship / revise / rerun 判断
- 不负责：
  - 简单名词解释
  - 没有证据支撑的观点包装
  - 纯公众号成稿
  - 只做网页摘要或资料搬运
  - 替用户作出医疗、法律、金融等高风险最终决定

如果用户只问“XX 是什么”，先给简明解释；只有上下文暗示要系统摸清来龙去脉、竞争位置或行动判断时，才进入本 skill。

## 使用场景

- 用户要研究一个新产品、公司、开源项目、技术范式或创业赛道。
- 用户要判断一个机会是否值得投入、学习、跟进、购买或对标。
- 用户要做竞品分析，但不想只得到参数表。
- 用户要知道某个人、组织、概念“怎么一步步走到今天”。
- 用户已经有一堆资料，希望整理成结构化报告或决策简报。
- 用户明确要求“多 agent”“并行研究”“分头查证”“research swarm”，或课题天然可拆成来源、时间线、竞品、用户信号、反方证据等互不阻塞的工作流。
- 用户说“横纵分析”“deep research”“帮我摸清楚”“研究一下这个来头”。
- 用户问“这次实测效果如何”“这份调研哪里还不够”“继续怎么优化”。

## 运行路由

先选本轮主模式，只交一个主产物：

- `research-orientation`
  - 研究对象还模糊，先锁研究问题、对象类型、范围、输出形态。
- `evidence-first-deep-dive`
  - 需要完整研究，先建证据账本，再做时间轴、截面对比和交叉洞察。
- `competitive-snapshot`
  - 用户重点问竞品、同类、替代方案、生态位。
- `decision-brief`
  - 用户要 go / hold / no-go、买不买、学不学、投不投入。
- `concept-lineage`
  - 用户研究概念、理论、技术范式或文化现象，重点看源流、争论、学派分叉、机制拐点和当前用法漂移。
- `research-update`
  - 用户已有旧报告，要补最新事实、修正判断、更新来源。
- `research-asset-pack`
  - 用户要可复用资料包、来源地图、证据账本、后续写作或交接用研究底座。
- `parallel-research-sprint`
  - 研究面很宽、时间敏感或用户明确要求多 Agent 并行；由一个 lead integrator 拆分并行子任务，通过 Researcher/Evidence-Verifier 对抗循环验证证据质量，Conflict Arbiter 系统化解决证据冲突，最后合并为可追溯的研究结论。使用 `multi-agent-protocol.md` 确保每个研究子任务都有明确的质量门禁、重试机制和状态追踪。
- `research-retrospective`
  - 用户要求评估一次真实调研表现；按研究问题、方法栈、证据强度、深度、反方证据、行动性和动态组合质量做诊断，不直接重写报告。

详细路由索引和 Token 预算见 [references/reference-routing-index.md](references/reference-routing-index.md)。

## 工作流程

### 1. 锁研究问题

先把任务压成一句研究问题：

- `我到底要弄清楚什么？`
- `最后要支持什么动作或判断？`
- `时间范围、地域、行业、对比对象有没有边界？`

信息不足时，不要长篇追问。先给一个默认研究框架，并列出会影响结论的缺口。

### 2. 选择方法论组合

先按 [references/research-methodology-atlas.md](references/research-methodology-atlas.md) 和 [references/methodology-routing-index.md](references/methodology-routing-index.md) 选择 `method stack`。

常见方法包括：

- `evidence-triangulation`
- `claim-citation-audit`
- `historical-lineage`
- `paradigm-analysis`
- `competitive-analysis`
- `jtbd-user-choice`
- `ecosystem-mapping`
- `literature-review`
- `osint-due-diligence`
- `user-signal-analysis`
- `causal-mechanism-analysis`
- `red-team-dissent`
- `scenario-planning`
- `decision-analysis`
- `monitoring-design`
- `benchmark-analysis`
- `formal-status-analysis`
- `research-quality-audit`
- `report-quality-scoring`

方法栈决定要使用哪些输出模块；模板只作为基础骨架。

### 3. 判断是否需要并行执行

只有当并行能缩短研究路径或增加独立验证时，才启用 [references/multi-agent-protocol.md](references/multi-agent-protocol.md)。

**⚠️ 多 Agent 实际调用执行指南：**
[references/multi-agent-protocol.md](references/multi-agent-protocol.md) §五~六
**必读：** 包含真正的多 Agent 并行调用指令。不要用"你现在扮演 X 角色"模拟，而是用独立 Agent 实例并行执行。每个 Research Agent 有独立的研究任务、证据账本和输出报告。

默认并行角色包括：

- `lead-integrator`：锁研究问题、拆任务、合并证据、输出最终判断。
- `source-scout`：找原始来源、二级来源关系和证据缺口。
- `timeline-analyst`：梳理起源、阶段变化和路径依赖。
- `competitive-analyst`：识别竞品、替代方案和用户选择逻辑。
- `dissent-reviewer`：寻找反方证据、冲突来源和会推翻结论的条件。
- `decision-analyst`：当用户要行动建议时，套用决策口径与监控阈值。

**关键执行要求：**

- 每个研究角色必须是独立 Agent 调用，不是单 Agent 模拟
- 每个 Agent 有独立的 Prompt、独立的上下文窗口
- 所有证据账本条目必须有 `evidence_id` 和 `lane_id`
- Lead Integrator 负责证据去重、冲突解决和最终合成

### 4. 建证据账本

凡涉及最新事实、价格、融资、版本、人物职位、政策、市场份额、产品能力、用户口碑、论文进展，都要先核实。

先按 [references/source-strategy.md](references/source-strategy.md) 选择来源组合：优先找原始材料和能互相独立验证的来源，再用社区信号补充真实使用体验。不要把同一条二手消息的多次转载当成多方确认。

关键结论按 [references/claim-citation-protocol.md](references/claim-citation-protocol.md) 做 claim-level traceability：官方状态、时间敏感事实、行动建议、风险判断和反转条件必须能回指到证据 ID；证据不足时降置信度或改成复核步骤。

政策、标准、考试、认证和官方项目按 [references/formal-adoption-status-protocol.md](references/formal-adoption-status-protocol.md) 先判定正式状态：区分已生效、已适用、已采用但未适用、政治协议、草案指南、征询文件、志愿代码、试点和机构规则。不要把“官方发布”直接等同于“已经普遍适用”。

证据账本至少区分：

- `confirmed_fact`：来源可靠、可复核的事实
- `reported_claim`：媒体、访谈、社区或第三方声称
- `user_signal`：用户评论、issue、论坛、社媒反馈
- `inference`：基于事实推出的判断
- `gap`：暂缺或互相矛盾的信息

账本格式以 [references/evidence-ledger.schema.json](references/evidence-ledger.schema.json) 为准。

### 5. 做三轴分析

默认使用三轴：

- `时间轴`
  - 起源、关键节点、阶段变化、路径依赖、错过的岔路口。
- `截面轴`
  - 同类对象、竞品、替代方案、用户选择理由、生态位。
- `机制轴`
  - 哪些历史选择塑造了当前优势和短板，哪些外部变量可能改变剧本。

研究不是年表加表格。时间轴要讲清因果，截面轴要讲清真实选择，机制轴要给出可争辩但有证据支撑的判断。

### 6. 动态组合输出形态

按用户目标选择最小有效产物：

- 需要快速搞懂：`research-brief`
- 需要完整沉淀：`deep-research-report`
- 需要行动判断：`decision-brief`
- 需要横向比较：`competitive-map`
- 需要发展历程：`concept-lineage-timeline`
- 需要后续复用：`research-asset-pack`
- 需要并行执行记录：`parallel-research-plan` 或在主产物附上 `parallel execution summary`

选择规则见 [references/output-routing-index.md](references/output-routing-index.md)。动态组合规则见 [references/dynamic-output-composer.md](references/dynamic-output-composer.md)，可插拔模块见 [assets/output-blocks/](assets/output-blocks/)。

### 7. 质量门禁

交付前检查：

- 关键事实有没有来源，是否标注访问时间或信息时间点。
- 关键结论有没有证据 ID，是否能追溯到来源标题、URL、发布时间、访问时间和可靠性。
- 官方状态有没有分清法律效力、适用日期、草案/政治协议/试点/机构规则。
- 方法论组合是否匹配用户问题，而不是直接套固定模板。
- 事实、推测、判断有没有分开。
- 有没有遗漏主要竞品、替代方案或反方证据。
- 纵向分析是不是解释了“为什么这样演化”，而不是只列日期。
- 横向分析是不是解释了“用户为什么会选它/放弃它”，而不是参数堆砌。
- 最终判断有没有给出置信度、证据缺口和可能被推翻的条件。
- 行动建议有没有给出最小下一步、监控指标和反方证据。
- 并行执行有没有清楚说明任务分工、独立证据、冲突处理和 lead integrator 的合并依据。
- 复杂或高风险输出有没有按质量评分决定 ship / revise / rerun。

### 8. 反向评估

当用户要求评估真实任务表现时，使用 [references/research-retrospective-protocol.md](references/research-retrospective-protocol.md)：

- 先给总评分和一句原因。
- 再按问题贴合、方法贴合、证据强度、机制深度、反方与缺口、行动性、组合质量打分。
- 使用 [references/report-quality-rubric.json](references/report-quality-rubric.json) 判断 ship / revise / rerun。
- 最后判断下一步应改执行、规则、资产还是 eval。

## 输出模板

输出分两级：**最小输出**和**完整输出**。根据路由和用户需求选择，不要对简单请求输出完整模板。

### 最小输出（适用于 `research-orientation`、`research-update`、`research-retrospective`）

- `研究问题`
  - 本轮到底要回答什么。
- `一句话结论`
  - 先给当前最重要判断，标注置信度。
- `证据底座`
  - 关键来源、事实、争议信息和缺口。
- `下一步`
  - 最小下一步行动或监控建议。

### 完整输出（适用于 `evidence-first-deep-dive`、`competitive-snapshot`、`decision-brief`、`concept-lineage`、`parallel-research-sprint`）

在最小输出基础上，根据方法论组合按需追加：

- `并行执行摘要`
  - 如启用多 Agent，列出角色分工、各自结论、冲突、合并决策。
- `时间轴`
  - 它如何一步步变成今天这样。
- `截面轴`
  - 它在当下和谁竞争、被谁替代、用户为什么选择。
- `机制洞察`
  - 历史如何塑造今天，今天的格局如何限制未来。
- `未来剧本`
  - 最可能、最危险、最乐观三个剧本。
- `行动建议`
  - 学习、购买、投资、对标、观望或继续研究的下一步。
- `反转条件`
  - 哪些新事实会推翻当前判断，接下来应该监控什么。

**切换规则**：如果用户只问"XX 是什么"或只要快速搞懂，用最小输出。如果用户要系统研究、竞品分析、决策判断或完整沉淀，用完整输出。不确定时默认最小输出并询问是否需要深入。

输出质量参考 [assets/few-shot-examples.md](assets/few-shot-examples.md) 中的正面和反面示例。
