# MemMA — Coordinating the Memory Cycle through Multi-Agent Reasoning and In-Situ Self-Evolution (2026)

> 学习次数：1 | 创建：2026-03-29 | 更新：2026-03-29
> 来源：arXiv 2603.18718（2026 年 3 月）
> 类别：agent-design | 波动性：medium | 置信度：high

## 核心问题

现有系统将记忆构建、检索和利用视为**独立子程序**，导致：
1. **战略盲区（Strategic Blindness）**：缺少全局策略指导记忆操作
2. **稀疏延迟监督（Sparse, Delayed Supervision）**：记忆失败通常在很久之后才被检测到

## 双路径架构

### 正向路径：推理感知协调（Forward Path）

**Planner-Worker 架构**——将战略推理与低层执行分离。

```
用户会话
    ↓
Meta-Thinker（策略师）
    ├── 生成结构化指导 → Memory Manager（记忆构建阶段）
    │   决定：保留什么 / 整合什么 / 丢弃什么
    └── 指导 → Query Reasoner（迭代检索阶段）
        决定：检索什么 / 如何精化查询
```

**关键特征**：
- 用**有意识的战略推理**替代**启发式驱动**的记忆操作
- Meta-Thinker 提供全局视角，而非每个组件各自为政

### 反向路径：原位自我进化（Backward Path — In-Situ Self-Evolution）

**核心创新**：记忆失败不再"事后发现"，而是在提交之前就检测和修复。

```
会话完成
    ↓
自动合成 Probe QA 对（探测问题）
    ↓
用探测问题验证当前记忆
    ↓
发现失败？
    ├── 是 → 基于证据的批评（Evidence-Grounded Critique）
    │   ↓
    │   语义整合修复（Semantic Consolidation）
    │   ↓
    │   修复后的记忆 → 提交
    └── 否 → 直接提交
```

**关键机制**：
1. **Probe QA 合成**：自动生成探测问题测试记忆质量
2. **即时修复**：失败转化为**立即、局部的修复动作**
3. **在提交前修复**：而非等到下次使用时才发现问题

## 与我们的进化模型对比

### 直接映射

| MemMA 概念 | 我们的对应 | 差距 |
|-----------|-----------|------|
| Meta-Thinker | 创建者（evo-skill-creator） | 我们不生成结构化指导 |
| Memory Manager | learn/scan 命令的知识沉淀 | 缺少战略推理层 |
| Query Reasoner | 唤醒时的 memory 加载 | 缺少迭代精化 |
| Probe QA | review 命令 | 不在每次会话后���动执行 |
| In-Situ Repair | 无 | **核心缺失** |

### 关键启示

1. **记忆质量验证应在"提交前"而非"使用后"**
   - 我们的 learn/scan 沉淀知识后直接写入 memory/，没有验证步骤
   - 应增加：沉淀新知识时，自动生成验证问题检验质量

2. **Planner-Worker 分离是通用模式**
   - 类似我们的 创建者（策略）→ 子智能体（执行）
   - 但在单个智能体内部，我们没有区分"策略推理"和"操作执行"

3. **In-Situ Self-Evolution 的本质**
   - 不是"事后回顾"式的进化，而是"即时修复"式的进化
   - 速度更快、代价更低、质量更高

### 改进方向

1. **短期**：learn/scan 命令沉淀知识时增加"自验证"步骤
   - 沉淀后自动生成 2-3 个验证问题
   - 验证不通过则修复后再提交

2. **中期**：在 review 命令中引入 Probe QA 机制
   - 对现有 knowledge/ 文件生成探测问题
   - 识别失效或不准确的知识

3. **长期**：实现完整的双路径记忆协调
   - Meta-Thinker 层指导所有记忆操作
   - In-Situ 修复在每次会话后自动运行
