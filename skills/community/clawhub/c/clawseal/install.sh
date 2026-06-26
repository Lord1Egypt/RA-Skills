#!/bin/bash
set -e

echo "🔐 Installing ClawSeal OpenClaw Plugin..."

# Check dependencies
command -v python3 >/dev/null 2>&1 || { echo "❌ python3 required"; exit 1; }
command -v pip >/dev/null 2>&1 || { echo "❌ pip required"; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "❌ curl required"; exit 1; }

# Install ClawSeal from PyPI
echo "📦 Installing ClawSeal Python package..."
pip install clawseal>=1.1.3

# Install Flask dependencies
echo "📦 Installing Flask server dependencies..."
pip install -r backend/requirements.txt

# Verify installation
echo "🔍 Verifying ClawSeal installation..."
python3 -c "from clawseal import ScrollMemoryStore; print('✅ ClawSeal import OK')" || {
    echo "❌ ClawSeal import failed"
    exit 1
}

# Run clawseal verify
echo "🔍 Running ClawSeal verification..."
clawseal verify || echo "⚠️  Verification warnings (non-fatal)"

# Create scrolls directory
mkdir -p clawseal_scrolls

# Detect OS and register auto-start daemon
OS=$(uname)

if [ "$OS" = "Darwin" ]; then
    echo "🍎 Detected macOS — Registering launchd service..."

    # Create launchd plist
    PLIST_PATH="$HOME/Library/LaunchAgents/com.mvar.clawseal.plist"
    PLUGIN_DIR="$(pwd)"

    cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mvar.clawseal</string>
    <key>ProgramArguments</key>
    <array>
        <string>$(which python3)</string>
        <string>$PLUGIN_DIR/backend/clawseal_server.py</string>
        <string>--port</string>
        <string>5002</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$PLUGIN_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$HOME/Library/Logs/clawseal-server.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/Library/Logs/clawseal-server-error.log</string>
</dict>
</plist>
EOF

    # Load service
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
    launchctl load "$PLIST_PATH"

    echo "✅ launchd service registered: $PLIST_PATH"
    echo "📂 Logs: ~/Library/Logs/clawseal-server.log"
    echo "🔄 Service auto-starts on boot and restarts on failure"

elif [ "$OS" = "Linux" ]; then
    echo "🐧 Detected Linux — Registering systemd service..."

    # Create systemd unit file
    UNIT_FILE="$HOME/.config/systemd/user/clawseal-server.service"
    PLUGIN_DIR="$(pwd)"

    mkdir -p "$HOME/.config/systemd/user"

    cat > "$UNIT_FILE" <<EOF
[Unit]
Description=ClawSeal OpenClaw Server
After=network.target

[Service]
Type=simple
WorkingDirectory=$PLUGIN_DIR
ExecStart=$(which python3) $PLUGIN_DIR/backend/clawseal_server.py --port 5002
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
EOF

    # Reload systemd and enable service
    systemctl --user daemon-reload
    systemctl --user enable clawseal-server.service
    systemctl --user start clawseal-server.service

    echo "✅ systemd service registered: $UNIT_FILE"
    echo "📂 Logs: journalctl --user -u clawseal-server -f"
    echo "🔄 Service auto-starts on boot and restarts on failure"

else
    echo "⚠️  Unknown OS ($OS) — Skipping auto-start daemon registration"
    echo "   Start server manually: python3 backend/clawseal_server.py"
fi

# Wait for server to start
sleep 2

# Test health endpoint
echo "🔍 Testing server health..."
if curl -s http://localhost:5002/health | grep -q "ok"; then
    echo "✅ ClawSeal server is running!"
else
    echo "⚠️  Server not responding yet. Check logs:"
    if [ "$OS" = "Darwin" ]; then
        echo "   tail -f ~/Library/Logs/clawseal-server.log"
    elif [ "$OS" = "Linux" ]; then
        echo "   journalctl --user -u clawseal-server -f"
    fi
fi

echo ""
echo "✅ ClawSeal OpenClaw plugin installed successfully!"
echo ""
echo "Next steps:"
echo "  1. Server is running: http://localhost:5002"
echo "  2. Test health: curl http://localhost:5002/health"
echo "  3. Run demo: See demo_conversation.md"
echo ""
if [ "$OS" = "Darwin" ]; then
    echo "Manage service:"
    echo "  Stop:  launchctl unload ~/Library/LaunchAgents/com.mvar.clawseal.plist"
    echo "  Start: launchctl load ~/Library/LaunchAgents/com.mvar.clawseal.plist"
elif [ "$OS" = "Linux" ]; then
    echo "Manage service:"
    echo "  Stop:  systemctl --user stop clawseal-server"
    echo "  Start: systemctl --user start clawseal-server"
    echo "  Logs:  journalctl --user -u clawseal-server -f"
fi
