#!/bin/bash
# Start the Appium bridge daemon (one-time setup)
# Usage: bash start_bridge.sh

set -e
echo "[*] Starting Appium bridge..."

# 1. Clean up all stale state.
# Kill only the daemon itself. A bare `pkill -f bridge_daemon` also matches any
# unrelated process whose command line merely contains that string, so match the
# script plus its --daemon flag, and never our own PID.
for pid in $(pgrep -f "bridge_daemon\.py --daemon" 2>/dev/null); do
    [ "$pid" = "$$" ] && continue
    kill "$pid" 2>/dev/null || true
done
rm -f ~/.cache/appium-bridge/bridge_cmd ~/.cache/appium-bridge/bridge_resp ~/.cache/appium-bridge/bridge.lock
sleep 1

# 2. Verify ADB connection
if ! adb devices | grep -q "device$"; then
    echo "[!] No ADB device connected. Check USB cable."
    exit 1
fi
echo "  [✓] ADB device found"

# 3. Start Appium if not running
if ! curl -s http://127.0.0.1:4723/status 2>/dev/null | grep -q '"ready":true'; then
    echo "[*] Starting Appium..."
    if [ -z "$ANDROID_HOME" ]; then
        for d in "$HOME/android-sdk" "$HOME/Library/Android/sdk" "/usr/lib/android-sdk"; do
            if [ -d "$d" ]; then export ANDROID_HOME="$d"; break; fi
        done
    fi
    export ANDROID_HOME="${ANDROID_HOME:-$HOME/android-sdk}"
    # No insecure features needed — the daemon only uses standard UiAutomator2
    # commands (find/click, mobile: clickGesture/scrollGesture).
    # --address 127.0.0.1: loopback only. Appium exposes full control of the
    # connected device; without this it binds broadly and any host on the LAN
    # could drive the phone.
    nohup appium --address 127.0.0.1 --log "$HOME/.cache/appium-bridge/appium.log" > /dev/null 2>&1 &
    sleep 4
fi

# 4. Verify Appium
if curl -s http://127.0.0.1:4723/status 2>/dev/null | grep -q '"ready":true'; then
    echo "  [✓] Appium running"
else
    echo "  [!] Appium failed to start"
    exit 1
fi

# 5. Start daemon (pre-warms session)
rm -f ~/.cache/appium-bridge/bridge_cmd ~/.cache/appium-bridge/bridge_resp
python3 ~/.openclaw/workspace/skills/appium-android-adb/bridge_daemon.py --daemon &
sleep 6  # Wait for daemon to create session

# 6. Test daemon with a quick dump
RESP=$(python3 ~/.openclaw/workspace/skills/appium-android-adb/bridge_daemon.py dump 2>/dev/null)
if echo "$RESP" | grep -q '"ok":true'; then
    echo "  [✓] Bridge daemon ready"
    echo "$RESP" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'     Package: {d[\"package\"]}')" 2>/dev/null
else
    echo "  [!] Daemon test failed: $RESP"
    echo "  [!] If the device blocks WRITE_SECURE_SETTINGS (Realme etc.), Appium"
    echo "      cannot work — use the OCR loop instead: ocr_bridge.py dump/tap-text/swipe"
    exit 1
fi

echo "[✓] Bridge is ready. Use bridge_daemon.py for all interactions."
