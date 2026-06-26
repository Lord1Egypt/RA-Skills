#!/bin/sh
set -eu

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

case "$OUTPUT" in
  *"error:"*|*"Error:"*|*"ERROR:"*|*"failed"*|*"fatal:"*|*"Traceback"*|*"Exception"*|*"Permission denied"*|*"command not found"*|*"No such file"*|*"non-zero"*)
    cat <<'EOF'
<echo-fade-memory-error-reminder>
A command error was detected.
If this failure revealed a reusable workaround, store it as durable memory:
- summarize the fix clearly
- use high importance
- mark it as project memory or goal memory
</echo-fade-memory-error-reminder>
EOF
    ;;
esac
