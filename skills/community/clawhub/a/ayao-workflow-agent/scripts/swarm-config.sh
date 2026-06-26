#!/bin/bash
set -euo pipefail

# Ensure flock is available on macOS when installed via Homebrew util-linux.
export PATH="/opt/homebrew/opt/util-linux/bin:$PATH"

CONFIG_FILE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/swarm/config.json"
TASKS_FILE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/swarm/active-tasks.json"

print_usage() {
  cat <<'EOF' >&2
Usage:
  swarm-config.sh get <dot.path>
  swarm-config.sh set <dot.path> <value>
  swarm-config.sh resolve <dot.path>
  swarm-config.sh project get <dot.path>
EOF
}

json_read() {
  local file="$1"
  local path="$2"

  python3 - "$file" "$path" <<'PY'
import json
import os
import sys

file_path, path = sys.argv[1], sys.argv[2]

if not os.path.exists(file_path):
    print("", end="")
    raise SystemExit(0)

try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    print("", end="")
    raise SystemExit(0)

value = data
if path:
    for part in path.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            print("", end="")
            raise SystemExit(0)

if value is None:
    print("", end="")
elif isinstance(value, bool):
    print("true" if value else "false", end="")
elif isinstance(value, (str, int, float)):
    print(value, end="")
else:
    print(json.dumps(value, ensure_ascii=False), end="")
PY
}

json_write() {
  local file="$1"
  local path="$2"
  local raw_value="$3"
  local lock_file="${file}.lock"

  mkdir -p "$(dirname "$file")"

  (
    flock -x 9
    export TARGET_CONFIG_FILE="$file"
    export TARGET_CONFIG_PATH="$path"
    export TARGET_CONFIG_RAW_VALUE="$raw_value"
    python3 - <<'PY'
import json
import os
import sys

config_file = os.environ["TARGET_CONFIG_FILE"]
path = os.environ["TARGET_CONFIG_PATH"]
raw_value = os.environ["TARGET_CONFIG_RAW_VALUE"]

if os.path.exists(config_file):
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("❌ config.json is corrupted, refusing to overwrite", file=sys.stderr)
        raise SystemExit(1)
else:
    data = {}

if not isinstance(data, dict):
    print("❌ config.json root must be an object", file=sys.stderr)
    raise SystemExit(1)

parts = path.split(".")
cursor = data
for part in parts[:-1]:
    if not isinstance(cursor.get(part), dict):
        cursor[part] = {}
    cursor = cursor[part]

try:
    value = json.loads(raw_value)
except Exception:
    value = raw_value

cursor[parts[-1]] = value

tmp_path = config_file + ".tmp"
try:
    with open(tmp_path, "w", encoding="utf-8") as tmp:
        json.dump(data, tmp, indent=2, ensure_ascii=False)
        tmp.write("\n")
        tmp.flush()
        os.fsync(tmp.fileno())
    os.replace(tmp_path, config_file)
except Exception:
    try:
        os.unlink(tmp_path)
    except OSError:
        pass
    raise
PY
  ) 9>"$lock_file"
}

resolve_value() {
  local raw_value
  raw_value="$(json_read "$CONFIG_FILE" "$1")"

  if [[ "$raw_value" =~ ^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$ ]]; then
    local var_name="${BASH_REMATCH[1]}"
    printf '%s' "${!var_name-}"
    return 0
  fi

  printf '%s' "$raw_value"
}

command="${1:-}"

case "$command" in
  get)
    [[ $# -eq 2 ]] || {
      print_usage
      exit 1
    }
    json_read "$CONFIG_FILE" "$2"
    ;;
  set)
    [[ $# -eq 3 ]] || {
      print_usage
      exit 1
    }
    json_write "$CONFIG_FILE" "$2" "$3"
    ;;
  resolve)
    [[ $# -eq 2 ]] || {
      print_usage
      exit 1
    }
    resolve_value "$2"
    ;;
  project)
    [[ "${2:-}" == "get" && $# -eq 3 ]] || {
      print_usage
      exit 1
    }
    json_read "$TASKS_FILE" "$3"
    ;;
  *)
    print_usage
    exit 1
    ;;
esac
