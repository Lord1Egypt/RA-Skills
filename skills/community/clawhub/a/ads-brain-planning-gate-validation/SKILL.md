---
name: ads-brain-planning-gate-validation
description: 规划 Agent 新框架中的门禁与校验通用协议。定义 Capability Gate、Scenario Gate、Business Guard、Payload Validation、Execution Gate、场景化 Guard、skipped 状态、blocked_reason 与 next_action。
---

# 规划 Agent 门禁与校验协议

## 1. 定位

本 Skill 定义规划 Agent 新框架下的通用门禁与校验协议。

当前阶段只做内容层定义：

- 不接入 `agent-card.json`。
- 不新增 Java Guard 服务。
- 不替换已有校验工具。
- 不直接调用执行 Tool。

本 Skill 供 `ads-brain-planning-pipeline`、`ads-brain-planning-create-pipeline`、`ads-brain-planning-optimize-pipeline` 引用。

---

## 2. 概念定义

| 概念 | 定义 | 是否一定阻断 | 例子 |
|---|---|---:|---|
| Gate 门禁 | 判断当前流程是否允许继续 | 可能 | 简单投准入、标准投不支持 |
| Validation 校验 | 判断输入/输出结构或字段是否合法 | 可能 | schema 校验、必要字段缺失 |
| Guard 条件保护 | 针对特定场景触发的保护逻辑 | 不一定 | 客资唯一性、诊断协作 |
| Block 硬阻断 | 明确不能继续当前流程 | 是 | 不支持投放类型、无权限 |
| Warning 软提醒 | 可以继续，但需要提示风险或假设 | 否 | 数据缺失、默认预算假设 |
| Route Hint 转路由提示 | 当前能力不处理，建议转其他能力 | 是/否 | 创编转优化、标准投转人工 |

---

## 3. 五层门禁与校验

```text
Capability Gate
  ↓
Scenario Gate
  ↓
Business Guard
  ↓
Payload Validation
  ↓
Execution Gate
```

| 层级 | 回答的问题 |
|---|---|
| Capability Gate | 请求应由 create、optimize 还是 unsupported 处理？ |
| Scenario Gate | 进入能力后，当前场景是否支持？ |
| Business Guard | 当前业务约束是否允许继续？ |
| Payload Validation | 当前输入、中间产物或输出结构是否合法？ |
| Execution Gate | 是否可以进入执行确认或真实执行？ |

---

## 4. 统一规则模型

每条规则都应能映射成以下结构。

```json
{
  "rule_id": "string",
  "rule_type": "capability_gate | scenario_gate | business_guard | payload_validation | execution_gate",
  "capability": "create | optimize | common",
  "stage": "string",
  "severity": "block | warn | route | ask | pass",
  "condition": "string",
  "result": {
    "allowed": true,
    "blocked_reason": "string | null",
    "warnings": [],
    "route_hint": "string | null",
    "required_clarifications": [],
    "next_action": "confirm_execution | ask_clarification | unsupported | no_action | continue"
  }
}
```

---

## 5. GateValidationResult

所有门禁与校验最终归一成 `GateValidationResult`。

```json
{
  "allowed": true,
  "final_decision": "pass | block | warn | ask | route",
  "blocked_reasons": [],
  "warnings": [],
  "route_hint": null,
  "required_clarifications": [],
  "next_action": "continue",
  "applied_rules": [
    {
      "rule_id": "string",
      "decision": "pass | block | warn | ask | route",
      "reason": "string"
    }
  ]
}
```

合并优先级：

```text
block > ask > route > warn > pass
```

---

## 6. Capability Gate

| rule_id | 条件 | 决策 | route_hint |
|---|---|---|---|
| `cap_create_intent` | 用户表达新建、创建、冷启、搭计划 | `pass:create` | null |
| `cap_optimize_intent` | 用户表达优化、放量、控成本、提转化、改创意 | `pass:optimize` | null |
| `cap_diagnosis_intent` | 用户表达为什么掉量、为什么成本高、不起量 | `pass:optimize` | `diagnosis_optional` |
| `cap_draft_optimize` | 用户对上一轮创编草案说更激进、更保守、更精准 | `pass:optimize` | `back_to_create_after_patch` |
| `cap_unsupported_standard_create` | 用户明确要求标准投、合约、品专新建 | `block` | `standard_create_or_manual` |
| `cap_ambiguous_mixed_intent` | 用户同时要求新建和优化且优先级不清 | `ask` | null |

---

## 7. Scenario Gate

### 7.1 创编场景门禁

| rule_id | 条件 | 决策 | blocked_reason |
|---|---|---|---|
| `create_simple_supported` | 简单投新建 | `pass` | null |
| `create_standard_unsupported` | `launch_form=standard` 或自然语言明确标准投 | `block` | `unsupported_launch_form` |
| `create_contract_unsupported` | 合约、品专等非简单投 | `block` | `unsupported_create_type` |
| `create_existing_delivery_misroute` | 用户语义指向已有计划优化 | `route` | `misrouted_to_create` |

### 7.2 优化场景门禁

| rule_id | 条件 | 决策 | blocked_reason |
|---|---|---|---|
| `optimize_goal_supported` | 放量、控成本、提转化、改创意、成效预估 | `pass` | null |
| `optimize_draft_supported` | 优化对象是 `launch_plan_draft` | `pass` | null |
| `optimize_missing_context` | 无对象、无草案、无改善目标且无法默认 | `ask` | `missing_optimization_context` |

---

## 8. 场景化 Guard

部分 Guard 只在特定场景触发，不能全局必跑。

### 8.1 设计原则

1. 先识别场景，再触发 Guard。
2. 未命中场景时，Guard 结果为 `skipped`。
3. 需要 Tool/RPC/Evidence 的 Guard 只有命中触发条件才执行。
4. `skipped` 必须记录原因，不能等同于 `passed`。
5. Guard 消费 `scenario_tags`，不要反复让模型猜。

### 8.2 Guard 输出结构

```json
{
  "guard_name": "string",
  "triggered": true,
  "status": "passed | blocked | warned | routed | skipped",
  "skip_reason": "string | null",
  "decision_reason": "string",
  "payload": {}
}
```

### 8.3 场景化 Guard 表

| Guard | 触发场景 | 不触发时 | 触发后动作 |
|---|---|---|---|
| `lead_generation_unique_guard` | `marketing_goal=lead_generation` 或用户明确客资收集 | `skipped:not_lead_generation` | 调客资唯一性检查，已存在则阻断新建或建议优化已有计划 |
| `simple_create_eligibility_guard` | `capability=create` 且 `create_scene=simple_create` | `skipped:not_simple_create` | 调准入检查，限制可用创建选项或阻断 |
| `standard_launch_form_guard` | `launch_form=standard` 或自然语言明确标准投 | `skipped:not_standard_launch_form` | 当前简单投创编直接 unsupported |
| `draft_patch_guard` | `capability=optimize` 且上下文是 `draft_plan` | `skipped:not_draft_plan` | 输出 draft patch，回流创编/simple-create |
| `diagnosis_collaboration_guard` | 用户问“为什么”或数据出现异常信号 | `skipped:no_diagnosis_intent_or_signal` | 调诊断能力或引用诊断结果 |
| `execution_confirmation_guard` | `next_action=confirm_execution` 且存在 payload/action | `skipped:no_executable_payload` | 生成确认卡片，等待用户确认 |
| `budget_risk_guard` | 预算超阈值、大幅调预算或预算缺失不可默认 | `skipped:no_budget_risk` | warn 或 ask_clarification |
| `force_refresh_guard` | 用户修改预算/目标/对象/时间窗口等影响数据有效性的字段 | `skipped:no_context_change` | 触发重新取数或标记 Evidence stale |

### 8.4 scenario_tags

上下文归一化阶段应生成 `scenario_tags`：

```json
{
  "scenario_tags": [
    "simple_create",
    "lead_generation",
    "draft_plan_optimize",
    "diagnosis_intent",
    "budget_changed"
  ],
  "scenario_confidence": {
    "lead_generation": "high",
    "diagnosis_intent": "medium"
  }
}
```

---

## 9. 控制规则目录

本协议是新框架中门禁与校验的统一控制面。创编和优化 Pipeline 只需要消费这里定义的 rule / guard / validation，不需要在各自正文中重复发明控制规则。

### 9.1 创编控制规则

| 业务约束 | 新规则类型 | rule / guard | 行为 |
|---|---|---|---|
| 非简单投识别 | Scenario Gate | `create_standard_unsupported` / `create_contract_unsupported` | 标准投、合约、品专等不进入简单投创编 |
| 简单投准入检查 | Business Guard | `guard_simple_create_eligibility` | 准入失败或全集为空时，不输出 `create_campaign` |
| 客资唯一计划检查 | 场景化 Guard | `lead_generation_unique_guard` | 仅明确客资收集时触发，已存在则不新建 |
| 客资全自动限制 | Business Guard | `guard_lead_generation_unique` / `validate_launch_plan_draft` | 客资收集只支持全自动，半自动诉求不生成 `create_campaign` |
| create_campaign 字段白名单 | Payload Validation | `validate_create_campaign_schema` | schema 校验失败不进入执行确认 |
| 渐进式方案输出 | Payload Validation / Output Guard | `validate_launch_plan_draft` / `next_action` | 首轮精简版，详情追问再展开 |
| 枚举码/字段名外泄禁止 | Payload Validation / Output Guard | `validate_customer_visible_text` | 客户可见文案必须中文化 |

### 9.2 优化控制规则

| 业务约束 | 新规则类型 | rule / guard | 行为 |
|---|---|---|---|
| 优化类型识别 | Capability / Scenario Gate | `cap_optimize_intent` / `optimize_goal_supported` | 放量、控成本、改创意、成效预估进入优化 |
| 自主查数 | Business Guard / Evidence Guard | `guard_evidence_collection` | 按目标选择查询维度，失败降级 |
| 批量查询纪律 | Business Guard | `guard_evidence_batching` | ≥2 个 apiKey 使用批量 queries，pending 不重试 |
| 诊断协作 | 场景化 Guard | `diagnosis_collaboration_guard` | 问原因或异常信号明显时调用诊断 |
| 精简版输出 | Payload Validation / Output Guard | `validate_optimization_plan` | 首轮 3～5 条核心动作，每条有依据和动作 |
| 风险护栏 | Business Guard | `guard_budget_safety` / `guard_execution_confirmation` | 调幅、冷启、批量范围、策略冲突只提示和分阶段 |
| 不直接执行修改 | Execution Gate | `exec_requires_confirmation` | 有 action 也必须先确认 |
| 内部字段外泄禁止 | Payload Validation / Output Guard | `validate_customer_visible_text` | 禁止输出字段名、apiKey、数字编码 |

### 9.3 需要补充的通用输出校验

当前协议层建议新增一个逻辑校验项：

| rule_id | 校验对象 | 作用 |
|---|---|---|
| `validate_customer_visible_text` | 用户可见自然语言 | 禁止思考过程、内部字段、枚举码、数字编码、apiKey、Tool 名、内部过渡语外泄 |
| `validate_next_action_consistency` | 输出整体 | 确保 `blocked_reason`、`gate_validation.final_decision` 与 `next_action` 一致 |
| `validate_guard_skipped_reason` | Guard 结果 | 确保未触发的场景化 Guard 标记 `skipped` 而非 `passed` |

---

## 10. Business Guard

| rule_id | capability | 触发条件 | 决策 |
|---|---|---|---|
| `guard_simple_create_eligibility` | create | 简单投准入检查 | `pass` / `block` / `warn` |
| `guard_lead_generation_unique` | create | 客资收集场景 | `pass` / `block` / `route` |
| `guard_budget_safety` | create / optimize | 预算明显异常或缺失 | `warn` / `ask` |
| `guard_draft_patch` | optimize | 优化对象是待创建草案 | `pass`，输出 draft patch |
| `guard_diagnosis_collaboration` | optimize | 用户问原因或数据异常 | `pass`，可调用诊断 |
| `guard_execution_confirmation` | create / optimize | 存在可执行 payload/action | `pass`，进入执行确认 |

---

## 11. Payload Validation

| rule_id | 校验对象 | 决策 |
|---|---|---|
| `validate_context_required_fields` | 归一化上下文 | `pass` / `ask` |
| `validate_launch_plan_draft` | `launch_plan_draft` | `pass` / `ask` / `block` |
| `validate_create_campaign_schema` | `create_campaign` | `pass` / `block` |
| `validate_optimization_plan` | `optimization_plan` | `pass` / `warn` / `ask` |
| `validate_execution_action` | `execution_action` | `pass` / `block` |

校验原则：

1. 缺字段但可安全默认：`warn`，并写入 `assumptions`。
2. 缺字段且不能安全默认：`ask`。
3. 字段非法且不可修复：`block`。
4. 字段非法但可修复：修复后记录 `warnings`。

---

## 12. Execution Gate

| rule_id | 条件 | 决策 |
|---|---|---|
| `exec_payload_exists` | 存在可执行 payload/action | `pass` |
| `exec_payload_valid` | payload 校验通过 | `pass` |
| `exec_requires_confirmation` | 动作会修改线上投放 | `pass:confirm_execution` |
| `exec_missing_confirmation_template` | 缺确认卡片模板 | `block` |
| `exec_risk_requires_warning` | 高风险动作，如大幅加预算 | `warn` |

---

## 13. blocked_reason 枚举

| blocked_reason | 含义 |
|---|---|
| `missing_advertiser_id` | 缺少广告主 ID |
| `unsupported_launch_form` | 不支持当前投放形式 |
| `unsupported_create_type` | 不支持当前新建类型 |
| `misrouted_to_create` | 优化请求误入创编 |
| `misrouted_to_optimize` | 创编请求误入优化 |
| `simple_create_not_eligible` | 简单投准入不通过 |
| `lead_generation_campaign_exists` | 客资唯一计划已存在 |
| `missing_required_context` | 缺少必要上下文 |
| `invalid_launch_plan_draft` | 创编草案非法 |
| `create_campaign_schema_invalid` | 创建 payload schema 非法 |
| `missing_optimization_context` | 缺少优化上下文 |
| `invalid_optimization_plan` | 优化方案非法 |
| `execution_payload_invalid` | 执行 payload 非法 |
| `confirmation_template_missing` | 缺少确认卡片模板 |

---

## 14. next_action 枚举

| next_action | 含义 |
|---|---|
| `continue` | 继续当前流程 |
| `confirm_execution` | 进入执行确认 |
| `ask_clarification` | 追问用户 |
| `unsupported` | 当前能力不支持 |
| `route` | 建议转其他能力 |
| `no_action` | 只回答，不进入后续动作 |

---

## 15. 接入建议

当前阶段：

- 只作为内容层协议被其他新 Pipeline Skill 引用。
- 不要求 Java 强制执行。
- 不要求 agent-card 暴露。

后续可分阶段接入：

1. Prompt 文档接入。
2. 结构化输出协议接入。
3. JSON/YAML 规则配置接入。
4. Java Guard 服务接入。
5. 测试与观测接入。
