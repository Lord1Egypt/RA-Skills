#!/bin/bash
# Parse EDID from file or sysfs path
# Usage: ./parse_edid.sh <edid-file-or-path>

if [ -z "$1" ]; then
    echo "Usage: $0 <edid-file-or-path>"
    echo "Example: $0 /sys/class/drm/card0-HDMI-A-1/edid"
    echo "Example: $0 /path/to/edid.bin"
    exit 1
fi

EDID_PATH="$1"

# Check if file/path exists
if [ ! -e "$EDID_PATH" ]; then
    echo "Error: $EDID_PATH does not exist"
    exit 1
fi

# Check if edid-decode is available
if ! command -v edid-decode &> /dev/null; then
    echo "Error: edid-decode not found. Install with: sudo apt-get install edid-decode"
    exit 1
fi

# Check if EDID has data
if [ ! -s "$EDID_PATH" ]; then
    echo "⚠️  EDID is empty (no data)"
    exit 1
fi

echo "=== EDID Decode: $EDID_PATH ==="
echo ""

# Decode and display
edid-decode "$EDID_PATH" 2>&1

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✅ EDID decode completed successfully"
else
    echo ""
    echo "⚠️  EDID decode completed with warnings/errors (exit code: $exit_code)"
fi