#!/bin/bash
# macOS/Linux - Start Chrome with remote debugging port 9222 (Reuse main profile, will close existing windows)
# NOTE: This script starts Chrome and exits immediately. Run health.py after 3 seconds to verify.

echo "Starting Chrome with remote debugging port 9222..."
echo "Mode: Reuse main profile (WILL CLOSE all existing Chrome windows)"
echo ""
echo "WARNING: This will close all existing Chrome windows!"
echo ""

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
fi

# Check and close process occupying port 9222
echo "[INFO] Checking 9222 port occupation..."
if command -v lsof >/dev/null 2>&1; then
    if lsof -Pi :9222 -sTCP:LISTEN -t >/dev/null 2>&1; then
        for pid in $(lsof -Pi :9222 -sTCP:LISTEN -t); do
            echo "[INFO] Found process PID occupying port 9222: $pid"
            echo "[INFO] Closing process $pid..."
            kill -9 $pid 2>/dev/null
        done
    fi
fi

# Close all existing Chrome instances
echo "[INFO] Closing all Chrome processes..."
if [[ "$OS" == "macos" ]]; then
    pkill -f "Google Chrome" 2>/dev/null
else
    pkill -f "chrome" 2>/dev/null
    pkill -f "google-chrome" 2>/dev/null
fi

# Wait briefly for processes to terminate
sleep 2

echo ""

# Auto-find Chrome path
CHROME_PATH=""

if [[ "$OS" == "macos" ]]; then
    # macOS Chrome paths
    if [ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
        CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif [ -f "$HOME/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
        CHROME_PATH="$HOME/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    else
        CHROME_APP=$(mdfind "kMDItemCFBundleIdentifier == 'com.google.Chrome'" 2>/dev/null | head -n 1)
        if [ -n "$CHROME_APP" ] && [ -f "$CHROME_APP/Contents/MacOS/Google Chrome" ]; then
            CHROME_PATH="$CHROME_APP/Contents/MacOS/Google Chrome"
        fi
    fi
else
    # Linux Chrome paths
    for cmd in google-chrome google-chrome-stable chromium chromium-browser chrome; do
        if command -v "$cmd" >/dev/null 2>&1; then
            CHROME_PATH=$(command -v "$cmd")
            break
        fi
    done
    
    # Check common paths
    if [ -z "$CHROME_PATH" ]; then
        for path in \
            "/usr/bin/google-chrome" \
            "/usr/bin/google-chrome-stable" \
            "/usr/bin/chromium" \
            "/usr/bin/chromium-browser" \
            "/opt/google/chrome/chrome" \
            "/snap/bin/chromium"; do
            if [ -f "$path" ]; then
                CHROME_PATH="$path"
                break
            fi
        done
    fi
fi

# Check if Chrome was found
if [ -z "$CHROME_PATH" ] || [ ! -f "$CHROME_PATH" ]; then
    echo "[ERROR] Chrome browser not found."
    echo ""
    echo "Please make sure Google Chrome browser is installed."
    exit 1
fi

echo "[INFO] Chrome path: $CHROME_PATH"

# Start Chrome (non-blocking)
echo ""
echo "[INFO] Starting Chrome in background..."
nohup "$CHROME_PATH" \
    --remote-debugging-port=9222 \
    --no-first-run \
    --no-default-browser-check >/dev/null 2>&1 &

echo ""
echo "========================================"
echo "[INFO] Chrome launch command executed"
echo "[INFO] Debug port: 9222"
echo "[INFO] Endpoint: http://127.0.0.1:9222"
echo "========================================"
echo ""
echo "IMPORTANT: Wait 3 seconds then run health.py to verify"
echo ""
exit 0
