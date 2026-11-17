# 实战模式卡片

从 AI 公司的工程博客、客户案例和开发者实践中提取的
可复用模式。每张卡片回答三个问题：

1. **这个模式解决了什么问题？**（问题本质）
2. **为什么它有效？**（关键洞察）
3. **我的用户能从中得到什么？**（对 Carpe Diem 的启发）

## 可用卡片

| 卡片 | 问题本质 | 适用阶段 |
|------|----------|----------|
| [Claude Code 最佳实践](claude-code-best-practices.md) | 如何最大化 AI Coding Agent 的产出质量，减少无效迭代 | Discover, Validate, Plan |
| [构建有效的 AI Agent](building-effective-agents.md) | 如何在 Agent 自主性和可控性之间找到平衡 | Discover, Validate, Plan |
| [AI Agent 的上下文工程](context-engineering.md) | 如何高效组织和管理 Agent 的上下文，避免注意力稀释 | Discover, Validate, Plan |
| [用 Agent Skills 装备真实世界的 Agent](agent-skills.md) | 如何将领域知识打包为可复用模块，让 Agent 按需加载 | Discover, Validate, Plan |

## 自动加载

SKILL.md 的"每次调用"流程第5步会根据当前阶段自动匹配并加载以上卡片。
卡片需包含对应阶段的小节指引才能被加载。