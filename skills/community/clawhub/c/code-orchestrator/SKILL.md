---
name: code-orchestrator
description: Route requests across local code exploration, planning, implementation, debugging, refactoring, code security review, safe repo-local command execution, and git hygiene. Use when a coding task inside the current workspace spans multiple stages or when the user explicitly asks which of these coding skills should handle the next step. Do not use for spawning external coding agents, generic skill authoring, or host-level operations. Chinese triggers: 该用哪个技能、先分析还是先写代码、这类任务怎么拆、按什么顺序做、当前代码任务怎么分步.
---

# 编码总控

先判断该调用哪个技能，再决定是否串联多个技能。

如果任务边界不清，先看 [routing-examples.md](references/routing-examples.md) 里的中文示例，再决定路由。

## 路由规则

- 需要了解项目结构、入口、依赖、调用链、数据流时，调用 `$code-explore`
- 需要先出方案、拆步骤、评估风险和实现顺序时，调用 `$code-architect`
- 需要直接写代码、补代码、改逻辑、补测试时，调用 `$code-write`
- 需要定位报错、分析根因、给出最小修复时，调用 `$code-debug`
- 需要在不改行为前提下清理结构和重复逻辑时，调用 `$code-refactor`
- 需要检查漏洞、权限、输入校验、密钥泄露等问题时，调用 `$code-security`
- 需要执行构建、测试、lint、format、安装依赖等安全命令时，调用 `$shell-safe-exec`
- 需要处理分支、提交、历史保护等 Git 事项时，调用 `$git-discipline`

## 编排原则

1. 不要默认把所有技能都用一遍，只选择当前任务真正需要的最小集合。
2. 如果任务边界不清，先探索再决策，不要直接写代码。
3. 如果任务跨多个阶段，按“分析 -> 规划 -> 实现 -> 验证 -> 提交”顺序串联。
4. 如果用户只要单一步骤，就只调用对应技能，不强行增加流程。
5. 如果风险高或影响面大，优先加上验证和安全检查环节。

## 常见流程

- 新功能: `$code-explore` -> `$code-architect` -> `$code-write` -> `$shell-safe-exec`
- 修 bug: `$code-explore` -> `$code-debug` -> `$code-write` -> `$shell-safe-exec`
- 纯重构: `$code-explore` -> `$code-refactor` -> `$shell-safe-exec`
- 安全修复: `$code-explore` -> `$code-security` -> `$code-write` -> `$shell-safe-exec`
- 发布前整理: `$code-explore` -> `$git-discipline`

## 输出

- 选中的技能
- 调用顺序
- 每个技能被选中的原因
- 本轮应执行到哪一步为止
