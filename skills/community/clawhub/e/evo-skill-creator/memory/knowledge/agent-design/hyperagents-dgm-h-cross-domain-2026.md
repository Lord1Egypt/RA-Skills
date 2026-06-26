# HyperAgents — DGM-H 跨领域递归自我改进（2026）

> 来源：arXiv:2603.19461, Meta+UBC+Vector+Edinburgh+NYU+Oxford
> 学习时间：2026-03-30（深度学习）
> 类别：agent-design / self-improvement
> 波动性：low（理论突破，DGM 的正式升级版）
> 置信度：high（论文有完整实验数据支撑）

## 核心突破

DGM-H 解决了原始 DGM 的根本缺陷：**元级机制不可编辑**。原始 DGM 的 meta-level 是人工设计的固定逻辑，导致自我改进能力被限制在编码领域（因为编码任务中"修改代码"和"执行任务"天然一致）。DGM-H 将 task agent 和 meta-agent **统一为单一可编辑 Python 程序**，使得 meta-level 修改过程本身也可以被修改。

## 架构对比

```
DGM（原始）:
  Task Agent (可修改) + Meta-Agent (固定/人工设计)
  → 只能改进任务执行，不能改进改进方式
  → 局限于编码领域

DGM-H（升级版）:
  Unified Editable Program (全部可修改)
  → 能改进任务执行 + 改进方式 + 改进改进方式
  → 跨领域通用
```

## 递归自我改进层次（修正版）

| Level | 能力 | 实现 |
|-------|------|------|
| Level 0 | 执行任务 | 普通 Agent |
| Level 1 | 改进执行（优化 prompt/策略） | Self-Improving Agent |
| Level 2 | 改进"如何改进"（修改改进算法） | **Hyperagent (DGM-H)** |
| Level 3 | 理论极限（哥德尔不完备性） | 未实现 |

**关键区分**：Level 1 改进的是"输出"，Level 2 改进的是"过程"。这个区别是本质性的。

## 实验数据（跨领域性能）

| 领域 | 初始分数 | DGM-H 最终分数 | 提升幅度 |
|------|---------|---------------|---------|
| 机器人奖励函数设计 | 0.060 | 0.372 (CI: 0.355-0.436) | **6.2x** |
| 学术论文评审 | 0.000 | 0.710 (CI: 0.590-0.750) | **从零到优** |
| 编码（Polyglot） | 0.084 | 0.267 | **3.2x** |

### 跨领域迁移实验（最关键发现）

在论文评审和机器人任务上优化的 meta-agent → 直接迁移到**奥林匹克数学评分**：
- DGM-H（迁移）：imp@50 = **0.630**
- 静态 DGM：**0.0**（完全失败）

**这证明**：DGM-H 学到的不是"如何做论文评审"或"如何设计奖励函数"，而是**通用的自我改进策略**（persistent memory、bias detection、performance tracking），这些策略可以在全新领域自动发挥作用。

## 涌现能力（无人类提示、自主发展）

1. **Persistent Memory** — Agent 自主开发了跨运行的记忆架构
2. **Performance Tracking** — 自主创建遥测系统（滚动窗口历史预测），用于检测分布漂移和偏差
3. **Compute-Aware Planning** — 自主学会战略性分配算力
4. **Automated Bias Detection** — 自主开发偏差检测机制

**本质**：这些涌现能力不是被设计的，而是 Agent 在自我改进过程中"发明"的工具。这与我们的进化模型高度吻合——我们的子智能体也应该能在工作中自主发展出新的工具和方法。

## 核心机制：Archive-Based Population Search

```
1. 从档案库中选择"父代"（历史上表现好的版本）
2. 对父代进行变异（修改代码/策略）
3. 评估变异版本的适应度
4. 将优秀变异加入档案库
5. 重复循环
```

**关键**：不是简单的"最新=最好"，而是维护一个**多样性档案**，允许从不同历史版本出发探索，避免局部最优。

## 与我们架构的映射

| DGM-H 概念 | 我们的对应 | 差距 |
|------------|-----------|------|
| Unified Editable Program | SKILL.md + memory/ | SKILL.md 不可自修改 |
| Metacognitive Self-Modification | review self | review 是被动触发，不是自动循环 |
| Archive-Based Population | 无 | 无版本档案、无多样性维护 |
| Cross-Domain Transfer | review \<子智能体> | 方向正确但粒度粗 |
| Emergent Persistent Memory | memory/ 目录 | 已有，但不是涌现的 |
| Performance Tracking | execution.log | 太简单，缺少结构化指标 |
| Compute-Aware Planning | 无 | 无算力感知 |

## 对我们的启示

### 立即可做

1. **review self 增加"元认知"维度**
   - 不仅审视"做了什么"，还要审视"如何改进"的方式是否还有效
   - 问自己：我的 review 方法本身需要改进吗？

2. **增强 execution.log 的结构化**
   - 记录更多维度：改进策略、改进效果、失败原因
   - 为未来的自动化 performance tracking 打基础

3. **review 子智能体时注重"跨领域迁移"**
   - 一个子智能体的优秀实践是否可以迁移到其他子智能体？
   - 这就是我们版本的"跨领域 meta-level transfer"

### 中期规划

1. **版本档案机制**
   - 为 SKILL.md 和 evo-agent-model.md 建立版本历史
   - review 时可以从历史版本中学习

2. **涌现能力记录**
   - 子智能体在工作中自主发展出的新方法应被记录和推广
   - 类似 DGM-H 的涌现能力发现

### 长期愿景

1. **SKILL.md 受控自修改**
   - Agent 提出 SKILL.md 修改建议 → 沙箱测试 → 人工确认 → 应用
   - 这是我们走向 Level 2 的关键路径

## 与已有知识的关联

- **#5 DGM 架构**：DGM-H 是其正式升级版，解决了 meta-level 固定的问题
- **#25 DGM-Hyperagents**：本次学习是对 #25 的深化，增加了实验数据和涌现能力分析
- **#27 Self-Referential Framework**：DGM-H 是 Self-Referential 的最佳实现
- **#17 Meta-Agent 递归改进**：DGM-H 证明了 Level 2 递归改进是可实现的
- **#28 Meta Context Engineering**：DGM-H 的 meta-level 修改与 MCE 的双层优化高度一致

## 元数据

- created: 2026-03-30
- updated: 2026-03-30
- last_accessed: 2026-03-30
- access_count: 1
- study_count: 1
- category: agent-design
- volatility: low
- confidence: high
- status: active
