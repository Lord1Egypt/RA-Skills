# ClawOrchestra 🎼

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw/openclaw)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)

> **OpenClaw 原生多智能体编排器** —— 基于四元组动态创建子Agent，像乐团指挥一样协调多个 Agent 完成复杂任务。

---

## 🎯 核心亮点

### 动态四元组编排
任何 Agent 都可以形式化为四元组 `Φ = (I, C, T, M)`：

```
┌─────────────────────────────────────────────────────┐
│  Φ = (I, C, T, M)  动态子Agent创建                   │
├─────────────────────────────────────────────────────┤
│  I = Instruction  → 任务指令（动态生成）             │
│  C = Context      → 精选上下文（智能路由）           │
│  T = Tools        → 工具子集（按需分配）             │
│  M = Model        → 模型选择（成本-性能权衡）        │
├─────────────────────────────────────────────────────┤
│  ✨ 根据任务需求，动态生成专业化子Agent              │
│  🔀 同一轮 spawn = 真并行，节省 50%+ 时间            │
└─────────────────────────────────────────────────────┘
```

### 编排器动作
编排器只有两个动作：
- `Delegate(Φ)` → 创建子 Agent 执行
- `Finish(answer)` → 输出最终答案

---

## ✨ 特性

| 特性 | 说明 |
|------|------|
| 🎯 **四元组抽象** | 动态创建专业化子Agent |
| 🚀 **并行执行** | 同一轮 spawn = 真并行 |
| 🔀 **智能路由** | 自动选择模型、工具、上下文 |
| 📚 **经验库** | 记录成功策略，越用越聪明 |
| 💰 **成本追踪** | 记录 token 消耗，成本可控 |
| 🎼 **开箱即用** | 作为 OpenClaw Skill 安装即用 |

---

## 📦 安装

### 方式 1：作为 OpenClaw Skill（推荐）

```bash
# 复制到 OpenClaw skills 目录
cp -r skill/claw-orchestra /path/to/openclaw/skills/
```

### 方式 2：独立使用

```bash
git clone https://github.com/zcyynl/claw-orchestra.git
cd claw-orchestra
pip install -e .
```

---

## 🚀 快速开始

```python
from claw_orchestra import Orchestrator, AgentTuple

# 创建编排器
orchestrator = Orchestrator(
    main_model="glm",
    sub_models=["glm", "kimi"],
)

# 执行任务
result = orchestrator.run("帮我调研 LangChain 框架")
```

### 四元组模式

```python
from claw_orchestra import AgentTuple

# 创建子任务定义
phi = AgentTuple(
    instruction="搜索 LangChain 的核心特性",  # I
    context=["用户在做 AI 框架调研"],         # C
    tools=["web_search", "web_fetch"],       # T
    model="glm",                             # M
    role="🔍 researcher",
)

# 转换为 spawn 参数
params = phi.to_spawn_params()
```

---

## 🎭 触发词

在 OpenClaw 中说以下任意一个，自动激活：

**中文**：编排器、编排、协调器、指挥官、乐团、四元组、Agent编排、多智能体编排、自动分解任务、智能调度、并行调研

**英文**：orchestra, orchestrator, orchestrate, ClawOrchestra

---

## 📂 项目结构

```
claw-orchestra/
├── core/                    # 核心模块
│   ├── four_tuple.py        # 四元组抽象
│   ├── orchestrator.py      # 编排器
│   ├── action_space.py      # 动作空间
│   ├── openclaw_adapter.py  # OpenClaw 适配
│   └── llm_decision.py      # LLM 决策
├── router/                  # 路由器
│   ├── context_router.py    # 上下文精选
│   ├── model_router.py      # 模型选择
│   └── tool_router.py       # 工具分配
├── learner/                 # 学习模块
│   ├── experience_store.py  # 经验库
│   └── cost_tracker.py      # 成本追踪
├── skill/                   # OpenClaw Skill
│   ├── SKILL.md            # Skill 定义
│   └── scripts/            # 脚本
└── examples/               # 示例
```

---

## 🤖 模型选择

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| 搜索、收集信息 | GLM | 便宜、快速、中文好 |
| 代码、分析、长文 | Kimi | 长上下文、代码强 |
| 复杂推理 | GLM | 均衡 |

---

## 📊 示例输出

```
🎼 ClawOrchestra 动态编排器已激活

📋 任务: 调研 Agent Swarm 和编排器最新进展
🎯 类型: 调研 | 复杂度: 中等 | 模式: 🔀 并行

⚡ 动态四元组生成中...

┌─────────────────────────────────────────────────────┐
│  Agent-1: 🔍 Swarm专家                              │
│  ├── I: "搜索 Agent Swarm 最新框架"                 │
│  ├── C: [主任务上下文]                               │
│  ├── T: [web_search, web_fetch]                     │
│  └── M: GLM (快速搜索，成本低)                       │
├─────────────────────────────────────────────────────┤
│  Agent-2: 🎯 编排专家                               │
│  ├── I: "搜索 Agent 编排器技术"                     │
│  └── M: GLM                                         │
├─────────────────────────────────────────────────────┤
│  Agent-3: 📊 协作专家                               │
│  ├── I: "搜索多智能体协作模式"                       │
│  └── M: Kimi (深度分析，长上下文)                    │
└─────────────────────────────────────────────────────┘

🚀 子Agent小队出发 (并行模式)

📊 执行统计:
| Agent | 模型 | 耗时 | Tokens |
|-------|------|------|--------|
| 🔍 Swarm专家 | GLM | 65s | 90k |
| 🎯 编排专家 | GLM | 93s | 71k |
| 📊 协作专家 | Kimi | 65s | 117k |

⚡ 并行节省: 67% 时间
💰 总成本: ~278k tokens
```

---

## 📄 License

MIT License

---

## 📮 联系

- GitHub: https://github.com/zcyynl/claw-orchestra
- OpenClaw 社区: https://discord.com/invite/clawd
