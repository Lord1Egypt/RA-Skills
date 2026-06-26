#!/usr/bin/env bash
# Copies .Tests.txt to a temp .Tests.ps1 in the same directory (so $PSScriptRoot resolves correctly),
# runs Pester, then cleans up.
set -euo pipefail

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP="$TESTS_DIR/_temp_Invoke-BHNarrator.Tests.ps1"

trap 'rm -f "$TEMP"' EXIT
cp "$TESTS_DIR/Invoke-BHNarrator.Tests.txt" "$TEMP"
pwsh -NoProfile -Command "Invoke-Pester '$TEMP' -Output Detailed"
