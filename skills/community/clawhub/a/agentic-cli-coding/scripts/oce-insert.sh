#!/usr/bin/env bash
# oce-insert — Insert content at a line, before or after a pattern match.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

FILE=""; LINE=""; BEFORE=""; AFTER=""
CONTENT=""; CONTENT_FILE=""; TXN=""; SKIP_VALIDATE="0"

while [ $# -gt 0 ]; do
  case "$1" in
    --line)         LINE="$2"; shift 2 ;;
    --before-match) BEFORE="$2"; shift 2 ;;
    --after-match)  AFTER="$2"; shift 2 ;;
    --content)      CONTENT="$2"; shift 2 ;;
    --content-file) CONTENT_FILE="$2"; shift 2 ;;
    --txn)          TXN="$2"; shift 2 ;;
    --no-validate)  SKIP_VALIDATE="1"; shift ;;
    --json)         OCE_JSON_MODE="1"; shift ;;
    --dry-run)      OCE_DRY_RUN="1"; shift ;;
    -h|--help)
      cat <<'EOF'
oce insert <file> [--line N | --before-match P | --after-match P] (--content S | --content-file F | < stdin)
  Inserts the given content at the chosen anchor.
  Anchor exactly one:
    --line N           Insert before line N (1-indexed)
    --before-match P   Insert before the first line containing literal P
    --after-match P    Insert after the first line containing literal P
EOF
      exit 0 ;;
    -*) die "Unknown flag: $1" ;;
    *)  FILE="$1"; shift ;;
  esac
done

[ -n "$FILE" ] || die "Usage: oce insert <file> [--line N | --before-match P | --after-match P]"
require_file "$FILE"
preflight_check "$FILE"

# Resolve content
if [ -n "$CONTENT_FILE" ]; then
  CONTENT=$(cat "$CONTENT_FILE")
elif [ -z "$CONTENT" ] && [ ! -t 0 ]; then
  CONTENT=$(cat)
fi
[ -n "$CONTENT" ] || die "No content provided (use --content, --content-file, or pipe to stdin)"

# Resolve target line
ANCHOR_COUNT=0
[ -n "$LINE" ]   && ANCHOR_COUNT=$((ANCHOR_COUNT + 1))
[ -n "$BEFORE" ] && ANCHOR_COUNT=$((ANCHOR_COUNT + 1))
[ -n "$AFTER" ]  && ANCHOR_COUNT=$((ANCHOR_COUNT + 1))
[ "$ANCHOR_COUNT" -eq 1 ] || die "Specify exactly one of --line, --before-match, --after-match"

if [ -n "$LINE" ]; then
  TARGET="$LINE"
elif [ -n "$BEFORE" ]; then
  M=$(grep -n -F -- "$BEFORE" "$FILE" | head -1 | cut -d: -f1 || true)
  [ -n "$M" ] || die "Pattern not found: $BEFORE"
  TARGET="$M"
else
  M=$(grep -n -F -- "$AFTER" "$FILE" | head -1 | cut -d: -f1 || true)
  [ -n "$M" ] || die "Pattern not found: $AFTER"
  TARGET=$((M + 1))
fi

if [ "$OCE_DRY_RUN" = "1" ]; then
  inserted_lines=$(printf '%s\n' "$CONTENT" | wc -l)
  if [ "$OCE_JSON_MODE" = "1" ]; then
    emit_json status dry_run file "$FILE" target_line "raw:$TARGET" \
      lines_to_insert "raw:$inserted_lines"
  else
    info "DRY RUN: would insert $inserted_lines line(s) at line $TARGET in $FILE"
  fi
  exit 0
fi

BACKUP=$(create_backup "$FILE")
[ -n "$TXN" ] && [ -d "$OCE_TXN_DIR/$TXN" ] && \
  printf '%s\t%s\n' "$FILE" "$BACKUP" >> "$OCE_TXN_DIR/$TXN/files.log"

node - "$FILE" "$TARGET" "$CONTENT" <<'NODE'
const fs = require('fs');
const [,, file, target, content] = process.argv;
const lines = fs.readFileSync(file, 'utf8').split('\n');
const at = parseInt(target, 10) - 1;
const newLines = content.split('\n');
if (newLines[newLines.length - 1] === '') newLines.pop();
lines.splice(at, 0, ...newLines);
fs.writeFileSync(file, lines.join('\n'));
NODE

if [ "$SKIP_VALIDATE" = "0" ]; then
  if ! bash "$(dirname "$0")/oce-validate.sh" "$FILE" >/dev/null 2>&1; then
    cp "$BACKUP" "$FILE"
    die "Insertion caused validation failure — rolled back. Backup: $BACKUP"
  fi
fi

INSERTED=$(printf '%s\n' "$CONTENT" | wc -l)
if [ "$OCE_JSON_MODE" = "1" ]; then
  emit_json status success file "$FILE" target_line "raw:$TARGET" \
    inserted_lines "raw:$INSERTED" backup "$BACKUP"
else
  success "Inserted $INSERTED line(s) at line $TARGET in $FILE"
fi
