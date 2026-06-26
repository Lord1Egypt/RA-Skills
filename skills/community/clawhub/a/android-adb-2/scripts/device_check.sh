#!/usr/bin/env bash
# Quick device health check: lists devices, shows basic info for each
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/adb_env.sh"

if [ -z "$ADB_BIN" ]; then
  echo "ADB not found. Run: bash $SCRIPT_DIR/install_adb.sh"
  exit 1
fi

devices=$($ADB_BIN devices -l 2>/dev/null | tail -n +2 | grep -v "^$" || true)

if [ -z "$devices" ]; then
  echo "No devices connected."
  exit 1
fi

count=$(echo "$devices" | wc -l | tr -d ' ')
echo "=== $count device(s) found ==="
echo ""

i=1
echo "$devices" | while IFS= read -r line; do
  serial=$(echo "$line" | awk '{print $1}')
  state=$(echo "$line" | awk '{print $2}')

  echo "--- Device $i: $serial ($state) ---"

  if [ "$state" = "device" ]; then
    model=$($ADB_BIN -s "$serial" shell getprop ro.product.model 2>/dev/null || echo "unknown")
    brand=$($ADB_BIN -s "$serial" shell getprop ro.product.brand 2>/dev/null || echo "unknown")
    version=$($ADB_BIN -s "$serial" shell getprop ro.build.version.release 2>/dev/null || echo "unknown")
    sdk=$($ADB_BIN -s "$serial" shell getprop ro.build.version.sdk 2>/dev/null || echo "unknown")
    echo "  Brand:   $brand"
    echo "  Model:   $model"
    echo "  Android: $version (API $sdk)"
  else
    echo "  State: $state (cannot query properties)"
  fi
  echo ""
  i=$((i + 1))
done
