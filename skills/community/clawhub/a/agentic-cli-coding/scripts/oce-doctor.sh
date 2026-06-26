#!/usr/bin/env bash
# oce-doctor — Verify the toolkit is installed correctly.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

OCE_JSON_MODE="${OCE_JSON_MODE:-0}"
for a in "$@"; do
  [ "$a" = "--json" ] && OCE_JSON_MODE=1
done

errors=0
warnings=0
declare -A RESULTS

check() {
  local label="$1" cmd="$2" required="${3:-1}"
  if eval "$cmd" >/dev/null 2>&1; then
    RESULTS["$label"]="ok"
    [ "$OCE_JSON_MODE" = "0" ] && printf '  %s✓%s %s\n' "$C_GREEN" "$C_RESET" "$label"
  else
    if [ "$required" = "1" ]; then
      RESULTS["$label"]="missing"
      errors=$((errors + 1))
      [ "$OCE_JSON_MODE" = "0" ] && printf '  %s✗%s %s\n' "$C_RED" "$C_RESET" "$label"
    else
      RESULTS["$label"]="absent"
      warnings=$((warnings + 1))
      [ "$OCE_JSON_MODE" = "0" ] && printf '  %s○%s %s (optional)\n' "$C_YELLOW" "$C_RESET" "$label"
    fi
  fi
  return 0
}

if [ "$OCE_JSON_MODE" = "0" ]; then
  printf '%sEnvironment%s\n' "$C_BLUE" "$C_RESET"
  printf '  OCE_HOME      = %s\n' "$OCE_HOME"
  printf '  OCE_STATE_DIR = %s\n\n' "$OCE_STATE_DIR"
  printf '%sCore tools%s\n' "$C_BLUE" "$C_RESET"
fi

check "node"  "command -v node"
check "patch" "command -v patch"
check "diff"  "command -v diff"
check "grep"  "command -v grep"
check "acorn" "node -e \"require('$OCE_HOME/node_modules/acorn')\""

[ "$OCE_JSON_MODE" = "0" ] && printf '\n%sOptional formatters/validators%s\n' "$C_BLUE" "$C_RESET"

check "prettier"   "command -v prettier || [ -x ./node_modules/.bin/prettier ]" 0
check "eslint"     "command -v eslint   || [ -x ./node_modules/.bin/eslint ]"   0
check "tsc"        "command -v tsc      || [ -x ./node_modules/.bin/tsc ]"      0
check "gofmt"      "command -v gofmt"   0
check "rustfmt"    "command -v rustfmt" 0
check "php"        "command -v php"     0
check "ruby"       "command -v ruby"    0
check "python3"    "command -v python3" 0
check "rubocop"    "command -v rubocop" 0
check "black"      "command -v black"   0

if [ "$OCE_JSON_MODE" = "1" ]; then
  checks="{"
  first=1
  for k in "${!RESULTS[@]}"; do
    [ $first = 1 ] && first=0 || checks+=","
    checks+="\"$k\":\"${RESULTS[$k]}\""
  done
  checks+="}"
  emit_json status "$([ $errors -eq 0 ] && echo ok || echo error)" \
    errors "raw:$errors" warnings "raw:$warnings" \
    home "$OCE_HOME" state_dir "$OCE_STATE_DIR" \
    checks "raw:$checks"
else
  printf '\n'
  if [ $errors -eq 0 ]; then
    success "Setup OK ($warnings optional tool(s) missing — that's fine)"
  else
    die "$errors required tool(s) missing"
  fi
fi
