# Tool Governance — Extended Patterns

### E2.1: Tool Concurrency Safety
**What it does**: 每个工具声明 `isConcurrencySafe()` 属性——标记该工具是否可以与其他工具并行执行。Read/Glob/Grep 返回 true（只读操作），Write/Edit/Bash 返回 false（有副作用）。执行引擎在收到多个 tool_use block 时，只有全部 concurrency-safe 的工具才并行执行。
**Why it matters**: 并行执行工具调用能显著降低延迟（E1.4），但 Write + Read 同一文件时并行会读到过期内容。`isConcurrencySafe()` 是细粒度的并发控制——不需要全局串行化，只对有副作用的工具加锁。
**Source evidence**: Claude Code 内部的 Tool 接口定义。流式工具执行（E1.4）依赖此标记做并行决策。

### E2.2: Ordered Context Replay
**What it does**: 当多个工具并行执行时，将结果按原始 tool_use block 在 response 中的出现顺序重新排列后再送回模型。即使 Tool B 先于 Tool A 完成，模型看到的顺序仍是 A → B。
**Why it matters**: 模型的推理依赖工具结果的顺序。如果模型说"先看文件 A，再看文件 B"，但 B 的结果先返回，模型可能混淆两个结果的对应关系。保持顺序一致性让并行执行对模型透明——模型不知道也不需要知道执行是并行的。
**Source evidence**: Claude Code 内部的 tool result aggregation 逻辑。并行执行框架中的 result ordering 机制。

### E2.3: Schema-Driven Tool Registration
**What it does**: 每个工具用 Zod schema 定义输入和输出类型，一份 schema 同时服务 4 个消费者：(1) 发送给模型的 tool description（自动从 schema 生成 JSON Schema）；(2) 运行时输入验证（parse before execute）；(3) TypeScript 类型推断（`z.infer<typeof schema>`）；(4) hook 系统的 tool_input 类型校验。
**Why it matters**: 手动维护 tool description + 运行时验证 + 类型定义会出现不一致——description 说支持某参数但运行时 schema 没定义。Single source of truth 消除这类 bug。模型看到的 tool description 和实际的验证规则始终同步。
**Source evidence**: Claude Code 的 `buildTool()` 函数使用 Zod schema 作为唯一的工具定义来源。

### E2.4: Fail-Closed Defaults via buildTool()
**What it does**: 工具注册的 `buildTool()` 工厂函数强制要求定义 permission check、input schema、error handler。遗漏任何一项的工具无法注册——编译时报错而非运行时漏过。默认行为是拒绝（fail-closed），而非允许（fail-open）。
**Why it matters**: 新增工具时最容易犯的错误是"先让功能跑通，后面再加权限检查"。Fail-open 的默认值意味着每个遗漏都是一个安全漏洞。`buildTool()` 把安全检查从"opt-in"变成"opt-out"——你必须显式声明"这个工具不需要权限检查"，而非默认不检查。
**Source evidence**: Claude Code 内部的 Tool registration API。安全工程的 fail-closed 原则。

### E2.5: Bash 6-Layer Defense-in-Depth
**What it does**: Bash 工具的安全防护分 6 层，每层独立运作：(1) 命令黑名单（正则匹配危险模式）；(2) 路径边界（realpath 检查）；(3) seatbelt/sandbox（OS 级沙箱）；(4) 权限降级（非 root 执行）；(5) 超时限制（命令执行时间上限）；(6) 输出截断（防止巨量输出填满 context）。
**Why it matters**: 任何单一防护层都可以被绕过——正则可以用 `eval` 逃逸、路径检查可以用符号链接绕过、沙箱可能配置不当。6 层独立防护的价值在于：攻击者需要同时绕过所有 6 层才能造成伤害。每层的误报和漏报模式不同，叠加后整体安全性远超任何单层。
**Source evidence**: Claude Code 内部的 Bash tool 实现。OMC 的安全配置中的多层检查。defense-in-depth 安全架构原则。
