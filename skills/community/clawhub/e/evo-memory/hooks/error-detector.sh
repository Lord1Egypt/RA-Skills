#!/bin/bash
# Self-Evolution Error Detector
# Hook: PostToolUse (matcher: Bash)
# 检测命令失败，自动写入 pending

PENDING_FILE="$HOME/.openclaw/workspace/self-evolution/pending.jsonl"
TS=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")
OUTPUT="$CLAUDE_TOOL_OUTPUT"

# 检测错误模式
if echo "$OUTPUT" | grep -qiE "error:|failed|command not found|No such file|Permission denied|fatal:|Exception|Traceback|npm ERR!|ModuleNotFoundError|SyntaxError|TypeError|exit code|non-zero|ENOENT|EACCES"; then
  # 提取第一行错误信息作为摘要
  ERROR_LINE=$(echo "$OUTPUT" | grep -iE "error:|failed|denied|fatal:|Exception|Traceback" | head -1 | cut -c1-80)
  echo "{\"ts\":\"$TS\",\"signal\":\"tool_failure\",\"brief\":\"命令失败: $ERROR_LINE\",\"source\":\"hook\"}" >> "$PENDING_FILE"
  echo "<self-evolution-signal>检测到命令失败，已记录到 pending。</self-evolution-signal>"
fi
