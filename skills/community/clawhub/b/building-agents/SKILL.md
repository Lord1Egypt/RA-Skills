---
name: building-agents
slug: building-agents
display_name: "构建 AI Agent 实战指南"
displayName: "构建 AI Agent 实战指南"
description: 【构建 AI Agent 实战指南】把 OpenAI《A Practical Guide to Building Agents》蒸馏成可执行的 Agent 设计方法论。覆盖：判断是否该建 Agent（vs 规则引擎）、Agent 三组件（Model/Tools/Instructions）、模型选型、工具设计、写 agent instructions、单/多智能体编排（Manager/Decentralized 模式）、Guardrails 与 human-in-the-loop。当用户说"帮我设计一个 agent""single agent 还是 multi-agent""怎么写 agent 指令""agent 工具怎么设计""agent 需要哪些 guardrails""该不该上 agent""agent 编排模式怎么选"时使用。
agent_created: true
version: 1.0.0
category: productivity
emoji: "🤖"
author: jiaxinmmhh
platforms:
  - WorkBuddy
  - QClaw
  - ima
  - Claude Code
  - Cursor
---

# Building Agents — 实战指南

把 OpenAI 的《A Practical Guide to Building Agents》变成**可照做的设计方法论**。不是 RAG 检索原文，而是把"怎么设计一个可靠 Agent"内化为决策规则、反模式、模板，让你边设计边套用。

## 何时用这个技能

- 判断一个需求**该不该用 Agent**（还是确定性脚本就够）
- 设计 Agent 的 **Model / Tools / Instructions** 三组件
- 模型选型、工具设计、写 agent instructions
- 选编排模式：**single agent** vs **multi-agent（Manager / Decentralized）**
- 设计 **Guardrails**（分层防御 + human-in-the-loop）

## 核心心智

- Agent = LLM 控制工作流执行 + Tools + Instructions + Guardrails。简单 chatbot / 单轮LLM / 分类器**不是** agent。
- **先判断是否该建**：传统规则搞不定的（微妙判断、规则难维护、非结构化数据）才上 agent。
- **渐进式**：从 single agent + 工具开始，必要时才演化到 multi-agent。
- **Guardrails 是分层防御**，且必须配合认证授权、访问控制、标准安全。

## 怎么用

1. 读 `references/building-agents.md` 获取完整程序化知识（决策规则、反模式、模板、章节映射）。
2. 按需求定位：
   - 该不该建 → §1 决策规则 + 验证清单
   - 三组件 / 选型 / 工具 / instructions → §2–§5
   - 编排模式选型 → §6（single / Manager / Decentralized + 拆分时机）
   - Guardrails → §7（类型表 + 构建 heuristic + human intervention 触发）
3. 关键技术决策用里面的 IF/ELSE 规则与 Quick reference 决策表直接套。

## 内容边界

- 偏**设计方法论与架构决策**，不含具体框架的逐行代码（原书示例基于 OpenAI Agents SDK，模式可移植到任意库或手写）。
- 安全部分给出分层防御思路与 human-in-the-loop 触发条件，落地时请结合你自己的认证授权与访问控制。

## 验证要点（交付前自检）

- 是否先回答了"该不该建 agent"？避免为简单任务过度工程。
- 三组件是否齐全（model + tools + instructions），工具是否标准化定义、无重叠歧义？
- 编排是否从 single 起步？多 agent 是否有明确拆分理由（复杂逻辑 / 工具过载）？
- Guardrails 是否分层（relevance / safety / PII / moderation / tool safeguards）且含 human-in-the-loop 触发？
