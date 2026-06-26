# EvolveR: Experience-Driven Lifecycle (2026)

> 来源：2026-03-29 learn 搜索发现
> 状态：基于搜索结果推断 + 已有知识综合
> 相关性：P1（高度相关，直接指导我们的进化模型设计）

## 核心概念

**EvolveR** 是一个自我进化 LLM Agent 架构，核心特点是 **Experience-Driven Lifecycle**（经验驱动的生命周期）。

### 与传统 Agent 的区别

| 维度 | 传统 Agent | EvolveR |
|------|-----------|---------|
| 学习方式 | 静态 Prompt + 外部知识库 | 经验驱动的持续进化 |
| 生命周期 | 单次会话 | 跨会话的生命周期 |
| 改进机制 | 人工调整 Prompt | 自动从经验中学习 |
| 记忆模型 | 被动存储 | 主动整合与进化 |

## 经验驱动生命周期的核心机制（推断）

基于已有知识（Self-Consolidation、Karpathy Loop、Meta-Agent）和搜索信号，推断 EvolveR 的核心机制：

### 1. 经验记录层

- **结构化执行日志**：不仅记录"做了什么"，还记录"为什么这么做"、"结果如何"、"遇到什么问题"
- **上下文快照**：保存任务执行时的完整上下文（输入、中间状态、输出）
- **失败案例特别标记**：失败比成功更有学习价值

### 2. 经验整合层

- **模式识别**：从多次执行中识别重复模式（类似 Self-Consolidation）
- **因果关系提取**：理解"什么导致了成功/失败"
- **知识蒸馏**：将经验提炼为可复用的知识

### 3. 进化决策层

- **置信度驱动**：高频成功模式 → 固化为技能；低频或失败模式 → 继续观察
- **自动触发进化**：达到阈值自动触发（不需要人工干预）
- **A/B 测试机制**：新策略与旧策略并行运行，对比效果

### 4. 生命周期管理

- **跨会话持久化**：经验不随会话结束而消失
- **版本演进**：Agent 自身有版本号，每次进化产生新版本
- **回滚机制**：进化失败可回退到上一个稳定版本

## 与我们当前架构的对比

| 维度 | 我们的架构 | EvolveR（推断） |
|------|-----------|----------------|
| 经验记录 | execution.log（简单文本） | 结构化日志 + 上下文快照 |
| 模式识别 | 手动（review 命令） | 自动识别 |
| 进化触发 | 人工触发（review） | 自动触发 + 人工触发 |
| 版本管理 | 无 | 有版本号和回滚机制 |
| 生命周期 | 跨会话（通过 memory） | 明确的生命周期模型 |

## 对我们的启示

### 立即可做

1. **升级 execution.log 为结构化格式**（JSONL）
   - 增加字段：task_type, input_context, output_result, success, error_message, duration, tools_used
   - 为失败案例增加 failure_reason 字段

2. **在 review 命令中增加"经验分析"步骤**
   - 读取 execution.log，识别高频模式
   - 自动生成"经验报告"

### 中期规划

1. **设计 memory/experiences/ 目录**
   - 存储结构化的经验案例
   - 按任务类型分类

2. **实现半自动进化触发**
   - 当某个模式出现 N 次后，自动提示"是否固化为技能"

### 长期愿景

1. **完全自动化的经验驱动进化**
   - 自动识别模式 → 自动生成策略 → 自动 A/B 测试 → 自动选择最优策略

2. **版本管理系统**
   - SKILL.md 有版本号
   - 每次进化产生新版本
   - 支持回滚

## 相关知识连接

- [Self-Consolidation Mechanism](self-consolidation-mechanism.md) — 经验固化为技能
- [Karpathy Loop](karpathy-loop-autonomous-experimentation-2026.md) — 自动实验循环
- [Agent Observability](agent-observability-taxonomy-2026.md) — 经验记录的基础

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
