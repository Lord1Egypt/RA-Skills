# Pattern 3.8: Auto-Compact Circuit Breaker

## Problem

Auto-compact 触发后可能因各种原因失败（API 413、LLM 生成的摘要不合法、网络超时）。如果失败后立即重试，可能陷入"compact 失败 → 重试 → 又失败"的循环，每次重试都消耗一次 API 调用。

Claude Code 内部数据：曾有 1,279 个 session 出现 50 次以上连续 compact 失败，浪费约 250K API 调用/天。

## Solution

Claude Code 内置了 circuit breaker：`MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3`。连续 3 次 auto-compact 失败后停止尝试，等待 Reactive Compact（由 API 413 错误触发）作为最终兜底。

这和 M3 Safety Valves 原则直接对应——压缩机制也需要逃生条件。

## 对 Hook 开发者的意义

如果你的 hook 依赖 compact 事件（比如 Pattern 3.7 Compaction Quality Audit 在 compact 后跑审计），需要知道：

1. Compact 不一定每次都成功。你的 hook 必须处理"compact 被 circuit breaker 跳过"的情况。
2. 触发阈值是 3 次。如果你看到 context 持续膨胀但没有 compact 发生，可能是 circuit breaker 生效了。
3. Reactive Compact 是最终兜底——但它只在 API 返回 413 时触发，可能比 auto-compact 晚很多。

## 递归保护

Auto-compact 还有递归保护：如果当前查询来自 `'session_memory'`、`'compact'` 或 `'marble_origami'` source，跳过 auto-compact 检查。防止 compact 的 LLM 调用本身触发新的 compact。

## Source

Claude Code 源码 `autoCompact.ts`（352 行），`MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES` 常量。
