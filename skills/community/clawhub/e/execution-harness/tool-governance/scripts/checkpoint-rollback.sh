#!/usr/bin/env bash
# checkpoint-rollback.sh — PreToolUse hook: git stash before destructive bash commands
# Creates automatic backup checkpoint before potentially destructive operations.

set -euo pipefail

INPUT=$(head -c 20000)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null)

# Only intercept Bash
[ "$TOOL" != "Bash" ] && echo '{"continue":true}' && exit 0

COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null)
[ -z "$COMMAND" ] && echo '{"continue":true}' && exit 0

# Check for destructive patterns
DESTRUCTIVE=false
if echo "$COMMAND" | grep -qiE '(rm\s+-rf|git\s+reset\s+--hard|git\s+checkout\s+--|git\s+clean\s+-f|drop\s+table|truncate\s+table|git\s+push\s+--force|git\s+push\s+-f)'; then
  DESTRUCTIVE=true
fi

if [ "$DESTRUCTIVE" = "true" ]; then
  # Only stash if we're in a git repo with changes
  if git rev-parse --is-inside-work-tree &>/dev/null; then
    if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
      STASH_MSG="harness-checkpoint-$(date +%s)"
      git stash push -m "$STASH_MSG" --include-untracked &>/dev/null || true
      jq -n --arg ctx "Auto-checkpoint created: '${STASH_MSG}'. Use 'git stash pop' to restore if needed." \
        '{"hookSpecificOutput":{"additionalContext":$ctx}}'
      exit 0
    fi
  fi
fi

echo '{"continue":true}'
