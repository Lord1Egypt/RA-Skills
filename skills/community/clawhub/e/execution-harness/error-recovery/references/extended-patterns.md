# Error Recovery — Extended Patterns

### E5.1: Per-Error-Code Recovery Map
**What it does**: 为每种错误码定义专门的恢复策略：429（rate limit）→ 指数退避等待；529（server overloaded）→ 切换 fallback 模型；PTL（prompt too long）→ 触发 reactive compact；401/403（auth）→ 停止执行，通知用户；500（server error）→ 重试 2 次后放弃。每种错误的恢复路径独立，不共享重试计数。
**Why it matters**: 不同错误码的最优恢复策略完全不同——429 等一下就好了，但 529 等再久也没用（要换模型）；PTL 需要减少 context 而非重试。统一的"出错就重试"策略在 529 上浪费时间、在 PTL 上永远不会成功。Per-error-code mapping 让恢复策略精准匹配错误类型。
**Source evidence**: Claude Code 内部的 error handling 分支。OMC 的 error recovery map。API 文档的错误码语义。

### E5.2: Watermark-Based Error Scoping
**What it does**: 在 error recovery 前记录当前 context 的 "watermark"（消息数量或 token count），recovery 操作后如果 watermark 没有前进（没有新的有用输出），标记 recovery 失败。防止 recovery 本身消耗 context 但没有推进任务。
**Why it matters**: Recovery 操作（重试、compact、切换模型）消耗 token 和时间。如果 recovery 后 agent 又立即遇到同样的错误，说明 recovery 无效。Watermark 提供了一个客观指标判断"recovery 是否真正帮助 agent 继续前进"，避免在无效 recovery 上循环。
**Source evidence**: Claude Code 内部的 recovery 效果评估逻辑。OMC 的 stale state detection 思路在 error recovery 上的应用。

### E5.3: Recovery Anti-Loop Guards
**What it does**: 用 boolean flag（如 `hasAttemptedReactiveCompact`）标记已尝试过的 recovery 策略，防止同一 recovery 被重复触发。Flag 在 recovery 成功后重置，在 session 切换时清除。多个 flag 组合形成 recovery 状态机：compact 失败 → fallback 模型 → truncate head → 放弃。
**Why it matters**: 最危险的 failure mode 是 recovery-of-recovery 循环——compact 触发 error → error 触发 compact → 无限循环。Anti-loop guard 确保每种 recovery 最多尝试一次，失败后必须升级到下一种策略而非重复。
**Source evidence**: Claude Code 内部的 `hasAttemptedReactiveCompact` flag。OMC 的 recovery 状态跟踪。

### E5.4: max_output_tokens Continuation Recovery
**What it does**: 检测模型输出因 `max_output_tokens` 被截断的情况（`stop_reason: "max_tokens"`），自动注入 continuation prompt 让模型从断点继续生成。Continuation prompt 包含截断位置的最后 200 token 作为 anchor。
**Why it matters**: 长输出（大文件编辑、详细分析）经常被 max_output_tokens 截断。如果不处理，agent 的工具调用 JSON 可能不完整（截断在 tool_use block 中间），导致解析失败和整轮丢失。自动 continuation 让长输出透明地完成，agent 不需要知道输出被拆分了。
**Source evidence**: Claude API 的 stop_reason 字段。Claude Code 的 output token 限制处理逻辑。

### E5.5: Recovery-of-Recovery (truncateHead Fallback)
**What it does**: 当所有常规 recovery 策略（retry、compact、model fallback）都失败后，最后手段是 truncate conversation head——丢弃最早的 N 条消息，只保留系统指令 + 最近的交互。这是不可逆操作，丢失早期 context，但保证 agent 能继续运行。
**Why it matters**: 有些场景下 compact 无法解决问题（比如 compact 本身因 context 过大而超时），这时需要一个 guaranteed-to-work 的兜底方案。TruncateHead 通过直接删除消息来强制释放空间，不依赖 LLM 做摘要。代价是丢失早期上下文，但比完全停止好——配合 `.working-state/` 的 filesystem memory 可以部分恢复丢失的关键决策。
**Source evidence**: Claude Code 内部的 emergency context recovery 逻辑。OMC 的 recovery 升级链：compact → reactive compact → truncate head。
