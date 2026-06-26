#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ps1_path="$script_dir/d-switch.ps1"

if command -v cygpath >/dev/null 2>&1; then
  ps1_path="$(cygpath -w "$ps1_path")"
fi

powershell -NoProfile -ExecutionPolicy Bypass -File "$ps1_path" "$@"
