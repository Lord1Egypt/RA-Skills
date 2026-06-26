#!/usr/bin/env bash
# Security Manifest
# - Env: none
# - Endpoints: none
# - Reads: local file paths passed as arguments, airdrop-send.swift in the same directory
# - Writes: stdout and stderr only
# - Network: triggers the native macOS AirDrop sharing service only

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./airdrop-send.sh <file> [file ...]
  ./airdrop-send.sh --shortcut "Shortcut Name" <file> [file ...]

Modes:
  direct    Launch native AirDrop via AppKit and macOS sharing services.
  shortcut  Pass file inputs into an existing user-owned Shortcut.
EOF
}

need_bin() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required binary: $1" >&2
    exit 1
  }
}

validate_files() {
  local path
  for path in "$@"; do
    if [[ ! -e "$path" ]]; then
      echo "Missing file: $path" >&2
      exit 1
    fi
  done
}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SWIFT_FILE="${SCRIPT_DIR}/airdrop-send.swift"

[[ $# -gt 0 ]] || {
  usage >&2
  exit 1
}

if [[ "${1:-}" == "--shortcut" ]]; then
  need_bin shortcuts
  [[ $# -ge 3 ]] || {
    usage >&2
    exit 1
  }
  SHORTCUT_NAME="$2"
  shift 2
  validate_files "$@"

  cmd=(shortcuts run "$SHORTCUT_NAME")
  for path in "$@"; do
    cmd+=(--input-path "$path")
  done

  echo "Running Shortcut mode for ${#@} item(s): ${SHORTCUT_NAME}"
  exec "${cmd[@]}"
fi

[[ -f "$SWIFT_FILE" ]] || {
  echo "Missing helper: $SWIFT_FILE" >&2
  exit 1
}

validate_files "$@"

if command -v xcrun >/dev/null 2>&1; then
  exec xcrun swift "$SWIFT_FILE" "$@"
fi

if command -v swift >/dev/null 2>&1; then
  exec swift "$SWIFT_FILE" "$@"
fi

echo "Neither xcrun nor swift is available. Use --shortcut mode or install Xcode Command Line Tools." >&2
exit 1
