#!/bin/bash
# Ganidhuz-FoxX: Check Firefox environment

echo "Checking Firefox environment..."

# Firefox binary
if command -v firefox &>/dev/null; then
    echo "OK: firefox binary found at $(command -v firefox)"
else
    echo "WARN: firefox not found in PATH"
fi

# X display
DISPLAY_CHECK="${DISPLAY:-:1}"
if xdpyinfo -display "$DISPLAY_CHECK" &>/dev/null 2>&1; then
    echo "OK: X display $DISPLAY_CHECK reachable"
else
    echo "WARN: X display $DISPLAY_CHECK not reachable"
fi

# Playwright
if python3 -c "import playwright" &>/dev/null 2>&1; then
    echo "OK: playwright Python package found"
else
    echo "WARN: playwright not installed. Run: pip install playwright && playwright install firefox"
fi

echo "Done."
