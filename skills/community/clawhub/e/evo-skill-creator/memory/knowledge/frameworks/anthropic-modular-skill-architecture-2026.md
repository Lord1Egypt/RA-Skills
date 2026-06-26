# Anthropic Modular Skill Architecture (2026)

> 学习次数：1 | 创建：2026-03-29 | 更新：2026-03-29
> 来源：WebSearch 综合多个来源
> 类别：frameworks | 波动性：medium | 置信度：high

## 核心概念

Anthropic 在 2026 年推出的模块化 Skill 架构，将 AI Agent 从"单体 Prompt"转向**可组合、可复用的模块化组件（Agent Skills）**。

### 关键定义

- **Claude 不是 Agent，而是推理引擎**：Claude 本身是推理核心，"Claude Agents" 是围绕引擎构建的应用层
- **Skills 是可组合模块**：独立的文件夹/包，包含特定能力的指令、工具和配置
- **按需加载**：仅在触发时加载完整指令，避免上下文窗口耗尽

## Skill 标准结构（2026 规范）

```
skill/
├── SKILL.md          # [必需] 指令核心，含 YAML frontmatter 元数据
├── scripts/          # [可选] 确定性逻辑（计算、API 调用、文件操作）
├── references/       # [可选] 密集领域知识（编码标准、品牌指南）
└── assets/           # [可选] 模板或静态文件
```

### SKILL.md 设计要点

- YAML frontmatter 中的 description 是**最重要的部分**——决定 Claude 何时"发现"并触发此 Skill
- 控制在 ~500 行以内，超出则拆分到 references/
- 触发关键词要具体、唯一

## 三层架构

1. **输入与上下文管理** — 准备推理环境
2. **推理/编排** — Claude 核心逻辑决定调用哪些 Skills
3. **执行** — Skill 触发的实际工具调用或脚本执行

## 核心设计原则

### 1. 渐进式披露（Token 经济）

- 元数据轻量展示，完整指令按需加载
- 触发关键词决定加载时机
- 避免预加载所有 Skill 到上下文窗口

### 2. 单一职责与可组合性

- **反模式**：Mega-Skill（一个 Skill 做所有事）
- **最佳实践**：Micro-Skills 套件，通过编排器链式调用
- 每个 Skill 只做一件事，组合成复杂工作流

### 3. 确定性 vs 概率性逻辑分离

- **LLM（概率性）**：推理、摘要、自然语言理解
- **脚本（确定性）**：数据验证、API 交互、文件 IO、数学计算
- **经验法则**：如果两次运行需要完全相同的输出，不要信任 LLM——写脚本

### 4. 职责分离

- **Agents**：负责决策和规划
- **Tools/MCP Servers**：提供外部能力（数据库、Slack、API）
- **Skills**：编码"配方"——如何使用 Agents 和 Tools 解决特定业务问题

## Agent Teams（2026 新模式）

从"子 Agent 黑盒调用"升级为"可见、持久、可通信的多 Agent 团队"。

### 与传统 Sub-agent 的区别

| 维度 | Sub-agent（旧模式） | Agent Teams（2026） |
|------|---------------------|---------------------|
| 通信 | 只返回最终结果 | 直接互相消息 |
| 可见性 | 黑盒 | tmux/分屏可监控 |
| 协作 | 无 | 共享任务列表 |
| 上下文 | 隔离 | 可共享 |

### 编排模式

1. **Fan-out & Fan-in**：Team Lead 分解任务 → 分发给专门 Teammates → 合成结果
2. **Autonomous ReAct Loops**：每个 Agent 内部自主 ReAct 循环
3. **冲突解决**：LLM-based 结果合成，需 Reviewer Agent 签字
4. **Inbox 模式**：文件系统级通信（`~/.claude/teams/{name}/inboxes/{agent}.json`）

## Meta-Skill 模式

- 构建一个"skill-creator" skill，用它来生成新 Skill 的目录结构、验证逻辑和初始 SKILL.md
- 这正是我们 evo-skill-creator 的实践！

## 与我们的进化模型对比

### 我们已经做对的

1. **模块化结构**：我们的 SKILL.md + memory/ + output/ 符合标准结构
2. **Meta-Skill 模式**：evo-skill-creator 就是 Meta-Skill
3. **references/ 分离**：我们已经将 evo-agent-model.md 和 model-capability.md 放在 references/
4. **按需加载**：memory 文件按命令相关性选择性加载

### 我们的差距

1. **YAML frontmatter 元数据**：我们的 SKILL.md 缺少标准化的 YAML frontmatter（name、description、trigger keywords）
2. **确定性逻辑分离**：我们几乎没有 scripts/ 目录，所有逻辑都在 SKILL.md 中
3. **Micro-Skills 套件**：我们的 Skill 偏大，缺少微粒度拆分
4. **Agent Teams 协作**：子智能体之间不能直接通信，只能通过创建者中转
5. **编排层缺失**：没有 DAG 编排或 Fan-out/Fan-in 模式
6. **触发关键词精度**：部分 Skill 的触发描述不够精确

### 改进方向

1. **短期**：为子智能体 SKILL.md 添加标准化 YAML frontmatter
2. **短期**：在创建子智能体时增加 scripts/ 目录引导
3. **中期**：引入确定性逻辑分离原则到 evo-agent-model.md
4. **中期**：设计子智能体间的直接通信机制
5. **长期**：引入 DAG 编排层支持复杂工作流
