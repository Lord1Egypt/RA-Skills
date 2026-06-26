#!/usr/bin/env bash
set -euo pipefail

OLD_ID="${1:-}"
NEW_ID="${2:-}"
MODE="${3:-copy}"

if [[ -z "$OLD_ID" || -z "$NEW_ID" ]]; then
  echo "Usage: copy_session_content.sh <old-agent-id> <new-agent-id> [copy|summary]"
  exit 1
fi

OLD_DIR="$HOME/.openclaw/agents/$OLD_ID/sessions"
NEW_DIR="$HOME/.openclaw/agents/$NEW_ID/sessions"
mkdir -p "$NEW_DIR"

if [[ ! -d "$OLD_DIR" ]]; then
  echo "Old session dir not found: $OLD_DIR"
  exit 2
fi

mapfile -t FILES < <(find "$OLD_DIR" -maxdepth 1 -type f \( -name '*.jsonl' -o -name 'sessions.json' \) | sort)
if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No session files found in $OLD_DIR"
  exit 3
fi

case "$MODE" in
  copy)
    for f in "${FILES[@]}"; do
      base=$(basename "$f")
      cp "$f" "$NEW_DIR/migrated-from-$OLD_ID-$base"
      echo "COPIED $f -> $NEW_DIR/migrated-from-$OLD_ID-$base"
    done
    ;;
  summary)
    OUT="$NEW_DIR/migration-summary-from-$OLD_ID.txt"
    {
      echo "Migration summary from $OLD_ID to $NEW_ID"
      echo "Generated: $(date -Is)"
      echo
      printf 'Files:\n'
      printf '%s\n' "${FILES[@]}"
    } > "$OUT"
    echo "WROTE $OUT"
    ;;
  *)
    echo "Unknown mode: $MODE"
    exit 4
    ;;
esac
