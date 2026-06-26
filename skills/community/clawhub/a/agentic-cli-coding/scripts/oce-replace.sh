#!/usr/bin/env bash
# oce-replace — Exact string replacement (no regex surprises).
# Single Node invocation handles count + replacement + sidecar write atomically.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

FILE=""; OLD=""; NEW=""; OLD_FILE=""; NEW_FILE=""
REPLACE_ALL="0"; EXPECTED_COUNT=""; TXN=""; SKIP_VALIDATE="0"

while [ $# -gt 0 ]; do
  case "$1" in
    --old)         OLD="$2"; shift 2 ;;
    --old=*)       OLD="${1#*=}"; shift ;;
    --old-file)    OLD_FILE="$2"; shift 2 ;;
    --new)         NEW="$2"; shift 2 ;;
    --new=*)       NEW="${1#*=}"; shift ;;
    --new-file)    NEW_FILE="$2"; shift 2 ;;
    --all)         REPLACE_ALL="1"; shift ;;
    --count)       EXPECTED_COUNT="$2"; shift 2 ;;
    --txn)         TXN="$2"; shift 2 ;;
    --no-validate) SKIP_VALIDATE="1"; shift ;;
    --json)        OCE_JSON_MODE="1"; shift ;;
    --dry-run)     OCE_DRY_RUN="1"; shift ;;
    -h|--help)
      cat <<'EOF'
oce replace <file> --old STR --new STR [options]
  Exact string match (NOT regex). If multiple matches found and --all is not
  given, the command FAILS — make --old more specific to disambiguate.

  --old STR | --old-file F     The literal string to find
  --new STR | --new-file F     The literal replacement (may be empty)
  --all                        Replace every occurrence
  --count N                    Assert exactly N matches will be replaced
  --txn ID                     Register backup with a transaction
  --no-validate                Skip post-write syntax validation
  --dry-run                    Show match count and proposed change, do nothing
EOF
      exit 0 ;;
    -*) die "Unknown flag: $1" ;;
    *)  FILE="$1"; shift ;;
  esac
done

[ -n "$FILE" ] || die "Usage: oce replace <file> --old STR --new STR [--all]"
require_file "$FILE"
preflight_check "$FILE"

[ -n "$OLD_FILE" ] && OLD=$(cat "$OLD_FILE")
[ -n "$NEW_FILE" ] && NEW=$(cat "$NEW_FILE")
[ -n "$OLD" ] || die "--old is required and may not be empty"

PENDING="${FILE}.oce.pending.$$"
trap 'rm -f "$PENDING"' EXIT

# Single Node invocation — counts AND writes pending atomically
# `|| true` guards against `set -e`; we capture the real exit via $?
set +e
RESULT=$(node - "$FILE" "$PENDING" "$OLD" "$NEW" "$REPLACE_ALL" <<'NODE'
const fs = require('fs');
const [,, file, pending, oldStr, newStr, all] = process.argv;
const content = fs.readFileSync(file, 'utf8');

let count = 0, idx = 0;
while ((idx = content.indexOf(oldStr, idx)) !== -1) {
  count++; idx += oldStr.length;
}

if (count === 0) {
  process.stdout.write(JSON.stringify({ status: 'no_match', count: 0 }));
  process.exit(2);
}
if (count > 1 && all !== '1') {
  process.stdout.write(JSON.stringify({ status: 'ambiguous', count }));
  process.exit(3);
}

const out = all === '1'
  ? content.split(oldStr).join(newStr)
  : content.replace(oldStr, newStr);

fs.writeFileSync(pending, out);
process.stdout.write(JSON.stringify({
  status: 'ready', count,
  bytes_changed: out.length - content.length
}));
NODE
)
NODE_EXIT=$?
set -e

# Parse status from JSON without spawning another node
STATUS=$(printf '%s' "$RESULT" | sed -n 's/.*"status":"\([^"]*\)".*/\1/p')
COUNT=$(printf '%s' "$RESULT"  | sed -n 's/.*"count":\([0-9]*\).*/\1/p')

case "$NODE_EXIT" in
  0)  ;;
  2)  die "No match found for --old in $FILE" ;;
  3)  die "Found $COUNT matches; pass --all or make --old more unique" ;;
  *)  die "Replacement failed (node exit $NODE_EXIT)" ;;
esac

if [ -n "$EXPECTED_COUNT" ] && [ "$COUNT" != "$EXPECTED_COUNT" ]; then
  die "Expected $EXPECTED_COUNT replacements but found $COUNT"
fi

if [ "$OCE_DRY_RUN" = "1" ]; then
  rm -f "$PENDING"
  if [ "$OCE_JSON_MODE" = "1" ]; then
    emit_json status dry_run file "$FILE" matches "raw:$COUNT" \
      message "would replace $COUNT occurrence(s)"
  else
    info "DRY RUN: would replace $COUNT occurrence(s) in $FILE"
  fi
  exit 0
fi

BACKUP=$(create_backup "$FILE")
[ -n "$TXN" ] && [ -d "$OCE_TXN_DIR/$TXN" ] && \
  printf '%s\t%s\n' "$FILE" "$BACKUP" >> "$OCE_TXN_DIR/$TXN/files.log"

mv "$PENDING" "$FILE"
trap - EXIT

if [ "$SKIP_VALIDATE" = "0" ]; then
  if ! bash "$(dirname "$0")/oce-validate.sh" "$FILE" >/dev/null 2>&1; then
    cp "$BACKUP" "$FILE"
    die "Replacement caused validation failure — rolled back. Backup: $BACKUP"
  fi
fi

if [ "$OCE_JSON_MODE" = "1" ]; then
  emit_json status success file "$FILE" replacements "raw:$COUNT" \
    backup "$BACKUP" message "replaced $COUNT occurrence(s)"
else
  success "Replaced $COUNT occurrence(s) in $FILE"
fi
