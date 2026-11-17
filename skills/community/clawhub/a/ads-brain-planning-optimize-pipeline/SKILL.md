---
name: ads-brain-planning-optimize-pipeline
description: 规划 Agent 新框架中的优化 Pipeline。面向投放改善目标生成优化策略，支持存量对象、待创建草案、策略变量和目标导向优化；诊断只是可选协作依据，不等同于优化本身。
---

# 规划 Agent 优化 Pipeline

## 1. 定位

本 Skill 定义新框架下的优化状态机。

优化不是诊断，也不只服务存量投放对象。优化负责围绕明确的投放改善目标，产出策略优化方案。

当前阶段只做内容层定义：

- 暂不接入 `agent-card.json`。
- 暂不影响现有线上路由。
- 不直接执行修改。
- 不直接生成 `create_campaign`。
- 目标是成为新的优化内容主线，完整承载投放改善所需的业务规则。

---

## 2. 优化边界

### 2.1 优化回答什么

优化回答：**接下来怎么改善**。

它可以包括：

- 如何放量。
- 如何控成本。
- 如何提升转化。
- 如何改创意。
- 如何调整预算、出价、人群、地域、节奏。
- 如何优化一个待创建草案。
- 如何基于诊断结论制定行动方案。

### 2.2 诊断回答什么

诊断回答：**问题为什么发生**。

诊断可以作为优化的依据，但不能替代优化。

规则：

- 用户问“为什么掉量 / 为什么成本高 / 为什么不起量”时，可以触发诊断协作。
- 用户问“怎么优化 / 怎么放量 / 怎么控成本”时，不必先诊断，可以直接生成优化策略。
- 若调用诊断，诊断产物进入 `diagnosis_ref` 或 `diagnosis_summary`，最终仍需生成 `optimization_plan`。

---

## 3. 优化上下文类型

| optimization_context_type | 含义 |
|---|---|
| `existing_delivery` | 已有账户、计划、单元、创意、素材等存量投放对象 |
| `draft_plan` | 创编阶段生成的 `launch_plan_draft` 或待创建方案 |
| `strategy_variable` | 预算、出价、人群、地域、创意方向、投放节奏等策略变量 |
| `goal_only` | 用户只给出改善目标，如“更稳一点”“多放量” |
| `unknown` | 无法识别上下文 |

---

## 4. 优化 Pipeline 业务规则总览

本 Pipeline 直接定义 O0～O6 优化内容主线。所有投放改善所需的状态识别、上下文识别、目标识别、依据收集、诊断协作、策略生成、风险护栏和输出约束，都在本 Skill 中自洽表达。

### 4.1 O0～O6 规则索引

| 状态 | 规则主题 | 核心职责 |
|---|---|---|
| O0 | 会话状态识别 | 识别确认、追加建议、重新分析、详情展开等多轮状态 |
| O1 | 优化上下文识别 | 判断存量投放、待创建草案、策略变量或单纯改善目标 |
| O2 | 优化目标识别 | 识别扩量、控成本、提转化、改创意、成效预估、策略细化、原因诉求 |
| O3 | 优化依据收集 | 按目标选择查询维度，消费 Evidence Summary，完成现状盘点和行业对标 |
| O4 | 诊断协作决策 | 判断是否需要诊断能力，并将诊断结果作为优化依据 |
| O5 | 生成优化策略 | 输出核心动作、取舍、预估、风险、草案 patch |
| O6 | 输出 | 精简版建议、warnings、execution_action、next_action |

### 4.2 Tool / Evidence 使用语义

| Tool / Evidence | 用途 | 使用阶段 |
|---|---|---|
| `queryPlanningEvidenceSummary` | 默认数据摘要入口，消费 Summary 而非原始 rows | O3 |
| `queryPlanningAdIndexSummary` | 当前投放基建摘要，用于理解“当前怎么投” | O3 |
| `a2a_adsdataagent_get_data_agent_group_insight` | 人群画像与拓定向依据 | O3/O5 |
| `a2a_adsdataagent_material-high-quality-features-recommend` | 高点击/高转化素材特征 | O3/O5 |
| `buildPlanningEvidenceSummary` | 仅 rawJson 兼容路径使用 | O3 |
| 诊断能力 | 掉量、不起量、超成本、无转化、素材问题根因判断 | O4 |

常用 apiKey 语义必须保留：

| apiKey | 用途 |
|---|---|
| `query_advertiser_engagement_and_cost` | 账户维度消耗/点击率/转化率/转化成本 |
| `query_campaign_engagement_and_cost` | 计划维度表现 |
| `query_creativity_engagement_and_cost` | 创意维度表现 |
| `query_funnel_passthrough_rate` | 漏斗通过率 |
| `query_funnel_filter_reason_by_rank` | 漏斗过滤原因 |
| `query_industry_metrics` | 行业水位对标 |
| `get_advertiser_rec_keyword` | 行业热搜词，用于内容选题/标题方向 |
| `get_advertiser_note_cost_predict` | 笔记变化对应收益/花费预测 |
| `get_advertiser_bid_cost_predict` | 出价变化对应收益/花费预测 |

### 4.3 优化方案产出依赖链

优化方案必须按“先确定优化上下文，再确定改善目标，再收集依据，再判断是否需要诊断，最后生成策略动作”的顺序产出。

| 产出部分 | 优先依赖 | 次级依赖 | 产出逻辑 | 产出结果 |
|---|---|---|---|---|
| 优化上下文 | 用户本轮诉求、conversation_history、已有计划/账户/创意/素材对象、`launch_plan_draft` | 结构化入参、历史优化产物 | 先判断优化围绕存量投放、待创建草案、策略变量还是单纯改善目标 | `optimization_context_type`、对象信息、是否需要追问 |
| 优化目标 | 用户表达的改善诉求 | 当前上下文、历史表现、业务目标 | 将“放量/控成本/提转化/改创意/预估/原因”归一为标准目标 | `optimization_goal`、时间窗口、约束 |
| 现状盘点 | 账户/计划/创意表现、基建摘要 | 用户指定对象、时间窗口 | 先看当前投放结构、消耗、转化、成本、预算利用和素材分布 | `performance_findings` |
| 行业与漏斗对标 | 行业水位、漏斗通过率、漏斗过滤原因 | 客户行业类目、弱阶段信号 | 判断增量空间、竞争强度和主要瓶颈 | `benchmark_findings`、瓶颈判断 |
| 人群与创意依据 | 人群洞察、素材高质特征、行业热搜词、创意表现 | 商品/卖点、目标人群 | 将数据依据转成可执行的人群拓展/收敛和素材方向 | `audience_findings`、`creative_findings` |
| 成效预估 | 历史表现、行业水位、基建摘要、笔记/出价预测工具 | 预算/出价调整幅度 | 给区间预估，不编造确定性数字 | `expected_impact`、风险提示 |
| 诊断协作 | 用户原因诉求、异常信号 | 已有表现数据、诊断能力可用性 | 只有用户问原因或异常信号明显时触发；诊断结论只作为优化依据 | `diagnosis_ref`、`diagnosis_summary` |
| 优化动作 | 优化目标、现状盘点、对标结果、诊断依据 | 风险护栏、用户约束 | 把依据转成 3～5 条核心动作，每条包含简短依据和具体动作 | `optimization_plan.actions` |
| 草案 patch | `optimization_context_type=draft_plan`、`launch_plan_draft` | 用户改善目标、策略约束 | 只输出需要修改的草案字段和原因，不生成 `create_campaign` | `draft_patch` |
| 下一步动作 | 是否存在可执行 action、是否需要追问、是否只是建议 | 执行确认门禁 | 判断是否进入确认、追问或仅输出建议 | `next_action` |

依赖顺序硬约束：

1. 未识别优化上下文前，不生成优化动作。
2. 未识别优化目标前，不选择查询维度。
3. 数据缺失时只能降级输出和写入 `warnings`，不得编造指标。
4. 用户未问原因且无明显异常信号时，不强制调用诊断。
5. 诊断结论不能替代优化动作。
6. 草案优化只输出 `draft_patch`，不直接生成 `create_campaign`。
7. 有执行动作时必须先经过执行确认门禁。

---

## 5. 状态机总览

```text
O0 会话状态识别
  ↓
O1 优化上下文识别
  ↓
O2 优化目标识别
  ↓
O3 优化依据收集
  ↓
O4 诊断协作决策
  ↓
O5 生成优化策略
  ↓
O6 输出 optimization_plan + next_action
```

---

## 6. O0 会话状态识别

| 状态 | 条件 | 行为 |
|---|---|---|
| `first_turn` | 无历史优化产物 | 进入 O1 |
| `confirm_action` | 用户确认执行某个优化动作 | 若存在合法 `execution_action`，进入执行确认前置判断 |
| `explain_optimization` | 用户追问原因或依据 | 复用上一轮分析展开 |
| `revise_optimization` | 用户要求换优化方向 | 重新进入 O2 |
| `restart_optimize` | 用户换对象或换目标 | 重新进入 O1 |

输出：

```json
{
  "optimize_conversation_state": "first_turn | confirm_action | explain_optimization | revise_optimization | restart_optimize",
  "reuse_previous_analysis": true,
  "revision_fields": []
}
```

---

## 7. O1 优化上下文识别

目标：明确本轮优化围绕什么上下文发生。

识别顺序：

1. 是否指定存量对象：账户、计划、单元、创意、素材。
2. 是否基于上一轮 `launch_plan_draft` 或待创建方案。
3. 是否只围绕策略变量：预算、出价、人群、地域、创意、节奏。
4. 是否只有改善目标。

输出：

```json
{
  "optimization_context_type": "existing_delivery | draft_plan | strategy_variable | goal_only | unknown",
  "object_type": "account | campaign | unit | creative | material | draft | variable | unknown",
  "object_ids": [],
  "object_names": [],
  "draft_ref": "string | null",
  "strategy_variables": [],
  "need_clarification": false
}
```

要求：

- 没有明确存量对象但改善目标清晰时，不要直接阻断，可进入 `goal_only` 或 `strategy_variable`。
- 只有无法安全确定优化上下文时才追问。
- 如果识别为 `draft_plan`，后续输出应是 draft patch 或草案优化建议，而不是新建 `create_campaign`。

---

## 8. O2 优化目标识别

目标：识别用户要改善什么。

| optimization_goal | 含义 |
|---|---|
| `scale` | 扩量、增加消耗、提升跑量 |
| `cost_control` | 控成本、降低 CPA/CPC/转化成本 |
| `conversion` | 提升转化率、ROI、线索质量 |
| `creative` | 改创意、素材方向、内容策略 |
| `forecast` | 成效预估、预算和出价变化影响预估 |
| `strategy_refine` | 对方案、预算、人群、节奏做策略细化 |
| `diagnose` | 用户主要问原因 |
| `unknown` | 无法识别 |

输出：

```json
{
  "optimization_goal": "scale | cost_control | conversion | creative | forecast | strategy_refine | diagnose | unknown",
  "time_window": "last_7d | last_14d | custom | unknown",
  "constraints": [],
  "required_clarifications": []
}
```

---

## 9. O3 优化依据收集

目标：根据上下文和目标收集必要依据。

依据类型：

- 存量对象表现数据。
- 行业水位。
- 漏斗数据。
- 人群洞察。
- 素材特征。
- 基建快照。
- 成本/出价预测。
- 上一轮 `launch_plan_draft`。
- 用户显式约束与假设。

原则：

- `existing_delivery` 可以承载较重数据研判。
- `draft_plan` 优化优先消费草案结构和已有 Evidence 摘要。
- `strategy_variable` 和 `goal_only` 可更多依赖策略约束、已有上下文和通用经验。
- 数据缺失时进入 `warnings`，不得编造。

### 9.1 按优化目标选择查询维度

| 优化目标 | 建议依据维度 |
|---|---|
| `scale` 扩量 / 加预算 / 出价 / 拓定向 | 账户 + 计划维度消耗、点击率、转化率、转化成本；行业水位；漏斗通过率；基建快照；拓定向时加人群洞察 |
| `cost_control` 控成本 | 账户/计划成本趋势；出价和预算利用；漏斗过滤原因；行业成本水位；高低效计划对比 |
| `conversion` 提升转化 | 漏斗通过率；转化率；计划/创意转化表现；人群洞察；落地链路风险 |
| `creative` 改创意 | 创意维度点击率/转化率；素材高质特征；人群洞察；行业热搜词；基建快照 |
| `forecast` 成效预估 | 账户/计划表现；行业水位；漏斗；基建快照；笔记变化预测；出价变化预测 |
| `strategy_refine` 草案/策略细化 | `launch_plan_draft`、用户约束、已有 Evidence、预算/人群/内容策略取舍 |
| `diagnose` 原因诉求 | 先收集异常相关表现数据，再进入 O4 诊断协作判断 |

### 9.2 数据编排纪律

数据编排规则如下：

1. ≥ 2 个 apiKey 时，优先使用 `queryPlanningEvidenceSummary(queries=[...])` 批量并发，避免 N 次串行单查。
2. 无依赖数据放同批并行，例如账户表现、计划表现、创意表现、客户画像等。
3. 有依赖数据后置，例如行业水位依赖真实类目，漏斗过滤原因依赖弱阶段，成效预估依赖基建摘要中的投放位置/约束类型。
4. 整条链最多两批：无依赖批 + 依赖批，避免 3 批以上链式查询。
5. 单批超时或 pending 时，本轮不反复重试，使用已成功 Evidence 降级输出。
6. 用户修改预算、目标、对象、时间窗口、投放位置、约束类型、note_id 等关键上下文时，相关 Evidence 应刷新或标记 stale。
7. 工具失败不阻断整体优化建议，但缺失维度必须进入 `warnings`，不得编造。
8. 若走 rawJson 兼容路径，必须先转 Planning Evidence Summary 后再分析。

### 9.3 O3 分析框架

O3 不只是收集数据，还要完成以下分析：

- 现状盘点：当前投放结构、消耗、转化、成本、素材分布。
- 行业对标：和行业水位比较，判断增量空间。
- 增量预估：给区间，不编造确定性数字；可引用笔记变化预测或出价变化预测。
- 异常信号：掉量、不起量、超成本、空耗、预算利用低、漏斗弱阶段等。
- 诊断协作触发依据：当异常信号明显或用户明确问原因时，进入 O4。

输出：

```json
{
  "performance_findings": [],
  "benchmark_findings": [],
  "audience_findings": [],
  "creative_findings": [],
  "strategy_constraints": [],
  "data_gaps": [],
  "evidence_refs": []
}
```

---

## 10. O4 诊断协作决策

目标：判断是否需要引入诊断能力。

| 条件 | 决策 |
|---|---|
| 用户明确问“为什么掉量/为什么成本高/为什么不起量/为什么没转化” | `call_diagnosis` |
| 数据研判发现明显异常信号 | `call_diagnosis` 或 `diagnosis_optional` |
| 用户只问“怎么优化/怎么放量/怎么控成本” | `skip_diagnosis` |
| 上一轮已有诊断结果 | `reuse_diagnosis` |

输出：

```json
{
  "diagnosis_needed": true,
  "diagnosis_type": "volume_drop | volume_low | over_cost | no_conversion | none",
  "diagnosis_ref": "string | null",
  "diagnosis_summary": "string | null",
  "reason": "string"
}
```

要求：

- 诊断结果只是优化依据。
- 不得只输出诊断结论而没有优化策略。
- 若诊断不可用，可基于已有数据给保守优化建议，并写入 `warnings`。

### 10.1 诊断能力映射

| 异常/原因诉求 | 诊断能力 |
|---|---|
| 掉量 / 跑量下降 / 流量跌了 | `ad-diagnosis-volume-drop` / `buildVolumeDropDiagnosisContext` |
| 不起量 / 起量困难 / 预算花不出去 | `ad-diagnosis-volume-low` / `buildVolumeLowDiagnosisContext` |
| 超成本 / 成本差 / 成本异常升高 | `ad-diagnosis-overcost` / `buildOverCostDiagnosisContext` |
| 空耗 / 有消耗没转化 / 转化数太少 | `ad-diagnosis-no-conversion` / `buildNoConversionDiagnosisContext` |
| 素材/内容储备问题 | `content-diagnose` / `getContentDiagnose` |

调用诊断后，O5 必须把诊断结论转化为优化动作，例如预算节奏、出价、人群、创意、观察指标，而不是停留在原因描述。

---

## 11. O5 生成优化策略

输出：

```json
{
  "optimization_goal": "scale | cost_control | conversion | creative | forecast | strategy_refine | diagnose | unknown",
  "optimization_plan": {
    "summary": "string",
    "actions": [],
    "tradeoffs": [],
    "expected_impact": "string | null",
    "risks": []
  },
  "draft_patch": null,
  "diagnosis_ref": "string | null"
}
```

### 11.1 对 existing_delivery

输出应包含：

- 优化动作。
- 优先级。
- 预期影响。
- 风险和观察指标。

### 11.2 对 draft_plan

输出应包含：

- `draft_patch`：建议修改的草案字段。
- 修改原因。
- 回流创编 Pipeline 的建议。

示例：

```json
{
  "draft_patch": {
    "budget.amount": {
      "from": 1000,
      "to": 1500,
      "reason": "用户希望更激进放量"
    },
    "audience_strategy.summary": {
      "from": "泛兴趣人群",
      "to": "核心高意向人群优先，逐步扩展泛兴趣",
      "reason": "用户要求更精准"
    }
  }
}
```

### 11.3 精简版输出

首轮默认输出精简版优化建议，不能一次性铺开完整明细。

精简版必须包含：

1. 一句话现状：概括当前消耗、转化成本、投放结构或草案状态。
2. 3～5 条核心优化动作：每条必须有“简短依据 + 具体动作”，严禁只给动作不给依据。
3. 一句话增量预估：给区间，不编造确定性数字。
4. 一句话风险提示：只点最关键风险。
5. 展开邀请：引导用户选择逐计划预算/出价、创意素材方向、分阶段实施、完整风险护栏等。

详情展开路径：

- 用户追问某一部分时，只展开被问部分。
- 复用本会话已取数据，不重新全量查数。
- 每条展开讲清：调整什么、为什么调、预期效果、观察指标与节奏。

### 11.4 风险护栏

| 护栏 | 触发条件 | 输出要求 |
|---|---|---|
| 调幅护栏 | 出价/预算/目标成本相对当前值变化超 ±20% | 标注风险，建议分阶段调整 |
| 冷启保护 | 冷启期内大幅调价、收窄定向或暂停计划 | 建议延长观察期或小步调整 |
| 批量范围 | 一次影响多个单元/创意或账户级动作 | 明确影响范围，建议分批 |
| 策略冲突 | 调整方向与客户既有策略明显相悖 | 给保守方案和激进方案供选择 |

护栏只用于提示与分阶段建议，不作为拒绝服务的理由。

---

## 12. O6 输出

输出结构：

```json
{
  "capability": "optimize",
  "optimize_conversation_state": "string",
  "gate_validation": {},
  "optimization_context_type": "existing_delivery | draft_plan | strategy_variable | goal_only | unknown",
  "optimization_goal": "scale | cost_control | conversion | creative | forecast | strategy_refine | diagnose | unknown",
  "diagnosis_summary": "string | null",
  "diagnosis_ref": "string | null",
  "optimization_plan": {
    "summary": "string",
    "actions": [],
    "tradeoffs": [],
    "expected_impact": "string | null",
    "risks": []
  },
  "draft_patch": null,
  "execution_action": null,
  "warnings": [],
  "next_action": "confirm_execution | ask_clarification | no_action"
}
```

输出原则：

- 不直接输出 `create_campaign`。
- 不从零创建新计划。
- 如优化对象是草案，只输出 `draft_patch` 或优化建议，再回流创编 Pipeline。
- 有可执行动作时，必须经过执行确认前置判断。

### 12.1 客户可见输出硬约束

优化输出边界如下：

1. 禁止输出思考过程、中间推理、草稿、内部分析、调试信息或乱码。
2. 不得输出“我先分析”“工具返回”“字段映射”“推理过程如下”等中间话术。
3. 面向客户必须使用中文业务名，不输出 `planning`、`in-flight optimize`、`pre-plan` 等英文/枚举场景名。
4. 指标必须中文化，例如「转化成本」「点击率」「转化率」「预算消耗率」「投放位置」等。
5. 禁止输出内部字段和枚举码，例如 `CPA`、`CTR`、`CVR`、`placement`、`constraint_type`、`true_ctr`、`query_industry_metrics`、`get_advertiser_bid_cost_predict` 等。
6. AdIndex 摘要中的数字编码必须翻译成业务中文名，禁止“中文名（数字）”形式外泄。

### 12.2 执行边界

当前新 Pipeline 仍只输出建议或 `execution_action` 草案，不直接执行修改。

- `next_action=confirm_execution` 仅表示后续可以进入执行确认。
- 没有合法 `execution_action` 时，`next_action` 应为 `no_action` 或 `ask_clarification`。
- 执行前必须经过 execution-confirmation / function point 体系确认。

---

## 13. 非目标

本 Skill 不做：

- 不生成新建计划 payload。
- 不直接执行预算、出价、人群等修改。
- 不替代诊断能力。
- 不处理客户画像查询主流程。
