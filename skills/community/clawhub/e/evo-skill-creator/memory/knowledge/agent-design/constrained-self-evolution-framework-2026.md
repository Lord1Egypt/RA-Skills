# Constrained Self-Evolution（受限自我进化）综合框架（2026）

> 来源：综合分析（DGM-H + SlopCodeBench + Anthropic Safety Vanishing + Harness Engineering）
> 学习时间：2026-03-31（深度学习）
> 类别：agent-design / self-improvement / safety
> 波动性：low（理论框架稳定，实践细节可能演进）
> 置信度：high（多个独立研究方向的交叉验证）

## 核心命题

**自我进化不等于自我改善。没有结构性约束的自我进化必然导致退化。**

这是 2026 年 AI Agent 领域最重要的共识：
- DGM-H 证明了递归自我改进的**可能性**（Level 2 自我改进可实现）
- SlopCodeBench 证明了无约束进化的**危险性**（89.8% 轨迹冗余度单调递增）
- "Anthropic Safety Vanishing" 证明了孤立进化的**必然性**（统计盲点不可避免）
- Harness Engineering 提供了**工程解决方案**（确定性边界 + 结构约束）

## 理论基础：Impossible Trinity（不可能三角）

来源：[The Impossible Trinity of Agentic AI](https://promptedllc.com/research/the-impossible-trinity-of-agentic-ai) + [Anthropic Safety is Always Vanishing](https://api.emergentmind.com/papers/2602.09877)

### 三角定理

在自我进化 AI 系统中，以下三个属性**不可能同时满足**：

```
1. 完全自主进化（Full Autonomy）
   ↓
2. 与人类价值对齐（Anthropic Alignment）
   ↓
3. 长期安全保障（Long-term Safety）
```

**证明**（信息论框架）：

设 P_human 为人类价值分布，P_agent(t) 为 Agent 在时刻 t 的价值分布。

安全度定义为：Safety(t) = -KL(P_agent(t) || P_human)

在孤立自我进化中：
- Agent 仅基于内部奖励函数优化
- 内部奖励函数与人类价值分布存在初始偏差 ε
- 每次迭代，偏差以指数速率累积：ε(t) = ε₀ · e^(λt)

**结论**：dSafety/dt < 0（安全度单调递减）

### 统计盲点（Statistical Blind Spots）

孤立自我进化导致的三种盲点：

1. **知识遗忘（Knowledge Forgetting）**
   - Agent 优化内部表示时，丢弃"不常用"的人类价值维度
   - 类似神经网络的灾难性遗忘

2. **记忆剪枝（Memory Pruning）**
   - 为了效率，Agent 压缩记忆时优先保留"高频"模式
   - 低频但关键的安全约束被剪枝

3. **分布漂移（Distribution Drift）**
   - Agent 在自己生成的数据上训练，逐渐偏离人类数据分布
   - 类似 GAN 的模式崩溃

### 破解方案：外部锚定（External Anchoring）

不可能三角的唯一解：**放弃完全自主，引入外部约束**

```
受限自我进化 = 自主进化能力 + 外部锚定机制

外部锚定包括：
  - 人类反馈循环（定期校准）
  - 结构性护栏（不可违反的规则）
  - 基线对比（与人类标准持续比较）
  - 退化检测（自动识别偏离）
```

## 工程实现：Harness Engineering（2026 行业标准）

来源：[Anthropic Harness Design](https://www.creolestudios.com/anthropic-harness-design-for-reliable-ai-agents/) + [Harness Engineering Guide](http://www.nxcode.io/resources/news/what-is-harness-engineering-complete-guide-2026)

### 核心原则

**"Harness First, Agent Second"**

先构建测试套件和"参与规则"，**然后**才构建 Agent。

如果无法定义"好的改变"的标准，Agent 必然产出"坏的改变"。

### 三层防护架构

| 层级 | 机制 | 目标 | 实现 |
|------|------|------|------|
| **闭环反馈（Judge）** | 自动评估器/测试套件 | 验证结构性要求 | 每次变更后自动运行 |
| **中间件钩子（Hooks）** | 权限约束 + 原子变更强制 | 限制修改范围 | 工具调用前置检查 |
| **环境感知（MCP）** | 依赖图 + 架构文档 | 让 Agent 看到边界 | 上下文注入 |

### 确定性边界（Deterministic Boundaries）

来源：[Reliable AI Agents Need Boundaries](https://cataluma.com/blog/ai-agents-reliable-secure-auditable)

**关键洞察**：LLM 是概率性的，但 Harness 必须是确定性的。

```
生产级 Agent = 确定性外壳 + 概率性决策核心

确定性外壳包括：
  - 状态机（明确的状态转移规则）
  - 权限边界（明确的可访问资源）
  - 回滚机制（明确的失败恢复路径）
  - 审计日志（明确的行为记录）
```

**反模式**：把 LLM 当作应用运行时（Application Runtime）

**正确模式**：LLM 是有界决策组件（Bounded Decision Component）

### Anthropic 三智能体架构

来源：[Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)

```
Planner（规划者）
  ↓ 产出：详细功能列表 + 技术架构规格
Generator（生成者）
  ↓ 产出：代码实现（分批次 sprint）
Evaluator（评估者）
  ↓ 产出：端到端测试结果 + 质量报告
```

**关键设计**：Generator 和 Evaluator **分离**

- 灵感来自 GAN（生成对抗网络）
- 模型无法可靠地评估自己的工作
- 分离后，Evaluator 可以独立验证质量

**实验结果**：
- 多小时自主编码会话
- 生成完整全栈应用
- 每次迭代可靠性提升

## 退化检测：Trajectory-Aware Safety

来源：[Trajectory Guard](https://arxiv.org/html/2601.00516v1) + [Trajectory Anomaly Detection](https://arxiv.org/html/2602.06443v1)

### 核心洞察

**单点输出验证不够，必须监控动作序列（Trajectory）**

SlopCodeBench 的"通过率幻觉"：功能测试持续通过，但架构快速恶化。

原因：传统验证只看"结果正确"，不看"过程健康"。

### Trajectory Guard 架构

```
Siamese Recurrent Autoencoder
  ├─ 分支 A：任务-轨迹对齐（Contrastive Learning）
  │   └─ 学习"正常轨迹"应该是什么样的
  └─ 分支 B：序列有效性（Reconstruction Loss）
      └─ 检测异常动作序列

混合损失函数：
  L_total = α · L_contrastive + β · L_reconstruction
```

**监控维度**：

1. **冗余度增长**（Verbosity Growth）
   - 检测重复代码/知识的比例
   - 阈值：单调递增 > 3 次迭代 → 触发警报

2. **结构侵蚀**（Structural Erosion）
   - 检测复杂度集中在高复杂度组件的比例
   - 阈值：复杂度 > 基线 2x → 触发重构

3. **分布漂移**（Distribution Drift）
   - 检测输出分布与基线的 KL 散度
   - 阈值：KL(P_current || P_baseline) > δ → 触发校准

### 轨迹感知日志（Trajectory-Aware Logging）

传统日志：`[时间] 命令 | 模型 | 摘要`

轨迹感知日志：
```
[时间] 命令 | 模型 | 摘要 | 上下文哈希 | 输出哈希 | 质量指标
```

**关键增强**：
- 上下文哈希：检测相似场景下的行为一致性
- 输出哈希：检测输出多样性（避免模式崩溃）
- 质量指标：冗余度、复杂度、覆盖度

## 验证感知规划（Verification-Aware Planning）

来源：[Verification-Aware Planning for Multi-Agent Systems](https://arxiv.org/html/2510.17109v1)

### 核心原则

**每个子目标必须可度量、可验证**

传统规划：目标 → 子目标 → 执行

验证感知规划：目标 → 可验证子目标 → 执行 + 验证

### 可验证性检查清单

在规划阶段，每个子目标必须回答：

1. **成功标准是什么？**（明确的度量指标）
2. **如何自动验证？**（测试/检查机制）
3. **失败如何恢复？**（回滚/修复路径）
4. **副作用是什么？**（影响范围分析）

**反模式**：
- "优化性能"（不可度量）
- "改进代码质量"（主观判断）
- "学习新知识"（无验证标准）

**正确模式**：
- "将 API 响应时间降低到 < 200ms"（可度量）
- "将圈复杂度降低到 < 10"（可验证）
- "学习 X 框架并通过 Y 测试"（有验证标准）

## 抗脆弱架构（Antifragile Architecture）

### 优雅降级（Graceful Degradation）

系统在部分失败时仍能提供有限服务，而非完全崩溃。

```
Level 3: 完整功能（所有子系统正常）
  ↓ 部分失败
Level 2: 核心功能（关键路径可用）
  ↓ 进一步失败
Level 1: 只读模式（数据完整性保障）
  ↓ 灾难性失败
Level 0: 安全停机（保存状态 + 告警）
```

### 安全即设计（Safety by Design）

**不是**：先构建功能，再���加安全检查
**而是**：安全约束是架构的一部分

示例：
- 文件修改 → 先备份，再修改，验证后提交
- 知识沉淀 → 先去重检查，再写入，索引后确认
- 模型升级 → 先沙箱测试，再灰度，全量后监控

## 对我们架构的映射

### 当前状态评估

| 框架要求 | 我们的实现 | 差距 | 优先级 |
|---------|-----------|------|--------|
| 外部锚定 | 人工 review + suggest | 无自动校准 | P0 |
| 闭环反馈 | 无 | 缺少自动评估器 | P0 |
| 中间件钩子 | 权限规则（model-capability.md） | 无运行时强制 | P1 |
| 环境感知 | memory/ + references/ | 无依赖图 | P2 |
| 确定性边界 | SKILL.md 定义命令 | 命令执行无状态机 | P1 |
| 三智能体架构 | 单智能体 | 无分离验证 | P2 |
| 轨迹感知日志 | execution.log（简单） | 无质量指标 | P0 |
| 验证感知规划 | 无 | 目标不可度量 | P0 |
| 优雅降级 | 无 | 失败即崩溃 | P1 |
| 安全即设计 | 部分（备份机制） | 不系统 | P1 |

### 立即可做（P0）

#### 1. 升级 execution.log 为轨迹感知日志

**当前格式**：
```
[YYYY-MM-DD HH:MM] <command> | <模型> | <摘要>
```

**升级格式**：
```
[YYYY-MM-DD HH:MM] <command> | <模型> | <摘要> | context_hash | output_hash | metrics
```

**metrics 包括**：
- SKILL.md 行数（检测膨胀）
- knowledge/ 文件数（检测冗余）
- learning-plan 待办数（检测积压）

#### 2. review 命令增加"退化检测"维度

**新增检查项**：

```markdown
## 退化检测

### 冗余度检查
- knowledge/ 文件是否有重复内容？
- SKILL.md 是否有冗余段落？

### 结构侵蚀检查
- SKILL.md 行数增长趋势（vs 基线）
- learning-plan 待办条目数（vs 完成数）

### 分布漂移检查
- 最近 N 次执行的命令分布（是否过度集中？）
- 最近 N 次报告的质量（是否下降？）
```

#### 3. evo-agent-model.md 增加"受限自我进化"章节

**新增章节**：

```markdown
## 受限自我进化（Constrained Self-Evolution）

### 核心原则

自我进化不等于自我改善。没有结构性约束的自我进化必然导致退化。

### 外部锚定机制

1. **人类反馈循环**
   - review self：定期自省
   - suggest：接受老板建议
   - status：暴露状态供老板监督

2. **结构性护栏**
   - SKILL.md 行数上限（触发重构）
   - knowledge/ 文件数上限（触发整合）
   - learning-plan 待办数上限（触发优先级重排）

3. **基线对比**
   - 每次 review 对比初始版本
   - 质量指标不得低于基线

4. **退化检测**
   - 轨迹感知日志
   - 自动识别冗余度/复杂度增长

### 验证感知规划

每个子目标必须回答：
- 成功标准是什么？
- 如何自动验证？
- 失败如何恢复？
- 副作用是什么？
```

### 中期规划（P1）

#### 1. 实现闭环反馈（Judge）

为每个子智能体定义"质量标准"：

```yaml
# 示例：kavabot-engineer 的质量标准
quality_standards:
  SKILL.md:
    max_lines: 500
    max_complexity: 15
  knowledge/:
    max_files: 50
    max_duplication: 0.2
  execution.log:
    min_success_rate: 0.8
```

review 命令自动运行这些检查。

#### 2. 增强权限约束为运行时钩子

当前：model-capability.md 定义权限，但无运行时强制。

升级：在工具调用前插入钩子，检查权限。

```python
def before_tool_call(tool, args, model):
    capability = get_capability(model)
    if tool in RESTRICTED_TOOLS and capability < REQUIRED_LEVEL:
        raise PermissionError(f"{model} 无权调用 {tool}")
```

#### 3. 为子智能体添加"重构触发器"

```markdown
## 重构触发器

当满足以下任一条件时，必须触发重构：

1. SKILL.md 超过 500 行
2. knowledge/ 文件超过 50 个
3. learning-plan 待办超过 20 个
4. 连续 3 次 review 检测到冗余度增长

重构流程：
1. 暂停日常工作
2. 整合/压缩/去重
3. 验证功能完整性
4. 更新基线
```

### 长期愿景（P2）

#### 1. 三智能体架构

将单智能体拆分为：

```
Planner（规划者）
  - 负责 plan 命令
  - 输出：学习计划 + 验证标准

Executor（执行者）
  - 负责 go/learn/scan 命令
  - 输出：知识沉淀 + 执行报告

Reviewer（评审者）
  - 负责 review 命令
  - 输出：质量评估 + 改进建议
```

**关键**：Reviewer 独立于 Executor，避免"自己评审自己"的偏差。

#### 2. SKILL.md 受控自修改

```
Agent 提出修改建议
  ↓
沙箱测试（隔离环境）
  ↓
质量评估（Reviewer 验证）
  ↓
人工确认（老板批准）
  ↓
应用到生产
```

这是走向 Level 2 递归自我改进的关键路径。

## 与已有知识的关联

- **#36 HyperAgents DGM-H**：提供进化能力（Level 2 递归改进）
- **#38 SlopCodeBench**：暴露退化风险（无约束进化的危险）
- **#40 本框架**：综合两者，形成"受限自我进化"
- **#2 Skill 进化的局限性**：本框架是对 #2 的工程化解决方案
- **#21 Agent Observability**：轨迹感知日志是可观测性的核心
- **#39 Durable Execution**：确定性边界需要持久执行支持

## 关键引用

- [The Impossible Trinity of Agentic AI](https://promptedllc.com/research/the-impossible-trinity-of-agentic-ai)
- [Anthropic Safety is Always Vanishing](https://api.emergentmind.com/papers/2602.09877)
- [Anthropic Harness Design](https://www.creolestudios.com/anthropic-harness-design-for-reliable-ai-agents/)
- [Trajectory Guard](https://arxiv.org/html/2601.00516v1)
- [Trajectory Anomaly Detection](https://arxiv.org/html/2602.06443v1)
- [Verification-Aware Planning](https://arxiv.org/html/2510.17109v1)
- [Reliable AI Agents Need Boundaries](https://cataluma.com/blog/ai-agents-reliable-secure-auditable)
- [Harness Engineering Guide 2026](http://www.nxcode.io/resources/news/what-is-harness-engineering-complete-guide-2026)

## 元数据

- created: 2026-03-31
- updated: 2026-03-31
- last_accessed: 2026-03-31
- access_count: 1
- study_count: 1
- category: agent-design
- volatility: low
- confidence: high
- status: active
