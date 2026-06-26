#!/bin/bash
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE"

if [ ! -d .git ]; then
  echo "⚠️ Versioning not initialized"
  echo "Run \`/agent-changelog setup\` to get started."
  exit 1
fi

FILE="${1:-}"
COMMIT="${2:-}"
REASON="${3:-}"

if [ -z "$FILE" ] || [ -z "$COMMIT" ]; then
  echo "**Usage:** \`/agent-changelog restore <file> <commit> [reason]\`"
  echo ""
  echo "Restores a single file to its state before the given commit."
  echo "Run \`/agent-changelog log\` to find the right commit."
  exit 1
fi

if ! git cat-file -e "$COMMIT" 2>/dev/null; then
  echo "⚠️ Commit \`$COMMIT\` not found"
  exit 1
fi

if ! git diff-tree --no-commit-id -r --name-only "$COMMIT" | grep -qF "$FILE"; then
  echo "⚠️ \`$FILE\` was not changed in \`$COMMIT\`"
  exit 1
fi

TARGET_SHORT=$(git rev-parse --short "$COMMIT")

# Read sender identity from capture hook context
USER="unknown"
USER_ID="unknown"
CHANNEL="unknown"
CTX="$WORKSPACE/.version-context"
if [ -f "$CTX" ] && command -v jq &>/dev/null; then
  USER=$(jq -r '.user // "unknown"' "$CTX" 2>/dev/null || echo "unknown")
  USER_ID=$(jq -r '.userId // "unknown"' "$CTX" 2>/dev/null || echo "unknown")
  CHANNEL=$(jq -r '.channel // "unknown"' "$CTX" 2>/dev/null || echo "unknown")
fi

# Restore file to its state before the target commit and stage it
git checkout "${COMMIT}^" -- "$FILE"
git add "$FILE"

# Log to pending so the next commit includes restore attribution
ENTRY=$(jq -n \
  --argjson ts "$(date +%s000)" \
  --arg user "$USER" \
  --arg userId "$USER_ID" \
  --arg channel "$CHANNEL" \
  --arg file "$FILE" \
  --arg from "$TARGET_SHORT" \
  --arg reason "$REASON" \
  '{"ts":$ts,"user":$user,"userId":$userId,"channel":$channel,"action":"restore","file":$file,"from":$from,"reason":$reason,"files":[]}')
printf '%s\n' "$ENTRY" >> "$WORKSPACE/pending_commits.jsonl"

echo "📌 **Staged restore**"
echo "\`$FILE\` → before \`$TARGET_SHORT\`"
echo "_by ${USER}_"
echo ""
echo "Commit with \`/agent-changelog commit\`"
