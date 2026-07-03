# 多智能体协作

## 设计原理

### 为什么需要多 Agent 协作？

单 Agent 的三重瓶颈：
- **上下文窗口有限**（200K tokens）：单 Agent 处理多文件项目探索时，文件内容 + 工具结果快速填满窗口
- **认知负载饱和**：任务复杂度超过一定阈值后，Agent 开始"迷失"——跳过步骤、遗忘约束、产出质量下降
- **无并行能力**：线性的 read → think → act 循环无法利用并行资源

多 Agent 协作的本质是**分治策略**——将复杂任务拆解为独立子任务，分配给多个子 Agent 并行处理，最后综合结果。

### 子 Agent 上下文隔离设计（核心机制）

**为什么必须隔离上下文？**

如果子 Agent 共享父 Agent 的完整消息历史，每个子 Agent 都携带 100K+ tokens 的历史包袱。10 个子 Agent × 100K tokens = 1M tokens 的上下文开销，经济上不可行，认知上不可维护。

**上下文隔离机制：**

```
┌──────────────────────────────────────────────────────┐
│  父 Agent (Coordinator)                              │
│  messages: [sys_prompt, ..., user_task]  (30K tokens)│
│                                                      │
│  接收到子 Agent 结果：summary (500 tokens) ← 不是原始数据 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────────┐  ┌─────────────────┐            │
│  │ 子 Agent A      │  │ 子 Agent B      │            │
│  │ messages: []    │  │ messages: []    │  ← 空白启动│
│  │ + sys_prompt    │  │ + sys_prompt    │            │
│  │ + subtask_A     │  │ + subtask_B     │            │
│  │ (total ~8K)     │  │ (total ~8K)     │            │
│  │                 │  │                 │            │
│  │ 结果 → summary  │  │ 结果 → summary  │            │
│  └─────────────────┘  └─────────────────┘            │
└──────────────────────────────────────────────────────┘
```

**Token 节省量化分析（10 文件探索场景）：**

```
场景：探索 10 个文件，每个文件约 2000 行

方案 A（无隔离，单 Agent）：
  读取 10 个文件 → 10 × ~5K tokens 工具输出 = 50K tokens
  全部保留在上下文中 → 累积在消息列表中
  总上下文占用：~50K tokens（仅文件内容）

方案 B（上下文隔离，多 Agent）：
  10 个子 Agent，各处理 1 个文件
  每个子 Agent 上下文：~5K（sys_prompt + 1 个文件）
  每个子 Agent 返回摘要：~200 tokens
  父 Agent 收到的总摘要：10 × 200 = 2K tokens
  总上下文占用：~2K tokens（父 Agent 视角）

节省率：(50K - 2K) / 50K = 96%
```

**启动开销量化：**
每个子 Agent 需要独立加载 system prompt → 约 5-10K tokens/子 Agent。在 10 文件场景下，10 个子 Agent × 8K 系统提示 = 80K 系统提示总开销。但系统提示通过 **prompt cache** 命中（前缀稳定），实际 API 计费 token 远低于此值。

**关键设计约束：**
- 子 Agent 从空白 `messages` 列表启动，不继承父 Agent 的任何对话历史
- 子 Agent 完成后，**只向父 Agent 返回摘要**（结构化 summary），不返回原始工具输出或完整对话
- 父 Agent 看到的是压缩后的信息——这意味着父 Agent 的决策质量取决于摘要质量

---

## Worktree 隔离机制

子 Agent 的文件系统隔离通过 Git worktree 实现。这是多 Agent 协作中保证文件操作安全的关键机制：

```
宿主机文件系统：
  /project/
    ├── .git/                  ← 共享 Git 仓库
    ├── main/                  ← 主 worktree（父 Agent 工作区）
    └── worktrees/
        ├── agent-a/           ← 子 Agent A 的隔离 worktree
        │   └── (从 main 检出)
        ├── agent-b/           ← 子 Agent B 的隔离 worktree
        │   └── (从 main 检出)
        └── agent-c/           ← 子 Agent C 的隔离 worktree
            └── (从 main 检出)
```

**隔离特性：**
- 每个子 Agent 拥有独立的文件系统视图——对文件的修改互不干扰
- Git worktree 保证分支隔离：子 Agent A 的 commit 不会污染子 Agent B 的工作区
- 子 Agent 完成后，worktree 中的变更通过 PR/branch 形式合并回主 worktree
- 沙箱与 worktree 组合：子 Agent 的沙箱根目录即为其 worktree 路径，无法访问其他 worktree

**生命周期：**
```
创建：parent spawns sub-agent → `git worktree add worktrees/agent-N`
执行：sub-agent operates within worktree/agent-N
提交：sub-agent returns summary + `git diff` to parent
清理：parent evaluates → `git worktree remove worktrees/agent-N`
```

---

## Coordinator 模式（中心化协调）

### 任务分解算法（抽象设计，非可执行代码）

Coordinator 的核心职责是将复杂任务分解为可并行执行的独立子任务。分解质量直接决定多 Agent 协作的效率和结果质量。

**任务分解策略：**

```
算法：Coordinator.decompose(complexTask) → List[SubTask]

阶段 1 —— 依赖分析
  ├── 构建任务依赖图 DAG
  │   ├── 顶点 = 任务单元（文件、模块、功能点）
  │   └── 边 = 依赖关系（A 的输出是 B 的输入）
  ├── 找出所有入度为 0 的顶点 → 第 1 批并行子任务
  └── 标记依赖链 → 顺序执行批次

阶段 2 —— 独立性判定
  ├── 判定条件：
  │   ├── 操作的文件集合是否无交集？
  │   ├── 结果是否可以独立验证？
  │   └── 是否需要其他子任务的中间产物？
  ├── 若满足全部条件 → 标记为独立子任务，可并行
  └── 若任一条不满足 → 标记为依赖子任务，需顺序执行

阶段 3 —— 粒度控制
  ├── 过粗：单个子任务仍然超过 30K tokens 上下文 → 继续拆分
  ├── 过细：子任务 < 1K tokens → 启动开销 > 执行开销 → 合并
  └── 黄金粒度：每个子任务预估 5-15K tokens 上下文占用
```

**子 Agent 分配策略：**

```
算法：Coordinator.allocate(subtasks, agents) → Map<Agent, SubTask>

策略选项：
  A. 轮转分配（Round-Robin）
     - 适合：同构 Agent，子任务难度均匀
     - 复杂度：O(n)

  B. 启发式分配（Heuristic Matching）
     - 适合：异构 Agent（不同 skill/工具集）
     - 逻辑：为每个子任务匹配最合适的 Agent profile
     - 复杂度：O(n × m)，n=子任务数, m=Agent类型数

  C. 负载感知分配（Load-Aware）
     - 适合：子任务大小不均
     - 逻辑：预估每个子任务的 token 消耗，动态分配给最空闲的 Agent
     - 复杂度：O(n log m)（优先队列）
```

**结果综合策略：**

```
算法：Coordinator.synthesize(results) → FinalOutput

综合模式：
  模式 1 —— 拼接（Concatenation）
    - 使用场景：子结果互不重叠（如各模块的文档、各文件的测试）
    - 操作：按顺序拼接 → 格式统一 → 输出

  模式 2 —— 合并（Merge）
    - 使用场景：子结果有重叠域（如多个子 Agent 改同一文件的不同部分）
    - 操作：diff 合并 → 冲突检测 → 人工或自动解决冲突

  模式 3 —— 总结（Summarization）
    - 使用场景：子结果信息量大，需提炼核心发现
    - 操作：LLM 通读所有子结果 → 生成综合报告 → 标注各发现的来源

  模式 4 —— 验证后合并（Verify-then-Merge）
    - 使用场景：子结果需要交叉验证（如一个 Agent 生成代码，另一个生成测试）
    - 操作：运行验证 Agent → 检查一致性 → 若失败则重新调度
```

---

## Swarm 模式（去中心化协调）

### Coordinator vs Swarm 对比

| 特性 | Coordinator | Swarm |
|------|-------------|-------|
| 控制方式 | 中心化（一个协调者分配任务） | 去中心化（Agent 间对等通信） |
| 通信方式 | 主从（Parent → Child） | 对等（Peer-to-Peer 消息广播） |
| 任务分配 | 协调者主动分解和分配 | Agent 自行根据消息选择任务 |
| 适用场景 | 任务可预先分解（结构化任务） | 任务边界模糊（探索性任务） |
| 复杂度 | 低——协调者逻辑是瓶颈 | 高——需要共识算法和冲突解决 |
| 结果质量 | 取决于协调者分解质量 | 取决于 Agent 间通信效率 |
| 可预测性 | 高——执行路径确定 | 低——涌现行为，难以预测 |
| 故障容错 | 低——协调者单点故障 | 高——无单点，Agent 可互相替代 |
| 建议规模 | 3-10 个子 Agent | 5-50 个 Agent |

### Swarm 设计要点（抽象设计，非可执行代码）

**通信模型：**

```
Agent 间通信通过消息总线（Message Bus）实现：
  ├── 每条消息包含：sender_id, recipient_id（可为广播）, content, priority, ttl
  ├── 消息类型：TaskProposal, TaskClaim, ResultShare, ConflictAlert, ConsensusVote
  └── 消息持久化：总线保证消息不丢失，Agent 离线期间消息排队

共识机制（简化 Raft 风格）：
  ├── 提议阶段：任一 Agent 提出任务分配方案
  ├── 投票阶段：其他 Agent 对方案投票（accept/reject）
  ├── 达成条件：超过半数 Agent 在 TTL 内接受
  └── 超时处理：若超时未达成 → 随机退避后重新提议
```

**Swarm 适用性约束：**
Swarm 模式在以下条件同时满足时才优于 Coordinator：
1. 任务无法预先分解（子任务边界在执行中涌现）
2. Agent 数量 > 5（并行度需要去中心化调度）
3. 对结果的可预测性要求较低（接受探索性输出）
4. 通信开销（消息传递 tokens）相对于执行开销可忽略

---

## 规模适应性指南

### Minimal（最小可行）

多 Agent 协作不适用于 Minimal 规模——此规模下 Agent 本身的能力有限，上下文隔离和 worktree 的复杂度远超收益。**建议跳过**，用单 Agent 顺序处理。

### Professional（专业级）

- 实现 Coordinator 模式：任务分解 + 子 Agent 分配 + 结果综合
- 子 Agent 数量：3-5 个
- 上下文隔离：子 Agent 空白启动 + 摘要返回
- 不需要 Worktree：子 Agent 操作同一工作区但不同文件（通过文件级锁协调）
- 通信：函数调用（同进程内），无消息总线
- 代码量：~500-800 行

### Enterprise（企业级）

- 全功能实现：Coordinator + Swarm 双模式，按任务特征自动切换
- 子 Agent 数量：5-50 个，支持动态扩缩
- Worktree 隔离：每个子 Agent 独立 Git worktree + Docker 沙箱
- 消息总线：异步消息队列，支持 Agent 离线排队
- 共识算法：完整实现，含投票超时和冲突解决
- 监控：每个子 Agent 的 token 消耗、执行时间、成功率实时看板
- 代码量：~2000-3500 行

---

## 常见陷阱与失效模式

### 陷阱 1：子 Agent 上下文膨胀

**症状**：父 Agent 将完整对话历史注入子 Agent 的初始消息中，"为了方便子 Agent 理解背景"。

**后果**：10 个子 Agent 各带 100K 历史 → 1M tokens 上下文浪费。96% 的隔离收益消失。

**解决**：子 Agent 初始 messages 必须为空数组。仅通过 subtask 描述传递必要信息。如果 subAgent 需要历史上下文，父 Agent 应在分解 subtask 时主动提取相关信息塞入 subtask 描述。

### 陷阱 2：摘要信息丢失

**症状**：子 Agent 返回的摘要过于粗略（"检查完毕，没问题"），关键发现被丢弃。

**根因**：没有强制执行摘要结构。

**解决**：定义 Summary 的结构化 Schema（findings、files_modified、errors、suggestions 为必填字段）。在子 Agent 的系统提示中明确要求按 Schema 输出。Coordinator 在综合前校验 Schema 完整性——不完整的摘要退回子 Agent 重做。

### 陷阱 3：Task 分解粒度过细

**症状**：Coordinator 将"修改一个函数"拆成 5 个子任务，每个子 Agent 只改 3 行代码。

**后果**：子 Agent 启动开销（~8K tokens 系统提示）远超执行开销。Token 效率反而低于单 Agent 处理。

**解决**：每个子任务至少 5K tokens 预估上下文占用。低于此阈值的子任务应合并。

### 陷阱 4：Worktree 泄漏

**症状**：子 Agent 创建了 worktree 但 Coordinator 未能清理，磁盘上残留大量孤立 worktree。

**解决**：在 Coordinator 的 `finally` 块中执行 worktree 清理（类似 RAII 模式）。启动时先扫描 `worktrees/` 目录并清理上次会话的残留。

### 陷阱 5：Swarm 共识死锁

**症状**：Swarm 模式下，Agent 在投票阶段永远无法达成过半共识——每个 Agent 坚持自己的方案。

**解决**：设置最大投票轮次（3 轮）。超轮次后，随机选择一个 Agent 方案作为最终方案（Dictator Fallback）。或改用 Coordinator 模式降级。

---

## AI 构建提示

构建多 Agent 协作系统时，AI 不应直接复制代码，而应根据以下提示自行实现：

1. **先建抽象接口**：
   - `SubAgent` 接口：`execute(subtask, context) → Summary`。不接受完整消息历史。
   - `Coordinator` 接口：`decompose(task) → SubTask[]` → `allocate(subtasks, agents) → Assignments` → `synthesize(summaries) → Result`
   - `MessageBus` 接口（Swarm 用）：`publish(msg)`, `subscribe(pattern)`, `consume()`

2. **上下文隔离是硬约束**：子 Agent 构造函数不接受 messages 参数。子 Agent 内部自行构建消息列表，系统提示从模板注入。

3. **摘要格式标准化**：子 Agent 返回的摘要必须有固定结构——至少包含 `{findings, files_modified, errors, suggestions}` 字段。无结构摘要会导致综合阶段解析失败。

4. **Task decomposition 使用 LLM 辅助**：不要让 Coordinator 硬编码分解逻辑。将任务描述输入 LLM，要求输出结构化子任务列表（含依赖关系），然后 Coordinator 做 DAG 构建和并行调度。

5. **错误隔离**：一个子 Agent 失败不应阻塞其他子 Agent。Coordinator 收集所有子 Agent 结果后，对失败的任务决定：重试 / 替代方案 / 跳过并标记。

6. **测试策略**：
   - 单元测试：decompose → 验证子任务独立性（文件无交集）、synthesize → 验证摘要结构完整性
   - 集成测试：3 个子 Agent 并行处理同一项目的不同模块 → 验证 worktree 隔离（A 的修改不影响 B）、验证结果综合正确

7. **Worktree 实现**：通过 `git worktree` CLI 创建隔离工作区。子 Agent 的 `workdir` 指向其 worktree 路径。完成后由 Coordinator 执行 `git worktree remove` 清理。若子 Agent 在 worktree 中产生了有价值的变更，Coordinator 先 `git merge` 或创建 branch 再清理。

8. **Swarm 模式的共识算法**使用"轻量 Raft"——不实现完整的日志复制，只实现 Leader 选举和提议投票。Agent 数量通常 < 50，不需要完整的分布式共识协议。