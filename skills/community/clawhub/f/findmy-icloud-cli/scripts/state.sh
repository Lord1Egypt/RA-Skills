#!/bin/bash
set -euo pipefail

STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/icloud-findmy-cli"
STATE_FILE="$STATE_DIR/account.env"

ensure_state_dir() {
  mkdir -p "$STATE_DIR"
}

get_username() {
  if [[ -f "$STATE_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$STATE_FILE"
    if [[ -n "${ICLOUD_FINDMY_USERNAME:-}" ]]; then
      printf '%s\n' "$ICLOUD_FINDMY_USERNAME"
      return 0
    fi
  fi
  return 1
}

set_username() {
  local username="$1"
  ensure_state_dir
  cat > "$STATE_FILE" <<EOF
ICLOUD_FINDMY_USERNAME="$username"
EOF
}

require_username() {
  if get_username >/dev/null 2>&1; then
    get_username
    return 0
  fi
  echo "No stored Apple ID username for icloud-findmy-cli." >&2
  echo "Ask the user once, then run: ./scripts/account-set.sh their.email@example.com" >&2
  return 1
}
