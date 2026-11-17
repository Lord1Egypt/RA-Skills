#!/usr/bin/env bash
set -euo pipefail

# Setup TeamTalk 5 SDK: detect system, build from source if not found
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${BUILD_DIR:-./TeamTalk5}"

echo "=== TeamTalk 5 SDK Setup ==="

# Check if SDK built artifacts exist
if [ -f "$BUILD_DIR/Build/output/libTeamTalk.so" ] || \
   [ -f "$BUILD_DIR/Build/output/libTeamTalk.dylib" ] || \
   [ -f "$BUILD_DIR/Build/output/TeamTalk5.dll" ]; then
    echo "SDK already built in $BUILD_DIR"
    $SCRIPT_DIR/check_sdk.py
    exit 0
fi

echo "SDK not found. Building from source..."
bash "$SCRIPT_DIR/build_from_source.sh"
