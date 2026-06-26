#!/usr/bin/env bash
# oce-transaction — Atomic multi-file operations.
# Usage pattern:
#   TXN=$(oce transaction begin)
#   oce replace foo.js --old X --new Y --txn "$TXN"
#   oce replace bar.js --old X --new Y --txn "$TXN"
#   oce transaction validate "$TXN"
#   oce transaction commit "$TXN"   # or rollback

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

SUBCMD="${1:-}"
shift || true

case "$SUBCMD" in
  begin)
    TXN_ID="txn-$(date +%Y%m%d-%H%M%S)-$$"
    TXN_PATH="$OCE_TXN_DIR/$TXN_ID"
    mkdir -p "$TXN_PATH"
    {
      printf 'started_at\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
      printf 'pid\t%s\n' "$$"
      printf 'cwd\t%s\n' "$PWD"
    } > "$TXN_PATH/meta"
    : > "$TXN_PATH/files.log"
    printf '%s\n' "$TXN_ID"
    ;;

  status)
    TXN_ID="$1"
    TXN_PATH="$OCE_TXN_DIR/$TXN_ID"
    [ -d "$TXN_PATH" ] || die "Transaction not found: $TXN_ID"
    info "Transaction: $TXN_ID"
    cat "$TXN_PATH/meta"
    info "Files modified:"
    if [ -s "$TXN_PATH/files.log" ]; then
      while IFS=$'\t' read -r f b; do
        printf '  %s  (backup: %s)\n' "$f" "$b"
      done < "$TXN_PATH/files.log"
    else
      info "  (none yet)"
    fi
    ;;

  validate)
    TXN_ID="$1"
    TXN_PATH="$OCE_TXN_DIR/$TXN_ID"
    [ -d "$TXN_PATH" ] || die "Transaction not found: $TXN_ID"
    failed=0
    while IFS=$'\t' read -r file backup; do
      [ -z "$file" ] && continue
      if [ -f "$file" ]; then
        if bash "$(dirname "$0")/oce-validate.sh" "$file" >/dev/null 2>&1; then
          printf '  %s✓%s %s\n' "$C_GREEN" "$C_RESET" "$file"
        else
          printf '  %s✗%s %s\n' "$C_RED" "$C_RESET" "$file"
          failed=$((failed + 1))
        fi
      fi
    done < "$TXN_PATH/files.log"
    [ "$failed" = "0" ] || exit 1
    ;;

  commit)
    TXN_ID="$1"
    TXN_PATH="$OCE_TXN_DIR/$TXN_ID"
    [ -d "$TXN_PATH" ] || die "Transaction not found: $TXN_ID"

    failed=""
    while IFS=$'\t' read -r file backup; do
      [ -z "$file" ] && continue
      if [ -f "$file" ] && ! bash "$(dirname "$0")/oce-validate.sh" "$file" >/dev/null 2>&1; then
        failed="$failed $file"
      fi
    done < "$TXN_PATH/files.log"

    if [ -n "$failed" ]; then
      die "Validation failed for:$failed — run 'oce transaction rollback $TXN_ID'"
    fi

    mv "$TXN_PATH" "$OCE_TXN_DIR/committed-$TXN_ID"
    success "Transaction $TXN_ID committed"
    ;;

  rollback)
    TXN_ID="$1"
    TXN_PATH="$OCE_TXN_DIR/$TXN_ID"
    [ -d "$TXN_PATH" ] || die "Transaction not found: $TXN_ID"

    count=0
    # Process in reverse order so the *first* backup wins (oldest snapshot)
    tac "$TXN_PATH/files.log" | while IFS=$'\t' read -r file backup; do
      [ -z "$file" ] && continue
      if [ -f "$backup" ]; then
        cp "$backup" "$file"
        count=$((count + 1))
      fi
    done
    # Note: count inside `while | pipe` lives in subshell — recount
    count=$(wc -l < "$TXN_PATH/files.log" | tr -d ' ')

    mv "$TXN_PATH" "$OCE_TXN_DIR/rolled-back-$TXN_ID"
    success "Rolled back $count file(s) from transaction $TXN_ID"
    ;;

  list)
    ls -1t "$OCE_TXN_DIR" 2>/dev/null | head -20 || info "No transactions"
    ;;

  -h|--help|help|"")
    cat <<'EOF'
oce transaction <subcommand>
  begin                    Print a new transaction ID
  status <txn>             Show meta + files in transaction
  validate <txn>           Validate every file (exit 1 if any invalid)
  commit <txn>             Validate + finalize (rename dir to committed-*)
  rollback <txn>           Restore every file from snapshot
  list                     Recent transactions

Pass --txn <id> to oce replace/insert/delete/write/patch to register them.
EOF
    ;;

  *)
    die "Unknown subcommand: $SUBCMD"
    ;;
esac
