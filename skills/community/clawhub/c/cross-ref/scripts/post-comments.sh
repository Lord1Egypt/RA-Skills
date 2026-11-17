#!/usr/bin/env bash
# Post an explicitly approved queue of cross-reference comments.
# Usage: post-comments.sh <owner/repo> <workspace_dir> [--execute] [daily_max]

set -euo pipefail

REPO="${1:?Usage: post-comments.sh <owner/repo> <workspace_dir> [--execute] [daily_max]}"
WORKSPACE="${2:?Usage: post-comments.sh <owner/repo> <workspace_dir> [--execute] [daily_max]}"
MODE="${3:-dry-run}"
DAILY_MAX="${4:-20}"

if ! [[ "$REPO" =~ ^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$ ]]; then
  echo "Error: invalid repo format; expected owner/repo" >&2
  exit 1
fi
if ! [[ "$DAILY_MAX" =~ ^[1-9][0-9]*$ ]]; then
  echo "Error: daily_max must be a positive integer" >&2
  exit 1
fi

COMMENTS_FILE="$WORKSPACE/approved-comments.json"
PROGRESS_FILE="$WORKSPACE/comment-progress.json"
BODY_FILE="$WORKSPACE/.approved-comment-body.txt"

if [ ! -f "$COMMENTS_FILE" ]; then
  echo "Error: $COMMENTS_FILE not found" >&2
  exit 1
fi
if ! jq -e 'type == "object" and .approved == true and (.approved_at | type == "string") and (.comments | type == "array")' "$COMMENTS_FILE" >/dev/null; then
  echo "Error: approval file must be an object with approved=true, approved_at, and comments[]" >&2
  exit 1
fi

TOTAL=$(jq '.comments | length' "$COMMENTS_FILE")
echo "=== Cross-Ref Approved Comment Queue ==="
echo "Repo: $REPO"
echo "Approved comments: $TOTAL"

if [ "$MODE" != "--execute" ]; then
  echo "Mode: dry-run (no GitHub writes)"
  jq -r '.comments[] | "- #\(.target_number) [\(.type)]"' "$COMMENTS_FILE"
  exit 0
fi

START_INDEX=0
DAY_COUNT=0
TODAY=$(date -u +%Y-%m-%d)

if [ -f "$PROGRESS_FILE" ]; then
  START_INDEX=$(jq '.completed // 0' "$PROGRESS_FILE")
  if [ "$(jq -r '.day_start_utc // ""' "$PROGRESS_FILE")" = "$TODAY" ]; then
    DAY_COUNT=$(jq '.day_count // 0' "$PROGRESS_FILE")
  fi
fi

save_progress() {
  local completed="$1"
  local tmp="${PROGRESS_FILE}.tmp"
  jq -n \
    --argjson total "$TOTAL" \
    --argjson completed "$completed" \
    --argjson remaining "$((TOTAL - completed))" \
    --argjson day_count "$DAY_COUNT" \
    --arg day_start_utc "$TODAY" \
    --arg last_commented_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '{total_planned:$total,completed:$completed,remaining:$remaining,day_count:$day_count,day_start_utc:$day_start_utc,last_commented_at:$last_commented_at}' \
    > "$tmp"
  mv "$tmp" "$PROGRESS_FILE"
}

cleanup() {
  rm -f "$BODY_FILE"
}
trap cleanup EXIT

for ((i=START_INDEX; i<TOTAL; i++)); do
  if [ "$DAY_COUNT" -ge "$DAILY_MAX" ]; then
    echo "Daily maximum reached ($DAILY_MAX); review progress before resuming."
    exit 0
  fi

  TARGET=$(jq -r ".comments[$i].target_number" "$COMMENTS_FILE")
  TYPE=$(jq -r ".comments[$i].type" "$COMMENTS_FILE")
  BODY=$(jq -r ".comments[$i].body" "$COMMENTS_FILE")

  if ! [[ "$TARGET" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: comments[$i].target_number must be a positive integer" >&2
    exit 1
  fi
  if [ -z "$BODY" ] || [ "$BODY" = "null" ] || [ "${#BODY}" -gt 65536 ]; then
    echo "Error: comments[$i].body is empty or exceeds GitHub's limit" >&2
    exit 1
  fi

  printf '%s\n' "$BODY" > "$BODY_FILE"
  echo "[$((i + 1))/$TOTAL] Posting approved $TYPE comment on #$TARGET"
  if ! gh issue comment "$TARGET" --repo "$REPO" --body-file "$BODY_FILE"; then
    echo "GitHub rejected the request; stopping without retry." >&2
    exit 1
  fi

  DAY_COUNT=$((DAY_COUNT + 1))
  save_progress "$((i + 1))"

  if [ "$((i + 1))" -lt "$TOTAL" ]; then
    sleep 1
  fi
done

echo "Done: $TOTAL approved comments processed."
