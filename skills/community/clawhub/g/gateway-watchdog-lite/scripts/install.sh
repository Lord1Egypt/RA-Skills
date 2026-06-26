#!/bin/bash
# install.sh — Install the Gateway Watchdog Lite LaunchAgent (macOS)
#
# Usage:
#   WORKSPACE_PATH=/your/workspace OC_PORT=18789 TELEGRAM_ID=your_id bash install.sh
#
# Parameters:
#   WORKSPACE_PATH  — Path to OpenClaw workspace  (run `openclaw status` to find it)
#   OC_PORT         — Gateway port to probe        (usually 18789)
#   TELEGRAM_ID     — Your Telegram user ID        (message @userinfobot, or "" to disable)
#
# Supplied by ConfusedUser.com — OpenClaw tools & skills
# Full version with crash loop detection: https://confuseduser.com

set -euo pipefail

WORKSPACE_PATH="${WORKSPACE_PATH:-}"
OC_PORT="${OC_PORT:-}"
TELEGRAM_ID="${TELEGRAM_ID:-}"

if [ -z "$WORKSPACE_PATH" ] || [ -z "$OC_PORT" ]; then
    echo "ERROR: Missing required parameters."
    echo ""
    echo "Usage:"
    echo "  WORKSPACE_PATH=/your/workspace OC_PORT=18789 TELEGRAM_ID=your_id bash install.sh"
    exit 1
fi

SCRIPTS_DIR="$WORKSPACE_PATH/scripts"
WATCHDOG_SCRIPT="$SCRIPTS_DIR/gateway-watchdog-lite.sh"
PLIST_PATH="$HOME/Library/LaunchAgents/ai.openclaw.gateway-watchdog.plist"
LABEL="ai.openclaw.gateway-watchdog"

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> Installing Gateway Watchdog Lite"
echo "    WORKSPACE_PATH : $WORKSPACE_PATH"
echo "    OC_PORT        : $OC_PORT"
echo "    TELEGRAM_ID    : ${TELEGRAM_ID:-"(disabled)"}"

# 1. Copy + patch watchdog script
mkdir -p "$SCRIPTS_DIR"
cp "$SKILL_DIR/scripts/gateway-watchdog.sh" "$WATCHDOG_SCRIPT"
chmod +x "$WATCHDOG_SCRIPT"

sed -i '' "s|PROBE_URL=\"http://127.0.0.1:YOUR_OC_PORT\"|PROBE_URL=\"http://127.0.0.1:${OC_PORT}\"|g" "$WATCHDOG_SCRIPT"
sed -i '' "s|YOUR_TELEGRAM_ID|${TELEGRAM_ID}|g" "$WATCHDOG_SCRIPT"
echo "[OK] Watchdog script installed to $WATCHDOG_SCRIPT"

# 2. Write LaunchAgent plist
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST_PATH" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>${LABEL}</string>
    <key>Comment</key>
    <string>OpenClaw Gateway Watchdog Lite — auto-recovers gateway if down</string>
    <key>RunAtLoad</key>
    <false/>
    <key>StartInterval</key>
    <integer>120</integer>
    <key>ProgramArguments</key>
    <array>
      <string>/bin/bash</string>
      <string>${WATCHDOG_SCRIPT}</string>
    </array>
    <key>StandardOutPath</key>
    <string>/tmp/openclaw/gateway-watchdog.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/openclaw/gateway-watchdog-err.log</string>
    <key>EnvironmentVariables</key>
    <dict>
      <key>HOME</key>
      <string>${HOME}</string>
      <key>PATH</key>
      <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
  </dict>
</plist>
PLIST
echo "[OK] LaunchAgent plist written to $PLIST_PATH"

# 3. Bootstrap
launchctl bootout "gui/$UID/$LABEL" 2>/dev/null || true
sleep 1

if launchctl bootstrap "gui/$UID" "$PLIST_PATH" 2>/dev/null; then
    echo "[OK] LaunchAgent bootstrapped"
    echo ""
    echo "==> Installation complete!"
    echo "    Watchdog probes gateway every 2 minutes."
    echo "    Verify:  launchctl list | grep watchdog"
    echo "    Logs:    tail -f /tmp/openclaw/gateway-watchdog.log"
else
    echo "[FAIL] launchctl bootstrap failed — try: launchctl bootstrap gui/\$UID $PLIST_PATH"
    exit 1
fi
