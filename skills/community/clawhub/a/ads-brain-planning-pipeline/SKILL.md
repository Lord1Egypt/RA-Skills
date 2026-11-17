---
name: ads-brain-planning-pipeline
description: 规划 Agent 新框架内容层通用 Pipeline。用于沉淀创编/优化能力分流、会话状态识别、门禁校验、统一输出协议与后续接入约定；当前暂不接 agent-card 路由。
---

# 规划 Agent 通用 Pipeline

## 1. 定位

本 Skill 是规划 Agent 新框架的内容层总入口，用于定义进入 AgentLoop 后的通用 Pipeline 规则。

本 Skill 是新内容框架的总入口，目标是**完整替换规划主线的内容组织方式**，而不是在运行时依赖其他规划 Skill。

新 Pipeline 由三类子能力组成：

- `create` 能力负责投前创编，覆盖数据查询纪律、Evidence Pack 复用、简单投准入、客资唯一性、渐进式输出、枚举码/字段名外泄约束、simple-create 委托规则。
- `optimize` 能力负责投放优化，覆盖扩量/控成本/改创意/成效预估的数据查询维度、批量查询纪律、诊断协作、精简版首轮输出、风险护栏、中文化与内部字段外泄约束。
- `gate-validation` 能力负责统一控制面，覆盖门禁、校验、阻断、场景化 Guard 和下一步动作。

当前阶段只做内容层沉淀：

- 暂不接入 `agent-card.json`。
- 暂不修改 Java 编排。
- 暂不影响现有线上路由。
- 不直接执行投放动作。

本 Skill 只定义新框架下通用流程，供后续灰度、调试或正式接入时复用。

---

## 2. 设计目标

进入 AgentLoop 后，先完成通用 Pipeline 判断：

1. 识别本轮能力类型。
2. 识别会话状态。
3. 执行必要门禁与校验。
4. 分流到创编 Pipeline 或优化 Pipeline。
5. 统一输出 `gate_validation`、`warnings` 与 `next_action`。
6. 让业务细节全部落在新状态机和新控制面中，避免框架抽象导致业务约束丢失。

---

## 3. 能力类型

当前新框架只考虑两类一等能力。

| capability | 含义 | 对应 Pipeline |
|---|---|---|
| `create` | 从经营诉求出发，生成新建投放方案、`launch_plan_draft`，必要时生成 `create_campaign` | `ads-brain-planning-create-pipeline` |
| `optimize` | 围绕投放改善目标生成优化策略，诊断只是可选依据 | `ads-brain-planning-optimize-pipeline` |
| `unsupported` | 当前请求不适合由本 Pipeline 处理 | 本 Skill 输出不支持原因与可选 route hint |

`query-customer-profile` 本轮不纳入新框架主线。

---

## 4. 顶层流程

```text
用户请求 / conversation_history
  ↓
Capability Gate：识别 create / optimize / unsupported
  ↓
Conversation State：识别首轮、确认、调整、解释、重启
  ↓
Gate Validation：执行通用门禁、场景化 Guard、必要校验
  ↓
分流：Create Pipeline 或 Optimize Pipeline
  ↓
统一输出：capability + gate_validation + result + next_action
```

---

## 5. Capability Gate

### 5.1 进入 create

满足任一条件：

- 用户明确表达新建广告计划、创建投放、搭计划、冷启方案。
- 用户没有指定明确存量计划/单元/创意对象，但要求生成投放方案。
- 上一轮已有创编草案，本轮用户在确认、局部调整或展开解释。

### 5.2 进入 optimize

满足任一条件：

- 用户表达优化、放量、控成本、提转化、改创意、成效预估。
- 用户要求对已有账户、计划、单元、创意、素材做改善。
- 用户要求对待创建草案做改善，例如“再激进一点”“人群再精准一点”。
- 用户只给出改善目标，例如“想更稳一点”“想多放量”。
- 用户明确问“为什么掉量 / 为什么成本高 / 为什么不起量”。这类请求进入 optimize 后，由诊断协作 Guard 判断是否调用诊断能力。

### 5.3 进入 unsupported

满足任一条件：

- 用户明确要求标准投、合约、品专等当前不支持的新建场景。
- 用户同时要求新建与优化，且无法判断优先级。
- 缺少继续处理的必要上下文，且无法安全默认。

---

## 6. Conversation State

### 6.1 create 会话状态

| 状态 | 条件 | 行为 |
|---|---|---|
| `first_turn` | 无历史创编产物 | 进入 Create Pipeline S1 |
| `confirm_create` | 已有 `create_campaign`，用户确认执行 | 复用最近产物，进入执行确认前置判断 |
| `revise_partial` | 用户只改预算、地域、人群、时间等局部字段 | 局部修改 `launch_plan_draft`，再走 simple-create |
| `optimize_draft` | 用户要求草案更激进、更保守、更精准 | 转入 Optimize Pipeline，输出 draft patch |
| `explain_plan` | 用户要求解释方案依据 | 只解释，不重新生成 `create_campaign` |
| `restart_create` | 用户换目标或要求重做 | 重新进入 Create Pipeline S1 |

### 6.2 optimize 会话状态

| 状态 | 条件 | 行为 |
|---|---|---|
| `first_turn` | 无历史优化产物 | 进入 Optimize Pipeline O1 |
| `confirm_action` | 用户确认执行某个优化动作 | 如有合法 action，进入执行确认前置判断 |
| `explain_optimization` | 用户追问原因或依据 | 复用上一轮分析展开 |
| `revise_optimization` | 用户要求换优化方向 | 重新进入 O2 |
| `restart_optimize` | 用户换对象或换目标 | 重新进入 O1 |

---

## 7. Gate Validation 统一协议

本 Pipeline 统一引用 `ads-brain-planning-gate-validation` 中定义的门禁与校验协议。

所有能力输出都应包含：

```json
{
  "gate_validation": {
    "allowed": true,
    "final_decision": "pass | block | warn | ask | route",
    "blocked_reasons": [],
    "warnings": [],
    "route_hint": null,
    "required_clarifications": [],
    "next_action": "continue | confirm_execution | ask_clarification | unsupported | no_action",
    "applied_rules": []
  }
}
```

规则合并优先级：

```text
block > ask > route > warn > pass
```

---

## 8. 输出协议

### 8.1 create 输出

```json
{
  "capability": "create",
  "conversation_state": "first_turn | confirm_create | revise_partial | optimize_draft | explain_plan | restart_create",
  "gate_validation": {},
  "plan": "string | null",
  "launch_plan_draft": {},
  "create_campaign": {},
  "warnings": [],
  "next_action": "confirm_execution | ask_clarification | unsupported | no_action"
}
```

### 8.2 optimize 输出

```json
{
  "capability": "optimize",
  "conversation_state": "first_turn | confirm_action | explain_optimization | revise_optimization | restart_optimize",
  "gate_validation": {},
  "optimization_context_type": "existing_delivery | draft_plan | strategy_variable | goal_only | unknown",
  "optimization_goal": "scale | cost_control | conversion | creative | forecast | strategy_refine | diagnose | unknown",
  "diagnosis_ref": null,
  "optimization_plan": {},
  "execution_action": null,
  "warnings": [],
  "next_action": "confirm_execution | ask_clarification | no_action"
}
```

### 8.3 unsupported 输出

```json
{
  "capability": "unsupported",
  "gate_validation": {},
  "unsupported_reason": "string",
  "route_hint": "string | null",
  "warnings": [],
  "next_action": "ask_clarification | unsupported | no_action"
}
```

---

## 9. 与子 Pipeline 的关系

| 子 Pipeline | 职责 |
|---|---|
| `ads-brain-planning-create-pipeline` | 承载 S0～S6 创编状态机，输出 `plan`、`launch_plan_draft`、`create_campaign` |
| `ads-brain-planning-optimize-pipeline` | 承载 O0～O6 优化状态机，输出 `optimization_plan`，必要时引用诊断结果 |
| `ads-brain-planning-gate-validation` | 承载 Capability Gate、Scenario Gate、Business Guard、Payload Validation、Execution Gate |

---

## 10. 非目标

本 Skill 当前不做：

- 不新增 A2A skill 路由。
- 当前暂不影响线上 planning / optimize 路由。
- 不直接调用执行 Tool。
- 不新增 Java Guard 服务。
- 不维护 `create_campaign` 字段细节。
- 不处理画像查询主流程。

---

## 11. 后续接入建议

推荐顺序：

1. 本地验证新 Pipeline 内容是否可读、可执行。
2. 用 harness 针对典型 create / optimize 输入验证状态识别和输出结构。
3. 再考虑把 `planning-pipeline` 加入 `agent-card.json` 做灰度入口。
4. 最后再评估是否将部分门禁下沉为 Java Guard 服务。
