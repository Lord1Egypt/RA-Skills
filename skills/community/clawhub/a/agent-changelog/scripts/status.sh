#!/bin/bash
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE"

if [ ! -d .git ]; then
  echo "⚠️ Versioning not initialized"
  echo "Run \`/agent-changelog setup\` to get started."
  exit 0
fi

HASH=$(git log --format="%h" -1 2>/dev/null || true)

if [ -z "$HASH" ]; then
  echo "📸 No commits yet"
else
  DATE=$(git log --format="%ad" --date=format:"%b %d, %H:%M" -1)
  SUBJECT=$(git log --format="%s" -1)
  BODY=$(git log --format="%b" -1)

  # Parse commit type from subject prefix
  if echo "$SUBJECT" | grep -qi "^auto-commit"; then
    TYPE="Auto"
    FILES=$(echo "$SUBJECT" | sed 's/^[Aa]uto-commit[^:]*: //')
  elif echo "$SUBJECT" | grep -qi "^manual commit"; then
    TYPE="Manual"
    FILES=$(echo "$SUBJECT" | sed 's/^[Mm]anual commit[^:]*: //')
  elif echo "$SUBJECT" | grep -qi "^rollback"; then
    TYPE="Rollback"
    FILES=""
  else
    TYPE=""
    FILES="$SUBJECT"
  fi

  # Parse identity from commit body
  IDENTITY=$(echo "$BODY" | grep "^Triggered by:" | sed 's/Triggered by: //' | tr -d '\n' | sed 's/cli/CLI/g' || true)

  # Build output line
  echo "📸 \`$HASH\` · $DATE"

  META_PARTS=()
  [ -n "$TYPE" ] && META_PARTS+=("$TYPE")
  [ -n "$IDENTITY" ] && META_PARTS+=("by $IDENTITY")
  [ -n "$FILES" ] && META_PARTS+=("$FILES")
  if [ ${#META_PARTS[@]} -gt 0 ]; then
    (IFS=' · '; echo "_${META_PARTS[*]}_")
  fi
fi

echo ""

MODIFIED=$(git diff HEAD --name-only 2>/dev/null)
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null)
ALL_CHANGES=$(printf '%s\n%s\n' "$MODIFIED" "$UNTRACKED" | grep -v '^$' || true)
CHANGES=$(printf '%s\n' "$ALL_CHANGES" | grep -c . || true)

if [ "$CHANGES" -gt 0 ]; then
  LABEL=$([ "$CHANGES" -eq 1 ] && echo "file" || echo "files")
  echo "✏️ **$CHANGES uncommitted $LABEL:**"
  while IFS= read -r file; do
    [ -z "$file" ] && continue
    if echo "$MODIFIED" | grep -qF "$file"; then
      added=$(git diff HEAD -- "$file" 2>/dev/null | grep -c '^+[^+]' || true)
      removed=$(git diff HEAD -- "$file" 2>/dev/null | grep -c '^-[^-]' || true)
      echo "• \`$file\` +$added/-$removed"
    else
      echo "• \`$file\` new"
    fi
  done <<< "$ALL_CHANGES"
else
  echo "✓ No uncommitted changes"
fi
