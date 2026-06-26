#!/usr/bin/env bash
# oce-validate — Multi-language syntax validation. Best-effort: when a
# language-specific validator isn't installed, the file passes (we can't
# claim it's invalid). Validators are checked in order of reliability.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

FILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --json)  OCE_JSON_MODE="1"; shift ;;
    -h|--help)
      cat <<'EOF'
oce validate <file>
  Auto-detects language from extension and runs the appropriate syntax check.
  Returns exit 0 if valid OR no validator available; non-zero on definite syntax error.
  Supported (when tools installed): JS/TS, JSON, YAML, Python, Bash, Go, Rust,
  PHP, Ruby, HTML, CSS. See references/language-support.md for details.
EOF
      exit 0 ;;
    *) FILE="$1"; shift ;;
  esac
done

[ -n "$FILE" ] || die "Usage: oce validate <file>"
require_file "$FILE"

LANG=$(detect_language "$FILE")
VALID=1
OUTPUT=""
VALIDATOR="none"

run() { OUTPUT=$("$@" 2>&1); local rc=$?; return $rc; }

case "$LANG" in
  javascript|jsx)
    if command -v node >/dev/null; then
      VALIDATOR="node --check"
      run node --check "$FILE" || VALID=0
    fi ;;
  typescript|tsx)
    if [ -x "./node_modules/.bin/tsc" ]; then
      VALIDATOR="local tsc"
      run ./node_modules/.bin/tsc --noEmit --allowJs --skipLibCheck "$FILE" || VALID=0
    elif command -v tsc >/dev/null; then
      VALIDATOR="tsc"
      run tsc --noEmit --allowJs --skipLibCheck "$FILE" || VALID=0
    elif command -v node >/dev/null; then
      # Last resort: parse with acorn after stripping types (best-effort only)
      VALIDATOR="acorn (TS stripped, syntax-only)"
      OUTPUT=$(node -e "
        try {
          const fs = require('fs');
          const acorn = require('acorn');
          let src = fs.readFileSync('$FILE','utf8');
          // Naive type stripping — only catches gross syntax issues
          src = src.replace(/:\s*[A-Za-z_\$][\w\.<>\[\]\|& ,?]*/g,'');
          src = src.replace(/\binterface\s+\w+\s*\{[\s\S]*?\}/g,'');
          src = src.replace(/\btype\s+\w+\s*=[^;]+;/g,'');
          acorn.parse(src,{ecmaVersion:'latest',sourceType:'module'});
        } catch(e) { console.error(e.message); process.exit(1); }
      " 2>&1) || VALID=0
    fi ;;
  vue|svelte)
    # No bundled validator — these are component formats. Defer to project tooling.
    VALIDATOR="none (use project linter)"
    ;;
  python)
    if command -v python3 >/dev/null; then
      VALIDATOR="python3 -m py_compile"
      run python3 -m py_compile "$FILE" || VALID=0
    elif command -v python >/dev/null; then
      VALIDATOR="python -m py_compile"
      run python -m py_compile "$FILE" || VALID=0
    fi ;;
  json)
    VALIDATOR="JSON.parse"
    run node -e "JSON.parse(require('fs').readFileSync('$FILE','utf8'))" || VALID=0
    ;;
  yaml)
    if [ -d "$OCE_HOME/node_modules/js-yaml" ]; then
      VALIDATOR="js-yaml"
      run node -e "require('js-yaml').load(require('fs').readFileSync('$FILE','utf8'))" || VALID=0
    elif command -v python3 >/dev/null; then
      VALIDATOR="python yaml"
      run python3 -c "import sys,yaml; yaml.safe_load(open('$FILE'))" || VALID=0
    fi ;;
  bash|zsh)
    VALIDATOR="bash -n"
    run bash -n "$FILE" || VALID=0
    ;;
  go)
    if command -v gofmt >/dev/null; then
      VALIDATOR="gofmt -e"
      run gofmt -e "$FILE" >/dev/null || VALID=0
    fi ;;
  rust)
    # rustc as a syntax-only check is heavy; prefer rustfmt for parse validation
    if command -v rustfmt >/dev/null; then
      VALIDATOR="rustfmt --check"
      run rustfmt --check "$FILE" || VALID=0
    fi ;;
  php)
    if command -v php >/dev/null; then
      VALIDATOR="php -l"
      run php -l "$FILE" || VALID=0
    fi ;;
  ruby)
    if command -v ruby >/dev/null; then
      VALIDATOR="ruby -c"
      run ruby -c "$FILE" || VALID=0
    fi ;;
  java)
    # No lightweight syntax-only checker; defer to build system
    VALIDATOR="none (use project compiler)"
    ;;
  html)
    if command -v node >/dev/null; then
      # Best-effort: just confirm balanced angle brackets at gross level
      VALIDATOR="basic HTML check"
      run node -e "
        const html = require('fs').readFileSync('$FILE','utf8');
        const opens = (html.match(/</g) || []).length;
        const closes = (html.match(/>/g) || []).length;
        if (opens !== closes) { console.error('Mismatched <> count'); process.exit(1); }
      " || VALID=0
    fi ;;
  *)
    # markdown, xml, css, scss, sql, toml, dockerfile, makefile, unknown:
    # nothing reliable to run with zero deps. Pass through.
    VALIDATOR="none (no validator for $LANG)"
    ;;
esac

if [ "$OCE_JSON_MODE" = "1" ]; then
  emit_json status "$([ $VALID -eq 1 ] && echo success || echo error)" \
    file "$FILE" language "$LANG" validator "$VALIDATOR" \
    valid "raw:$([ $VALID -eq 1 ] && echo true || echo false)" \
    output "$OUTPUT"
else
  if [ $VALID -eq 1 ]; then
    if [ "$VALIDATOR" = "none" ] || [[ "$VALIDATOR" == "none "* ]]; then
      success "$FILE: $VALIDATOR — accepted ($LANG)"
    else
      success "$FILE: valid ($LANG via $VALIDATOR)"
    fi
  else
    [ -n "$OUTPUT" ] && printf '%s\n' "$OUTPUT" >&2
    die "$FILE: validation failed ($LANG via $VALIDATOR)"
  fi
fi

exit $((1 - VALID))
