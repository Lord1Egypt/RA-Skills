#!/bin/bash
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE"

if [ ! -d .git ]; then
  echo "⚠️ Versioning not initialized"
  echo "Run \`/agent-changelog setup\` to get started."
  exit 1
fi

if [ $# -eq 0 ]; then
  CHANGED=$(git diff HEAD --name-only --no-color 2>/dev/null | tr '\n' ' ' | sed 's/ $//' || true)
  if [ -z "$CHANGED" ]; then
    echo "✓ No uncommitted changes"
    exit 0
  fi
  echo "✏️ **Uncommitted changes**"
  echo "\`$CHANGED\`"
  echo ""
  echo '```diff'
  git diff HEAD --no-color 2>/dev/null || git diff --no-color
  echo '```'
elif [ $# -eq 1 ]; then
  SUBJECT=$(git log --format="%s" -1 "$1" 2>/dev/null || true)
  DATE=$(git log --format="%ad" --date=format:"%b %d, %H:%M" -1 "$1" 2>/dev/null || true)
  echo "🔍 **\`$1\`** · $DATE"
  echo "_$SUBJECT_"
  echo ""
  echo '```diff'
  git show "$1" --stat --patch --no-color
  echo '```'
elif [ $# -eq 2 ]; then
  echo "🔍 **Diff** \`$1\` → \`$2\`"
  echo ""
  echo '```diff'
  git diff "$1" "$2" --no-color
  echo '```'
fi
