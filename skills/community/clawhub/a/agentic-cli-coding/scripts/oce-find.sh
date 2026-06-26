#!/usr/bin/env bash
# oce-find — Pattern search with sensible language filters and excludes.
# Defaults to fixed-string match (-F) for safety; pass --regex for regex.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

PATTERN=""; PATH_ARG="."; TYPE=""; FILES_ONLY=0; MAX=200
USE_REGEX=0; CASE_INSENSITIVE=0

while [ $# -gt 0 ]; do
  case "$1" in
    --type)         TYPE="$2"; shift 2 ;;
    --files-only)   FILES_ONLY=1; shift ;;
    --max)          MAX="$2"; shift 2 ;;
    --regex)        USE_REGEX=1; shift ;;
    -i|--ignore-case) CASE_INSENSITIVE=1; shift ;;
    --json)         OCE_JSON_MODE="1"; shift ;;
    -h|--help)
      cat <<'EOF'
oce find <pattern> [--type LANG] [--regex] [-i] [--files-only] [path]
  Search for PATTERN under [path] (default: cwd). Auto-excludes node_modules,
  .git, dist, build, .next, __pycache__, vendor, target, .venv.

  --type LANG    Limit to a language: js, ts, py, go, rb, java, c, cpp, php,
                 vue, svelte, sh, sql, css, html, md (or any extension)
  --regex        Treat pattern as a regex (default is literal/fixed-string)
  -i             Case-insensitive
  --files-only   Print matching filenames only
  --max N        Cap results (default 200)
EOF
      exit 0 ;;
    -*) die "Unknown flag: $1" ;;
    *)  if [ -z "$PATTERN" ]; then PATTERN="$1"; else PATH_ARG="$1"; fi; shift ;;
  esac
done

[ -n "$PATTERN" ] || die "Usage: oce find <pattern> [--type LANG] [path]"

INCLUDE=()
case "$TYPE" in
  js)        INCLUDE=(--include='*.js' --include='*.mjs' --include='*.cjs') ;;
  ts)        INCLUDE=(--include='*.ts' --include='*.tsx') ;;
  jsx)       INCLUDE=(--include='*.jsx') ;;
  vue)       INCLUDE=(--include='*.vue') ;;
  svelte)    INCLUDE=(--include='*.svelte') ;;
  py)        INCLUDE=(--include='*.py') ;;
  go)        INCLUDE=(--include='*.go') ;;
  rb)        INCLUDE=(--include='*.rb') ;;
  java)      INCLUDE=(--include='*.java') ;;
  kt)        INCLUDE=(--include='*.kt' --include='*.kts') ;;
  c)         INCLUDE=(--include='*.c' --include='*.h') ;;
  cpp)       INCLUDE=(--include='*.cpp' --include='*.cc' --include='*.cxx' --include='*.hpp' --include='*.hh') ;;
  cs)        INCLUDE=(--include='*.cs') ;;
  php)       INCLUDE=(--include='*.php') ;;
  rs)        INCLUDE=(--include='*.rs') ;;
  sh)        INCLUDE=(--include='*.sh' --include='*.bash') ;;
  sql)       INCLUDE=(--include='*.sql') ;;
  css)       INCLUDE=(--include='*.css' --include='*.scss' --include='*.sass' --include='*.less') ;;
  html)      INCLUDE=(--include='*.html' --include='*.htm') ;;
  md)        INCLUDE=(--include='*.md' --include='*.mdx') ;;
  json)      INCLUDE=(--include='*.json') ;;
  yaml)      INCLUDE=(--include='*.yaml' --include='*.yml') ;;
  "")        INCLUDE=() ;;
  *)         INCLUDE=(--include="*.$TYPE") ;;
esac

EXCLUDE=(
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist
  --exclude-dir=build --exclude-dir=.next --exclude-dir=__pycache__
  --exclude-dir=vendor --exclude-dir=target --exclude-dir=.venv
  --exclude-dir=.oce --exclude-dir=coverage --exclude-dir=.cache
)

FLAGS=(-r)
[ "$USE_REGEX" = "0" ] && FLAGS+=(-F)
[ "$CASE_INSENSITIVE" = "1" ] && FLAGS+=(-i)
if [ "$FILES_ONLY" = "1" ]; then FLAGS+=(-l); else FLAGS+=(-n); fi

# Run the search
RESULTS=$(grep "${FLAGS[@]}" "${INCLUDE[@]}" "${EXCLUDE[@]}" -- "$PATTERN" "$PATH_ARG" 2>/dev/null | head -n "$MAX" || true)

if [ "$OCE_JSON_MODE" = "1" ]; then
  if [ "$FILES_ONLY" = "1" ]; then
    node - <<NODE
const lines = $(printf '%s' "$RESULTS" | node -e 'let d=""; process.stdin.on("data",c=>d+=c).on("end",()=>{const arr=d?d.split("\n").filter(Boolean):[];process.stdout.write(JSON.stringify(arr))})');
process.stdout.write(JSON.stringify({status:"success", mode:"files-only", count:lines.length, files:lines}) + "\n");
NODE
  else
    node - <<NODE
const text = $(printf '%s' "$RESULTS" | node -e 'let d=""; process.stdin.on("data",c=>d+=c).on("end",()=>process.stdout.write(JSON.stringify(d)))');
const matches = text ? text.split("\n").filter(Boolean).map(line => {
  const m = line.match(/^([^:]+):(\d+):(.*)$/);
  return m ? { file: m[1], line: parseInt(m[2], 10), text: m[3] } : { file: null, line: null, text: line };
}) : [];
process.stdout.write(JSON.stringify({status:"success", count:matches.length, matches}) + "\n");
NODE
  fi
else
  if [ -z "$RESULTS" ]; then
    info "No matches"
  else
    printf '%s\n' "$RESULTS"
  fi
fi
