#!/bin/bash
# squad-config.sh — View or update agent-squad settings
# Usage: squad-config.sh show
#        squad-config.sh set <key> <value>

set -euo pipefail

BASE_DIR="${HOME}/.openclaw/workspace/agent-squad"
CONFIG_FILE="${BASE_DIR}/config.json"

# --- Check python3 ---
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 is required but not found in PATH."
  exit 1
fi

ACTION="${1:?Usage: squad-config.sh show | set <key> <value>}"

case "$ACTION" in
  show)
    if [ -f "$CONFIG_FILE" ]; then
      echo "Config: $CONFIG_FILE"
      echo ""
      python3 -c "import json,sys; [print(f'  {k}: {v}') for k,v in json.load(open(sys.argv[1])).items()]" "$CONFIG_FILE"
    else
      echo "No config file found. Using defaults."
      echo ""
      echo "  projects_dir: ${BASE_DIR}/projects"
    fi
    ;;

  set)
    KEY="${2:?Usage: squad-config.sh set <key> <value>}"
    VALUE="${3:?Usage: squad-config.sh set <key> <value>}"

    # Validate key
    case "$KEY" in
      projects_dir)
        # Resolve to absolute path (mkdir -p is a no-op if it already exists)
        mkdir -p "$VALUE"
        VALUE=$(cd "$VALUE" && pwd)
        ;;
      *)
        echo "ERROR: Unknown config key '$KEY'. Supported keys: projects_dir"
        exit 1
        ;;
    esac

    # Write config (safe via sys.argv)
    mkdir -p "$BASE_DIR"
    python3 -c "
import json, sys, os
config_file = sys.argv[1]
key = sys.argv[2]
value = sys.argv[3]
config = {}
if os.path.exists(config_file):
    with open(config_file) as f:
        config = json.load(f)
config[key] = value
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)
    f.write('\n')
" "$CONFIG_FILE" "$KEY" "$VALUE"

    echo "Set $KEY = $VALUE"
    echo "New squads will use this setting. Existing squads are not affected."
    ;;

  *)
    echo "Usage: \"Show squad settings\" or \"Set default project dir to ~/code\""
    exit 1
    ;;
esac
