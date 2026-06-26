#!/usr/bin/env bash
# oce-ast — Structural edits for JS/TS via acorn AST.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

AST_HELPER="$OCE_HOME/scripts/lib/ast-helper.js"
SUBCMD="${1:-}"
shift || true

case "$SUBCMD" in
  symbols)
    FILE="${1:-}"
    [ -n "$FILE" ] || die "Usage: oce ast symbols <file>"
    require_file "$FILE"
    node "$AST_HELPER" symbols "$FILE"
    ;;

  rename)
    FILE=""; OLD=""; NEW=""; TXN=""
    while [ $# -gt 0 ]; do
      case "$1" in
        --from) OLD="$2"; shift 2 ;;
        --to)   NEW="$2"; shift 2 ;;
        --txn)  TXN="$2"; shift 2 ;;
        --json) OCE_JSON_MODE="1"; shift ;;
        *)      FILE="$1"; shift ;;
      esac
    done
    [ -n "$FILE" ] && [ -n "$OLD" ] && [ -n "$NEW" ] || \
      die "Usage: oce ast rename <file> --from NAME --to NAME"
    require_file "$FILE"

    BACKUP=$(create_backup "$FILE")
    [ -n "$TXN" ] && [ -d "$OCE_TXN_DIR/$TXN" ] && \
      printf '%s\t%s\n' "$FILE" "$BACKUP" >> "$OCE_TXN_DIR/$TXN/files.log"

    RES=$(node "$AST_HELPER" rename "$FILE" "$OLD" "$NEW") || {
      printf '%s\n' "$RES" >&2
      cp "$BACKUP" "$FILE"
      die "AST rename failed — rolled back"
    }
    mv "${FILE}.oce.pending" "$FILE"

    if ! bash "$(dirname "$0")/oce-validate.sh" "$FILE" >/dev/null 2>&1; then
      cp "$BACKUP" "$FILE"
      die "Rename caused validation failure — rolled back"
    fi

    COUNT=$(printf '%s' "$RES" | sed -n 's/.*"count":\([0-9]*\).*/\1/p')
    if [ "$OCE_JSON_MODE" = "1" ]; then
      emit_json status success file "$FILE" replacements "raw:$COUNT" \
        from "$OLD" to "$NEW" backup "$BACKUP"
    else
      success "Renamed '$OLD' → '$NEW' in $FILE ($COUNT identifier reference(s))"
    fi
    ;;

  extract)
    FILE="${1:-}"; NAME="${2:-}"
    [ -n "$FILE" ] && [ -n "$NAME" ] || die "Usage: oce ast extract <file> <symbol>"
    require_file "$FILE"
    node "$AST_HELPER" extract "$FILE" "$NAME"
    ;;

  replace-symbol)
    FILE=""; NAME=""; TXN=""
    while [ $# -gt 0 ]; do
      case "$1" in
        --txn)  TXN="$2"; shift 2 ;;
        --json) OCE_JSON_MODE="1"; shift ;;
        *)      if [ -z "$FILE" ]; then FILE="$1"
                elif [ -z "$NAME" ]; then NAME="$1"
                else die "Unexpected arg: $1"; fi
                shift ;;
      esac
    done
    [ -n "$FILE" ] && [ -n "$NAME" ] || die "Usage: oce ast replace-symbol <file> <symbol> < new_code"
    require_file "$FILE"

    BACKUP=$(create_backup "$FILE")
    [ -n "$TXN" ] && [ -d "$OCE_TXN_DIR/$TXN" ] && \
      printf '%s\t%s\n' "$FILE" "$BACKUP" >> "$OCE_TXN_DIR/$TXN/files.log"

    if ! node "$AST_HELPER" replace-symbol "$FILE" "$NAME"; then
      cp "$BACKUP" "$FILE"
      die "AST replace-symbol failed — rolled back"
    fi
    mv "${FILE}.oce.pending" "$FILE"

    if ! bash "$(dirname "$0")/oce-validate.sh" "$FILE" >/dev/null 2>&1; then
      cp "$BACKUP" "$FILE"
      die "Replacement caused validation failure — rolled back"
    fi

    if [ "$OCE_JSON_MODE" = "1" ]; then
      emit_json status success file "$FILE" symbol "$NAME" backup "$BACKUP"
    else
      success "Replaced symbol '$NAME' in $FILE"
    fi
    ;;

  -h|--help|help|"")
    cat <<'EOF'
oce ast <subcommand>
  symbols <file>                  List functions/classes with line ranges
  rename <file> --from N --to N   Rename every identifier reference
  extract <file> <symbol>         Print the source of a function/class
  replace-symbol <file> <symbol>  Replace a function/class body from stdin

WORKS ON: .js, .mjs, .cjs, .jsx (acorn parses these natively)
LIMITED ON: .ts, .tsx (TypeScript-specific syntax may not parse)
              For TypeScript, prefer text-based edits (replace, patch).
EOF
    ;;

  *)
    die "Unknown subcommand: $SUBCMD"
    ;;
esac
