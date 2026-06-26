#!/usr/bin/env bash
# FaceTime Auto Call - Setup script
# Create NodeRunner.app and guide the user through Accessibility permission setup.

set -euo pipefail

echo "========================================="
echo "FaceTime Auto Call - Setup"
echo "========================================="
echo

if [ -d ~/Applications/NodeRunner.app ]; then
    echo "✅ NodeRunner.app already exists"
else
    echo "📦 Creating NodeRunner.app..."
    mkdir -p ~/Applications/NodeRunner.app/Contents/MacOS

    cat > ~/Applications/NodeRunner.app/Contents/MacOS/NodeRunner <<'EOF'
#!/bin/bash
exec /opt/homebrew/bin/node "$@"
EOF
    chmod +x ~/Applications/NodeRunner.app/Contents/MacOS/NodeRunner

    cat > ~/Applications/NodeRunner.app/Contents/Info.plist <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>NodeRunner</string>
    <key>CFBundleIdentifier</key>
    <string>com.openclaw.noderunner</string>
    <key>CFBundleName</key>
    <string>NodeRunner</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>
EOF

    echo "✅ NodeRunner.app created"
fi

echo
echo "Next: grant Accessibility permission"
echo "1. Open System Settings"
echo "2. Go to Privacy & Security → Accessibility"
echo "3. Add ~/Applications/NodeRunner.app"
echo "4. Enable it"
echo
echo "Test command:"
echo "  bash /path/to/facetime-auto-call/scripts/call.sh audio \"test@icloud.com\""
echo

open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
