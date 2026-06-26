# 生产级多 Agent 编排模式与框架实践（2026）

> 学习次数：1（2026-04-02 深度学习）
> 来源：多轮 WebSearch 综合分析
> 关联学习项：#42 Agent-as-System、#44 Claude Tasks、#39 Durable Execution、#48 AgentOps

## 核心认知

### 2026 行业共识

1. **"Agent as System" 取代 "Agent as Prompt"**：生产级 Agent 不再是"一段精心设计的 Prompt"，而是包含状态管理、持久化、可观测性、故障恢复的完整系统
2. **多 Agent ≠ 万能**：行业出现"Multi-Agent Trap"反思——盲目拆分导致复杂度爆炸、延迟增加、调试困难。Cognition（Devin 背后公司）公开表示不使用多 Agent 系统
3. **混合架构成为主流**：CrewAI 做发现/推理 → LangGraph 做执行/控制，前端灵活后端可靠
4. **持久执行 > 检查点**：Diagrid 明确指出"Checkpoints Are Not Durable Execution"——LangGraph/CrewAI/ADK 的检查点只是状态快照，不等于真正的持久执行（Temporal/Dapr 级别）

### 何时使用多 Agent vs 单 Agent

**使用多 Agent 的条件**（至少满足 2 个）：
- 任务涉及多个独立领域（如代码 + 文档 + 测试）
- 需要并行执行以提高吞吐
- 需要相互校验/辩论来提高质量
- 工作流有明确的阶段划分

**保持单 Agent 的条件**：
- 任务高度连贯，上下文切换成本 > 并行收益
- 模型能力足够处理全部任务（Opus 4.6 这类大模型）
- 共享状态复杂度高，拆分后通信成本大
- 团队对调试多 Agent 系统经验不足

## 四大编排模式

### 1. Sequential（顺序链式）

```
Agent A → Agent B → Agent C → 结果
```

- **适用场景**：流水线式任务（研究→写作→审核）
- **优点**：简单、可预测、易调试
- **缺点**：延迟 = 所有步骤之和，瓶颈效应
- **生产实践**：CrewAI 的默认模式，适合大多数简单工作流

### 2. Parallel（并行扇出-汇聚）

```
         ┌→ Agent A ─┐
Input ───┼→ Agent B ──┼→ Aggregator → 结果
         └→ Agent C ─┘
```

- **适用场景**：多源搜索、并行审核、独立子任务
- **优点**：延迟 = 最慢一个步骤，高吞吐
- **缺点**：结果聚合复杂，需要幂等设计
- **生产实践**：Claude Code 的 Agent 工具就是并行模式

### 3. Hierarchical（层级管理者-工人）

```
         Coordinator
         ┌───┼───┐
    Manager A  Manager B
    ┌──┼──┐    ┌──┼──┐
   W1  W2 W3  W4  W5 W6
```

- **适用场景**：大规模任务分解、企业级多部门协作
- **优点**：清晰的职责分工、可嵌套扩展
- **缺点**：深层级通信开销大、协调器成为瓶颈
- **生产实践**：Google ADK 原生支持、LangGraph Supervisor 模式
- **变体**：Coordinator-Worker-Sub-agent（三层结构，适合中等复杂度）

### 4. Collaborative（协作/辩论）

```
Agent A ←→ Agent B ←→ Agent C
    ↕           ↕           ↕
    └───── 共享状态 ─────┘
```

- **适用场景**：需要多视角验证、创意生成、复杂推理
- **优点**：更高质量输出、自纠错能力
- **缺点**：非确定性、难以控制终止条件、Token 消耗高
- **生产实践**：AutoGen 的多 Agent 对话、Socratic Reasoning Framework
- **2026 新发现**：研究表明允许 Agent "粗鲁打断"对方反而提高推理质量

## 三大框架对比（2026 状态）

| 维度 | LangGraph | CrewAI | AutoGen |
|------|-----------|--------|---------|
| **核心范式** | 图状态机 | 角色团队 | 对话模式 |
| **最佳场景** | 生产级复杂持久工作流 | 快速原型/角色委派 | 研究/动态对话 |
| **控制力** | 高（显式状态/流程） | 中（角色抽象） | 高（但涌现/流动） |
| **学习曲线** | 陡峭 | 最简单 | 中等 |
| **持久化** | 检查点（PostgreSQL/SQLite） | 基础 | 基础 |
| **可观测性** | LangSmith 集成 | 有限 | 有限 |
| **人机协作** | 原生支持 | 有限 | 对话式支持 |
| **生态成熟度** | 最成熟 | 快速增长 | 微软生态 |

### 2026 新玩家

- **Google ADK**：原生多 Agent 支持，与 Vertex AI 深度集成
- **Dapr Agents 1.0**（CNCF）：真正的持久执行，基于 Dapr 的分布式运行时
- **Amazon Bedrock AgentCore**：AWS 原生 Agent 基础设施
- **Claude Code Agent SDK**：Anthropic 的 Agent 工具链（我们正在使用的）

## 持久执行：检查点 vs 持久工作流

### Diagrid 的核心论点

> "Checkpoints Are Not Durable Execution"

**检查点（LangGraph 等）的局限**：
- 只保存 Agent 状态快照，不保存工具调用的副作用
- 从检查点恢复 = 重新执行工具调用，可能导致重复副作用
- 不保证 exactly-once 语义
- 适合短期任务，不适合长时间运行的工作流

**持久执行（Temporal/Dapr）的特点**：
- 保存完整的事件历史（Event Sourcing）
- 从任意点恢复时，replay 事件历史而非重新执行
- 保证 exactly-once 语义
- 适合需要故障恢复的长时间工作流

### 四大持久 Agent 模式（Diagrid 总结）

1. **Durable Tool Execution**：工具调用的持久化和重试
2. **Durable Agent Conversation**：对话历史的持久化
3. **Durable Multi-Agent Workflow**：多 Agent 协作的持久化
4. **Durable Human-in-the-Loop**：人机交互等待的持久化

## 映射到我们的架构

### 当前架构 vs 行业标准

| 维度 | 我们的架构 | 行业标准 | 差距 |
|------|-----------|---------|------|
| **编排模式** | Hierarchical（steward → 子智能体）| 混合模式 | 只有一种模式 |
| **状态管理** | execution.log（append-only） | 图状态机 + 检查点 | 无结构化状态 |
| **持久化** | 文件系统（memory/） | PostgreSQL + Event Sourcing | 够用但不优雅 |
| **可观测性** | 单行日志 | Tracing + Metrics + Logging | 差距大 |
| **故障恢复** | 无（依赖 scheduler 重新调度） | 检查点恢复 | 无容错 |
| **人机协作** | AskUserQuestion（同步） | 异步等待 + 恢复 | 够用 |

### 关键洞察：我们的定位

**我们不需要完整的生产级 Agent 基础设施**，原因：

1. **执行环境是 Claude Code**：本身就是交互式的，不需要独立的运行时
2. **状态通过文件系统持久化**：memory/ 目录天然持久，不需要数据库
3. **scheduler 是轻量级 cron**：不是通用编排器，定位清晰
4. **单会话上下文**：每次唤醒是独立会话，不需要跨会话状态恢复

**但我们可以借鉴的**：

1. **从 Hierarchical 模式**：steward 的多角色管理可以引入"任务分解 + 并行执行 + 结果聚合"
2. **从 Collaborative 模式**：review 命令可以引入"交叉校验"——让另一个智能体视角审视
3. **从持久执行**：execution.log 可以增加结构化字段（工具调用记录、状态变更），使其具备轻量级"事件历史"能力
4. **从 Multi-Agent Trap**：避免过度拆分。我们的智能体粒度（按领域角色拆分）是合理的，不需要再拆更细

### 具体行动建议

1. **steward 的升级方向**：
   - 当前：串行代理唤醒（"叫 XX 过来"）
   - 建议：支持并行唤醒（"让 A 和 B 同时做 X 和 Y"）→ 映射到 Parallel 模式
   - 可用 Claude Code 的 Agent 工具实现并行执行

2. **review 命令的升级方向**：
   - 当前：单一视角自省
   - 建议：引入"第二视角"——调用另一个智能体对同一产出进行交叉审查
   - 这是 Collaborative 模式的轻量应用

3. **execution.log 的升级方向**：
   - 当前：`[时间] 命令 | 模型 | 摘要` 单行格式
   - 建议：增加结构化字段——`工具调用次数 | 输入 Token | 输出 Token | 命令级错误计数`
   - 这是"轻量级可观测性"的第一步

4. **scheduler 保持现状**：
   - cron 调度器定位正确——不要试图做成 LangGraph 或 Temporal
   - 如果未来需要更复杂的编排，考虑在 scheduler 上层引入 workflow 概念

## 参考来源

- [CrewAI vs LangGraph vs AutoGen 对比](https://openagents.org)
- [Checkpoints Are Not Durable Execution](https://www.diagrid.io/blog/checkpoints-are-not-durable-execution)
- [Dapr Agents 1.0 GA](https://cloudnativenow.com/kubecon-cloudnativecon-europe-2026/cncf-announces-general-availability-of-dapr-agents-v1-0-for-production-ai-workloads/)
- [Multi-Agent Trap](https://towardsdatascience.com/the-multi-agent-trap/)
- [Claude Code's Hidden Multi-Agent System](https://paddo.dev/blog/claude-code-hidden-swarm)
- [Google ADK Multi-Agents](https://google.github.io/adk-docs/agents/multi-agents/)
- [CNCF Cloud Native Agentic Standards](https://www.cncf.io/blog/2026/03/23/cloud-native-agentic-standards/)
- [AI Agent Orchestration Guide 2026](https://ztabs.co/blog/ai-agent-orchestration-guide)
- [Why Cognition Does Not Use Multi-Agent Systems](https://jxnl.co/writing/2025/09/11/why-cognition-does-not-use-multi-agent-systems/)
