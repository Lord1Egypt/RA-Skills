#!/bin/bash
# ai-self-evolution Error Detector Hook
# Triggers on PostToolUse for Bash to detect command failures
# Reads CLAUDE_TOOL_OUTPUT and CLAUDE_EXIT_CODE environment variables

set -e

# Check exit code first (most reliable signal)
EXIT_CODE="${CLAUDE_EXIT_CODE:-0}"
OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

# If exit code is non-zero, it's definitely an error
if [ "$EXIT_CODE" != "0" ]; then
    cat << 'EOF'
<error-detected>
命令以非零退出码结束。若满足以下任一条件，建议记录到 .learnings/ERRORS.md：
- 错误是非预期或不明显的
- 需要排查才能定位或解决
- 在类似场景中可能再次出现
- 解决方案对后续会话有参考价值

使用格式：[ERR-YYYYMMDD-XXX]
记录前先搜索已有条目：grep -r "关键词" .learnings/
</error-detected>
EOF
    exit 0
fi

# Patterns indicating errors in output (even with exit code 0)
ERROR_PATTERNS=(
    "error:"
    "Error:"
    "ERROR:"
    "failed"
    "FAILED"
    "command not found"
    "No such file"
    "Permission denied"
    "fatal:"
    "Exception"
    "Traceback"
    "npm ERR!"
    "ModuleNotFoundError"
    "SyntaxError"
    "TypeError"
    "ReferenceError"
    "ImportError"
    "ConnectionRefused"
    "ECONNREFUSED"
    "ENOENT"
    "ETIMEDOUT"
    "panic:"
    "segfault"
    "core dumped"
    "killed"
    "OOM"
    "out of memory"
)

# Check if output contains any error pattern
contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

# Only output reminder if error detected
if [ "$contains_error" = true ]; then
    cat << 'EOF'
<error-detected>
检测到命令输出中包含错误信息。若满足以下任一条件，建议记录到 .learnings/ERRORS.md：
- 错误是非预期或不明显的
- 需要排查才能定位或解决
- 在类似场景中可能再次出现
- 解决方案对后续会话有参考价值

使用格式：[ERR-YYYYMMDD-XXX]
记录前先搜索已有条目：grep -r "关键词" .learnings/
</error-detected>
EOF
fi
