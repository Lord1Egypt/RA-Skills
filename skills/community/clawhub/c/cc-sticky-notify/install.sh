#!/bin/bash
# cc-sticky-notify install script (self-contained, no files need to be copied elsewhere)
# Usage: bash ~/.claude/skills/cc-sticky-notify/install.sh

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS_DIR="$SKILL_DIR/scripts"
SETTINGS="$HOME/.claude/settings.json"

echo "==> cc-sticky-notify installation started"
echo "    Skill dir: $SKILL_DIR"

# ── Dependency check: Xcode Command Line Tools ───────────────────────────────
# Covers swiftc (compile), codesign (sign), and python3 (session JSON parsing)
if ! xcode-select -p >/dev/null 2>&1; then
    echo "ERROR: Xcode Command Line Tools not found."
    echo "       Install with: xcode-select --install"
    echo "       Then re-run this script."
    exit 1
fi

# Ensure scripts are executable (git clone / file copy may strip +x bit)
chmod +x "$SCRIPTS_DIR/notify.sh"

# ── Step 1: build .app bundle ───────────────────────────────────────────────
APP_BUNDLE="$SCRIPTS_DIR/sticky-notify.app"
APP_BINARY="$APP_BUNDLE/Contents/MacOS/sticky-notify-app"

if [ -f "$APP_BINARY" ]; then
    echo "    [1/2] App bundle already exists, skipping compilation"
else
    echo "    [1/2] Compiling Swift floating window (~10-20 s)..."
    mkdir -p "$APP_BUNDLE/Contents/MacOS"
    swiftc "$SCRIPTS_DIR/sticky-window.swift" -o "$APP_BINARY"

    cat > "$APP_BUNDLE/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>sticky-notify-app</string>
    <key>CFBundleIdentifier</key>
    <string>com.cc-sticky-notify.app</string>
    <key>CFBundleName</key>
    <string>Sticky Notify</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
PLIST

    _ent="$SCRIPTS_DIR/sticky-notify.entitlements"
    cat > "$_ent" << 'ENTEOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <false/>
    <key>com.apple.security.automation.apple-events</key>
    <true/>
</dict>
</plist>
ENTEOF

    codesign --sign - --force --deep --timestamp=none --entitlements "$_ent" "$APP_BUNDLE" 2>/dev/null
    echo "          Built: $APP_BINARY"
fi

# ── Step 2: check settings.json hook configuration ──────────────────────────
NOTIFY_CMD="$HOME/.claude/skills/cc-sticky-notify/scripts/notify.sh"
if grep -q "cc-sticky-notify" "$SETTINGS" 2>/dev/null; then
    echo "    [2/2] cc-sticky-notify hook already configured in settings.json, skipping"
else
    echo "    [2/2] ⚠️  No hook configuration detected"
    echo ""
    echo "    Add the following to the hooks field in $SETTINGS,"
    echo "    or ask Claude Code to: install sticky notify hook configuration"
    echo ""
    echo "    Stop hook command: $NOTIFY_CMD"
    echo "    permission_prompt command: $NOTIFY_CMD '🔐 Permission approval required, check terminal'"
    echo "    idle_prompt command: $NOTIFY_CMD '💬 Awaiting your input, check terminal'"
fi

# ── Verify ───────────────────────────────────────────────────────────────────
echo ""
echo "==> Verifying installation..."
"$SCRIPTS_DIR/notify.sh" '✅ cc-sticky-notify installed successfully'
echo "    A yellow sticky note and system notification should appear in the top-right corner"
echo ""
echo "==> Installation complete! All files are in $SKILL_DIR"
