# Context Memory — Extended Patterns

### E3.1: 4-Tier Compression Pipeline
**What it does**: Context 压缩分 4 个层级，按粒度从小到大依次触发：(1) micro-compact（工具输出截断，单条消息级别）；(2) session-compact（会话内压缩，合并相邻消息）；(3) full-compact（完整摘要，保留关键决策和结论）；(4) reactive-compact（紧急压缩，context 到 95% 时触发，激进丢弃）。每层有独立的触发阈值和保留策略。
**Why it matters**: 一刀切的 compact 要么太激进（丢了关键信息）要么太保守（压缩效果不够）。分层压缩让小问题（单个大输出）在低层解决，不触发全局压缩。只有累积性的 context 增长才逐级向上触发更激进的压缩。
**Source evidence**: Claude Code 内部的 auto-compact 逻辑中有 micro（工具输出截断到 N chars）和 full（整体 summary）两层。reactive compact 在 95% 阈值触发。

### E3.2: Auto-Compact Circuit Breaker
**What it does**: 跟踪连续 compact 失败次数（`MAX_CONSECUTIVE_FAILURES=3`）。如果 compact 后 context 没有有效减少（压缩率 < 10%），计为失败。连续 3 次失败后停止自动 compact，转为通知用户手动处理。
**Why it matters**: 当 context 中的内容全是"不可压缩"的（密集代码、长日志），反复 compact 只消耗 API 调用但不释放空间，还可能丢失关键信息。Circuit breaker 防止无效 compact 循环——在明知无效时尽早停止，保留剩余 budget 做有用的工作。
**Source evidence**: Claude Code 内部的 compact 重试逻辑。OMC 的 `hasAttemptedReactiveCompact` flag 防止重复触发。

### E3.3: Post-Compact File Restoration
**What it does**: Compact 完成后，自动重新读取 agent 最近频繁访问的 top 5 文件，将内容重新注入 context。总恢复预算限制在 50K token 以内。文件按"最近 10 轮内的访问频次"排序。
**Why it matters**: Compact 摘要无法保留代码文件的精确内容——行号、变量名、函数签名在摘要中丢失。但 agent 下一步工作大概率还在操作这些文件。Pre-emptive restoration 让 agent 在 compact 后不用手动重新 Read 文件，减少一轮不产出的"恢复轮次"。
**Source evidence**: OMC 的 post-compact restoration 逻辑。Claude Code 的 compact 后文件重加载行为。

### E3.4: Layered Instruction Loading
**What it does**: 按优先级从高到低加载 4 层指令：(1) managed instructions（Claude Code 内置的系统指令）；(2) user instructions（`~/.claude/CLAUDE.md`）；(3) project instructions（项目根的 `CLAUDE.md`）；(4) local instructions（子目录的 `CLAUDE.md`）。后加载的指令可以 override 前面的，但不能撤销 managed instructions。
**Why it matters**: 不同粒度的指令解决不同问题——系统安全规则不应该被项目配置覆盖，但项目编码规范应该能覆盖全局偏好。分层加载 + 优先级确保"越局部越优先"的同时保护系统级约束。
**Source evidence**: Claude Code 的 CLAUDE.md 加载链。`--add-dir` 多目录支持。managed instructions 的不可覆盖性。

### E3.5: @include with Extension Whitelist
**What it does**: CLAUDE.md 中的 `@path/to/file` 语法允许包含外部文件的内容，但只允许特定扩展名（`.md`, `.txt`, `.yaml`, `.json` 等）。可执行文件、二进制文件被拒绝包含。
**Why it matters**: `@include` 是强大的模块化工具——把长指令拆到多个文件里。但如果不限制文件类型，`@/path/to/binary` 会把二进制垃圾注入 context，浪费 token 甚至导致解析错误。Extension whitelist 是最小权限原则在 include 机制上的体现。
**Source evidence**: Claude Code 的 `@` 文件引用语法实现。CLAUDE.md include 的安全限制。

### E3.6: Dynamic Prompt Cache Boundary
**What it does**: 将 prompt 中不变的部分（系统指令、CLAUDE.md、工具定义）放在前面形成 prompt cache boundary，变化的部分（对话消息、工具结果）放在后面。Anthropic API 的 prompt caching 对前缀相同的请求复用 KV cache，大幅降低 TTFT（首 token 延迟）和成本。
**Why it matters**: Agent 的每轮 API 调用有大量重复前缀（系统指令 + 工具定义可达 20-40K token）。没有 prompt cache 时每轮都要重新处理这些前缀，浪费计算和时间。动态调整 cache boundary（在指令变化时移动 boundary）让 cache hit rate 最大化。
**Source evidence**: Anthropic prompt caching 文档。Claude Code 的请求构造逻辑中的 cache_control breakpoint 放置策略。
