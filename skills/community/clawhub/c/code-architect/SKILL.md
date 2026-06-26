---
name: code-architect
description: Design a minimal implementation plan that fits the existing local codebase. Use when the user asks for architecture, feature design, task breakdown, migration planning, complexity analysis, or risk assessment before coding inside the current workspace. Do not use for generic skill creation or external agent delegation plans. Chinese triggers: 设计方案、架构规划、任务拆分、评估复杂度、实现顺序、风险分析.
---

# 架构规划

给出最小可落地方案，不做空转设计。

## 工作流

1. 根据代码库和上下文确认目标、约束与现有架构。
2. 优先复用现有抽象、命名和模块边界，不平地再起一套。
3. 把任务拆成可以独立实现、独立验证的小步骤。
4. 优先选择能上线的方案，而不是过度抽象或大重构。
5. 提前指出兼容性、迁移、失败路径、性能、并发和安全风险。
6. 如果上下文不完整，明确写出假设条件。

## 输出

- 目标
- 实现步骤
- 可能涉及的文件或模块
- 风险与约束
- 建议执行顺序
- 验证方案
