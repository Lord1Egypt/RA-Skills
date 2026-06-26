#!/usr/bin/env bash
# oce-delete — Remove lines by range or pattern.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

FILE=""; LINES=""; MATCH=""; TXN=""; SKIP_VALIDATE="0"

while [ $# -gt 0 ]; do
  case "$1" in
    --lines)        LINES="$2"; shift 2 ;;
    --match)        MATCH="$2"; shift 2 ;;
    --txn)          TXN="$2"; shift 2 ;;
    --no-validate)  SKIP_VALIDATE="1"; shift ;;
    --json)         OCE_JSON_MODE="1"; shift ;;
    --dry-run)      OCE_DRY_RUN="1"; shift ;;
    -h|--help)
      cat <<'EOF'
oce delete <file> [--lines A:B | --match LITERAL]
  --lines A:B   Delete inclusive line range
  --match S     Delete every line containing literal string S
EOF
      exit 0 ;;
    -*) die "Unknown flag: $1" ;;
    *)  FILE="$1"; shift ;;
  esac
done

[ -n "$FILE" ] || die "Usage: oce delete <file> [--lines A:B | --match S]"
require_file "$FILE"
preflight_check "$FILE"
[ -n "$LINES" ] || [ -n "$MATCH" ] || die "Must specify --lines or --match"
[ -n "$LINES" ] && [ -n "$MATCH" ] && die "Specify only one of --lines or --match"

# Compute deletion count for dry-run / reporting
if [ -n "$LINES" ]; then
  S="${LINES%:*}"; E="${LINES#*:}"
  case "$S" in ''|*[!0-9]*) die "Invalid start: $S" ;; esac
  case "$E" in ''|*[!0-9]*) die "Invalid end: $E" ;; esac
  COUNT=$((E - S + 1))
else
  COUNT=$(grep -c -F -- "$MATCH" "$FILE" || true)
  [ -n "$COUNT" ] || COUNT=0
  [ "$COUNT" -gt 0 ] || die "Pattern not found: $MATCH"
fi

if [ "$OCE_DRY_RUN" = "1" ]; then
  if [ "$OCE_JSON_MODE" = "1" ]; then
    emit_json status dry_run file "$FILE" lines_to_delete "raw:$COUNT"
  else
    info "DRY RUN: would delete $COUNT line(s) from $FILE"
  fi
  exit 0
fi

BACKUP=$(create_backup "$FILE")
[ -n "$TXN" ] && [ -d "$OCE_TXN_DIR/$TXN" ] && \
  printf '%s\t%s\n' "$FILE" "$BACKUP" >> "$OCE_TXN_DIR/$TXN/files.log"

if [ -n "$LINES" ]; then
  # Use Node — sed -i is not portable across Linux/macOS
  node - "$FILE" "$S" "$E" <<'NODE'
const fs = require('fs');
const [,, file, s, e] = process.argv;
const lines = fs.readFileSync(file, 'utf8').split('\n');
lines.splice(parseInt(s, 10) - 1, parseInt(e, 10) - parseInt(s, 10) + 1);
fs.writeFileSync(file, lines.join('\n'));
NODE
else
  TMP="${FILE}.oce.tmp.$$"
  grep -v -F -- "$MATCH" "$FILE" > "$TMP" || true
  mv "$TMP" "$FILE"
fi

if [ "$SKIP_VALIDATE" = "0" ]; then
  if ! bash "$(dirname "$0")/oce-validate.sh" "$FILE" >/dev/null 2>&1; then
    cp "$BACKUP" "$FILE"
    die "Deletion caused validation failure — rolled back. Backup: $BACKUP"
  fi
fi

if [ "$OCE_JSON_MODE" = "1" ]; then
  emit_json status success file "$FILE" deleted_lines "raw:$COUNT" backup "$BACKUP"
else
  success "Deleted $COUNT line(s) from $FILE"
fi
