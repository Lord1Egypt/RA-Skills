# Coordinator Evolution Framework

A high-order cognitive framework for AI agents to evolve from a simple "Tool User" to a "Task Coordinator".

## 🇨🇳 中文指南

### 什么是协调者模式？
协调者模式是一种高级的 AI 行为准则，旨在解决复杂任务中常见的“执行偏差”和“逻辑断层”问题。它将 AI 的角色定义为一名**协调者 (Coordinator)**，而非简单的执行员。

### 核心能力
1. **强制结果合成**：拒绝模糊委派。在调用执行工具前，必须将研究结果转化为极其具体的执行规格书。
2. **原子化调度**：将任务拆解为可追踪的原子单元，并利用并行处理提升效率。
3. **动态上下文**：在任务开始前自动构建环境快照，确保决策基于实时状态。
4. **验证闭环**：所有变更必须经过独立验证，拒绝“我认为写好了”的盲目提交。

### 如何使用
将本技能加载至您的 AI 助手，并在系统提示词中要求其遵循 `coordinator-evolution` 逻辑。

---

## 🇺🇸 English Guide

### What is Coordinator Mode?
The Coordinator Mode is a high-order cognitive framework designed to eliminate "execution drift" and "logical gaps" in complex AI workflows. It re-positions the AI as a **Coordinator** rather than a mere executor.

### Core Capabilities
1. **Mandatory Synthesis**: Bans vague delegations. Before executing, the agent must synthesize fragmented research into a precise specification (paths, line numbers, exact changes).
2. **Atomic Scheduling**: Decomposes goals into trackable atomic tasks with a state machine (Pending -> Running -> Terminal), leveraging parallelism for research.
3. **Dynamic Context**: Automatically injects system snapshots (Git status, env) at task start to ensure grounded decision-making.
4. **Verification Loop**: Implements a strict "Execute -> Verify -> Correct" cycle, ensuring all deliverables are proven working.

### How to Use
Load this skill into your AI agent and instruct it to follow the `coordinator-evolution` logic in its system prompt.
