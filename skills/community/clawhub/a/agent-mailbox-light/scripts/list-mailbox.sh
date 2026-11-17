#!/usr/bin/env bash
set -euo pipefail

workspace="${1:-$(pwd)}"
limit="${2:-5}"
view="${3:-inbox}"
inbox="$workspace/.agent-mailbox/inbox"
keep="$workspace/.agent-mailbox/keep"
mkdir -p "$inbox" "$keep"

list_dir() {
  find "$1" -maxdepth 1 -type f -name '*.md' | sort -r | head -n "$limit"
}

case "$view" in
  inbox)
    list_dir "$inbox"
    ;;
  keep)
    list_dir "$keep"
    ;;
  startup)
    printf '%s\n' '=== KEEP (retained, possibly stale) ==='
    list_dir "$keep"
    printf '%s\n' '=== INBOX (new mail) ==='
    list_dir "$inbox"
    ;;
  *)
    echo "Usage: $0 [workspace] [limit] [inbox|keep|startup]" >&2
    exit 1
    ;;
esac
