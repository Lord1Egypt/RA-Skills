#!/usr/bin/env bash
set -euo pipefail

# Wrapper script for get-gotchi.js

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<USAGE
Usage: ./gotchi-info.sh <gotchi-id-or-name>

Examples:
  ./gotchi-info.sh 9638
  ./gotchi-info.sh aaigotchi
  ./gotchi-info.sh "My Gotchi Name"
USAGE
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -lt 1 ]; then
  usage
  exit 1
fi

IDENTIFIER="$*"
cd "$SCRIPT_DIR" && node get-gotchi.js "$IDENTIFIER"
