#!/usr/bin/env bash
# agent-token-usage · apply-ui.sh
# Inject the 📊 button into the OpenClaw Control UI header (optional UI part).
# CLI usage works without running this — just call scripts/agent_token_usage.py.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAYLOAD="$SKILL_DIR/scripts/token-usage-button.iife.js"
REFRESH="$SKILL_DIR/scripts/refresh-data.sh"
AGGREGATOR="$SKILL_DIR/scripts/agent_token_usage.py"
MARKER="__milly_token_usage_btn_v1__"

[[ -f "$PAYLOAD" ]] || { echo "✗ payload missing: $PAYLOAD" >&2; exit 2; }
[[ -f "$AGGREGATOR" ]] || { echo "✗ aggregator missing: $AGGREGATOR" >&2; exit 2; }

red()    { printf '\033[31m%s\033[0m\n' "$*"; }
green()  { printf '\033[32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }
dim()    { printf '\033[2m%s\033[0m\n' "$*"; }

CANDIDATES=()
[[ -n "${OPENCLAW_HOME:-}" && -d "$OPENCLAW_HOME" ]] && CANDIDATES+=("$OPENCLAW_HOME")
if command -v npm >/dev/null 2>&1; then
  R="$(npm root -g 2>/dev/null || true)"
  [[ -n "$R" && -d "$R/openclaw" ]] && CANDIDATES+=("$R/openclaw")
fi
for NVM_BASE in "$HOME/.nvm/versions/node" "/usr/local/n/versions/node"; do
  [[ -d "$NVM_BASE" ]] || continue
  while IFS= read -r d; do [[ -n "$d" ]] && CANDIDATES+=("$d"); done \
    < <(find "$NVM_BASE" -maxdepth 4 -path "*/lib/node_modules/openclaw" -type d 2>/dev/null)
done

DEDUPED=()
for R in "${CANDIDATES[@]:-}"; do
  skip=0
  for E in "${DEDUPED[@]:-}"; do [[ "$E" == "$R" ]] && { skip=1; break; }; done
  [[ $skip -eq 0 ]] && DEDUPED+=("$R")
done
CANDIDATES=("${DEDUPED[@]:-}")

[[ ${#CANDIDATES[@]} -eq 0 ]] && { red "✗ No OpenClaw install found."; exit 3; }

PATCHED_ANY=0
for ROOT in "${CANDIDATES[@]}"; do
  CAND_BASE=""
  for REL in "dist/control-ui" "ui/dist"; do
    [[ -d "$ROOT/$REL/assets" ]] && { CAND_BASE="$ROOT/$REL"; break; }
  done
  [[ -z "$CAND_BASE" ]] && continue
  ASSETS="$CAND_BASE/assets"
  INDEX_HTML="$CAND_BASE/index.html"

  ENTRY_NAME=""
  [[ -f "$INDEX_HTML" ]] && ENTRY_NAME="$(grep -oE 'src="[^"]*assets/index-[^"]*\.js"' "$INDEX_HTML" | head -n1 | sed 's|.*/||;s|"$||')"
  [[ -z "$ENTRY_NAME" ]] && continue
  DIST_JS="$ASSETS/$ENTRY_NAME"
  [[ -f "$DIST_JS" ]] || continue

  dim "→ openclaw root: $ROOT"
  dim "→ entry bundle:  $DIST_JS"

  if grep -q "$MARKER" "$DIST_JS"; then
    green "✓ Already patched at $ROOT."
  else
    [[ -f "$DIST_JS.tk.bak" ]] || cp "$DIST_JS" "$DIST_JS.tk.bak"
    { printf '\n;/* milly:token-usage-btn v0.2 */\n'; cat "$PAYLOAD"; } >> "$DIST_JS"
    if ! grep -q "$MARKER" "$DIST_JS"; then
      red "✗ Patch append failed, restoring."
      cp "$DIST_JS.tk.bak" "$DIST_JS"; continue
    fi
    if [[ -f "$INDEX_HTML" && "$ENTRY_NAME" != *.tk-*.js ]]; then
      BUST="tk-$(date +%s | tail -c 6)"
      NEW_NAME="${ENTRY_NAME%.js}.${BUST}.js"
      mv "$DIST_JS" "$ASSETS/$NEW_NAME"
      [[ -f "$DIST_JS.tk.bak" ]] && mv "$DIST_JS.tk.bak" "$ASSETS/$NEW_NAME.tk.bak"
      [[ -f "$INDEX_HTML.tk.bak" ]] || cp "$INDEX_HTML" "$INDEX_HTML.tk.bak"
      sed -i.tmp "s|$ENTRY_NAME|$NEW_NAME|g" "$INDEX_HTML" && rm -f "$INDEX_HTML.tmp"
      green "✓ Patched + cache-busted: $ENTRY_NAME → $NEW_NAME"
    fi
  fi

  DATA_DIR="$CAND_BASE/data"
  mkdir -p "$DATA_DIR"
  python3 "$AGGREGATOR" --format json > "$DATA_DIR/agent-token-usage.json.tmp" 2>/dev/null \
    && mv "$DATA_DIR/agent-token-usage.json.tmp" "$DATA_DIR/agent-token-usage.json" \
    && green "✓ Initial data: $DATA_DIR/agent-token-usage.json" \
    || yellow "⚠ Failed to write initial data."

  PATCHED_ANY=1
done

[[ $PATCHED_ANY -eq 0 ]] && { red "✗ No Control UI dist found."; exit 3; }

if [[ "$OSTYPE" == "darwin"* ]]; then
  LABEL="com.symbolstar.openclaw.token-usage-refresh"
  PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
  mkdir -p "$HOME/Library/LaunchAgents" "$HOME/.openclaw/logs"
  cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>$REFRESH</string></array>
  <key>StartInterval</key><integer>300</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>$HOME/.openclaw/logs/token-usage-refresh.log</string>
  <key>StandardErrorPath</key><string>$HOME/.openclaw/logs/token-usage-refresh.err.log</string>
</dict>
</plist>
EOF
  launchctl unload "$PLIST" 2>/dev/null || true
  launchctl load "$PLIST" && green "✓ launchd job installed (refreshes every 5min): $LABEL"
fi

dim "  Refresh your Control UI tab. 📊 button appears next to Search."
dim "  Disable per browser: localStorage.setItem('milly.tokenUsageBtn', 'off')"
