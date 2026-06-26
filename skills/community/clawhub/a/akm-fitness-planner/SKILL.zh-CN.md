---
name: "akm-fitness-planner"
description: "AKM 在训练决策工作流中的实现，在输出训练决定前先建模目标、身体限制、器械环境、时间预算与恢复状态。"
---

<!--
文件：SKILL.zh-CN.md
核心功能：作为 AKM Fitness skill 的中文正式说明页，定义其定位、输入要求、工作流、输出契约、双语规则与边界。
输入：Fitness 分支方法结构、提示词文件、记录模板与公开 skill 设计。
输出：供 GitHub 中文页、技能市场或代理工具直接引用的中文 skill 文档。
-->

# AKM Fitness Skill

<p align="center">
  <a href="./SKILL.md">English</a> | <a href="./SKILL.zh-CN.md">简体中文</a>
</p>

**没有画像，就没有严肃训练决策。**

AKM Fitness 是一个面向真实约束训练决策的 skill 包。
它处理的是身体限制、器械现实、时间预算、恢复状态和目标层级都会实质影响训练选择的场景。

## 定位

AKM Fitness 不是泛泛的训练问答工具。
它把训练规划重写成“画像优先的决策流程”。

## 必需输入

- `training goals`
- `body limitations or injury constraints`
- `available equipment`
- `weekly frequency`
- `session time budget`
- `recovery context`

缺关键输入时，skill 必须显式输出 `MissingInputs`，而不是伪造确定性。

## 工作流

1. `ELICITATION_PROMPT.md`
2. `RECORD_TEMPLATE.md`
3. `EXECUTION_PROMPT.md`

## 输出契约

输出应包含：

- `StateJudgment`
- `PrimaryDecision`
- `DecisionConfidence`
- `Plan`
- `RiskNotes`
- `NonNegotiables`
- `MissingInputs`

## 双语规则

公开落地页采用英文主页 + 中文切换。
字段 key 保持英文，以保证输出稳定。
实际提示词提供英文版和中文版。

## 边界

- 不是医疗诊断工具
- 不替代康复建议
- 不是健美模板生成器
- 不能用鸡血语言掩盖不确定性
