#!/bin/bash
# async-queue install script
# Sets up the queue daemon + queue-wake plugin for any OpenClaw user on macOS.
#
# What this does:
#   1. Installs daemon.js + push.js to ~/.openclaw/queue/
#   2. Installs the queue-wake plugin to ~/.openclaw/extensions/queue-wake/
#   3. Registers the daemon under launchd (auto-starts on login)
#
# Run: bash scripts/install.sh

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
QUEUE_DIR="$HOME/.openclaw/queue"
PLUGIN_DIR="$HOME/.openclaw/extensions/queue-wake"
PLIST="$HOME/Library/LaunchAgents/ai.openclaw.queue-daemon.plist"

echo "🔧 Installing async-queue..."
echo ""

# ── 1. Queue daemon ──────────────────────────────────────────────────────────
echo "  → Creating queue directory: $QUEUE_DIR"
mkdir -p "$QUEUE_DIR"

echo "  → Copying daemon.js and push.js"
cp "$SKILL_DIR/scripts/daemon.js" "$QUEUE_DIR/daemon.js"
cp "$SKILL_DIR/scripts/push.js"   "$QUEUE_DIR/push.js"

# Initialize empty queue if it doesn't exist
if [ ! -f "$QUEUE_DIR/queue.json" ]; then
  echo '[]' > "$QUEUE_DIR/queue.json"
  echo "  → Initialized empty queue.json"
fi

# ── 2. queue-wake plugin ─────────────────────────────────────────────────────
echo "  → Installing queue-wake plugin to: $PLUGIN_DIR"
mkdir -p "$PLUGIN_DIR"
cp "$SKILL_DIR/plugin/index.ts"                "$PLUGIN_DIR/index.ts"
cp "$SKILL_DIR/plugin/openclaw.plugin.json"    "$PLUGIN_DIR/openclaw.plugin.json"
echo "  → Plugin installed. Reload OpenClaw (or run: openclaw gateway restart) to activate."

# ── 3. launchd plist ─────────────────────────────────────────────────────────
echo "  → Installing launchd plist: $PLIST"
cat > "$PLIST" <<PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.openclaw.queue-daemon</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/env</string>
    <string>node</string>
    <string>${QUEUE_DIR}/daemon.js</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>${QUEUE_DIR}/daemon.log</string>
  <key>StandardErrorPath</key>
  <string>${QUEUE_DIR}/daemon.log</string>
</dict>
</plist>
PLIST_EOF

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo ""
echo "✅ async-queue installed and running!"
echo ""
echo "  Queue file:  $QUEUE_DIR/queue.json"
echo "  Daemon log:  $QUEUE_DIR/daemon.log"
echo "  Plugin:      $PLUGIN_DIR/"
echo ""
echo "Usage:"
echo "  node $QUEUE_DIR/push.js --to main --task \"your task\" --delay 30m"
echo ""
echo "⚠️  Remember to restart OpenClaw gateway to load the queue-wake plugin:"
echo "  openclaw gateway restart"
