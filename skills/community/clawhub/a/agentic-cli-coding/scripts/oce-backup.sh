#!/usr/bin/env bash
# oce-backup — Backup management (list, restore, diff, clean).

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

SUBCMD="${1:-}"
shift || true

case "$SUBCMD" in
  list)
    FILE=""
    JSON=0
    while [ $# -gt 0 ]; do
      case "$1" in
        --json) JSON=1; shift ;;
        *) FILE="$1"; shift ;;
      esac
    done
    if [ -n "$FILE" ]; then
      backups=$(list_backups "$FILE")
    else
      backups=$(ls -t "$OCE_BACKUP_DIR"/*.bak 2>/dev/null | head -50 || true)
    fi
    if [ "$JSON" = "1" ]; then
      OCE_JSON_MODE=1
      node - <<NODE
const list = $(printf '%s' "$backups" | node -e 'let d=""; process.stdin.on("data",c=>d+=c).on("end",()=>process.stdout.write(JSON.stringify(d)))');
const arr = list ? list.split('\n').filter(Boolean) : [];
process.stdout.write(JSON.stringify({status:'success', count:arr.length, backups:arr}) + '\n');
NODE
    else
      if [ -z "$backups" ]; then
        info "No backups found"
      else
        printf '%s\n' "$backups"
      fi
    fi
    ;;

  restore)
    FILE=""; AT=0
    while [ $# -gt 0 ]; do
      case "$1" in
        --at) AT="$2"; shift 2 ;;
        --json) OCE_JSON_MODE=1; shift ;;
        *) FILE="$1"; shift ;;
      esac
    done
    [ -n "$FILE" ] || die "Usage: oce backup restore <file> [--at N]"
    backups=$(list_backups "$FILE")
    [ -n "$backups" ] || die "No backups found for $FILE"
    target=$(printf '%s\n' "$backups" | sed -n "$((AT + 1))p")
    [ -n "$target" ] || die "No backup at position $AT for $FILE (newest is 0)"
    cp "$target" "$FILE"
    if [ "$OCE_JSON_MODE" = "1" ]; then
      emit_json status success file "$FILE" restored_from "$target"
    else
      success "Restored $FILE from $target"
    fi
    ;;

  diff)
    FILE="${1:-}"; AT="${2:-0}"
    [ -n "$FILE" ] || die "Usage: oce backup diff <file> [N]"
    backups=$(list_backups "$FILE")
    [ -n "$backups" ] || die "No backups for $FILE"
    target=$(printf '%s\n' "$backups" | sed -n "$((AT + 1))p")
    [ -n "$target" ] || die "No backup at position $AT for $FILE"
    diff -u "$target" "$FILE"
    ;;

  clean)
    DAYS="${1:-30}"
    case "$DAYS" in ''|*[!0-9]*) die "DAYS must be a number" ;; esac
    removed=$(find "$OCE_BACKUP_DIR" -name '*.bak' -type f -mtime +"$DAYS" -print -delete 2>/dev/null | wc -l)
    success "Cleaned $removed backup(s) older than $DAYS days"
    ;;

  -h|--help|help|"")
    cat <<'EOF'
oce backup <subcommand>
  list [<file>]              List backups (newest first)
  restore <file> [--at N]    Restore Nth backup (0 = most recent)
  diff <file> [N]            Diff vs Nth backup
  clean [DAYS]               Delete backups older than DAYS (default 30)
EOF
    ;;

  *)
    die "Unknown subcommand: $SUBCMD (try: oce backup help)"
    ;;
esac
