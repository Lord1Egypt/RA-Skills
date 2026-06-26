---
name: openclaw-orchestra
description: "OpenClaw native multi-agent orchestrator. Based on AOrchestra 4-tuple (I,C,T,M) abstraction. Dynamically creates sub-agents, parallel execution, smart routing, experience store, cost tracking. Trigger words: orchestra, orchestrator, 编排器, 编排, 协调器, 指挥官, 四元组, Agent编排, 多智能体编排, 自动分解任务, 智能调度, 并行调研, ClawOrchestra."
---

# ClawOrchestra 🎼

> **OpenClaw 原生的多智能体编排器** —— 用乐团指挥的方式协调多个 Agent 完成复杂任务。

---

## ⚠️ 核心规则（必读）

### 1. 结果交付方式
**必须生成 MD 文件发送给用户**，不要在聊天中输出长文本！

### 2. 子Agent完成后必须主动整合
**最后一个子Agent完成后，主Agent必须立即整合结果并发送报告**，不能等待用户催促！

### 3. 动态四元组必须突出
每次编排都要展示四元组的动态生成过程，让用户感受到"智能编排"的价值。

---

## 🎯 编排流程

### 步骤1：启动公告

```
🎼 ClawOrchestra 动态编排器已激活

📋 任务: [用户任务简述]
🎯 类型: 调研 | 复杂度: 中等 | 模式: 🔀 并行
```

### 步骤2：动态四元组生成

```
⚡ 动态四元组生成中...

┌─────────────────────────────────────────────────────┐
│  Φ = (I, C, T, M)  动态子Agent创建                   │
├─────────────────────────────────────────────────────┤
│  Agent-1: 🔍 Swarm专家                              │
│  ├── I: "搜索 Agent Swarm 最新框架和论文"            │
│  ├── C: [主任务上下文]                               │
│  ├── T: [web_search, web_fetch]                     │
│  └── M: GLM (快速搜索，成本低)                       │
├─────────────────────────────────────────────────────┤
│  Agent-2: 🎯 编排专家                               │
│  ├── I: "搜索 Agent 编排器技术和趋势"                │
│  ├── C: [主任务上下文]                               │
│  ├── T: [web_search, web_fetch]                     │
│  └── M: GLM (快速搜索)                               │
├─────────────────────────────────────────────────────┤
│  Agent-3: 📊 协作专家                               │
│  ├── I: "搜索多智能体协作模式"                       │
│  ├── C: [主任务上下文]                               │
│  ├── T: [web_search, web_fetch]                     │
│  └── M: Kimi (深度分析，长上下文)                    │
└─────────────────────────────────────────────────────┘

✨ 智能决策: 3个子Agent并行执行，预计节省 60% 时间
```

### 步骤3：派遣子Agent

```
🚀 子Agent小队出发 (并行模式)

[1] 🔍 Swarm专家  → GLM  → Agent Swarm 调研
[2] 🎯 编排专家   → GLM  → 编排器技术调研
[3] 📊 协作专家   → Kimi → 多智能体协作分析

⏳ 执行中... (预计 60-90s)
```

### 步骤4：等待并整合（关键！）

**主Agent必须轮询等待所有子Agent完成，然后立即整合！**

```
⏳ 监控子Agent状态...

✅ Swarm专家 完成 (65s, 90k tokens)
✅ 编排专家 完成 (93s, 71k tokens)
✅ 协作专家 完成 (65s, 117k tokens)

📊 全部完成！正在整合结果...
```

### 步骤5：生成并发送报告

```
📝 生成调研报告...

📊 执行统计:
| Agent | 模型 | 耗时 | Tokens |
|-------|------|------|--------|
| 🔍 Swarm专家 | GLM | 65s | 90k |
| 🎯 编排专家 | GLM | 93s | 71k |
| 📊 协作专家 | Kimi | 65s | 117k |

⚡ 并行节省: 67% 时间
💰 总成本: ~278k tokens

📤 正在发送报告文件...
```

---

## 🔧 技术实现要点

### 1. 并行执行
同一轮 `sessions_spawn` 调用 = 真并行

### 2. 结果等待
使用 `subagents list` 轮询状态，直到所有子Agent完成

### 3. 结果获取
使用 `sessions_history` 获取子Agent输出

### 4. 报告生成
整合结果 → 生成 MD 文件 → `message(filePath=...)` 发送

---

## 🤖 模型选择

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| 搜索、收集信息 | GLM | 便宜、快速、中文好 |
| 代码、分析、长文 | Kimi | 长上下文、代码强 |
| 复杂推理 | GLM | 均衡 |

**注意**：目前仅支持 lixiang 内部模型（GLM、Kimi）

---

## 📚 参考文献

- [AOrchestra: Automating Sub-Agent Creation for Agentic Orchestration](https://arxiv.org/abs/2602.03786)
- GitHub: https://github.com/zcyynl/claw-orchestra

---

## 🗓️ 更新日志

### v0.1.1 (2026-03-16)
- ✅ 四元组抽象 (I, C, T, M)
- ✅ 编排器骨架 (Delegate/Finish)
- ✅ OpenClaw 适配器 (sessions_spawn)
- ✅ 智能路由 (上下文/模型/工具)
- ✅ 经验库 + 成本追踪
- ✅ 交互优化（动态四元组展示）
- ✅ 自动结果整合（不再卡住）