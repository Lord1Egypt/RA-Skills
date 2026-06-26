#!/bin/bash
# List all available display outputs with EDID information
# Usage: ./list_outputs.sh

echo "=== Available Display Outputs ==="
echo ""

# Find all EDID files in /sys/class/drm
for edid_path in /sys/class/drm/card*-* /sys/class/drm/card*-*/*; do
    if [[ -f "$edid_path" && "$edid_path" == */edid ]]; then
        # Check if EDID has data
        if [ -s "$edid_path" ]; then
            # Extract connector name from path
            connector=$(basename $(dirname "$edid_path"))
            
            echo "📺 $connector"
            echo "   Path: $edid_path"
            
            # Try to decode and extract key info
            info=$(edid-decode "$edid_path" 2>/dev/null | head -30)
            
            manufacturer=$(echo "$info" | grep "Manufacturer:" | head -1)
            model=$(echo "$info" | grep -E "(Model|Product Name):" | head -1)
            timing=$(echo "$info" | grep "Preferred timing" | head -1)
            
            [ -n "$manufacturer" ] && echo "   $manufacturer"
            [ -n "$model" ] && echo "   $model"
            [ -n "$timing" ] && echo "   $timing"
            echo ""
        else
            connector=$(basename $(dirname "$edid_path"))
            echo "📺 $connector"
            echo "   Path: $edid_path"
            echo "   ⚠️  EDID is empty (no display connected or monitor in sleep mode)"
            echo ""
        fi
    fi
done

echo "=== Raw DRM devices ==="
ls -la /sys/class/drm/ | grep -E "^d" | grep -v "\." | head -20