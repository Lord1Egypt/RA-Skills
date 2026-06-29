#!/bin/bash
# macOS/Linux - Start Chrome with remote debugging port 9222 (Independent profile, auto close port conflicts)
# NOTE: This script starts Chrome and exits immediately. Run health.py after 3 seconds to verify.

echo "Starting Chrome with remote debugging port 9222..."
echo "Mode: Independent profile (separate from main browser)"
echo ""

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
fi

# Set independent debug profile directory based on OS
if [[ "$OS" == "macos" ]]; then
    DEBUG_PROFILE="$HOME/Library/Application Support/Google/ChromeDebugProfile"
else
    DEBUG_PROFILE="$HOME/.config/chrome-debug-profile"
fi

# Create debug profile directory if not exists
if [ ! -d "$DEBUG_PROFILE" ]; then
    echo "[INFO] Creating debug profile directory: $DEBUG_PROFILE"
    mkdir -p "$DEBUG_PROFILE"
fi

# Check and close process occupying port 9222
echo ""
echo "[INFO] Checking 9222 port occupation..."
if command -v lsof >/dev/null 2>&1; then
    if lsof -Pi :9222 -sTCP:LISTEN -t >/dev/null 2>&1; then
        for pid in $(lsof -Pi :9222 -sTCP:LISTEN -t); do
            echo "[INFO] Found process PID occupying port 9222: $pid"
            echo "[INFO] Closing process $pid..."
            kill -9 $pid 2>/dev/null
            if [ $? -eq 0 ]; then
                echo "[SUCCESS] Process $pid has been closed"
            else
                echo "[WARNING] Unable to close process $pid"
            fi
        done
    fi
elif command -v netstat >/dev/null 2>&1; then
    # Linux fallback using netstat/fuser
    if command -v fuser >/dev/null 2>&1; then
        fuser -k 9222/tcp >/dev/null 2>&1
    fi
fi

# Brief wait for port release
sleep 1

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
        # Try mdfind
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
echo "[INFO] Debug profile: $DEBUG_PROFILE"

# Start Chrome with independent profile (non-blocking)
echo ""
echo "[INFO] Starting Chrome in background..."
nohup "$CHROME_PATH" \
    --remote-debugging-port=9222 \
    --user-data-dir="$DEBUG_PROFILE" \
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
