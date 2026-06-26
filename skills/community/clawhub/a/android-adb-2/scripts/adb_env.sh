#!/usr/bin/env bash
# ADB path resolver - source this file to get ADB_BIN variable
# Usage: source "$(dirname "$0")/adb_env.sh"
#
# Priority: system adb → common SDK paths → sandbox local adb
# After sourcing, use "$ADB_BIN" instead of "adb"

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SANDBOX_ADB="$SKILL_DIR/tools/platform-tools/adb"

if command -v adb &>/dev/null; then
    export ADB_BIN="adb"
elif [ -x "$HOME/Library/Android/sdk/platform-tools/adb" ]; then
    export ADB_BIN="$HOME/Library/Android/sdk/platform-tools/adb"
elif [ -x "$HOME/Android/Sdk/platform-tools/adb" ]; then
    export ADB_BIN="$HOME/Android/Sdk/platform-tools/adb"
elif [ -x "$SANDBOX_ADB" ]; then
    export ADB_BIN="$SANDBOX_ADB"
else
    export ADB_BIN=""
fi
