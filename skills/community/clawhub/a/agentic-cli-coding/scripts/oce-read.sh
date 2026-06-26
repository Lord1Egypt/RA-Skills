#!/usr/bin/env bash
# oce-read — Smart file reader with line numbers and context modes.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

FILE=""; LINES=""; AROUND=""; CONTEXT="10"; SHOW_LINES="1"

while [ $# -gt 0 ]; do
  case "$1" in
    --lines)      LINES="$2"; shift 2 ;;
    --lines=*)    LINES="${1#*=}"; shift ;;
    --around)     AROUND="$2"; shift 2 ;;
    --around=*)   AROUND="${1#*=}"; shift ;;
    --context|-c) CONTEXT="$2"; shift 2 ;;
    --context=*)  CONTEXT="${1#*=}"; shift ;;
    --no-numbers) SHOW_LINES="0"; shift ;;
    --json)       OCE_JSON_MODE="1"; shift ;;
    --no-color)   C_BLUE="" C_RESET=""; shift ;;
    -h|--help)
      cat <<'EOF'
oce read <file> [options]
  --lines A:B          Show lines A through B (B may be omitted for single line)
  --around PATTERN     Show CONTEXT lines around the first match
  --context N | -c N   Lines of context for --around (default 10)
  --no-numbers         Omit line number gutter
  --json               JSON output
EOF
      exit 0 ;;
    -*) die "Unknown flag: $1" ;;
    *)  FILE="$1"; shift ;;
  esac
done

[ -n "$FILE" ] || die "Usage: oce read <file> [--lines A:B | --around PATTERN]"
require_file "$FILE"

TOTAL=$(count_lines "$FILE")
LANG=$(detect_language "$FILE")

if [ -n "$LINES" ]; then
  START="${LINES%:*}"
  END="${LINES#*:}"
  [ "$START" = "$LINES" ] && END="$START"
elif [ -n "$AROUND" ]; then
  MATCH=$(grep -n -F -- "$AROUND" "$FILE" | head -1 | cut -d: -f1 || true)
  [ -n "$MATCH" ] || die "Pattern not found: $AROUND"
  START=$((MATCH - CONTEXT))
  END=$((MATCH + CONTEXT))
  [ "$START" -lt 1 ] && START=1
  [ "$END" -gt "$TOTAL" ] && END="$TOTAL"
else
  START=1
  END="$TOTAL"
fi

# Validate
case "$START" in ''|*[!0-9]*) die "Invalid start line: $START" ;; esac
case "$END" in ''|*[!0-9]*) die "Invalid end line: $END" ;; esac
[ "$START" -ge 1 ] || die "Start line must be >= 1"
[ "$END" -le "$TOTAL" ] || die "End line $END exceeds file length $TOTAL"
[ "$START" -le "$END" ] || die "Start must be <= end"

if [ "$OCE_JSON_MODE" = "1" ]; then
  node - "$FILE" "$START" "$END" "$LANG" "$TOTAL" <<'NODE'
const fs = require('fs');
const [,, file, s, e, lang, total] = process.argv;
const lines = fs.readFileSync(file, 'utf8').split('\n');
const start = +s, end = +e;
const slice = lines.slice(start - 1, end).map((content, i) => ({
  line: start + i, content
}));
process.stdout.write(JSON.stringify({
  status: 'success', file, language: lang,
  total_lines: +total, range: { start, end }, lines: slice
}) + '\n');
NODE
else
  printf '%s═══ %s ═══%s\n' "$C_BLUE" "$FILE" "$C_RESET"
  printf '%slang:%s %s  %slines:%s %d-%d of %d\n' \
    "$C_BLUE" "$C_RESET" "$LANG" "$C_BLUE" "$C_RESET" "$START" "$END" "$TOTAL"
  printf '%s───────────────────────%s\n' "$C_BLUE" "$C_RESET"
  if [ "$SHOW_LINES" = "1" ]; then
    awk -v s="$START" -v e="$END" \
      'NR>=s && NR<=e { printf "%5d │ %s\n", NR, $0 } NR>e{exit}' "$FILE"
  else
    sed -n "${START},${END}p" "$FILE"
  fi
fi
