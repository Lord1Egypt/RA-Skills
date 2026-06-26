#!/bin/bash
# Grant required adb permissions to ClawPaw app
# Run after installing APK with USB connected

PKG="com.clawpaw.phonecontrol"

ADB=""
for path in \
  "$HOME/Library/Android/sdk/platform-tools/adb" \
  "/opt/homebrew/share/android-commandlinetools/platform-tools/adb" \
  "/usr/local/bin/adb" \
  "$(which adb 2>/dev/null)"; do
  if [ -x "$path" ]; then
    ADB="$path"
    break
  fi
done

if [ -z "$ADB" ]; then
  echo "ERROR: adb not found"
  exit 1
fi

echo "=== Granting ClawPaw permissions ==="

echo -n "[1/3] WRITE_SETTINGS (brightness control)... "
"$ADB" shell appops set $PKG WRITE_SETTINGS allow 2>/dev/null && echo "OK" || echo "FAILED"

echo -n "[2/3] WRITE_SECURE_SETTINGS (auto-enable accessibility)... "
"$ADB" shell pm grant $PKG android.permission.WRITE_SECURE_SETTINGS 2>/dev/null && echo "OK" || echo "FAILED"

echo -n "[3/3] adb tcpip 5555 (enable wireless ADB)... "
"$ADB" tcpip 5555 2>/dev/null && echo "OK" || echo "FAILED"

echo ""
echo "=== Done. Now open ClawPaw app and verify Connected + SSH: Connected ==="
