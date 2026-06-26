#!/usr/bin/env bash
# oce-diff — Show what changed since the last backup.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

FILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --json) OCE_JSON_MODE="1"; shift ;;
    -h|--help)
      cat <<'EOF'
oce diff <file>
  Show unified diff against the most recent backup of <file>.
  Backups are created automatically by oce-replace, oce-insert, oce-delete,
  oce-write, oce-patch.
EOF
      exit 0 ;;
    *) FILE="$1"; shift ;;
  esac
done

[ -n "$FILE" ] || die "Usage: oce diff <file>"
require_file "$FILE"

LATEST=$(list_backups "$FILE" | head -1)
[ -n "$LATEST" ] || { warn "No backup to compare against for $FILE"; exit 0; }

if [ "$OCE_JSON_MODE" = "1" ]; then
  DIFF=$(diff -u "$LATEST" "$FILE" 2>/dev/null || true)
  emit_json status success file "$FILE" backup "$LATEST" diff "$DIFF"
else
  diff -u "$LATEST" "$FILE" | awk '
    /^---/ { print "\033[1m" $0 "\033[0m"; next }
    /^\+\+\+/ { print "\033[1m" $0 "\033[0m"; next }
    /^@@/  { print "\033[36m" $0 "\033[0m"; next }
    /^-/   { print "\033[31m" $0 "\033[0m"; next }
    /^\+/  { print "\033[32m" $0 "\033[0m"; next }
    { print }
  '
fi
