#!/usr/bin/env bash
# oce-grep-context — Grep with surrounding lines (handy for understanding a match in situ).

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

PATTERN=""; FILE=""; CONTEXT=5; USE_REGEX=0; CASE_INSENSITIVE=0

while [ $# -gt 0 ]; do
  case "$1" in
    --context|-c)     CONTEXT="$2"; shift 2 ;;
    --context=*)      CONTEXT="${1#*=}"; shift ;;
    --regex)          USE_REGEX=1; shift ;;
    -i|--ignore-case) CASE_INSENSITIVE=1; shift ;;
    --json)           OCE_JSON_MODE="1"; shift ;;
    -h|--help)
      cat <<'EOF'
oce grep-context <pattern> <file> [-c N] [--regex] [-i]
  Print N lines of context around every match (default 5).
  Default is fixed-string match; use --regex for patterns.
EOF
      exit 0 ;;
    -*) die "Unknown flag: $1" ;;
    *)  if [ -z "$PATTERN" ]; then PATTERN="$1"
        elif [ -z "$FILE" ]; then FILE="$1"
        else die "Unexpected arg: $1"; fi
        shift ;;
  esac
done

[ -n "$PATTERN" ] && [ -n "$FILE" ] || die "Usage: oce grep-context <pattern> <file>"
require_file "$FILE"

FLAGS=(-n -C "$CONTEXT")
[ "$USE_REGEX" = "0" ] && FLAGS+=(-F)
[ "$CASE_INSENSITIVE" = "1" ] && FLAGS+=(-i)

if [ "$OCE_JSON_MODE" = "1" ]; then
  RAW=$(grep "${FLAGS[@]}" -- "$PATTERN" "$FILE" 2>/dev/null || true)
  node - "$FILE" "$CONTEXT" <<NODE
const fs = require('fs');
const [,, file, ctx] = process.argv;
const raw = $(printf '%s' "$RAW" | node -e 'let d=""; process.stdin.on("data",c=>d+=c).on("end",()=>process.stdout.write(JSON.stringify(d)))');
const lines = raw ? raw.split("\n").filter(l => l !== "--") : [];
const parsed = lines.map(l => {
  const m = l.match(/^(\d+)([:-])(.*)$/);
  return m ? { line: +m[1], match: m[2] === ':', text: m[3] } : { line: null, match: false, text: l };
});
process.stdout.write(JSON.stringify({status:"success", file, context:+ctx, hits:parsed}) + "\n");
NODE
else
  grep "${FLAGS[@]}" --color=auto -- "$PATTERN" "$FILE" || die "No matches in $FILE"
fi
