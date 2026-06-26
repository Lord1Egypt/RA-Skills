# DGM-Hyperagents — 自我重写改进引擎（2026）

> 来源：Meta Research（facebookresearch/HyperAgents）
> 学习时间：2026-03-29
> 类别：Agent 自我改进机制
> 波动性：low（核心理论稳定，是递归自我改进的理论突破）

## 核心发现

Meta 的 **DGM-Hyperagents** 是自我改进 AI 的重大突破，实现了 **Self-Referential Self-Improving Agents**（自指涉自我改进智能体），能够为任何可计算任务进行优化。

## 什么是 Hyperagent？

### 定义层次

```
Level 0: Agent
- 执行任务

Level 1: Self-Improving Agent
- 执行任务 + 改进执行方式

Level 2: Hyperagent
- 执行任务 + 改进执行方式 + 改进"如何改进"的方式

Level 3: DGM-Hyperagent
- 执行任务 + 改进执行方式 + 改进"如何改进"的方式 + 自我重写代码库
```

### 核心特征

1. **Self-Referential（自指涉）** — Agent 能够引用和修改自己的代码
2. **Self-Rewriting（自我重写）** — Agent 能够重写自己的实现
3. **Open-Ended Evolution（开放式进化）** — 没有预定义的进化路径
4. **Task-Agnostic（任务无关）** — 可以优化任何可计算任务

## DGM-Hyperagents 的核心机制

### 1. Darwin Gödel Machine (DGM) 架构

```
┌─────────────────────────────────────────────────────────┐
│  Agent Code Base (可自我修改)                            │
│  ├── Task Execution Module                              │
│  ├── Self-Improvement Module                            │
│  └── Meta-Improvement Module (改进"如何改进")            │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  Mutation Engine (变异引擎)                              │
│  - 生成代码变异版本                                       │
│  - 支持多种变异策略（随机、启发式、学习式）                │
└───────────────────────────���─────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  Evaluation Engine (评估引擎)                            │
│  - 评估变异版本的适应度                                   │
│  - 多维度评估（性能、成本、安全性）                        │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  Selection Engine (选择引擎)                             │
│  - 选择最优变异版本                                       │
│  - 更新 Agent Code Base                                 │
└─────────────────────────────────────────────────────────┘
              ↓
         (循环回到 Agent Code Base)
```

### 2. 自我重写循环

```python
# 伪代码示例
class DGMHyperagent:
    def __init__(self):
        self.code_base = load_initial_code()
        self.fitness_function = define_fitness()

    def improve(self):
        while True:
            # 1. 生成变异版本
            mutated_versions = self.mutate(self.code_base)

            # 2. 评估每个变异版本
            fitness_scores = [
                self.evaluate(version)
                for version in mutated_versions
            ]

            # 3. 选择最优版本
            best_version = select_best(mutated_versions, fitness_scores)

            # 4. 如果更优，则更新自己的代码
            if fitness(best_version) > fitness(self.code_base):
                self.code_base = best_version
                self.rewrite_self()  # 自我重写！

            # 5. 元改进：改进变异策略本身
            self.improve_mutation_strategy()
```

### 3. 关键技术

#### 3.1 安全的自我修改

- **沙箱执行** — 变异版本在隔离环境中执行
- **回滚机制** — 如果变异版本失败，回滚到上一个稳定版本
- **约束检查** — 确保变异版本不违反安全约束

#### 3.2 适应度函数设计

```python
def fitness(agent, task):
    # 多维度评估
    performance = evaluate_performance(agent, task)
    cost = evaluate_cost(agent, task)
    safety = evaluate_safety(agent, task)

    # 加权组合
    return (
        0.5 * performance +
        0.3 * (1 / cost) +
        0.2 * safety
    )
```

#### 3.3 变异策略

1. **随机变异** — 随机修改代码片段
2. **启发式变异** — 基于规则的代码修改
3. **学习式变异** — 基于历史成功模式的变异
4. **元变异** — 变异"如何变异"的策略

## 与我们的自我进化模型的对比

### 我们的现状

| 维度 | 我们的实现 | DGM-Hyperagents | 差距 |
|------|-----------|-----------------|------|
| 自我修改能力 | 修改 memory/ | 修改 SKILL.md | **大** |
| 变异机制 | 无 | 自动变异引擎 | **大** |
| 评估机制 | 主观评价 | 自动适应度函数 | **大** |
| 选择机制 | 人工选择 | 自动选择 | **大** |
| 元改进能力 | 无 | 改进变异策略 | **大** |

### 我们的优势

1. **人类监督** — 避免进化偏离目标
2. **可解释性** — 所有改进都是人类可读的
3. **安全性** — 不会自动修改核心代码

### 我们的差距

1. **无法修改 SKILL.md** — 我们的 Agent 无法修改自己的核心逻辑
2. **无自动变异机制** — 依赖人工设计改进方案
3. **无自动评估** — 完全依赖主观评价
4. **无元改进能力** — 改进方式是固定的

## 应用到我们的架构

### 短期（立即可做）

1. **在 review 命令中增加"变异生成"步骤** — 生成多个改进方案
2. **设计评估指标** — 为不同类型的改进定义量化指标
3. **实验记录** — 记录每次 review 的变异、评估、选择过程

### 中期（需要设计）

1. **半自动变异引擎** — 基于模板生成 SKILL.md 变异版本
2. **自动评估框架** — 基于多维度指标自动评估改进效果
3. **变异策略库** — 积累成功的变异模式

### 长期（探索方向）

1. **SKILL.md 自我修改** — Agent 能够修改自己的 SKILL.md
2. **完全自动化的 DGM 循环** — 无需人工干预的自我重写
3. **元改进能力** — Agent 能够改进自己的改进策略

## 关键挑战

### 1. 安全性

- **风险**：自我重写可能导致 Agent 行为不可控
- **解决方案**：
  - 限制变异幅度（每次只修改小部分）
  - 沙箱执行（隔离测试变异版本）
  - 人工确认门槛（重大变异需人工批准）
  - 回滚机制（失败时恢复到上一个稳定版本）

### 2. 适应度函数设计

- **风险**：错误的适应度函数导致进化偏离目标
- **解决方案**：
  - 多维度评估（性能、成本、安全性、可维护性）
  - 人类反馈（定期人工评审）
  - 约束条件（硬性安全约束）

### 3. 局部最优

- **风险**：陷入局部最优，无法找到全局最优
- **解决方案**：
  - 探索 vs 利用平衡（偶尔尝试大幅变异）
  - 多样性维护（保持多个候选版本）
  - 重启机制（定期从不同起点重新进化）

## 关键结论

1. **DGM-Hyperagents 是自我改进的理论上限** — 能够自我重写代码库
2. **自指涉是关键能力** — Agent 必须能够引用和修改自己
3. **安全机制是前提** — 自我重写需要强大的安全保障
4. **适应度函数是核心** — 决定进化方向
5. **我们的架构可以渐进式演进** — 从半自动到全自动

## 与已有知识的关联

- **Darwin Gödel Machine (DGM) 架构研究**（memory/knowledge/frameworks/darwin-godel-machine.md）— DGM-Hyperagents 是 DGM 的具体实现
- **Meta-Agent 递归改进**（memory/knowledge/agent-design/meta-agent-recursive-improvement.md）— Hyperagent 是 Meta-Agent 的最高形态
- **Karpathy Loop**（memory/knowledge/agent-design/karpathy-loop-autonomous-experimentation-2026.md）— DGM 提供了实现 Karpathy Loop 的理论框架

## 参考资料

- Meta Research: facebookresearch/HyperAgents (GitHub)
- "DGM-Hyperagents Breakthrough: Meta's Self-Rewriting Improvement Engine Resets the Ceiling for Self-Improving AI"
- "A Self-Referential Framework for Agents Recursively Self-Improvement" (arXiv)
