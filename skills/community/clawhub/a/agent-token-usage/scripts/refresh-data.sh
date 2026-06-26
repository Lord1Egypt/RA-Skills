#!/usr/bin/env bash
# Regenerate agent-token-usage.json for every patched Control UI dist.
set -euo pipefail

AGG="$HOME/.openclaw/workspace/skills/agent-token-usage/scripts/agent_token_usage.py"
[[ -f "$AGG" ]] || { echo "✗ aggregator missing: $AGG" >&2; exit 2; }

ROOTS=()
[[ -n "${OPENCLAW_HOME:-}" && -d "$OPENCLAW_HOME" ]] && ROOTS+=("$OPENCLAW_HOME")
if command -v npm >/dev/null 2>&1; then
  R="$(npm root -g 2>/dev/null || true)"; [[ -n "$R" && -d "$R/openclaw" ]] && ROOTS+=("$R/openclaw")
fi
for NVM_BASE in "$HOME/.nvm/versions/node" "/usr/local/n/versions/node"; do
  [[ -d "$NVM_BASE" ]] || continue
  while IFS= read -r d; do [[ -n "$d" ]] && ROOTS+=("$d"); done \
    < <(find "$NVM_BASE" -maxdepth 4 -path "*/lib/node_modules/openclaw" -type d 2>/dev/null)
done

DATA="$(python3 "$AGG" --format json 2>/dev/null || echo '{}')"
for ROOT in "${ROOTS[@]:-}"; do
  for REL in "dist/control-ui" "ui/dist"; do
    BASE="$ROOT/$REL"
    [[ -d "$BASE/assets" ]] || continue
    mkdir -p "$BASE/data"
    printf '%s' "$DATA" > "$BASE/data/agent-token-usage.json.tmp"
    mv "$BASE/data/agent-token-usage.json.tmp" "$BASE/data/agent-token-usage.json"
  done
done
