#!/bin/bash
# connect.sh — Setup and verify Android device connection
#
# Usage:
#   ./connect.sh          # Auto-detect USB device
#   ./connect.sh usb      # USB mode (explicit)
#   ./connect.sh wifi <ip> [port]  # WiFi/TCP mode (default port: 5555)
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Check ADB installed
if ! command -v adb &>/dev/null; then
    echo -e "${RED}❌ ADB not found.${NC}"
    echo "Install it:"
    echo "  macOS:  brew install android-platform-tools"
    echo "  Ubuntu: sudo apt install android-tools-adb"
    exit 1
fi

MODE="${1:-usb}"
WIFI_IP="${2:-}"
WIFI_PORT="${3:-5555}"

echo -e "${CYAN}📱 android-agent — Device Connection${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$MODE" = "wifi" ]; then
    if [ -z "$WIFI_IP" ]; then
        echo -e "${RED}❌ WiFi mode requires an IP address.${NC}"
        echo "Usage: ./connect.sh wifi 192.168.1.100"
        exit 1
    fi
    echo -e "${YELLOW}📡 Connecting to ${WIFI_IP}:${WIFI_PORT}...${NC}"
    adb connect "${WIFI_IP}:${WIFI_PORT}"
    sleep 2
fi

# List devices
echo ""
echo -e "${CYAN}Connected devices:${NC}"
adb devices -l
echo ""

# Get first available device
SERIAL=$(adb devices | grep -E 'device$' | head -1 | awk '{print $1}')
if [ -z "$SERIAL" ]; then
    echo -e "${RED}❌ No authorized device found.${NC}"
    echo "• Check USB cable (must be data cable, not charge-only)"
    echo "• Authorize computer on phone's USB debugging prompt"
    echo "• Try: adb kill-server && adb start-server"
    exit 1
fi

echo -e "${GREEN}✅ Device connected: ${SERIAL}${NC}"
echo ""

# Device info
MODEL=$(adb -s "$SERIAL" shell getprop ro.product.model 2>/dev/null || echo "unknown")
ANDROID=$(adb -s "$SERIAL" shell getprop ro.build.version.release 2>/dev/null || echo "unknown")
API=$(adb -s "$SERIAL" shell getprop ro.build.version.sdk 2>/dev/null || echo "unknown")
BATTERY=$(adb -s "$SERIAL" shell dumpsys battery 2>/dev/null | grep level | awk '{print $2}' || echo "?")

echo -e "📱 Model:   ${MODEL}"
echo -e "🤖 Android: ${ANDROID} (API ${API})"
echo -e "🔋 Battery: ${BATTERY}%"

# Check DroidRun Portal
if adb -s "$SERIAL" shell pm list packages 2>/dev/null | grep -q "droidrun"; then
    PORTAL_VER=$(adb -s "$SERIAL" shell dumpsys package com.droidrun.portal 2>/dev/null | grep versionName | head -1 | awk -F= '{print $2}' || echo "?")
    echo -e "📦 Portal:  ${GREEN}installed${NC} (v${PORTAL_VER})"
else
    echo -e "📦 Portal:  ${YELLOW}not found${NC} — install DroidRun Portal APK"
fi

echo ""
echo -e "${CYAN}To use this device:${NC}"
echo "  export ANDROID_SERIAL=\"${SERIAL}\""
echo "  python scripts/run-task.py \"Your task here\""
