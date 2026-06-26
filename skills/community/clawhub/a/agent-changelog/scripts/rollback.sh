#!/bin/bash
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE"

if [ ! -d .git ]; then
  echo "⚠️ Versioning not initialized"
  echo "Run \`/agent-changelog setup\` to get started."
  exit 1
fi

TARGET="${1:-}"
REASON="${2:-}"

if [ -z "$TARGET" ]; then
  echo "**Usage:** \`/agent-changelog rollback <commit> [reason]\`"
  echo ""
  echo "**Recent commits:**"
  while IFS= read -r hash; do
    date=$(git log --format="%ad" --date=format:"%b %d, %H:%M" -1 "$hash")
    subject=$(git log --format="%s" -1 "$hash")
    echo "• \`$hash\` $date — $subject"
  done < <(git log --format="%h" -10)
  exit 1
fi

if ! git cat-file -e "$TARGET" 2>/dev/null; then
  echo "⚠️ Commit \`$TARGET\` not found"
  exit 1
fi

CURRENT_SHORT=$(git rev-parse --short HEAD)
TARGET_SHORT=$(git rev-parse --short "$TARGET")
TARGET_MSG=$(git log --format="%s" -1 "$TARGET")

# Read identity from version context
CTX="$WORKSPACE/.version-context"
ACTOR="unknown"
ACTOR_ID="unknown"
CHANNEL="unknown"
if [ -f "$CTX" ] && command -v jq &>/dev/null; then
  ACTOR=$(jq -r '.user // "unknown"' "$CTX" 2>/dev/null || echo "unknown")
  ACTOR_ID=$(jq -r '.userId // "unknown"' "$CTX" 2>/dev/null || echo "unknown")
  CHANNEL=$(jq -r '.channel // "unknown"' "$CTX" 2>/dev/null || echo "unknown")
fi
[ "$ACTOR" = "unknown" ] && ACTOR="skill invocation"
[ "$ACTOR_ID" = "unknown" ] && ACTOR_ID="skill invocation"

# Restore only tracked files
while IFS= read -r f; do
  git checkout "$TARGET" -- "$f" 2>/dev/null || true
done < <(jq -r '.tracked[]?' "$WORKSPACE/.agent-changelog.json" 2>/dev/null)

# Stage the same tracked files
while IFS= read -r f; do
  git add "$f" 2>/dev/null || true
done < <(jq -r '.tracked[]?' "$WORKSPACE/.agent-changelog.json" 2>/dev/null)

if ! git diff --cached --quiet; then
  ENTRY=$(jq -n \
    --argjson ts "$(date +%s000)" \
    --arg user "$ACTOR" \
    --arg userId "$ACTOR_ID" \
    --arg channel "$CHANNEL" \
    --arg target "$TARGET_SHORT" \
    --arg reason "$REASON" \
    '{"ts":$ts,"user":$user,"userId":$userId,"channel":$channel,"action":"rollback","target":$target,"reason":$reason,"files":[]}')
  printf '%s\n' "$ENTRY" >> "$WORKSPACE/pending_commits.jsonl"

  echo "⏪ **Staged rollback**"
  echo "\`$CURRENT_SHORT\` → \`$TARGET_SHORT\`"
  echo "_$TARGET_MSG_"
  echo ""
  echo "_by ${ACTOR}_"
  echo "Commit with \`/agent-changelog commit\`"
else
  echo "✓ Already at \`$TARGET_SHORT\`"
  exit 0
fi
