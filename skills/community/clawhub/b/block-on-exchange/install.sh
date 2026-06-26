#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "=== CalIn Installer ==="
echo

# Create virtualenv
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "Installing dependencies..."
"$VENV_DIR/bin/pip" install -q -r "$SCRIPT_DIR/requirements.txt"

echo "Dependencies installed."
echo

# Create data directory with restricted permissions
mkdir -m 700 -p ~/.calintegration

# Create .env template if it doesn't exist
ENV_FILE="$HOME/.calintegration/.env"
if [ ! -f "$ENV_FILE" ]; then
    touch "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    cat >> "$ENV_FILE" <<'ENVEOF'
# CalIn credentials — keep this file chmod 600
# CALINT_ICS_URL=
# CALINT_MS_CLIENT_ID=
# CALINT_MS_TENANT_ID=
ENVEOF
    echo "Created $ENV_FILE (chmod 600) — edit it with your credentials"
else
    echo "$ENV_FILE already exists"
fi

# Generate launchd plist with correct paths for this machine
PLIST_FILE="$SCRIPT_DIR/com.calintegration.sync.plist"
cat > "$PLIST_FILE" <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.calintegration.sync</string>

    <key>ProgramArguments</key>
    <array>
        <string>$VENV_DIR/bin/python</string>
        <string>$SCRIPT_DIR/main.py</string>
        <string>sync</string>
    </array>

    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>

    <key>StartInterval</key>
    <integer>300</integer>

    <key>StandardOutPath</key>
    <string>$HOME/.calintegration/sync.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/.calintegration/sync.err</string>

    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
PLISTEOF
echo "Generated plist with paths for this machine."
echo

echo "=== Next Steps ==="
echo "1. Edit credentials in $ENV_FILE:"
echo "   CALINT_ICS_URL=<your-ics-url>"
echo "   CALINT_MS_CLIENT_ID=<your-client-id>"
echo "   CALINT_MS_TENANT_ID=<your-tenant-id>"
echo "2. Run: $VENV_DIR/bin/python $SCRIPT_DIR/main.py setup"
echo "3. Run: $VENV_DIR/bin/python $SCRIPT_DIR/main.py sync"
echo
echo "To install as a launchd service (auto-sync every 5 min):"
echo "  cp $PLIST_FILE ~/Library/LaunchAgents/"
echo "  launchctl load ~/Library/LaunchAgents/com.calintegration.sync.plist"
