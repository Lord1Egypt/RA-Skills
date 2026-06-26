# Cybernetic Evolver

> 基于钱学森《工程控制论》的AI自我进化框架

## 什么是 Cybernetic Evolver？

**Cybernetic Evolver** 是一个受控理论启发的AI Agent自我进化框架。它将钱学森《工程控制论》中的核心概念——反馈、稳定性、自适应、最优控制、自组织——转化为可计算的Python类，使AI系统具备：

1. **闭环自我修正**：通过实时误差感知持续调整行为
2. **自适应学习**：根据环境变化自动调整策略参数
3. **结构进化**：突破局部最优，实现策略拓扑层面的自我进化
4. **稳定性保护**：Lyapunov判据确保进化过程不失控

## 核心原理（6大原理）

1. **闭环反馈驱动** — 感知→评价→决策→执行→反馈的持续闭环
2. **实时误差感知** — 每个时间步计算实际误差，驱动调整方向
3. **自适应参数调整** — 误差超阈值时自动调整控制参数
4. **探索-利用平衡** — ε-greedy/UCB策略平衡已知最优与新策略探索
5. **分层递阶进化** — 参数层→结构层→元策略层的多层次进化
6. **持续学习+稳定性** — 在保持核心稳定中持续从环境学习

## 文件结构

```
skills/cybernetic-evolver/
├── SKILL.md          # 技能规范（含Mermaid架构图）
├── README.md         # 本文件
├── ARCHITECTURE.md   # 详细架构设计文档
├── WORKFLOW.md       # 工作流程详述
├── CODE/
│   └── evolver.py    # CyberneticEvolver 类实现
└── DEMO/
    └── example.py    # 演示示例（3个场景）
```

## 快速开始

```python
from evolver import CyberneticEvolver

# 定义目标：最大化函数值
evolver = CyberneticEvolver(
    target=100.0,          # 目标值
    state_dim=4,           # 状态维度
    action_dim=5,          # 动作选项数
    epsilon_start=1.0,    # 初始探索率
    epsilon_decay=0.995   # 探索率衰减
)

# 运行进化循环
evolver.evolve(n_steps=1000)
```

## 理论基础

- 钱学森《工程控制论》(1954/1980)
- 维纳《控制论》(1948)
- 协同学（哈肯，1970s）
- 自适应控制理论（MIT方案、Popov超稳定性）
- 耗散结构理论（普利高津，1969）

## 应用场景

- AI Agent 自主策略进化
- 复杂环境下的自适应决策
- 多目标优化问题的自我探索
- 开放式环境中的持续学习
