#!/bin/bash
# Validate EDID and check for common issues
# Usage: ./validate_edid.sh [edid-file-or-path]

# Default to first available HDMI EDID if no path provided
EDID_PATH="${1:-}"

if [ -z "$EDID_PATH" ]; then
    # Try to find first available EDID
    for path in /sys/class/drm/card*-HDMI-*-*/edid /sys/class/drm/card*-DP-*/edid; do
        if [ -f "$path" ] && [ -s "$path" ]; then
            EDID_PATH="$path"
            break
        fi
    done
fi

if [ -z "$EDID_PATH" ]; then
    echo "❌ No EDID found. Please specify path or connect a display."
    exit 1
fi

echo "=== EDID Validation: $EDID_PATH ==="
echo ""

# Check if file exists
if [ ! -e "$EDID_PATH" ]; then
    echo "❌ Error: $EDID_PATH does not exist"
    exit 1
fi

# Check if edid-decode is available
if ! command -v edid-decode &> /dev/null; then
    echo "❌ Error: edid-decode not installed"
    echo "   Install with: sudo apt-get install edid-decode"
    exit 1
fi

# Run edid-decode
output=$(edid-decode "$EDID_PATH" 2>&1)
exit_code=$?

echo "--- Validation Results ---"
echo ""

# Check for various issues
issues=0

# Check 1: Empty EDID
if [ ! -s "$EDID_PATH" ]; then
    echo "❌ FAIL: EDID is empty"
    echo "   → No display connected or monitor in sleep mode"
    issues=$((issues + 1))
else
    echo "✅ PASS: EDID has data"
fi

# Check 2: EDID decode errors
if [ $exit_code -ne 0 ]; then
    echo "❌ FAIL: EDID decode failed (exit code: $exit_code)"
    issues=$((issues + 1))
else
    echo "✅ PASS: EDID decodes without errors"
fi

# Check 3: Required fields
manufacturer=$(echo "$output" | grep "Manufacturer:" | head -1)
if [ -z "$manufacturer" ]; then
    echo "❌ FAIL: Missing manufacturer information"
    issues=$((issues + 1))
else
    echo "✅ PASS: Manufacturer found"
fi

model=$(echo "$output" | grep -E "(Model|Product Name):" | head -1)
if [ -z "$model" ]; then
    echo "❌ FAIL: Missing model information"
    issues=$((issues + 1))
else
    echo "✅ PASS: Model found"
fi

# Check 4: Preferred timing
preferred=$(echo "$output" | grep "Preferred timing" | head -1)
if [ -z "$preferred" ]; then
    echo "⚠️  WARNING: No preferred timing found"
    issues=$((issues + 1))
else
    echo "✅ PASS: Preferred timing defined"
fi

# Check 5: Audio support
if echo "$output" | grep -q "Basic audio support"; then
    echo "✅ INFO: Audio output supported"
else
    echo "ℹ️  INFO: No audio support"
fi

# Check 6: YCbCr support
if echo "$output" | grep -q "Supports YCbCr 4:4:4"; then
    echo "✅ INFO: YCbCr 4:4:4 supported"
fi
if echo "$output" | grep -q "Supports YCbCr 4:2:2"; then
    echo "✅ INFO: YCbCr 4:2:2 supported"
fi

# Check 7: DTD (Detailed Timing Descriptors)
dtd_count=$(echo "$output" | grep -c "DTD [0-9]:" || true)
if [ "$dtd_count" -gt 0 ]; then
    echo "✅ INFO: $dtd_count detailed timing descriptor(s) found"
else
    echo "⚠️  WARNING: No detailed timing descriptors"
    issues=$((issues + 1))
fi

# Summary
echo ""
echo "--- Summary ---"
if [ $issues -eq 0 ]; then
    echo "✅ EDID validation: PASSED"
    exit 0
else
    echo "⚠️  EDID validation: $issues issue(s) found"
    exit 1
fi