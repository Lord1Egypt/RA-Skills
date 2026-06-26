#!/usr/bin/env bash
set -euo pipefail

MAILBOX_GLOB="${MAILBOX_GLOB:-$HOME/.openclaw/workspace*}"
SENDER="${SENDER:-main}"
PRIORITY="${PRIORITY:-info}"
SLUG="${SLUG:-mail}"
TITLE="${TITLE:-$SLUG}"
TAGS="${TAGS:-}"
SELF_WORKSPACE="${SELF_WORKSPACE:-}"

case "$PRIORITY" in
  info|warn|critical) ;;
  *) echo "Invalid PRIORITY: $PRIORITY" >&2; exit 1 ;;
esac

stamp="$(date +%Y%m%d%H%M%S)"
created_iso="$(date -Iseconds)"
slug="$(printf '%s' "$SLUG" | tr ' ' '-' | tr -cd 'a-zA-Z0-9._-' | sed 's/^-*//;s/-*$//')"
[[ -n "$slug" ]] || slug="mail"
filename="${stamp}--${SENDER}--${PRIORITY}--${slug}.md"
body_tmp="$(mktemp)"
cat > "$body_tmp"

delivered=0
shopt -s nullglob
for workspace in $MAILBOX_GLOB; do
  [[ -d "$workspace" ]] || continue
  [[ -n "$SELF_WORKSPACE" && "$workspace" == "$SELF_WORKSPACE" ]] && continue
  inbox="$workspace/.agent-mailbox/inbox"
  [[ -d "$inbox" ]] || continue
  file="$inbox/$filename"
  {
    printf 'Title: %s\n' "$TITLE"
    printf 'From: %s\n' "$SENDER"
    printf 'Created-At: %s\n' "$created_iso"
    printf 'Priority: %s\n' "$PRIORITY"
    printf 'Tags: %s\n' "$TAGS"
    printf '\n'
    cat "$body_tmp"
  } > "$file" || true
  if [[ -f "$file" ]]; then
    printf '%s\n' "$file"
    delivered=$((delivered + 1))
  fi
done

rm -f "$body_tmp"
printf 'Delivered: %s\n' "$delivered" >&2
