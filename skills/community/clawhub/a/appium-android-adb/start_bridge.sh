#!/bin/bash
# Start the Appium bridge daemon (one-time setup)
# Usage: bash start_bridge.sh

set -e
echo "[*] Starting Appium bridge..."

# 1. Clean up all stale state
pkill -f bridge_daemon 2>/dev/null || true
rm -f /tmp/bridge_cmd /tmp/bridge_resp /tmp/bridge.lock
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
    nohup appium --allow-insecure all --relaxed-security --log /tmp/appium.log > /dev/null 2>&1 &
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
rm -f /tmp/bridge_cmd /tmp/bridge_resp
python3 ~/.openclaw/workspace/skills/appium-android-adb/bridge_daemon.py --daemon &
sleep 6  # Wait for daemon to create session

# 6. Test daemon with a quick dump
RESP=$(python3 ~/.openclaw/workspace/skills/appium-android-adb/bridge_daemon.py dump 2>/dev/null)
if echo "$RESP" | grep -q '"ok":true'; then
    echo "  [✓] Bridge daemon ready"
    echo "$RESP" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'     Package: {d[\"package\"]}')" 2>/dev/null
else
    echo "  [!] Daemon test failed: $RESP"
    exit 1
fi

echo "[✓] Bridge is ready. Use bridge_daemon.py for all interactions."
