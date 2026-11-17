---
name: ads-brain-planning-create-pipeline
description: 规划 Agent 新框架中的创编 Pipeline。面向新建投放方案生成，负责从经营诉求归一化出发，经过场景门禁、创建必要门禁、生成 launch_plan_draft，并委托 simple-create 生成 create_campaign。
---

# 规划 Agent 创编 Pipeline

## 1. 定位

本 Skill 定义新框架下的创编状态机，只服务“从无到有生成投放方案”的场景。

当前阶段只做内容层定义：

- 暂不接入 `agent-card.json`。
- 暂不影响现有线上路由。
- 不直接调用执行 Tool。
- 不维护 `create_campaign` 字段细节。
- 目标是成为新的创编内容主线，完整承载投前创编所需的业务规则。

---

## 2. 创编边界

### 2.1 适用场景

- 用户要求新建广告计划。
- 用户要求冷启投放方案。
- 用户要求“帮我搭一个计划”“给我出一个投放方案”。
- 用户没有明确指定存量计划、单元或创意对象，但希望生成投放策略。
- 上一轮已有创编草案，本轮用户确认、局部调整或要求解释。

### 2.2 不适用场景

- 存量计划掉量、超成本、不起量等问题定位。
- 已有计划、单元、创意、素材的优化。
- 对草案说“更激进一点 / 更保守一点 / 更精准一点”等策略改善诉求，此类应转 `optimize`，由优化 Pipeline 输出 draft patch。
- 标准投、合约、品专等当前非简单投新建能力。

---

## 3. 创编 Pipeline 业务规则总览

本 Pipeline 直接定义 S0～S6 创编内容主线。所有投前创编所需的状态识别、场景门禁、上下文归一化、数据依据、准入规则、草案生成、结构化创建和输出约束，都在本 Skill 中自洽表达。

### 3.1 S0～S6 规则索引

| 状态 | 规则主题 | 核心职责 |
|---|---|---|
| S0 | 会话状态识别 | 识别确认、局部调整、详情展开、重新规划等多轮状态 |
| S1 | 创编场景门禁 | 标准投、合约、品专等硬阻断或 route，不降级为简单投 |
| S2 | 创编上下文归一化 | 复用经营信息、Evidence Pack、用户本轮输入，形成结构化上下文 |
| S3 | 创建必要门禁 | 简单投准入、客资唯一性、预算风险等 Guard |
| S4 | 生成 `launch_plan_draft` | 完成人群、内容、预算、出价、节奏、阶段规划等策略草案 |
| S5 | simple-create 转换 | 委托 simple-create 生成 `create_campaign` 并校验 schema |
| S6 | 输出 | 精简版方案、结构化结果、warnings、next_action |

### 3.2 Tool 与 Evidence 使用语义

本 Pipeline 只描述内容层规则，不新增 Tool 接入；但创编过程中需要使用以下 Tool / Evidence 语义。

| Tool / Evidence | 用途 | 使用阶段 |
|---|---|---|
| `getCurrentDateTime` | 需要当前日期、节日、大促、下周等时间推理时调用 | S2/S4 |
| `getMarketingPlanInfoCollect` | 读取客户已收集经营信息，减少重复追问 | S2 |
| `queryPlanningEvidenceSummary` | 默认数据摘要入口，消费 Planning Evidence Summary 而非原始 rows | S2/S4 |
| `queryPlanningAdIndexSummary` | 理解历史投放基建，延续既有基建风格 | S2/S4 |
| `checkSimpleCreateEligibility` | 简单投准入硬约束 | S3 |
| `checkSimpleClueCampaignExists` | 仅明确客资新建时做唯一性检查 | S3 |
| `a2a_adsdataagent_get_data_agent_group_insight` | 人群画像、拓定向、人群方向 | S4 |
| `a2a_adsdataagent_material-high-quality-features-recommend` | 素材/创意方向依据 | S4 |
| `validateCreateCampaignSchema` | simple-create 生成结果字段白名单校验 | S5 |

### 3.3 Evidence Pack 复用纪律

若上下文中已经注入 `【PlanningPrehook Evidence Pack】`：

1. `status=SUCCESS/EMPTY` 且有内容的数据块必须直接复用，不得重复调用同名 Tool。
2. `simple-clue-campaign-exists=SKIPPED_NOT_CLUE_CREATE_INTENT` 时，不得把泛化新建诉求默认判为客资收集。
3. 只有 Evidence 缺失、失败、超时、跳过，或用户修改预算/目标/对象/时间窗/版位/优化目标等关键口径时，才允许局部刷新。
4. `pending`、`WORKING`、`timeout`、`数据准备中` 等状态本轮不得反复重试，应使用已成功 Evidence 降级输出。
5. Evidence 失败不阻断自然语言规划；但准入失败、准入为空、schema 校验失败、客资唯一性命中时，不得输出 `create_campaign`。

### 3.4 创编方案产出依赖链

创编方案不是一次性拼装出来的，必须按“先识别客户与场景，再确定目标与约束，再生成结构和策略，最后生成可执行配置”的顺序产出。

| 产出部分 | 优先依赖 | 次级依赖 | 产出逻辑 | 产出结果 |
|---|---|---|---|---|
| 客户现状摘要 | `getMarketingPlanInfoCollect`、广告主基础信息、行业/类目、AdIndex 基建摘要 | 历史账户/计划/创意表现 | 先判断客户行业、经营阶段、历史投放基础和当前可用资产，形成创编起点 | 行业/类目、品牌或效果属性、历史投放基础、已有基建情况 |
| 投放目标判断 | 用户本轮诉求、已收集经营信息、TOP 优化目标、简单投准入全集 | 历史营销目标、行业经验 | 先尊重用户本轮诉求，再校准到当前支持的营销诉求和转化目标；若目标不在准入全集内，只出文字方案不生成创建配置 | 营销诉求、转化目标、冷启动/追投判断、策略风格 |
| 账户与计划结构 | AdIndex 基建摘要、历史计划结构、预算规模、目标复杂度 | 行业经验、类似账户结构 | 优先延续有效基建；若基建不足，则按目标和预算给简化结构 | 建议计划数、计划拆分方式、是否复用历史结构 |
| 预算与出价 | 用户预算诉求、历史消耗/转化/成本、行业水位 | 成效预估、冷启经验 | 先看客户预算和历史成本，再用行业水位校准；数据不足时给保守起量建议，并写入假设 | 日预算、计划预算分配、出价区间、分阶段放量建议 |
| 定向与人群 | 用户地域/人群诉求、已收集经营信息、人群洞察 | 历史定向、行业经验、地域编码 | 先确定基础可投人群，再结合高转化人群标签做拓展或收敛 | 地域、年龄/性别/兴趣、人群标签方向 |
| 创意与素材 | 用户商品/卖点、素材高质特征、创意表现 | 行业热搜词、人群洞察 | 从高点击/高转化特征中提炼素材表达，再映射到标题、封面、内容卖点 | 标题方向、封面方向、内容卖点、关键词/选题建议 |
| 风险与确认点 | 数据完整度、准入结果、客资唯一性、schema 校验结果 | 预算风险、预估不确定性 | 对缺失信息、能力限制、字段不可执行、预估不确定性显式提示 | `warnings`、需用户确认/补充的信息 |
| `launch_plan_draft` | 目标、预算、出价、人群、地域、创意、节奏等策略结论 | Evidence refs、assumptions、warnings | 将自然语言策略收敛为 simple-create 可消费的结构化草案 | `launch_plan_draft` |
| `create_campaign` | `launch_plan_draft`、准入结果、schema 约束 | 地域编码、simple-create 默认值 | 只将已可执行的草案交给 simple-create 转换，并通过字段白名单校验 | `create_campaign` 或 `validation_errors` |

依赖顺序硬约束：

1. 未完成场景门禁前，不生成 `launch_plan_draft`。
2. 未完成上下文归一化前，不生成预算、出价、人群、创意结论。
3. 未完成简单投准入前，不生成 `create_campaign`。
4. 未命中客资场景时，不触发客资唯一性检查。
5. 客资唯一性命中、准入失败、schema 校验失败时，只输出文字方案和 `warnings`，不输出 `create_campaign`。
6. `create_campaign` 必须由 simple-create 生成，创编 Pipeline 不直接拼最终字段。

---

## 4. 状态机总览

```text
S0 会话状态识别
  ↓
S1 创编场景门禁
  ↓
S2 创编上下文归一化
  ↓
S3 创建必要门禁
  ↓
S4 生成 launch_plan_draft
  ↓
S5 simple-create 生成 create_campaign
  ↓
S6 输出 plan + create_campaign + next_action
```

---

## 5. S0 会话状态识别

目标：避免多轮中重复生成方案或重复生成 `create_campaign`。

| 状态 | 条件 | 行为 |
|---|---|---|
| `first_turn` | 无历史创编产物 | 进入 S1 |
| `confirm_create` | 已有 `create_campaign`，用户确认执行 | 复用最近产物，进入执行确认前置判断 |
| `revise_partial` | 用户只改预算、地域、人群、时间等局部字段 | 修改 `launch_plan_draft` 对应字段，再进入 S5 |
| `optimize_draft` | 用户要求更激进、更保守、更精准等策略改善 | 转入优化 Pipeline，输出 draft patch |
| `explain_plan` | 用户要求解释方案依据 | 只解释，不重新生成 `create_campaign` |
| `restart_create` | 用户换目标或要求重做 | 重新进入 S1 |

输出：

```json
{
  "create_conversation_state": "first_turn | confirm_create | revise_partial | optimize_draft | explain_plan | restart_create",
  "reuse_previous_campaign": true,
  "revision_fields": []
}
```

---

## 6. S1 创编场景门禁

目标：判断当前请求是否支持进入创编主线。

### 6.1 支持

- 简单投新建。
- 未指定复杂投放形态的新建投放规划。

### 6.2 阻断

| 场景 | blocked_reason | next_action |
|---|---|---|
| `launch_form=standard` 或自然语言明确标准投 | `unsupported_launch_form` | `unsupported` |
| 合约、品专、DSP 等非简单投新建 | `unsupported_create_type` | `unsupported` |
| 语义指向已有计划优化 | `misrouted_to_create` | `route` |
| 缺少必要上下文且无法安全默认 | `missing_required_context` | `ask_clarification` |

输出：

```json
{
  "supported": true,
  "create_scene": "simple_create",
  "blocked_reason": null,
  "route_hint": null
}
```

---

## 7. S2 创编上下文归一化

目标：把用户输入、历史会话、经营信息、Evidence 摘要整理成稳定上下文。

输入来源优先级：

```text
本轮用户明确表达 > conversation_history 中最近确认内容 > 已收集经营信息 > Evidence 摘要 > 默认假设
```

输出：

```json
{
  "advertiser_id_source": "metadata",
  "business_context": {},
  "marketing_goal": "lead_generation | conversion | exposure | unknown",
  "launch_context": "cold_start | new_product | daily_operation | promotion | unknown",
  "strategy_style": "aggressive | conservative | precise | exploratory | unknown",
  "target_audience_hint": "string | null",
  "budget_hint": {
    "amount": null,
    "period": "daily | total | unknown"
  },
  "date_range_hint": {
    "start": null,
    "end": null
  },
  "geo_hint": [],
  "constraints": [],
  "assumptions": [],
  "missing_fields": [],
  "scenario_tags": []
}
```

要求：

- 所有默认值必须写入 `assumptions`。
- 用户本轮明确表达优先于历史信息和 Evidence。
- 不输出完整画像报告，只保留与创编决策相关的摘要。
- 生成 `scenario_tags`，供后续场景化 Guard 使用。

### 7.1 三维意图解析

三维意图解析不以长篇过程输出，而是沉淀进结构化上下文。

| 维度 | 识别内容 | 迁入字段 |
|---|---|---|
| 目标导向 | 品牌曝光、转化促单、客户留存、数据积累、客资收集等 | `marketing_goal`、`constraints` |
| 投放情境 | 新客冷启、新品上市、节日大促、日常运营、竞争应对 | `launch_context` |
| 策略风格 | 激进扩量、稳健保守、精准垂直、测试探索 | `strategy_style` |

“0 提问策略”定义如下：

- 行业/品类缺失时，优先通过客户画像或已收集经营信息补齐，仍缺失则用通用经验降级。
- 日预算缺失时，可按冷启标准做默认假设，但必须写入 `assumptions` 并在输出注意事项中说明。
- 地域、人群、时间等缺失时，能从经营信息/Evidence 推断则推断；不能安全默认时才追问。
- 全程不因非关键字段缺失阻断自然语言方案。

### 7.2 数据研判

数据研判结果应沉淀为 `evidence_refs`、`assumptions`、`warnings` 和 draft 的各策略字段。

必须考虑的依据：

| 依据 | 用途 |
|---|---|
| 广告主基础信息 / 行业类目 | 判断业务场景、行业水位查询条件、内容语境 |
| TOP 优化目标 / 品效属性 | 校准营销目标和投放链路 |
| 已收集经营信息 | 优先复用客户已填信息，减少重复追问 |
| AdIndex 基建摘要 | 延续既有出价方式、投放位置、投放速率、预算量级等有效风格 |
| 历史账户/计划/创意表现 | 判断相似性规划和差异性改善方向 |
| 行业水位 | 校准预算、出价、人群和素材竞争烈度 |
| 人群洞察 | 生成人群策略和定向方向 |
| 素材高质特征 / 热搜词 | 生成创意方向、标题钩子和内容卖点 |
| 简单投准入 | 决定是否允许生成 `create_campaign` |
| 客资唯一性 | 决定客资新建是否允许输出 `create_campaign` |

数据失败降级：

- 单个 Evidence 失败不阻断整体自然语言规划。
- 已成功 Evidence 要继续使用。
- 缺失维度只能进入 `warnings` 或 `assumptions`，不得编造。
- 准入失败、准入为空、客资唯一性命中、schema 校验失败时，不得输出 `create_campaign`。

---

## 8. S3 创建必要门禁

目标：只判断“能不能继续生成创建参数”。

### 8.1 必跑 Guard

| Guard | 触发条件 | 结果 |
|---|---|---|
| `simple_create_eligibility_guard` | `create_scene=simple_create` | `continue` / `block` / `limit_options` |

### 8.2 场景化 Guard

| Guard | 触发条件 | 未触发状态 | 结果 |
|---|---|---|---|
| `lead_generation_guard` | `marketing_goal=lead_generation` 或 `scenario_tags` 包含 `lead_generation` | `skipped:not_lead_generation` | `continue` / `stop_create` / `suggest_optimize_existing` |
| `budget_risk_guard` | 预算缺失不可默认、预算过大或大幅变更 | `skipped:no_budget_risk` | `warn` / `ask` |

### 8.3 输出

```json
{
  "eligible": true,
  "blocked_reasons": [],
  "available_create_options": {},
  "lead_generation_guard": {
    "triggered": false,
    "status": "skipped",
    "skip_reason": "not_lead_generation",
    "action": "continue | stop_create | suggest_optimize_existing"
  },
  "required_clarifications": []
}
```

要求：

- 客资唯一性只在客资场景触发，不得全局必跑。
- 准入失败时不得生成 `create_campaign`。
- 被 Guard 阻断时仍可输出自然语言说明，但 `next_action` 不得为 `confirm_execution`。

### 8.4 简单投准入规则

准入全集约束如下：

1. 简单投新建场景下，生成 `create_campaign` 前必须完成简单投准入检查。
2. 准入成功且返回非空 `availableKeys` / `available` 时，`create_campaign` 中的营销诉求 / 投放模式必须命中全集。
3. 不得把客户原始营销诉求擅自替换成全集中的相近目标。例如产品种草与种草直达语义不同，不得自动互相替代。
4. 准入调用失败、`canCreateSimpleAd=false`、`available` 为空时，自然语言规划可继续，但不得输出 `create_campaign`。
5. 客户可见文案不得展示 `availableKeys`、`available`、内部枚举码或数字编码。

### 8.5 客资唯一性规则

客资唯一计划门禁如下：

1. 只有本轮诉求或会话上下文明确指向客资收集 / 留资 / 线索 / 表单 / 私信 / 咨询 / 获客 / 到店咨询时，才触发 `lead_generation_guard`。
2. 泛化“新建简单投 / 开计划 / 投放方案 / 营销规划”不得默认判定为客资收集。
3. 若明确客资新建且已存在简单投客资计划，不得生成新的 `create_campaign`。
4. 老客仍必须输出文字规划方向，围绕人群、内容、预算出价、观察指标和现有计划优化给建议。
5. 客户可见文案只说明“当前账户已有简单投客资计划，不能再新建第二条，本次方向可用于现有计划优化”，不得展示 Tool 名、计划 ID、内部字段。
6. 客资收集在当前简单投新建链路只支持全自动；用户坚持半自动或高度自定义客资时，只输出文字规划，不生成 `create_campaign`。

---

## 9. S4 生成 launch_plan_draft

目标：生成 planning 与 simple-create 之间的稳定中间态。

`launch_plan_draft` 示例：

```json
{
  "marketing_goal": "string",
  "target_audience": "string",
  "budget": {
    "amount": null,
    "period": "daily | total | unknown",
    "rationale": "string"
  },
  "date_range": {
    "start": null,
    "end": null,
    "rationale": "string"
  },
  "geo": {
    "names": [],
    "rationale": "string"
  },
  "bidding_strategy": {
    "name": "string",
    "rationale": "string"
  },
  "audience_strategy": {
    "summary": "string",
    "included": [],
    "excluded": []
  },
  "creative_direction": [],
  "delivery_strategy": "string",
  "assumptions": [],
  "warnings": [],
  "evidence_refs": []
}
```

原则：

- 本阶段负责策略，不负责最终 `create_campaign` 字段枚举。
- `launch_plan_draft` 必须可被测试断言。
- 不展示内部枚举码。
- 不编造不存在的 Evidence。

### 9.1 方案生成规则

核心方案生成逻辑如下：

1. **先相似、再差异**：
   - 相似性规划：延续客户历史有效经验，如高效投放位置、出价方式、预算节奏、素材方向。
   - 差异性改善：针对历史短板做改进，如创意疲劳、漏斗通过率低、人群过宽或过窄、预算利用不足。
2. **目标达成与阶段规划**：
   - 给出核心目标、预算/出价、人群、内容、投放节奏和观察指标。
   - 阶段规划首轮可简写，详细版留到用户追问时展开。
3. **基建延续纪律**：
   - AdIndex 只作为历史风格和约束信号，不得覆盖用户本轮明确诉求。
   - `isNewAdvertiser=true` 只表示无在线基建可延续，不控制最终输出形态。
4. **准入全集约束**：
   - draft 中可描述客户原始营销诉求。
   - 但进入 `create_campaign` 的落地配置必须满足准入全集。
5. **Evidence 引用纪律**：
   - 只引用已成功或明确为空的 Evidence。
   - 对失败、超时、pending 的数据，只能说明“当前缺少该维度”，不能编造数值。

### 9.2 draft 字段与创编要素映射

| 创编要素 | draft 字段 |
|---|---|
| 营销诉求 / 转化目标 | `marketing_goal` |
| 日预算 / 总预算 | `budget` |
| 投放周期 / 预热窗口 | `date_range` |
| 地域 / 城市 | `geo` |
| 出价方式 / 成本目标 | `bidding_strategy` |
| 人群定向 / 拓定向方向 | `audience_strategy` |
| 素材方向 / 标题钩子 / 卖点 | `creative_direction` |
| 投放节奏 / 分阶段实施 | `delivery_strategy` |
| 默认值 / 数据缺失 | `assumptions` / `warnings` |
| Evidence 来源 | `evidence_refs` |

---

## 10. S5 simple-create 生成 create_campaign

目标：把 `launch_plan_draft` 交给 `ads-brain-simple-create` 转换为 `create_campaign`。

流程：

```text
launch_plan_draft
  ↓
ads-brain-simple-create
  ↓
getGeoCode / 字段映射 / 默认值落地
  ↓
validateCreateCampaignSchema
  ↓
create_campaign 或 validation_errors
```

要求：

- simple-create 输入应是 `launch_plan_draft` 或等价结构化草案。
- simple-create 不重新做完整策略规划。
- schema 校验失败时返回 `validation_errors`，不得进入执行确认。

---

## 11. S6 输出

输出结构：

```json
{
  "capability": "create",
  "create_conversation_state": "string",
  "gate_validation": {},
  "plan": "string",
  "launch_plan_draft": {},
  "create_campaign": {},
  "warnings": [],
  "next_action": "confirm_execution | ask_clarification | unsupported | no_action"
}
```

输出原则：

- 首轮输出精简版方案。
- 假设条件必须展示。
- 不展示内部字段、内部枚举、工具参数。
- `create_campaign` 校验通过后，`next_action` 才能是 `confirm_execution`。
- 如果只是解释或被阻断，`next_action` 应为 `no_action` / `ask_clarification` / `unsupported`。

### 11.1 渐进式输出

首轮默认只输出精简版方案，不一次性铺开所有依据。

精简版建议包含：

1. 系统已掌握：只保留影响规划的关键信息，不逐计划逐版位展开。
2. 投放规划 Brief：一句话概括本次投放目标和策略。
3. 规划聚焦：说明本次主要解决什么问题。
4. 人群策略：核心人群和拓展方向。
5. 内容策略：素材方向、标题钩子、卖点表达。
6. 投放策略：预算、出价、节奏、地域等关键取值。
7. 预估结果：给区间和假设，不编造确定性数字。
8. 分阶段实施：首轮简版，详细版追问再展开。
9. 需注意：默认假设、数据缺失、准入限制、客资唯一性等。
10. 下一步：根据 `next_action` 指引确认、追问或终止。

### 11.2 create_campaign 输出规则

1. 只有真实委托 `ads-brain-simple-create` 并拿到完整 `create_campaign`，且 `validateCreateCampaignSchema(valid=true)` 时，才能输出结构化创建结果。
2. 准入失败、准入为空、Tool 调用失败、schema 校验失败、客资唯一性命中时，不能输出 JSON 代码块。
3. 新 Pipeline 推荐统一输出 `plan + launch_plan_draft + create_campaign + next_action`，由后续接入层决定展示形式。
4. `create_campaign` 不得因精简版文字长度限制而截断。

### 11.3 客户可见文案硬约束

客户可见文案必须中文化，禁止泄漏：

- 内部枚举码：`MT4`、`MT9`、`MT13`、`MT20`、`MT9_AUTO`、`MT13_AUTO` 等。
- 字段名和数字编码：`biddingStrategy=7`、`targetType=2`、`placement=7` 等。
- apiKey / Tool 名：`query_industry_metrics`、`checkSimpleCreateEligibility` 等。
- 基建摘要中的括号数字：例如“客资收集（9）”“最大转化（7）”。
- 内部过渡语：例如“准入校验通过”“现有基建如下”“下面输出方案”。

必须统一翻译为业务中文名，例如「客资收集」「种草直达」「应用下载」「全自动」「半自动」「稳定成本」「最大转化」「信息流」「搜索」「视频内流」。

---

## 12. 与优化 Pipeline 的回流关系

当用户对创编草案提出“更激进 / 更保守 / 更精准 / 预算怎么分更好”等改善诉求时：

1. 创编 Pipeline 不直接重写完整方案。
2. 转入 Optimize Pipeline，`optimization_context_type=draft_plan`。
3. Optimize Pipeline 输出 `draft_patch` 或 `optimization_plan`。
4. 如用户确认 patch，再回流 S4/S5 重新生成 `launch_plan_draft` / `create_campaign`。

---

## 13. 非目标

本 Skill 不做：

- 不处理存量投放诊断。
- 不处理完整投中优化。
- 不直接执行创建。
- 不维护最终 create schema 细节。
- 不处理客户画像查询主流程。
