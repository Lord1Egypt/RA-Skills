# 技能编排器（Orchestration / Composer）

> 把多个**厚原子技能**串成一条工作流，由一个**薄编排器技能**调度。对应最高准则"厚技能 + 薄 harness"——原子技能厚（含逻辑/脚本），编排器薄（只描述顺序/分支/门/降级）。

## 一、为什么需要编排器

- 真实业务流是**多步、有条件、有人工门、会失败**的（如 询价→库存→支付→通知）。
- 不要做一个硕大无比的"超级技能"；应拆成可复用原子技能，再用编排器组合。
- 编排器本身应保持薄：声明式描述控制流，不内嵌业务细节。

## 二、五类编排模式

| 模式 | 适用 | 控制流 |
|------|------|--------|
| **串行 Sequential** | 步骤强依赖、上步输出是下步输入 | A → B → C |
| **并行 Parallel** | 步骤独立、可并发 | A ∥ B → 汇聚 |
| **条件 Conditional** | 按状态/结果分支 | if status==X then A else B |
| **人工门 Human Gate** | 高风险/不可逆动作前 | ... → [确认] → 写动作 |
| **降级 Fallback** | 某步失败要有兜底 | try A; on_fail → B/告警/回滚 |

## 三、编排器 SKILL.md 结构（生成器见 `scripts/compose.py`）

```yaml
name: <orchestrator-name>
description: 当用户要完成"<端到端目标>"时使用；按顺序调度以下原子技能。
mode: orchestrator
steps:
  - skill: validate-order      # 原子技能（厚）
    type: atomic
  - skill: check-inventory
    type: atomic
  - skill: charge-payment
    type: atomic
    human_gate: true           # 写钱前人工确认
  - skill: notify-customer
    type: atomic
    on_fail: fallback-notify    # 失败兜底
```

编排器只写"调用谁、什么顺序、哪里要确认、失败怎么办"，业务逻辑全在原子技能里。

## 四、编排自审清单

- [ ] 编排器薄（无业务细节，只描述控制流）？
- [ ] 原子技能厚且可独立复用？
- [ ] 写/不可逆步骤前有 human gate？
- [ ] 每步失败有 fallback/回滚/告警？
- [ ] 跨技能传递的数据有 schema 约束（见 process-systems 强 schema）？
- [ ] 端到端有 trace id 贯穿（见 agentic-governance 可观测）？
