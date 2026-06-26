#### Antigravity 介绍与使用指南

---

## name: antigravity-introduction
description: 提供关于 Google Antigravity IDE 的全面介绍、核心功能解析及最佳实践指南。当用户询问“什么是 Antigravity”、“如何使用 Antigravity”或需要了解其 Agent 优先理念时使用。
keywords: ["antigravity", "google ide", "ai coding", "agent-first", "gemini", "vibe coding"]

#### Antigravity 深度指南

**目标**
帮助用户理解并掌握 Google Antigravity 的核心概念，使其能够从传统 IDE 思维转变为 Agent-First（智能体优先）的开发模式。

#### 核心概念解析

Antigravity 是 Google 于 2025 年末发布的 Agent-First IDE（智能体优先集成开发环境）。它不仅仅是代码编辑器，更是一个让 AI 代理（Agent）作为核心开发者的平台。

- **Agent-First 理念**：不同于传统 IDE 将 AI 作为辅助插件，Antigravity 将 AI 置于工作流的中心。用户通过自然语言描述需求，由 Agent 负责规划、编写代码、调试和测试。
- **多模型支持**：原生支持 Google Gemini 3 Pro、Deep Think、Flash 以及 Anthropic 的 Claude Sonnet 4.5 和 Opus 4.5。
- **Mission Control**：内置面板，允许用户同时管理和监控多个并行工作的智能体。
- **Skills 系统**：允许用户通过简单的文件结构（SKILL.md）扩展 Agent 的能力，实现工作流的标准化和复用。

#### 使用场景与最佳实践

1. **Vibe Coding（氛围编程）**：
- **描述**：用户专注于逻辑和创意，将具体的语法实现、样板代码交给 Agent。
- **操作**：在对话框中输入自然语言需求，例如“创建一个响应式的登录页面，使用 Tailwind CSS”。
2. **Skills 的应用**：
- **项目专属技能**：将团队规范、特定框架的最佳实践封装在 `.agent/skills/` 目录下。
- **全局技能**：将通用的开发工具（如 Git 提交规范、代码审查流程）封装在 `~/.gemini/antigravity/skills/` 目录下。
3. **异步反馈**：
- 利用浏览器截图功能，直接在视觉层面上给 Agent 提供反馈，例如“把这个按钮的颜色调暗一点”。

#### 常见问题解答

- **Q: Antigravity 和 VS Code 有什么区别？**
- **A**：Antigravity 基于 VS Code 分支，但深度集成了 Agent 能力，底层架构针对异步 AI 任务进行了优化（参考了 Windsurf 的技术）。
- **Q: 如何安装 Skills？**
- **A**：通常通过 Git Clone 官方或社区的 Skills 仓库到指定目录，或者手动创建包含 `SKILL.md` 的文件夹。

#### 示例对话

**用户**：“帮我介绍一下 Antigravity 的 Skill 系统。”
**Agent**：“Antigravity 的 Skill 系统是一套开放标准，允许你通过 Markdown 文件教 Agent 学习新技能。比如你可以创建一个 Skill 来规范 Git 提交信息。只需在项目中创建 `.agent/skills/my-skill/SKILL.md`，写入指令，Agent 就会自动识别并执行。”

