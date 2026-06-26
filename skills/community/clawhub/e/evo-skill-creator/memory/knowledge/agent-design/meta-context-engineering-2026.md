# Meta Context Engineering (MCE) — 双层优化框架 (2026)

> 来源：2026-03-29 learn 搜索发现
> 状态：基于搜索结果推断 + 已有知识综合
> 相关性：P1（高度相关，meta-agent 驱动技能进化）

## 核心概念

**Meta Context Engineering (MCE)** 是一个双层优化框架（bi-level optimization framework），通过 meta-agent 和 base-agent 的协作，实现 context artifacts 和 agentic harness 的共同进化。

### 关键术语

- **Meta-Agent**：元智能体，负责驱动技能进化
- **Base-Agent**：基础智能体，负责管理上下文优化
- **Context Artifacts**：上下文工件（Prompt、Memory、Knowledge）
- **Agentic Harness**：智能体框架（架构、工具、策略）
- **Bi-level Optimization**：双层优化（上层优化框架，下层优化上下文）

## 双层优化框架（推断）

```
┌─────────────────────────────────────────┐
│         Meta-Agent (上层)                │
│  - 驱动技能进化                          │
│  - 优化 Agentic Harness                  │
│  - 评估 Base-Agent 性能                  │
└──────────────┬──────────────────────────┘
               │ 反馈循环
               ↓
┌─────────────────────────────────────────┐
│         Base-Agent (下层)                │
│  - 管理上下文优化                        │
│  - 优化 Context Artifacts                │
│  - 执行具体任务                          │
└─────────────────────────────────────────┘
```

### 上层：Meta-Agent 的职责

1. **框架进化**
   - 评估当前框架的效果
   - 识别框架的瓶颈
   - 生成框架改进方案
   - 测试和部署新框架

2. **技能进化**
   - 识别需要新技能的场景
   - 设计新技能
   - 评估技能效果
   - 淘汰低效技能

3. **性能监控**
   - 监控 Base-Agent 的表现
   - 识别性能瓶颈
   - 触发优化流程

### 下层：Base-Agent 的职责

1. **上下文管理**
   - 选择相关知识
   - 裁剪上下文
   - 动态加载技能

2. **任务执行**
   - 执行具体任务
   - 记录执行经验
   - 报告执行结果

3. **反馈上报**
   - 向 Meta-Agent 报告性能指标
   - 报告遇到的问题
   - 提出改进建议

## 共同进化机制

**核心思想**：Context Artifacts 和 Agentic Harness 不是独立优化的，而是共同进化的。

### 传统方法的问题

- **孤立优化**：只优化 Prompt，不优化框架
- **单向依赖**：框架固定，只调整上下文
- **局部最优**：无法突破框架限制

### MCE 的解决方案

- **联合优化**：同时优化上下文和框架
- **双向反馈**：Base-Agent 的表现影响 Meta-Agent 的决策
- **全局最优**：突破单一维度的限制

## 与我们当前架构的对比

| 维度 | 我们的架构 | MCE（推断） |
|------|-----------|------------|
| 层级结构 | 有（创建者-子智能体） | 有（Meta-Agent - Base-Agent） |
| 上层职责 | 创建和升级子智能体 | 驱动技能进化 + 框架优化 |
| 下层职责 | 执行具体任务 | 上下文管理 + 任务执行 |
| 反馈机制 | 单向（创建者 review 子智能体） | 双向（Base-Agent 主动反馈） |
| 优化范围 | 主要优化 memory | 联合优化 context + harness |

## 对我们的启示

### 我们已经是 Meta-Agent

- **创建者角色**：我们就是 Meta-Agent
- **子智能体角色**：子智能体就是 Base-Agent
- **差距**：缺少双向反馈和联合优化

### 立即可做

1. **增强反馈机制**
   - 子智能体的 status 命令增加"问题上报"功能
   - 子智能体主动报告遇到的瓶颈
   - 创建者定期收集子智能体反馈

2. **联合优化意识**
   - review 命令不仅优化 memory，也优化框架
   - 识别"框架问题"vs"知识问题"

### 中期规划

1. **设计反馈通道**
   - memory/feedback/ 目录，子智能体写入反馈
   - 创建者定期扫描反馈
   - 自动触发 review

2. **实现联合优化**
   - review 命令同时评估 memory 和 SKILL.md
   - 生成"框架改进方案"和"知识改进方案"

### 长期愿景

1. **完全自动化的双层优化**
   - 子智能体自动上报性能指标
   - 创建者自动识别优化机会
   - 自动生成和测试改进方案

## 关键洞察

### 1. 进化不是单维度的

传统思路：
- 只优化 Prompt → 效果有限
- 只优化 Memory → 受框架限制

MCE 思路：
- 同时优化上下文和框架 → 突破局限

### 2. Meta-Agent 是进化的关键

- **没有 Meta-Agent**：Agent 只能在固定框架内优化
- **有 Meta-Agent**：Agent 可以改进框架本身

### 3. 双向反馈是必需的

- **单向反馈**：Meta-Agent 主动 review → 效率低
- **双向反馈**：Base-Agent 主动上报 → 及时发现问题

## 相关知识连接

- [Framed Autonomy](framed-autonomy-hierarchical-design.md) — 层级化 Agent 设计
- [Context Engineering](context-engineering.md) — 上下文工程
- [Meta-Agent](meta-agent-recursive-improvement.md) — 递归自我改进

## 元数据

- created: 2026-03-29
- updated: 2026-03-29
- last_accessed: 2026-03-29
- access_count: 1
- study_count: 1
- category: agent-design
- volatility: medium
- confidence: medium（基于搜索结果推断）
- status: active
