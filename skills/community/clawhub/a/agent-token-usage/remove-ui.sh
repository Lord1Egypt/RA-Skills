#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LABEL="com.symbolstar.openclaw.token-usage-refresh"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
[[ -f "$PLIST" ]] && { launchctl unload "$PLIST" 2>/dev/null || true; rm -f "$PLIST"; echo "✓ launchd removed"; }

ROOTS=()
if command -v npm >/dev/null 2>&1; then
  R="$(npm root -g 2>/dev/null || true)"; [[ -n "$R" && -d "$R/openclaw" ]] && ROOTS+=("$R/openclaw")
fi
for NVM_BASE in "$HOME/.nvm/versions/node" "/usr/local/n/versions/node"; do
  [[ -d "$NVM_BASE" ]] || continue
  while IFS= read -r d; do [[ -n "$d" ]] && ROOTS+=("$d"); done \
    < <(find "$NVM_BASE" -maxdepth 4 -path "*/lib/node_modules/openclaw" -type d 2>/dev/null)
done

for ROOT in "${ROOTS[@]:-}"; do
  for REL in "dist/control-ui" "ui/dist"; do
    BASE="$ROOT/$REL"
    ASSETS="$BASE/assets"
    INDEX="$BASE/index.html"
    [[ -d "$ASSETS" ]] || continue
    for BAK in "$ASSETS"/*.tk.bak; do
      [[ -f "$BAK" ]] || continue
      ORIG="${BAK%.tk.bak}"
      [[ "$ORIG" == *.tk-*.js ]] && ORIG_BASE="${ORIG%.tk-*}.js" || ORIG_BASE="$ORIG"
      mv "$BAK" "$ORIG_BASE"
      [[ "$ORIG" != "$ORIG_BASE" && -f "$ORIG" ]] && rm -f "$ORIG"
      echo "✓ restored $ORIG_BASE"
    done
    [[ -f "$INDEX.tk.bak" ]] && { mv "$INDEX.tk.bak" "$INDEX"; echo "✓ restored $INDEX"; }
    [[ -d "$BASE/data" ]] && rm -rf "$BASE/data" && echo "✓ removed $BASE/data"
  done
done
