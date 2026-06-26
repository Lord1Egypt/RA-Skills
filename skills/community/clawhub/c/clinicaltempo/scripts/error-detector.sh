#!/bin/bash
# PostToolUse (Bash) — if tool output looks like an error, hint CLAWHUB.md logging.
# Reads CLAUDE_TOOL_OUTPUT when present (Claude Code).

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

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
    "Cannot POST /api"
    "Internal JSON-RPC"
    "402"
)

contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

if [ "$contains_error" = true ]; then
    cat << 'EOF'
<clinical-tempo-error-detected>
Output may indicate a failure. If this was non-obvious, add a **Failures** subsection to `CLAWHUB.md` (symptom / cause / fix). For stale Express routes, restart `npm run server` and check `GET http://localhost:8787/api/dance-extras/live`.
</clinical-tempo-error-detected>
EOF
fi
