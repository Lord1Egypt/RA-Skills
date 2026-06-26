#!/usr/bin/env bash
# oce-write — Safe atomic file writer.
# Reads new contents from stdin. Always backs up first, validates after,
# rolls back on validation failure.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

FILE=""; SKIP_VALIDATE="0"; TXN=""; FORCE_NEW=""

while [ $# -gt 0 ]; do
  case "$1" in
    --no-validate)  SKIP_VALIDATE="1"; shift ;;
    --txn)          TXN="$2"; shift 2 ;;
    --new)          FORCE_NEW="1"; shift ;;
    --json)         OCE_JSON_MODE="1"; shift ;;
    --dry-run)      OCE_DRY_RUN="1"; shift ;;
    -h|--help)
      cat <<'EOF'
oce write <file> < content
  Reads new contents from stdin. Atomic write (temp + rename).
  Auto-backs-up before writing. Validates after. Rolls back if invalid.

  --new           Require the file to NOT already exist
  --no-validate   Skip post-write validation (rare; use cautiously)
  --txn ID        Register backup with a transaction
  --dry-run       Print what would happen, change nothing
EOF
      exit 0 ;;
    -*) die "Unknown flag: $1" ;;
    *)  FILE="$1"; shift ;;
  esac
done

[ -n "$FILE" ] || die "Usage: oce write <file> < content"

CONTENT=$(cat)
[ -n "$CONTENT" ] || die "No content provided on stdin"

if [ "$FORCE_NEW" = "1" ] && [ -e "$FILE" ]; then
  die "File already exists (--new requires non-existent): $FILE"
fi

if [ "$OCE_DRY_RUN" = "1" ]; then
  bytes=$(printf '%s' "$CONTENT" | wc -c)
  lines=$(printf '%s\n' "$CONTENT" | wc -l)
  if [ "$OCE_JSON_MODE" = "1" ]; then
    emit_json status dry_run file "$FILE" bytes "raw:$bytes" lines "raw:$lines"
  else
    info "DRY RUN: would write $bytes bytes / $lines lines to $FILE"
  fi
  exit 0
fi

require_writable "$FILE"

BACKUP=""
if [ -f "$FILE" ]; then
  preflight_check "$FILE"
  BACKUP=$(create_backup "$FILE")
  log INFO "Backup created: $BACKUP"
fi

if [ -n "$TXN" ] && [ -d "$OCE_TXN_DIR/$TXN" ]; then
  printf '%s\t%s\n' "$FILE" "$BACKUP" >> "$OCE_TXN_DIR/$TXN/files.log"
fi

# Atomic write
TMPFILE="${FILE}.oce.tmp.$$"
printf '%s' "$CONTENT" > "$TMPFILE"
# Ensure trailing newline
if [ "$(tail -c1 "$TMPFILE" | wc -l)" -eq 0 ]; then
  printf '\n' >> "$TMPFILE"
fi
mv "$TMPFILE" "$FILE"

if [ "$SKIP_VALIDATE" = "0" ]; then
  if ! bash "$(dirname "$0")/oce-validate.sh" "$FILE" >/dev/null 2>&1; then
    if [ -n "$BACKUP" ]; then
      cp "$BACKUP" "$FILE"
      die "Write rolled back: file failed validation. Backup at $BACKUP"
    fi
    warn "Validation failed but no backup to roll back to"
  fi
fi

LINES=$(count_lines "$FILE")
if [ "$OCE_JSON_MODE" = "1" ]; then
  emit_json status success file "$FILE" lines "raw:$LINES" \
    backup "${BACKUP:-}" message "wrote $FILE ($LINES lines)"
else
  success "Wrote $FILE ($LINES lines)"
fi
