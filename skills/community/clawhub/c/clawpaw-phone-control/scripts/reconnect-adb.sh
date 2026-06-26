#!/bin/bash
# Reconnect adb after Pod restart (no USB needed, SSH tunnel must be active)
# Usage: ./reconnect-adb.sh <uid> <secret>

UID="$1"
SECRET="$2"
BACKEND="https://www.clawpaw.me"

if [ -z "$UID" ] || [ -z "$SECRET" ]; then
  echo "Usage: $0 <uid> <secret>"
  exit 1
fi

echo -n "Connecting adb via SSH tunnel... "
RESULT=$(curl -sk -X POST "$BACKEND/api/adb/connect" \
  -H "Content-Type: application/json" \
  -H "x-clawpaw-secret: $SECRET" \
  -d "{\"uid\":\"$UID\"}")

echo "$RESULT"

if echo "$RESULT" | grep -q "already connected\|connected to"; then
  echo ""
  echo "OK — testing with press_key home..."
  curl -sk -X POST "$BACKEND/api/adb/press_key" \
    -H "Content-Type: application/json" \
    -H "x-clawpaw-secret: $SECRET" \
    -d "{\"uid\":\"$UID\",\"key\":\"home\"}"
  echo ""
else
  echo ""
  echo "Note: If you see 'failed to authenticate', go to your phone and tap ALLOW on the USB debugging dialog."
fi
