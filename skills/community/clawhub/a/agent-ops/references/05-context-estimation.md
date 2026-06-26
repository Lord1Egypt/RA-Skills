# Pattern 5: 轻量 Context 使用量估算

## 问题

需要知道 agent 的 context window 用了多少，但 transcript JSONL 文件可能 100MB+，不能全部读取。

## 原理

Claude Code 的 transcript 是 append-only JSONL。最新的 API 响应在文件末尾，包含 `usage.input_tokens` 字段。读取最后一行即可提取当前 input token 数。

> **重要限制**：Claude Code 的 transcript JSONL **不包含** `context_window_size` 字段。该数据仅通过 statusLine stdin pipe 提供给 HUD 插件。因此，hook 脚本**无法计算 context 使用百分比**，只能获取原始 input token 数。

来自 Claude Code 内部的 HUD 实现（通过 stdin pipe 读取 `context_window.context_window_size` 和 `context_window.current_usage.input_tokens`）和 OMC 的 `context-guard-stop.mjs`。

## 实现（`scripts/context-usage.sh`）

```bash
TRANSCRIPT="$1"
[ -f "$TRANSCRIPT" ] || exit 0

# 读取最后一行（不是 tail -c 4096，因为真实 JSONL 行可达 20KB+）
LAST_LINE=$(tail -1 "$TRANSCRIPT" 2>/dev/null)
[ -z "$LAST_LINE" ] && exit 0

# 从嵌套的 usage 对象中提取 input_tokens
# 真实格式："usage":{"input_tokens":N,"cache_creation_input_tokens":0,...}
INPUT_TOKENS=$(echo "$LAST_LINE" | jq -r '.usage.input_tokens // empty' 2>/dev/null)

# 过滤流式占位符（input_tokens <= 10 是流式中间值）
if [ -n "$INPUT_TOKENS" ] && [ "$INPUT_TOKENS" -gt 10 ]; then
  echo "Input tokens: ${INPUT_TOKENS}"
fi
```

## 用途

1. **Token 预算管理**：通过原始 token 数做粗略阈值判断（如 >160K 告警，基于 200K context window 假设）
2. **Hook pair bracket 中的增量追踪**：每轮记录 token 增量（见 Pattern 11）
3. **外部监控**：周期性检查所有运行中 session 的 token 消耗

## 为什么不能算百分比

| 数据 | 来源 | Hook 脚本可访问 |
|------|------|----------------|
| `input_tokens` | transcript JSONL 的 `usage` 对象 | 是 |
| `context_window_size` | statusLine stdin pipe | 否 |
| `used_percentage` | statusLine stdin pipe | 否 |

HUD 插件（如 claude-hud）可以算百分比，因为它通过 stdin pipe 获取完整数据。Hook 脚本只能拿到 transcript。

## Claude Code 的 token 估算精度（来自源码分析 v2.1.88）

Claude Code 内部使用 3 级精度估算：

- **粗估**：bytes / 4（零成本，毫秒级）
- **代理**：Haiku input count（便宜但需要 API 调用）
- **精确**：countTokens API（慢但准确）

粗估还加 33% 保守缓冲：`Math.ceil(totalTokens * (4/3))`。transcript 尾部读取得到的是 API 返回的实际值，精度等同于精确级。
