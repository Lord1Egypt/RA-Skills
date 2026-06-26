---
name: agency-orchestrator
description: 多 Agent 协作调度系统 - 自动分析任务、选择最佳 Agent、协调多 Agent 协作完成复杂任务
version: 1.0.0
author: Agency Agents ZH
tags: [agent, orchestration, collaboration, ai, automation]
---

# Agency Orchestrator - 多 Agent 协作调度系统

## 功能

- 🧠 **智能任务分析** - 自动分析任务需求，识别所需技能
- 🤖 **Agent 自动选择** - 从 166+ 个 Agent 中选择最佳组合
- 🤝 **协作协调** - 管理多 Agent 通信和任务交接
- 📚 **持续学习** - 从每次交互中学习，优化 Agent 表现

## 使用方式

### 基础使用
```python
from agency_orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()
result = orchestrator.coordinate("帮我设计一个产品官网")
```

### 在 ClawX 中使用
```
qwen -p "使用 agency-orchestrator 完成以下任务：设计电商网站"
```

## 可用 Agent 分类

- design (8 个) - UI/UX 设计
- engineering (24 个) - 软件开发
- marketing (31 个) - 营销策略
- sales (8 个) - 销售支持
- product (5 个) - 产品管理
- testing (8 个) - 质量保证
- ... 25+ 分类

## 配置

配置文件：`~/.openclaw/agency-agents-zh/config/settings.json`

## 日志

- 调度日志：`~/.openclaw/agency-agents-zh/logs/orchestrator_log.json`
- 学习日志：`~/.openclaw/agency-agents-zh/logs/learning_log.json`
- 协作日志：`~/.openclaw/agency-agents-zh/logs/collaboration_log.json`
