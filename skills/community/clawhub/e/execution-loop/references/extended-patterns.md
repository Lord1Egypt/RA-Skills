# Execution Loop — Extended Patterns

### E1.1: Explicit Cross-Turn State Object
**What it does**: 将跨 turn 的状态封装到一个显式的 State 类型（如 QueryEngine 中的 `{messages, tools, context_usage, turn_count}`），每轮循环接收旧 state、产出新 state，而非依赖闭包或全局变量。
**Why it matters**: Agent 的执行循环在每轮需要做决策（是否继续、是否 compact、是否切换工具集），这些决策依赖跨 turn 的累积状态。隐式状态（散布在多个变量里）导致决策逻辑脆弱——改一个变量忘了改另一个。显式 State 对象让状态转换可追踪、可序列化、可在 crash 后恢复。
**Source evidence**: Claude Code 内部的 QueryEngine 类使用类型化的 state 对象在 `agentic_loop` 的每轮循环中传递。OMC 的 `persistent-mode.mjs` 在每次 Stop hook 触发时读写完整的 `ralph.json` state。

### E1.2: Multi-Layered Stop Conditions
**What it does**: 定义 5 种独立的停止语义，按优先级从高到低评估：(1) 紧急停止（context >=95%、auth 失败）→ 无条件放行；(2) 用户取消（cancel 信号 + TTL）→ 放行并清理；(3) 闲置超时（2h 无活动）→ 放行并标记 stale；(4) 迭代上限（max_iterations）→ 放行或 auto-extend；(5) 任务完成（checklist 全 checked）→ 放行。
**Why it matters**: 单一停止条件不够——只看迭代数会在 context 溢出时崩溃，只看 context 会在认证失败时浪费 token。分层且有优先级的停止条件确保在任何异常场景下都有合理的退出路径，不会出现"该停的时候停不下来"或"不该停的时候停了"。
**Source evidence**: OMC `persistent-mode.mjs` 的 5 个 NEVER-block 安全阀。Claude Code 内部的 `shouldStop()` 多条件评估。

### E1.3: Budget Enforcement Triad
**What it does**: 同时施加三种独立的预算约束：USD 成本上限（`--budget`）、执行轮数上限（`--max-turns`）、token 消耗上限（context window 的 95%）。三者中任一触顶即停止，互为安全网。
**Why it matters**: 单一预算维度有盲区：token 上限不防慢速高轮次任务、轮次上限不防单轮高 token 消耗、USD 上限不防 context 溢出。三维约束覆盖所有资源消耗模式。在 headless 场景尤其重要——没有人类监督，预算是唯一的自动刹车。
**Source evidence**: Claude Code CLI 的 `--max-turns` 和 `--budget` 参数。OMC 的 strict 模式同时检查 iteration count + context usage + cost。

### E1.4: Streaming Tool Execution
**What it does**: 在模型 response 还在流式生成时，一旦检测到完整的 tool_use block，立即开始执行该工具调用，不等整个 response 结束。
**Why it matters**: Agent 一轮交互中经常产生多个工具调用。如果等所有 tool_use block 都生成完再执行，耗时 = 生成时间 + 串行执行时间。Streaming 执行让生成和执行重叠，显著降低端到端延迟——尤其是当第一个 tool_use 是慢操作（如 Bash 编译）时。
**Source evidence**: Claude Code 内部的 tool execution pipeline 在流式 response 中检测完整的 tool_use JSON block 后立即 dispatch。需要 `isConcurrencySafe()` 标记来判断是否可以与其他工具并行执行。
