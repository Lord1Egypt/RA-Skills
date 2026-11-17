#!/usr/bin/env bash
# Build TarsX.app — a headless helper app so macOS Accessibility/Screen Recording
# permissions attach to a real .app bundle. Bare binaries (launchd node) never get
# the permission prompt; a bundle launched via LaunchServices does, and toggles stick.
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
APP="${TARSX_APP_DIR:-$HOME/Applications}/TarsX.app"
BUNDLE_ID="ai.topgemstoken.tarsx"

mkdir -p "$APP/Contents/MacOS"

cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key><string>$BUNDLE_ID</string>
    <key>CFBundleName</key><string>TarsX</string>
    <key>CFBundleExecutable</key><string>TarsX</string>
    <key>CFBundlePackageType</key><string>APPL</string>
    <key>CFBundleShortVersionString</key><string>1.0.3</string>
    <key>LSUIElement</key><true/>
    <key>NSAppleEventsUsageDescription</key><string>TarsX controls apps on your behalf (keystrokes, clicks, screenshots).</string>
</dict>
</plist>
PLIST

# Runner: launched via `open -W` (LaunchServices) with <task.json> <result.json>.
# Quoted heredoc — nothing here is expanded at build time.
cat > "$APP/Contents/MacOS/TarsX" <<'RUNNER'
#!/usr/bin/env bash
set -uo pipefail
IN="${1:-}"; OUT="${2:-}"
if [ -z "$IN" ] || [ -z "$OUT" ] || [ ! -f "$IN" ]; then
  printf '{"code":99,"stdout":"","stderr":"usage: TarsX <task.json> <result.json>"}' > "${OUT:-/tmp/tarsx-noout.json}"
  exit 1
fi
HERE="$(cd "$(dirname "$0")" && pwd)"
CLI="$HERE/cli.mjs"
NODE="$(command -v node || echo /usr/bin/node)"
python3 - "$IN" "$OUT" "$CLI" "$NODE" <<'PYEOF'
import json, subprocess, sys
inp, outp, cli, node = sys.argv[1:5]
task = json.load(open(inp))
argv = [str(a) for a in task.get("argv", [])]
try:
    r = subprocess.run([node, cli] + argv, capture_output=True, text=True, timeout=110)
    json.dump({"code": r.returncode, "stdout": r.stdout, "stderr": r.stderr}, open(outp, "w"))
except Exception as e:
    json.dump({"code": 98, "stdout": "", "stderr": str(e)}, open(outp, "w"))
PYEOF
RUNNER

chmod +x "$APP/Contents/MacOS/TarsX"
cp "$SRC_DIR/tarsx/cli.mjs" "$SRC_DIR/tarsx/core.mjs" "$APP/Contents/MacOS/"

codesign --force --deep -s - "$APP" 2>/dev/null || true

echo "built: $APP"
echo "if macOS asks, allow TarsX to control your computer (Accessibility); to add manually:"
echo "  System Settings → Privacy & Security → Accessibility → + → $APP"
