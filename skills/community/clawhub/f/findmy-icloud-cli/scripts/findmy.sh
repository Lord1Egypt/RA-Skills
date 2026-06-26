#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/state.sh"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/findmy.sh set-username <apple-id-email>
  ./scripts/findmy.sh show-username
  ./scripts/findmy.sh auth-status [extra icloud auth status args]
  ./scripts/findmy.sh auth-login [extra icloud auth login args]
  ./scripts/findmy.sh list [extra icloud devices list args]
  ./scripts/findmy.sh show <device-id-or-name> [extra icloud devices show args]
  ./scripts/findmy.sh set-person-alias <alias> <device-name-fragment> [more fragments...]
  ./scripts/findmy.sh show-person-aliases
EOF
}

cmd="${1:-}"
if [[ -z "$cmd" ]]; then
  usage >&2
  exit 1
fi
shift || true

case "$cmd" in
  set-username)
    username="${1:-}"
    if [[ -z "$username" ]]; then
      echo "Usage: ./scripts/findmy.sh set-username <apple-id-email>" >&2
      exit 1
    fi
    set_username "$username"
    echo "Stored Apple ID username: $username"
    echo "State file: ${XDG_STATE_HOME:-$HOME/.local/state}/icloud-findmy-cli/account.env"
    ;;
  show-username)
    get_username
    ;;
  auth-status)
    username="$(require_username)"
    exec icloud auth status --username "$username" "$@"
    ;;
  auth-login)
    username="$(require_username)"
    exec icloud auth login --username "$username" "$@"
    ;;
  list)
    username="$(require_username)"
    exec icloud devices list --username "$username" --with-family --locate --format json "$@"
    ;;
  show)
    username="$(require_username)"
    device="${1:-}"
    if [[ -z "$device" ]]; then
      echo "Usage: ./scripts/findmy.sh show <device-id-or-name>" >&2
      exit 1
    fi
    shift
    exec icloud devices show --username "$username" --with-family --locate --format json "$device" "$@"
    ;;
  set-person-alias)
    alias_name="${1:-}"
    shift || true
    if [[ -z "$alias_name" || "$#" -lt 1 ]]; then
      echo "Usage: ./scripts/findmy.sh set-person-alias <alias> <device-name-fragment> [more fragments...]" >&2
      exit 1
    fi
    python3 - "$alias_name" "$@" <<'PY'
import json, sys
from pathlib import Path
path = Path.home() / '.local' / 'state' / 'icloud-findmy-cli' / 'people-aliases.json'
path.parent.mkdir(parents=True, exist_ok=True)
alias_name = sys.argv[1].casefold()
fragments = [v.casefold() for v in sys.argv[2:] if v.strip()]
try:
    data = json.loads(path.read_text()) if path.exists() else {}
except Exception:
    data = {}
data[alias_name] = fragments
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
print(f"Stored alias '{sys.argv[1]}' -> {fragments}")
print(f"State file: {path}")
PY
    ;;
  show-person-aliases)
    python3 - <<'PY'
import json
from pathlib import Path
path = Path.home() / '.local' / 'state' / 'icloud-findmy-cli' / 'people-aliases.json'
if not path.exists():
    raise SystemExit('No stored person aliases.')
print(path.read_text(), end='')
PY
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    usage >&2
    exit 1
    ;;
esac
