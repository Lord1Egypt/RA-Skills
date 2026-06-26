#!/usr/bin/env bash
# oce-patch — Apply unified diffs with backup + validation rollback.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

SUBCMD="${1:-}"
shift || true

case "$SUBCMD" in
  apply)
    PATCHFILE=""; FUZZ=0; REVERSE=0; TXN=""; STRIP=1
    while [ $# -gt 0 ]; do
      case "$1" in
        --fuzz)    FUZZ="$2"; shift 2 ;;
        --reverse|-R) REVERSE=1; shift ;;
        --strip|-p) STRIP="$2"; shift 2 ;;
        --txn)     TXN="$2"; shift 2 ;;
        --json)    OCE_JSON_MODE="1"; shift ;;
        --dry-run) OCE_DRY_RUN="1"; shift ;;
        -*) die "Unknown flag: $1" ;;
        *)  PATCHFILE="$1"; shift ;;
      esac
    done

    [ -n "$PATCHFILE" ] || die "Usage: oce patch apply <patchfile>"
    require_file "$PATCHFILE"

    # Dry-run check first
    DRY_OUT=$(mktemp)
    trap 'rm -f "$DRY_OUT"' EXIT
    if ! patch --dry-run -p"$STRIP" --fuzz="$FUZZ" $([ "$REVERSE" = "1" ] && echo "-R") < "$PATCHFILE" > "$DRY_OUT" 2>&1; then
      cat "$DRY_OUT" >&2
      die "Patch does not apply cleanly. Adjust the diff or pass --fuzz N."
    fi

    if [ "$OCE_DRY_RUN" = "1" ]; then
      cat "$DRY_OUT"
      exit 0
    fi

    # Extract destination filenames from `+++ ` lines, strip a/ or b/ prefix
    FILES=$(grep -E '^\+\+\+ ' "$PATCHFILE" | awk '{print $2}' | sed 's|^[ab]/||' | sed 's|	.*$||')

    BACKUPS=""
    for f in $FILES; do
      [ "$f" = "/dev/null" ] && continue
      if [ -f "$f" ]; then
        BK=$(create_backup "$f")
        BACKUPS="$BACKUPS $f|$BK"
        [ -n "$TXN" ] && [ -d "$OCE_TXN_DIR/$TXN" ] && \
          printf '%s\t%s\n' "$f" "$BK" >> "$OCE_TXN_DIR/$TXN/files.log"
      fi
    done

    if patch -p"$STRIP" --fuzz="$FUZZ" $([ "$REVERSE" = "1" ] && echo "-R") < "$PATCHFILE"; then
      # Validate every affected file
      FAILED=""
      for f in $FILES; do
        [ "$f" = "/dev/null" ] && continue
        if [ -f "$f" ] && ! bash "$(dirname "$0")/oce-validate.sh" "$f" >/dev/null 2>&1; then
          FAILED="$FAILED $f"
        fi
      done
      if [ -n "$FAILED" ]; then
        warn "Validation failed for:$FAILED — rolling back"
        for pair in $BACKUPS; do
          file="${pair%|*}"; backup="${pair#*|}"
          [ -f "$backup" ] && cp "$backup" "$file"
        done
        die "Patch applied but validation failed — rolled back"
      fi
      n=$(echo "$FILES" | wc -w | tr -d ' ')
      success "Patch applied to $n file(s)"
    else
      die "Patch application failed"
    fi
    ;;

  create)
    FILE="$1"
    [ -n "$FILE" ] || die "Usage: oce patch create <file> < new_content"
    require_file "$FILE"
    TMPNEW=$(mktemp)
    trap 'rm -f "$TMPNEW"' EXIT
    cat > "$TMPNEW"
    diff -u "$FILE" "$TMPNEW" | sed "s|$TMPNEW|b/$FILE|; s|$FILE|a/$FILE|"
    ;;

  -h|--help|help|"")
    cat <<'EOF'
oce patch <apply|create>
  apply <patchfile>       Apply unified diff. Auto-backs-up affected files,
                          validates after, rolls back on validation failure.
    --fuzz N              Allow fuzzy context matching
    --reverse | -R        Apply patch in reverse
    --strip N | -p N      Strip path components (default 1)
    --txn ID              Register backups with a transaction
    --dry-run             Show what would be patched, change nothing
  create <file> < new     Generate a unified diff between <file> and stdin
EOF
    ;;

  *)
    die "Unknown subcommand: $SUBCMD"
    ;;
esac
