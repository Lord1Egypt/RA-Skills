# Pattern 4.1: 三种委托模式选型（Coordinator / Fork / Swarm）

## 问题

需要多个 agent 并行工作，但不同任务适合不同的协调方式。选错模式会导致 context 爆炸（Fork 用在大任务上）、协调混乱（Swarm 没有领导者）、或效率低下（Coordinator 用在简单并行上）。

来源：Claude Code 内部 + 开源 skill 蒸馏实践 + Anthropic "Building multi-agent systems"

## 三种模式

| 模式 | Context 共享 | 适用场景 | 约束 |
|------|-------------|---------|------|
| **Coordinator** | 无——worker 从零开始 | 复杂多阶段任务（research → synthesize → implement → verify） | 最慢但最安全 |
| **Fork** | 完整——child 继承 parent 上下文 | 快速并行分支，共享已加载的上下文 | **单层限制**——Fork 的 child 不能再 Fork |
| **Swarm** | 点对点——通过共享 task list | 长期独立工作流 | **扁平名单**——teammate 不能 spawn 新 teammate |

## 黄金法则

> Coordinator must synthesize, not delegate understanding — "Based on your findings, fix it" is an anti-pattern.

Coordinator 收到 worker 的结果后，MUST 自己理解并综合，而不是把原始结果直接传给下一个 worker。这是来自 Anthropic 博客的核心原则。

## 选型决策树

```
需要多 agent？
├── worker 需要 parent 的 context 吗？
│   ├── 是 → Fork（但注意单层限制）
│   └── 否 → worker 之间需要协调吗？
│       ├── 是，需要分阶段 → Coordinator
│       └── 否，各自独立 → Swarm
```

## Fork 的单层限制与 Cache 继承

**为什么限制单层**：Fork child 继承完整的 parent context。递归 Fork 的 context 成本指数增长。Claude Code 内部的实现中，Fork tool 在 child agent 的 tool pool 中仍然可见（为了 cache sharing），但在 call time 被 guard 阻止。

**Prompt cache 继承**：Fork subagent（`isForkSubagentEnabled()` 开启）不仅继承 parent 的对话历史，还共享 parent 的 prompt cache。这意味着 Fork 的第一次 API 调用只需付 cache read 的价格（$0.003/1K tokens），而不是 full input 的价格（$0.036/1K tokens）。

Fresh worker（非 Fork）从空 context 开始，没有 cache 可共享。

**选 Fork 还是 Fresh 的关键依据**：
- Worker 需要 parent 已经加载的文件和讨论 → Fork（省 token，启动快）
- Worker 的任务和 parent 的 context 无关 → Fresh（不浪费 context 装无关内容）
- Worker 需要写 memory 或做危险操作 → Fresh（Fork child 的工具集受限：no recursive delegation, no clarify, no memory writes）

## Swarm 的扁平名单

**为什么**：teammate 不能创建新 teammate，防止不可控增长。roster 保持扁平。所有 teammate 通过 file-based mailbox 通信（JSON 文件 + lockfile 序列化，10 次重试，5-100ms 指数退避）。

## Coordinator 的四阶段工作流

1. **Research**（并行）：多个 worker 各自探索不同区域
2. **Synthesis**（coordinator 独占，绝不委派）：综合所有 research 结果
3. **Implementation**（按文件集序列化）：写并行、但同一文件串行，防止 merge conflict
4. **Verification**（并行）：多个 worker 各自验证不同方面

## 与现有 Pattern 的关系

- Pattern 3.1 (Handoff) 是 Coordinator 模式的核心机制——阶段间通过 handoff 文档传递上下文
- Pattern 2.5 (Component-Scoped Hooks) 可以给不同 worker 配不同的验证门禁
- Pattern 1.1 (Ralph) 可以用在 Coordinator 上确保整个流程不会半途而废

## Review-Execution 分离实践

本项目蒸馏过程中使用了 Review-Execution 分离模式：
- **Codex (GPT 5.4 xhigh)** 做 review——以全新视角对照源码审查
- **Claude Code (Opus 4.6 max)** 做 execution——带着对先前决策的完整理解
- 两个 agent 互不可见对方的 session
- 每轮 review-action 都在新 session 中执行（fresh token budget）
- 通过 handoff 文件协调（不依赖 session 内的上下文）

这本质上是 Coordinator 模式的变体：人作为 coordinator，两个 agent 作为 specialized worker。
