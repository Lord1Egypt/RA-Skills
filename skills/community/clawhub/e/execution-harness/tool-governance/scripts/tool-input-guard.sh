#!/usr/bin/env bash
# tool-input-guard.sh — PreToolUse hook: validate bash inputs against safety rules
# Blocks dangerous patterns: rm -rf /, curl|sh, chmod 777 on system paths, etc.

set -euo pipefail

INPUT=$(head -c 20000)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null)

# Only check Bash commands
[ "$TOOL" != "Bash" ] && echo '{"continue":true}' && exit 0

COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null)
[ -z "$COMMAND" ] && echo '{"continue":true}' && exit 0

BLOCKED=""

# Check: rm -rf / or rm -rf ~
if echo "$COMMAND" | grep -qE 'rm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+)*(/|~)\s*$'; then
  BLOCKED="Blocked: rm -rf on root or home directory"
fi

# Check: rm on system directories
if echo "$COMMAND" | grep -qE 'rm\s+.*(/usr|/etc|/var|/System|/Library)\b'; then
  BLOCKED="Blocked: rm on system directory"
fi

# Check: chmod 777 on system paths
if echo "$COMMAND" | grep -qE 'chmod\s+777\s+(/|/usr|/etc|/var|/System)\b'; then
  BLOCKED="Blocked: chmod 777 on system path"
fi

# Check: curl|sh, wget|bash (pipe-to-shell)
if echo "$COMMAND" | grep -qE '(curl|wget)\s+.*\|\s*(sh|bash|zsh|dash)'; then
  BLOCKED="Blocked: pipe-to-shell pattern detected"
fi

# Check: write to system paths
if echo "$COMMAND" | grep -qE '(cp|mv|tee|dd|install)\s+.*(/usr/bin|/usr/local/bin|/etc|/System)'; then
  BLOCKED="Blocked: write to system path"
fi

if [ -n "$BLOCKED" ]; then
  jq -n --arg reason "$BLOCKED" \
    '{"hookSpecificOutput":{"permissionDecision":"deny","reason":$reason}}'
else
  echo '{"continue":true}'
fi
