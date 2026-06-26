#!/usr/bin/env bash
# BloodHound Narrator — bash entry point
# Copies the .txt script to a temp .ps1 so PowerShell can execute it natively.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_SCRIPT="$SCRIPT_DIR/Invoke-BHNarrator.txt"

if ! command -v pwsh &>/dev/null; then
    echo "Error: PowerShell (pwsh) is not installed." >&2
    echo "Install via: brew install powershell/tap/powershell" >&2
    exit 1
fi

TEMP="$(mktemp /tmp/bh-narrator-XXXXXX.ps1)"
trap 'rm -f "$TEMP"' EXIT
cp "$MAIN_SCRIPT" "$TEMP"
export BH_NARRATOR_DIR="$SCRIPT_DIR"
pwsh -NoProfile -File "$TEMP" "$@"
