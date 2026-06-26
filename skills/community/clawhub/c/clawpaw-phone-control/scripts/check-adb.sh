#!/bin/bash
# Check adb installation and device connectivity

ADB=""
# Search common locations
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
  echo "STATUS:NO_ADB"
  echo "adb not found. Install Android SDK Platform Tools:"
  echo "  brew install --cask android-platform-tools"
  echo "  or download from https://developer.android.com/tools/releases/platform-tools"
  exit 1
fi

echo "STATUS:ADB_FOUND:$ADB"

DEVICES=$("$ADB" devices 2>/dev/null | grep -v "List of devices" | grep "device$" | awk '{print $1}')
if [ -z "$DEVICES" ]; then
  echo "STATUS:NO_DEVICE"
  echo "No device connected via USB. Please:"
  echo "  1. Connect phone via USB cable"
  echo "  2. Enable Developer Options (tap Build Number 7 times)"
  echo "  3. Enable USB Debugging"
  echo "  4. Authorize this computer on the phone"
else
  echo "STATUS:DEVICE_FOUND:$DEVICES"
fi
