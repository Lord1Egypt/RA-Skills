# MCP Reconnection

## Problem

MCP server 在长会话中可能断开连接——进程 crash、网络抖动、资源被回收。断开后 agent 调用 MCP 工具会失败，但 agent 不知道是工具本身有问题还是连接断了，可能反复重试同一个调用。

## Solution

检测 MCP 工具调用的特征性失败模式（连接错误而非业务错误），用指数退避重试连接。超过重试上限后切换到 fallback 工具（见 graceful-degradation pattern）。

## Implementation

1. PostToolUse hook 检测 MCP 断开的特征性错误

```bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
OUTPUT=$(echo "$INPUT" | jq -r '.tool_output // ""')

# 检测 MCP 连接错误模式
if echo "$OUTPUT" | grep -qiE 'ECONNREFUSED|ECONNRESET|EPIPE|MCP.*disconnect|transport.*closed|server.*not.*running'; then
  SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')
  RETRY_FILE="sessions/${SESSION_ID}/mcp-retry-${TOOL}.json"
  
  # 读取或初始化重试状态
  if [ -f "$RETRY_FILE" ]; then
    ATTEMPT=$(jq -r '.attempt' "$RETRY_FILE")
    LAST=$(jq -r '.last_attempt_ts' "$RETRY_FILE")
  else
    ATTEMPT=0
  fi
  
  ATTEMPT=$((ATTEMPT + 1))
  MAX_RETRIES=5
  
  if [ "$ATTEMPT" -gt "$MAX_RETRIES" ]; then
    echo "{\"hookSpecificOutput\":{\"additionalContext\":\"[MCP] ${TOOL} 连接失败已达 ${MAX_RETRIES} 次上限。请使用替代工具完成任务（见 .working-state/fallback-tools.md），或手动重启 MCP server。\"}}"
    exit 0
  fi
  
  # 指数退避：1s, 2s, 4s, 8s, 16s
  BACKOFF=$(( 1 << (ATTEMPT - 1) ))
  
  jq -n --argjson att "$ATTEMPT" --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '{attempt: $att, last_attempt_ts: $ts}' > "$RETRY_FILE"
  
  echo "{\"hookSpecificOutput\":{\"additionalContext\":\"[MCP] ${TOOL} 连接断开，第 ${ATTEMPT}/${MAX_RETRIES} 次重试。等待 ${BACKOFF}s 后重试，或使用替代工具。\"}}"
fi
```

2. 可选：在 UserPromptSubmit hook 中尝试重连（通过 MCP restart 命令）

```bash
# 如果检测到 MCP 工具全部失败，尝试重启 MCP server
# 注意：Claude Code 不暴露 MCP restart API，只能通过重启 Claude Code 进程实现
```

## Tradeoffs

- **Pro**: 自动处理临时性连接断开，无需人工干预
- **Pro**: 指数退避避免在 MCP server crash 时疯狂重试
- **Con**: Claude Code 不提供直接的 MCP 重连 API，hook 只能提醒和记录
- **Con**: 需要区分"连接错误"和"业务错误"——误判会触发不必要的重连

## Source

标准的指数退避重连模式。Claude Code MCP server 生命周期管理。OMC 的 error-code recovery map（ECONNREFUSED → backoff retry）。
