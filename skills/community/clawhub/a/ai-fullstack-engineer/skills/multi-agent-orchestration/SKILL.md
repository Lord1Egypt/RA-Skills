---
name: multi-agent-orchestration
description: 多智能体编排：角色定义、任务委派、编排模式、通信与结果聚合。触发词："多智能体"、"智能体编排"、"Agent 团队"、orchestrator
source:
  type: derived
  repo: skills-repo/ai-fullstack-engineer
  path: skills/multi-agent-orchestration/SKILL.md
  version: 1.0.0
  updated: 2026-08-12
  url: https://skills.sh/qodex-ai/ai-agent-skills/multi-agent-orchestration
metadata:
  category: 多智能体
  platform: Web
  difficulty: 进阶
---

# 多智能体编排 (Multi-Agent Orchestration)

> 把"一个全能 Agent 硬扛复杂任务"拆成"多个专职 Agent 协作"：每个 Agent 有清晰的角色 / 目标 / 工具，由编排器（Orchestrator）统筹、结果聚合器汇总。覆盖协作式推理、并行分析、领域专长拆分等场景。

衍生自社区技能 `qodex-ai/ai-agent-skills`（skills.sh 2K 安装量），适配全栈工程师在应用里落地多 Agent 流水线。决策树、框架选型矩阵与踩坑清单见 [references/multi-agent-orchestration-playbook.md](../../references/multi-agent-orchestration-playbook.md)。

## 能力

- **角色定义**：为每个 Agent 明确 Role / Goal / Expertise / Tools / Context
- **编排模式**：顺序链、并行执行、层次（Manager→Specialist）、共识辩论、工具中介
- **通信协议**：直连消息、共享记忆（shared memory）、管理器广播三种模式
- **框架速选**：CrewAI / AutoGen / LangGraph / Swarm 的取舍与模板
- **结果聚合**：多 Agent 产出如何汇总、去冲突、质检
- **踩坑与清单**：冲突 / 慢执行 / 质量差 / 复杂工作流的对应解法（见 playbook）

## 何时用多智能体（vs 单 Agent）

- 任务需要**多种专职角色**（研究 + 分析 + 写作 + 评审）
- 需要**并行分析**不同侧面（竞品 / 市场 / 用户）以提速或增多样性
- 需要**协作式推理**（多个视角辩论、互相挑错、达成共识）
- 需要**韧性**：单个 Agent 失败不应拖垮整条链路

> 简单线性任务、单一领域、无需并行 → 单 Agent 即可，不要为"酷"而编排。决策树见 [references/multi-agent-orchestration-playbook.md](../../references/multi-agent-orchestration-playbook.md)。

## 编排模式速览

| 模式 | 适用 | 要点 |
|------|------|------|
| 顺序链 | 步骤强依赖 | 上一步输出是下一步输入 |
| 并行 | 独立任务 | 同时跑，末端聚合 |
| 层次 | 大项目 + 监管 | Manager 委派 Specialist，统一协调 |
| 共识 | 复杂决策 | 多方辩论 → 仲裁 / 投票 |
| 工具中介 | 大型系统 | 共享工具 / DB，弱直接通信 |

## 框架速选

- **CrewAI** — 角色清晰、层级结构明显
- **AutoGen** — 多轮对话、协商、谈判
- **LangGraph** — 需要状态管理 / 有环工作流
- **Swarm** — 简单 handoff、对话式路由

完整代码示例与选型矩阵见 [references/multi-agent-orchestration-playbook.md](../../references/multi-agent-orchestration-playbook.md)。

## 使用方式

```
/multi-agent-orchestration 帮我设计一个"研报生成"的多 Agent 流水线：研究→财务→风险→写作
/multi-agent-orchestration 这个任务该用并行还是层次编排？
/multi-agent-orchestration 用 LangGraph 画出带状态的多 Agent 工作流
```

## 工作流

1. 界定问题与统一目标，拆成可独立子任务
2. 为每个子任务定义 Agent 角色 / 目标 / 工具
3. 选编排模式与通信协议，定 handoff 点
4. 设成功标准、错误处理与降级策略
5. 实现并单 Agent 自测 → 联调 → 监控日志
6. 评质量与成本，迭代

## 适用场景

- 研报 / 周报 / 内容生成的"多角色流水线"
- 需要多视角评审的代码 / 方案评审 Agent 组
- 并行抓取 + 分析的爬虫 / 情报 Agent 组
- 对话式路由（triage → 专家 Agent）

## 限制

- 不替代单 Agent：简单任务用多 Agent 只增成本
- 框架具体 API 以各项目依赖版本为准，先查官方文档
- Agent 间的上下文 / 成本控制需用户自测
- 涉及生产编排、分布式调度等以报告呈现，不替你拍板
