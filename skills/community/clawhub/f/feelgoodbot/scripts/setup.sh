#!/bin/bash
# feelgoodbot setup script
# Installs feelgoodbot and configures Clawdbot webhook integration

set -e

echo "🛡️ Setting up feelgoodbot..."

# Check for Go
if ! command -v go &> /dev/null; then
    echo "❌ Go is required. Install with: brew install go"
    exit 1
fi

# Install feelgoodbot
echo "📦 Installing feelgoodbot..."
go install github.com/kris-hansen/feelgoodbot/cmd/feelgoodbot@latest

# Check if it installed
if ! command -v feelgoodbot &> /dev/null; then
    echo "❌ feelgoodbot not found in PATH. Add \$GOPATH/bin to your PATH"
    exit 1
fi

# Initialize if no baseline exists
if [ ! -f ~/.config/feelgoodbot/snapshots/baseline.json ]; then
    echo "📸 Creating initial baseline..."
    feelgoodbot init
else
    echo "✓ Baseline already exists"
fi

# Get Clawdbot hooks token
HOOKS_ENABLED=$(clawdbot config get hooks.enabled 2>/dev/null | tr -d '"' || echo "false")

if [ "$HOOKS_ENABLED" != "true" ]; then
    echo "⚙️ Enabling Clawdbot webhooks..."
    clawdbot config set hooks.enabled true
    TOKEN=$(openssl rand -base64 32)
    clawdbot config set hooks.token "$TOKEN"
    clawdbot gateway restart
    sleep 2
else
    echo "✓ Clawdbot webhooks already enabled"
fi

# Get token
TOKEN=$(clawdbot config get hooks.token 2>/dev/null | tr -d '"')

if [ -z "$TOKEN" ]; then
    echo "❌ Could not get hooks token"
    exit 1
fi

# Create config
CONFIG_DIR=~/.config/feelgoodbot
mkdir -p "$CONFIG_DIR"

cat > "$CONFIG_DIR/config.yaml" << EOF
# feelgoodbot configuration
scan_interval: 5m

alerts:
  clawdbot:
    enabled: true
    webhook: "http://127.0.0.1:18789/hooks/wake"
    secret: "$TOKEN"
  local_notification: true

response:
  on_critical:
    - alert
  on_warning:
    - alert
  on_info:
    - log
EOF

echo "✓ Config written to $CONFIG_DIR/config.yaml"

# Install and start daemon
echo "🚀 Installing daemon..."
feelgoodbot daemon install 2>/dev/null || true
feelgoodbot daemon stop 2>/dev/null || true
feelgoodbot daemon start

echo ""
echo "✅ feelgoodbot is running!"
echo ""
echo "Commands:"
echo "  feelgoodbot status    - Check status"
echo "  feelgoodbot scan      - Run manual scan"
echo "  feelgoodbot diff      - Show changes"
echo "  feelgoodbot snapshot  - Update baseline"
