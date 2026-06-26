# Multi-Agent — Extended Patterns

### E4.1: Cache-Safe Forking
**What it does**: Fork 模式下 child agent 继承 parent 的完整 prompt prefix（系统指令 + 对话历史到 fork 点）。这让 child 的首次 API 调用命中 parent 的 prompt cache，避免为共享前缀重复计算。
**Why it matters**: Fork 的价值在于"不用重新加载 context"。如果 fork 后 child 的 API 调用无法利用 parent 的 cache，fork 退化成一个带有初始上下文的 Coordinator——有额外的 context 开销但没有 cache 收益。Cache-safe forking 让 fork 的延迟和成本优势真正生效。
**Source evidence**: Claude Code Fork 工具的实现。Anthropic prompt caching 的 prefix matching 机制。OMC 的 cache-sharing 策略。

### E4.2: Complete Context Isolation
**What it does**: Coordinator 模式下 worker agent 从零 context 开始——不继承 coordinator 的对话历史。Worker 只看到 coordinator 显式传入的任务描述。Worker 的工具结果也不会回流到 coordinator 的 context（coordinator 只看 worker 的最终输出）。
**Why it matters**: 共享 context 看似高效，实际有两个隐患：(1) coordinator 的探索性对话（多次尝试、回退）会误导 worker；(2) worker 的大量工具输出会污染 coordinator 的 context。完全隔离让每个 agent 在干净的环境中工作，通过结构化 handoff 传递必要信息。
**Source evidence**: Claude Code Coordinator 模式的 worker 隔离设计。Anthropic multi-agent 最佳实践。

### E4.3: 4-Phase Workflow
**What it does**: 将复杂任务分为 4 个固定阶段执行：(1) Research——多 worker 并行探索，收集信息；(2) Synthesis——coordinator 独占，综合 research 结果（不可委派）；(3) Implementation——按文件集分配 worker，同文件串行、跨文件并行；(4) Verification——多 worker 并行验证不同方面。
**Why it matters**: 没有固定 workflow 的 coordinator 会"边 research 边 implement"——在信息不完整时就开始写代码，发现不对再推倒重来。4 阶段强制先全面了解再动手，synthesis gate（单独的 pattern）确保 coordinator 真的理解了 research 结果。Implementation 阶段的"同文件串行"防止 merge conflict。
**Source evidence**: Claude Code Coordinator 模式的推荐工作流。Anthropic multi-agent 博客。OMC 的多阶段任务执行流程。

### E4.4: File-Based Mailbox
**What it does**: Swarm 模式下 teammate 之间通过 JSON 文件通信——每个 teammate 有独立的收件箱目录（`.coordination/mailbox/<teammate-id>/`），消息写入 JSON 文件。并发写入通过 lockfile + 指数退避（10 次重试，5-100ms 间隔）序列化。
**Why it matters**: Agent 运行在不同进程（tmux pane / headless session），无法使用内存中的消息传递。文件系统是唯一的可靠共享通道。Lockfile 防止并发写入损坏 JSON，指数退避防止锁竞争下的 CPU 空转。消息持久化还允许 crash 恢复——重启后读取 mailbox 即可了解错过的消息。
**Source evidence**: OMC Swarm 的 file-based communication 机制（10 次重试，5-100ms 指数退避）。经典的 mailbox 并发模式。

### E4.5: Permission Delegation
**What it does**: Worker agent 不直接处理权限请求——当 worker 遇到需要人类确认的操作（destructive bash 命令、MCP 权限等），将权限请求上报给 coordinator/leader，由 leader 决策或转发给人类。Worker 的 `allowedTools` 被限制为安全子集。
**Why it matters**: Worker 运行在 headless 模式，没有交互能力来请求人类确认。如果 worker 有完整权限，一个失控的 worker 可以做任何事。Permission delegation 确保破坏性操作经过有权限决策能力的 agent（coordinator）或人类审批。
**Source evidence**: Claude Code 的 `--allowedTools` 参数。Coordinator 模式下 worker 权限配置最佳实践。

### E4.6: Structured Message Protocol
**What it does**: Agent 之间的通信使用结构化消息类型而非自由文本。定义的消息类型包括：`shutdown`（请求 teammate 停止）、`plan_approval`（请求确认执行计划）、`permission`（权限请求上报）、`status_update`（进度通报）、`task_result`（任务结果提交）。每种类型有固定的 JSON schema。
**Why it matters**: 自由文本通信依赖 agent 正确解读对方的意图——"我觉得可以开始了"是同意还是建议？结构化消息消除歧义，让接收方可以用确定性逻辑（jq/代码）处理消息而非依赖 LLM 理解。特别是 `shutdown` 消息——必须被可靠识别和执行，不能被 agent 的"我还没做完"推理覆盖。
**Source evidence**: OMC Swarm 的消息协议。Claude Code 内部的 agent 间通信 schema。
