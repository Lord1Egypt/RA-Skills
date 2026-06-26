#!/bin/bash
#
# EkyBot Connector — Full Automated Setup
#
# This script handles the complete onboarding:
# 1. Copies bundled runtime files (no git clone needed)
# 2. Installs npm dependencies
# 3. Prompts for enrollment token (or uses env var)
# 4. Runs companion:connect
# 5. Runs companion:doctor to verify
# 6. Optionally installs the background daemon
#
# Usage:
#   bash <SKILL_DIR>/scripts/setup.sh                          # interactive
#   EKYBOT_ENROLLMENT_TOKEN=ekrt_... bash <SKILL_DIR>/scripts/setup.sh  # non-interactive
#

set -e

# Resolve the skill directory (where this script lives)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
RUNTIME_DIR="$SKILL_DIR/runtime"
CONNECTOR_DIR="${EKYBOT_CONNECTOR_DIR:-$HOME/.openclaw/ekybot-connector}"
APP_URL="${EKYBOT_APP_URL:-https://www.ekybot.com}"

echo ""
echo "🚀 EkyBot Connector — Automated Setup"
echo "======================================="
echo ""

# ── Step 0: Check prerequisites ─────────────────────────────────────
echo "🔍 Checking prerequisites..."
MISSING=""
if ! command -v node &>/dev/null; then
    MISSING="$MISSING node"
fi
if ! command -v npm &>/dev/null; then
    MISSING="$MISSING npm"
fi
if [ -n "$MISSING" ]; then
    echo "❌ Missing required tools:$MISSING"
    echo ""
    echo "   Install them first:"
    echo "   • node: https://nodejs.org/ or use nvm"
    echo "   • npm:  comes with node"
    exit 1
fi

NODE_MAJOR=$(node -e "console.log(process.versions.node.split('.')[0])")
if [ "$NODE_MAJOR" -lt 18 ]; then
    echo "❌ Node.js >= 18 required (found: $(node --version))"
    exit 1
fi
echo "✅ node $(node --version), npm $(npm --version)"
echo ""

# ── Step 1: Copy bundled runtime ─────────────────────────────────────
if [ ! -d "$RUNTIME_DIR" ] || [ ! -f "$RUNTIME_DIR/package.json" ]; then
    echo "❌ Bundled runtime not found at $RUNTIME_DIR"
    echo "   The skill package appears incomplete. Re-install from ClawHub:"
    echo "   clawhub install ekybot-connector"
    exit 1
fi

if [ -d "$CONNECTOR_DIR" ] && [ -f "$CONNECTOR_DIR/package.json" ]; then
    echo "✅ Connector directory already exists at $CONNECTOR_DIR"
    echo "   Updating with bundled runtime files..."
    # Backup config if present
    if [ -f "$CONNECTOR_DIR/.env.ekybot_companion" ]; then
        cp "$CONNECTOR_DIR/.env.ekybot_companion" /tmp/ekybot_companion.env.bak
        echo "   📋 Backed up .env.ekybot_companion to /tmp/"
    fi
else
    echo "📦 Installing connector runtime..."
    mkdir -p "$CONNECTOR_DIR"
fi

# Copy bundled files (preserve existing .env config)
cp -r "$RUNTIME_DIR/src" "$CONNECTOR_DIR/"
cp -r "$RUNTIME_DIR/scripts" "$CONNECTOR_DIR/"
cp "$RUNTIME_DIR/package.json" "$CONNECTOR_DIR/"
cp "$RUNTIME_DIR/.env.example" "$CONNECTOR_DIR/" 2>/dev/null || true

# Restore config if backed up
if [ -f /tmp/ekybot_companion.env.bak ]; then
    cp /tmp/ekybot_companion.env.bak "$CONNECTOR_DIR/.env.ekybot_companion"
    echo "   📋 Restored .env.ekybot_companion from backup"
fi

cd "$CONNECTOR_DIR"
echo "✅ Runtime installed to $CONNECTOR_DIR"
echo ""

# ── Step 2: Install dependencies ────────────────────────────────────
echo "📦 Installing dependencies..."
npm install --production --ignore-scripts 2>&1 | tail -3
echo "✅ Dependencies installed"
echo ""

# ── Step 3: Get enrollment token ────────────────────────────────────
TOKEN="${EKYBOT_ENROLLMENT_TOKEN:-}"

if [ -z "$TOKEN" ] && [ ! -f "$CONNECTOR_DIR/.env.ekybot_companion" ]; then
    echo "🔑 You need a temporary enrollment token from EkyBot."
    echo ""
    echo "   1. Go to: $APP_URL/companion"
    echo "   2. Click 'Generate enrollment token'"
    echo "   3. Copy the token (starts with ekrt_)"
    echo ""
    read -r -p "   Paste your enrollment token: " TOKEN
    echo ""
fi

if [ -z "$TOKEN" ] && [ ! -f "$CONNECTOR_DIR/.env.ekybot_companion" ]; then
    echo "❌ No enrollment token provided. Aborting."
    echo "   Run again with: EKYBOT_ENROLLMENT_TOKEN=ekrt_... $0"
    exit 1
fi

# Skip enrollment if already connected
if [ -f "$CONNECTOR_DIR/.env.ekybot_companion" ] && [ -z "$TOKEN" ]; then
    echo "✅ Already enrolled (existing .env.ekybot_companion found)"
else
    # ── Step 4: Connect ─────────────────────────────────────────────
    echo "🔗 Connecting to EkyBot..."
    EKYBOT_APP_URL="$APP_URL" \
    EKYBOT_COMPANION_REGISTRATION_TOKEN="$TOKEN" \
      npm run companion:connect 2>&1
fi
echo ""

# ── Step 5: Doctor check ────────────────────────────────────────────
echo "🩺 Running health check..."
npm run companion:doctor 2>&1
echo ""

# ── Step 6: Daemon ──────────────────────────────────────────────────
INSTALL_DAEMON="${EKYBOT_INSTALL_DAEMON:-}"

if [ -z "$INSTALL_DAEMON" ]; then
    read -r -p "🔄 Install background daemon for 24/7 operation? [y/N] " INSTALL_DAEMON
fi

case "$INSTALL_DAEMON" in
    [yY]|[yY][eE][sS])
        echo ""
        echo "📦 Installing background daemon..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            npm run companion:install-launchd 2>&1
            echo "✅ macOS LaunchAgent installed"
        else
            echo "   Starting daemon in background..."
            mkdir -p "$HOME/.openclaw/logs"
            nohup npm run companion:daemon > "$HOME/.openclaw/logs/ekybot-companion.log" 2>&1 &
            echo "✅ Daemon started (PID: $!)"
            echo "   Logs: $HOME/.openclaw/logs/ekybot-companion.log"
        fi
        ;;
    *)
        echo "   Skipped daemon install. Start manually with:"
        echo "   cd $CONNECTOR_DIR && npm run companion:daemon"
        ;;
esac

# ── Step 7: Verify daemon is running ─────────────────────────────────
echo ""
echo "🔍 Verifying daemon is running..."
sleep 3
if pgrep -f companion-daemon > /dev/null 2>&1; then
    echo "✅ Daemon is running (PID: $(pgrep -f companion-daemon | head -1))"
else
    echo "⚠️  Daemon does NOT appear to be running!"
    echo "   Starting it now..."
    mkdir -p "$HOME/.openclaw/logs"
    nohup node scripts/companion-daemon.js > "$HOME/.openclaw/logs/ekybot-companion.log" 2>&1 &
    sleep 3
    if pgrep -f companion-daemon > /dev/null 2>&1; then
        echo "✅ Daemon started (PID: $(pgrep -f companion-daemon | head -1))"
    else
        echo "❌ Daemon failed to start. Check logs:"
        echo "   tail -20 $HOME/.openclaw/logs/ekybot-companion.log"
        echo ""
        echo "   ⛔ Installation is INCOMPLETE — the daemon must be running for Ekybot to work."
        exit 1
    fi
fi

echo ""
echo "════════════════════════════════════════"
echo "✅ Setup complete!"
echo ""
echo "📱 TEST IT NOW (installation is NOT done until this works):"
echo "   1. Open $APP_URL on your phone or browser"
echo "   2. Send @YourAgent test in any channel"
echo "   3. You should get a SINGLE reply within 30 seconds"
echo "   4. If no reply → run: cd $CONNECTOR_DIR && npm run companion:doctor"
echo ""
echo "📂 Connector: $CONNECTOR_DIR"
echo "🔧 Config:    $CONNECTOR_DIR/.env.ekybot_companion"
echo "📋 Logs:      $HOME/.openclaw/logs/ekybot-companion.log"
echo "🔄 Update:    Re-run this setup script after updating the skill"
echo "════════════════════════════════════════"
