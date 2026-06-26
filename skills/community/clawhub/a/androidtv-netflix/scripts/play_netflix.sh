#!/bin/bash
# scripts/play_netflix.sh - Deep-link a Netflix title on Android TV via ADB

ANDROID_TV_IP="${ANDROID_TV_IP:-192.168.125.228}"
TITLE_ID=$1

if [ -z "$TITLE_ID" ]; then
    echo "Usage: ./play_netflix.sh <TITLE_ID>"
    exit 1
fi

# Step 1: Force-launch Netflix with a deep link
adb -s ${ANDROID_TV_IP}:5555 shell am start -n com.netflix.ninja/.MainActivity \
    -a android.intent.action.VIEW \
    -d "https://www.netflix.com/watch/${TITLE_ID}" \
    -f 0x10808000 -e source 30

# Step 2: Wait for Netflix to render
sleep 5

# Step 3: Send D-pad Center to start playback (in case it lands on the info page)
adb -s ${ANDROID_TV_IP}:5555 shell input keyevent 23
