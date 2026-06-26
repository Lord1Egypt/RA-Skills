---
schema_version: "1.0"
document_type: handoff
task_id: ""           # 格式：{项目前缀}-{阶段}-{序号}
created: ""           # ISO-8601 时间戳
sender:
  agent: ""            # AGENT_REGISTRY 中的 agent id
  role: ""
receiver:
  agent: ""            # AGENT_REGISTRY 中的 agent id
  role: ""
status: submitted      # submitted | working | input-required | completed | failed
priority: P0           # P0=阻塞 | P1=重要 | P2=优化
depends_on: []         # 上游任务ID列表
produces: []           # 产出任务ID列表
forbidden_terms_checked: false
---

## 目标

（必填：一句话说明本次交接要达成什么。格式：`{动作} → {产出}`）

## 当前状态

（必填：上游做到哪了。包括已完成的所有关键产物、已达成的关键决策。）

## 来源依据

（推荐：已做的决策及理由。引用 DECISION_LOG.md 中的 decision_id。）

## 上游依赖

（必填：接收者必读的文件路径，精确到文件名。每份文件一行，说明"读什么"。）

| 路径 | 读什么 |
|------|--------|
| | |

## 下游产物

（必填：接收者必须产出的文件路径，精确到文件名。）

| 路径 | 说明 |
|------|------|
| | |

## 接手建议

（必填：具体执行步骤，非聊天摘要。）

1.

## 约束与禁区

（必填：不能做的事。引用 FORBIDDEN_TERMS.yaml 中的类别。）

- **禁用词**：不得出现（内部代号列表）
- **高风险表达**：（需条件的表达及使用条件）
- **其他约束**：（如有）

## 验证标准

**通过条件：**
1.
2.

**退回条件：**
- 发现任何 P0 禁用词违规
- 产物未写入约定路径
- （其他）
