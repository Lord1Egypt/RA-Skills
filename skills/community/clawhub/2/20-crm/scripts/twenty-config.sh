#!/bin/bash
set -euo pipefail

# Loads config for Twenty CRM API scripts.
# Config resolution order:
# 1) TWENTY_CONFIG_FILE env var
# 2) ../config/twenty.env relative to this script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_CONFIG_FILE="$(cd "$SCRIPT_DIR/.." && pwd)/config/twenty.env"
CONFIG_FILE="${TWENTY_CONFIG_FILE:-$DEFAULT_CONFIG_FILE}"

require_cmd() {
  local cmd="${1:-}"
  if [ -z "$cmd" ] || ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
}

validate_rest_path() {
  local path_part="${1:-}"
  if [[ -z "$path_part" || "$path_part" != /* || "$path_part" == *"?"* || "$path_part" == *$'\n'* || "$path_part" == *$'\r'* ]]; then
    echo "Invalid REST path '$path_part'. Use an absolute path like /companies and pass query parameters separately." >&2
    exit 1
  fi
}

if [ -f "$CONFIG_FILE" ]; then
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
fi

if [ -z "${TWENTY_BASE_URL:-}" ]; then
  echo "Missing TWENTY_BASE_URL. Set it in the environment or $CONFIG_FILE." >&2
  exit 1
fi

if [ -z "${TWENTY_API_KEY:-}" ]; then
  echo "Missing TWENTY_API_KEY. Set it in the environment or $CONFIG_FILE." >&2
  exit 1
fi

require_cmd curl

# Normalize trailing slash
TWENTY_BASE_URL="${TWENTY_BASE_URL%/}"

export TWENTY_BASE_URL
export TWENTY_API_KEY
