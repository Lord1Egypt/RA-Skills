#!/bin/bash
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE"

if [ ! -d .git ]; then
  echo "⚠️ Versioning not initialized"
  echo "Run \`/agent-changelog setup\` to get started."
  exit 1
fi

COUNT=10
for arg in "$@"; do
  case "$arg" in
    [0-9]*) COUNT="$arg" ;;
  esac
done

[ "${COUNT:-0}" -le 0 ] && COUNT=10

while IFS= read -r hash; do
  date=$(git log --format="%ad" --date=format:"%b %d, %H:%M" -1 "$hash")
  subject=$(git log --format="%s" -1 "$hash")
  body=$(git log --format="%b" -1 "$hash")
  triggered=$(echo "$body" | grep "^Triggered by:" | sed 's/Triggered by: //' || true)
  turns=$(echo "$body" | grep "^Turns:" | sed 's/Turns: //' || true)
  summary=$(echo "$body" | grep "^Summary:" | sed 's/Summary: //' || true)
  changelog=$(echo "$body" | awk '/^--- Change log ---/{found=1; next} found{print}' || true)

  echo "commit $hash"
  echo "date: $date"
  echo "subject: $subject"
  [ -n "$triggered" ] && echo "by: $triggered"
  [ -n "$turns" ]     && echo "turns: $turns"
  [ -n "$summary" ]   && echo "summary: $summary"
  [ -n "$changelog" ] && printf "changelog:\n%s\n" "$changelog"
  echo "---"
done < <(git log --format="%h" -n "$COUNT")
