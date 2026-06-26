#!/usr/bin/env bash
# Conventional Commits validation hook
# Install: cp scripts/commit-msg-hook.sh .git/hooks/commit-msg && chmod +x .git/hooks/commit-msg
MSG_FILE="$1"
MSG=$(cat "$MSG_FILE")
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# Try to find validate_commit_message.py relative to repo
VALIDATOR=""
for candidate in \
  "$SCRIPT_DIR/../../skills/commit-message-writing/scripts/validate_commit_message.py" \
  "$SCRIPT_DIR/../skills/commit-message-writing/scripts/validate_commit_message.py" \
  "skills/commit-message-writing/scripts/validate_commit_message.py"; do
  if [ -f "$candidate" ]; then
    VALIDATOR="$candidate"
    break
  fi
done
if [ -z "$VALIDATOR" ]; then
  echo "Warning: validate_commit_message.py not found, skipping validation"
  exit 0
fi
python3 "$VALIDATOR" --message "$MSG"
exit $?
