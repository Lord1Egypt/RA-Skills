#!/usr/bin/env bash
set -euo pipefail

EXIT_CODE="${CLAUDE_TOOL_EXIT_CODE:-${TOOL_EXIT_CODE:-}}"
OUTPUT="${CLAUDE_TOOL_OUTPUT:-${TOOL_OUTPUT:-}}"

contains_error=false

if [[ -n "$EXIT_CODE" && "$EXIT_CODE" != "0" ]]; then
  contains_error=true
fi

if [[ "$contains_error" == false ]]; then
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
    "non-zero"
  )

  for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
      contains_error=true
      break
    fi
  done
fi

if [[ "$contains_error" == true ]]; then
  cat <<'MSG'
<error-detected>
A likely command failure was detected.
Consider logging it only if the failure required real diagnosis, is likely to recur, or changed future workflow.
Use the workspace `.learnings/ERRORS.md`, not the skill directory.
</error-detected>
MSG
fi
