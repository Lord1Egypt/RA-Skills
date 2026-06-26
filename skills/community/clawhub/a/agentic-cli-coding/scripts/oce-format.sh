#!/usr/bin/env bash
# oce-format — Run the canonical formatter for a file's language, if available.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

FILE=""; CHECK_ONLY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --check)  CHECK_ONLY=1; shift ;;
    --json)   OCE_JSON_MODE="1"; shift ;;
    -h|--help)
      cat <<'EOF'
oce format <file> [--check]
  Runs the language's canonical formatter:
    JS/TS/JSON/CSS/MD: prettier (project-local preferred)
    Python:            black, then ruff format
    Go:                gofmt
    Rust:              rustfmt
    PHP:               php-cs-fixer
    Ruby:              rubocop -A
  --check    Don't write — just report whether the file is formatted
EOF
      exit 0 ;;
    -*) die "Unknown flag: $1" ;;
    *)  FILE="$1"; shift ;;
  esac
done

[ -n "$FILE" ] || die "Usage: oce format <file> [--check]"
require_file "$FILE"
LANG=$(detect_language "$FILE")
FORMATTER="none"
RESULT="not_run"

resolve_local() {
  if [ -x "./node_modules/.bin/$1" ]; then echo "./node_modules/.bin/$1"
  elif command -v "$1" >/dev/null; then echo "$1"
  else echo ""; fi
}

run_check_or_write() {
  local writer_cmd="$1" check_cmd="$2"
  if [ "$CHECK_ONLY" = "1" ]; then
    if eval "$check_cmd" >/dev/null 2>&1; then RESULT="formatted"; else RESULT="needs_format"; return 1; fi
  else
    BACKUP=$(create_backup "$FILE")
    if eval "$writer_cmd"; then RESULT="reformatted"
    else cp "$BACKUP" "$FILE"; RESULT="failed"; return 1; fi
  fi
}

case "$LANG" in
  javascript|typescript|jsx|tsx|json|css|scss|less|markdown|html|vue|svelte)
    P=$(resolve_local prettier)
    if [ -n "$P" ]; then
      FORMATTER="prettier"
      run_check_or_write "$P --write '$FILE'" "$P --check '$FILE'" || true
    fi ;;
  python)
    if command -v black >/dev/null; then
      FORMATTER="black"
      run_check_or_write "black '$FILE'" "black --check '$FILE'" || true
    elif command -v ruff >/dev/null; then
      FORMATTER="ruff format"
      run_check_or_write "ruff format '$FILE'" "ruff format --check '$FILE'" || true
    fi ;;
  go)
    if command -v gofmt >/dev/null; then
      FORMATTER="gofmt"
      run_check_or_write "gofmt -w '$FILE'" "gofmt -l '$FILE' | grep -q . && exit 1; exit 0" || true
    fi ;;
  rust)
    if command -v rustfmt >/dev/null; then
      FORMATTER="rustfmt"
      run_check_or_write "rustfmt '$FILE'" "rustfmt --check '$FILE'" || true
    fi ;;
  php)
    if command -v php-cs-fixer >/dev/null; then
      FORMATTER="php-cs-fixer"
      run_check_or_write "php-cs-fixer fix '$FILE'" "php-cs-fixer fix --dry-run '$FILE'" || true
    fi ;;
  ruby)
    if command -v rubocop >/dev/null; then
      FORMATTER="rubocop"
      run_check_or_write "rubocop -A '$FILE'" "rubocop '$FILE'" || true
    fi ;;
esac

if [ "$OCE_JSON_MODE" = "1" ]; then
  emit_json status success file "$FILE" language "$LANG" \
    formatter "$FORMATTER" result "$RESULT"
else
  if [ "$FORMATTER" = "none" ]; then
    info "$FILE: no formatter configured for $LANG"
  else
    success "$FILE: $FORMATTER → $RESULT"
  fi
fi
