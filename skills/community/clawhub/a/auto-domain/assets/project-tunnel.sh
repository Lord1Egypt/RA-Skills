#!/usr/bin/env bash
if [ -z "${BASH_VERSION:-}" ]; then
  exec /usr/bin/env bash "$0" "$@"
fi
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  ./project-tunnel.sh start
  ./project-tunnel.sh start --port 5318
  ./project-tunnel.sh start -p 5318
  ./project-tunnel.sh start 5318
  ./project-tunnel.sh start --port 5180 --startsh scripts/dev-restart.sh
  ./project-tunnel.sh start --start-cmd "npm run dev -- --host 127.0.0.1 --port 5180"
  ./project-tunnel.sh stop
  ./project-tunnel.sh status

Default behavior (zero-config):
- PROJECT_DIR: current directory
- PROJECT_NAME: package.json.name or current folder name
- PROJECT_PORT: .tunnel-port > .env.local/.env PORT= > 3000
- USER_ID: current system user
- SUBDOMAIN: <project>-<user>
- DOMAIN_MODE: fixed (stable domain)

Optional env vars:
- BASE_DOMAIN=vyibc.com
- CONTROL_API_BASE=http://152.32.214.95:3002/control
- PUBLIC_SCHEME=https
- DOMAIN_MODE=fixed|random
- SUBDOMAIN=custom-subdomain
- FORCE_NEW_DOMAIN=1
- BUILD_CMD='npm run build'
- START_CMD='npm run start -- -p 3000'
- START_SH='scripts/dev-restart.sh'
- SKIP_BUILD=1

Agent auto-download:
- AGENT_GITHUB_REPO=ChangfengHU/tunneling
- AGENT_VERSION=latest (or a release tag)
- AGENT_BIN=~/.tunneling/bin/agent
- FORCE_AGENT_DOWNLOAD=1

Compatibility:
- Script runtime: macOS/Linux/Git-Bash(Windows)
- Agent binaries auto-selected:
  darwin-arm64 / darwin-amd64 / linux-amd64 / windows-amd64
USAGE
}

cmd="${1:-start}"
if [[ "${cmd}" == "-h" || "${cmd}" == "--help" ]]; then
  usage
  exit 0
fi
shift || true

cli_project_port=""
cli_project_name=""
cli_user_id=""
cli_subdomain=""
cli_base_domain=""
cli_start_sh=""
cli_start_cmd=""
cli_build_cmd=""
cli_skip_build=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--port)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: $1 requires a value" >&2
        usage
        exit 1
      fi
      cli_project_port="$2"
      shift 2
      ;;
    --project-name)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: $1 requires a value" >&2
        usage
        exit 1
      fi
      cli_project_name="$2"
      shift 2
      ;;
    --user-id)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: $1 requires a value" >&2
        usage
        exit 1
      fi
      cli_user_id="$2"
      shift 2
      ;;
    --subdomain)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: $1 requires a value" >&2
        usage
        exit 1
      fi
      cli_subdomain="$2"
      shift 2
      ;;
    --base-domain)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: $1 requires a value" >&2
        usage
        exit 1
      fi
      cli_base_domain="$2"
      shift 2
      ;;
    --startsh|--start-sh)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: $1 requires a value" >&2
        usage
        exit 1
      fi
      cli_start_sh="$2"
      shift 2
      ;;
    --start-cmd)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: $1 requires a value" >&2
        usage
        exit 1
      fi
      cli_start_cmd="$2"
      shift 2
      ;;
    --build-cmd)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: $1 requires a value" >&2
        usage
        exit 1
      fi
      cli_build_cmd="$2"
      shift 2
      ;;
    --skip-build)
      cli_skip_build="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -z "${cli_project_port}" && "$1" =~ ^[0-9]{2,5}$ ]]; then
        cli_project_port="$1"
        shift
        continue
      fi
      echo "ERROR: unknown arg '$1'" >&2
      usage
      exit 1
      ;;
  esac
done

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "ERROR: missing command '$1'" >&2
    exit 1
  fi
}

sanitize_dns_label() {
  local input="$1"
  local out
  out="$(echo "${input}" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9-]+/-/g; s/^-+//; s/-+$//; s/-{2,}/-/g')"
  echo "${out:0:40}"
}

sanitize_key() {
  local input="$1"
  local out
  out="$(echo "${input}" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9_.-]+/-/g; s/^-+//; s/-+$//')"
  echo "${out:0:90}"
}

shell_quote() {
  printf '%q' "$1"
}

json_get() {
  local path="$1"
  $PYTHON -c '
import json
import sys
obj = json.load(sys.stdin)
for p in sys.argv[1].split("."):
    obj = obj[p]
if isinstance(obj, bool):
    print("true" if obj else "false")
elif obj is None:
    print("")
else:
    print(obj)
' "${path}"
}

state_get() {
  local key="$1"
  [[ -f "${STATE_FILE}" ]] || return 1
  $PYTHON - "${STATE_FILE}" "${key}" <<'PY'
import json
import os
import sys

state_file, key = sys.argv[1], sys.argv[2]
if not os.path.exists(state_file):
    raise SystemExit(1)
with open(state_file, "r", encoding="utf-8") as f:
    data = json.load(f)
if key not in data or data[key] is None:
    raise SystemExit(1)
v = data[key]
if isinstance(v, bool):
    print("true" if v else "false")
else:
    print(v)
PY
}

state_write() {
  $PYTHON - "${STATE_FILE}" \
    "${PROJECT_NAME}" "${PROJECT_DIR}" "${PROJECT_PORT}" "${USER_ID}" "${BASE_DOMAIN}" \
    "${DOMAIN_MODE}" "${SUBDOMAIN}" "${HOSTNAME}" "${PUBLIC_URL}" \
    "${TUNNEL_ID}" "${TUNNEL_TOKEN}" "${TARGET}" "${MACHINE_AGENT_ADMIN_ADDR}" \
    "${AGENT_BIN}" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone

(
    state_file,
    project_name,
    project_dir,
    project_port,
    user_id,
    base_domain,
    domain_mode,
    subdomain,
    hostname,
    public_url,
    tunnel_id,
    tunnel_token,
    target,
    agent_admin_addr,
    agent_bin,
) = sys.argv[1:]

os.makedirs(os.path.dirname(state_file), exist_ok=True)

state = {
    "project_name": project_name,
    "project_dir": project_dir,
    "project_port": int(project_port),
    "user_id": user_id,
    "base_domain": base_domain,
    "domain_mode": domain_mode,
    "subdomain": subdomain,
    "hostname": hostname,
    "public_url": public_url,
    "tunnel_id": tunnel_id,
    "tunnel_token": tunnel_token,
    "target": target,
    "agent_admin_addr": agent_admin_addr,
    "agent_bin": agent_bin,
    "updated_at": datetime.now(timezone.utc).isoformat(),
}
with open(state_file, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
PY
}

api_post() {
  local url="$1"
  local payload="$2"
  local body_file
  body_file="$(mktemp)"
  local status
  status="$(curl -sS -o "${body_file}" -w "%{http_code}" -X POST "${url}" \
    -H "Content-Type: application/json" \
    --data "${payload}")"
  if ((status < 200 || status >= 300)); then
    echo "ERROR: POST ${url} status=${status}" >&2
    cat "${body_file}" >&2
    rm -f "${body_file}"
    return 1
  fi
  cat "${body_file}"
  rm -f "${body_file}"
}

api_delete() {
  local url="$1"
  local body_file
  body_file="$(mktemp)"
  local status
  status="$(curl -sS -o "${body_file}" -w "%{http_code}" -X DELETE "${url}")"
  if ((status < 200 || status >= 300)); then
    rm -f "${body_file}"
    return 1
  fi
  rm -f "${body_file}"
  return 0
}

list_project_sibling_states() {
  local root="$1"
  local project_name="$2"
  local user_id="$3"
  local base_domain="$4"
  local hostname="$5"
  local current_port="$6"
  $PYTHON - "${root}" "${project_name}" "${user_id}" "${base_domain}" "${hostname}" "${current_port}" <<'PY'
import glob
import json
import os
import sys

root, project_name, user_id, base_domain, hostname, current_port = sys.argv[1:]
pattern = os.path.join(root, "*", "state.json")
for path in glob.glob(pattern):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        continue

    if str(data.get("project_name", "")) != project_name:
        continue
    if str(data.get("user_id", "")) != user_id:
        continue
    if str(data.get("base_domain", "")) != base_domain:
        continue

    port = str(data.get("project_port", ""))
    if not port or port == str(current_port):
        continue

    old_host = str(data.get("hostname", "")).strip()
    if hostname and old_host and old_host != hostname:
        continue

    state_dir = os.path.dirname(path)
    fields = [
        state_dir,
        port,
        str(data.get("tunnel_id", "")),
        old_host,
        str(data.get("target", "")),
        str(data.get("agent_admin_addr", "")),
    ]
    print("\t".join(fields))
PY
}

cleanup_other_ports_for_same_project() {
  local line state_dir old_port old_tunnel old_host old_target old_admin old_admin_port tmp_file
  tmp_file="$(mktemp)"
  list_project_sibling_states "${STATE_ROOT}" "${PROJECT_NAME}" "${USER_ID}" "${BASE_DOMAIN}" "${HOSTNAME}" "${PROJECT_PORT}" >"${tmp_file}" || true
  while IFS=$'\t' read -r state_dir old_port old_tunnel old_host old_target old_admin; do
    [[ -n "${state_dir}" ]] || continue
    echo "[cleanup] remove old port state dir=${state_dir} port=${old_port}"

    stop_by_pid_file "${state_dir}/app.pid"
    stop_by_pid_file "${state_dir}/agent.pid"
    if [[ "${old_port}" =~ ^[0-9]{2,5}$ ]]; then
      stop_by_tcp_port "${old_port}"
    fi
    old_admin_port="${old_admin##*:}"
    if [[ "${old_admin_port}" =~ ^[0-9]{2,5}$ ]]; then
      stop_by_tcp_port "${old_admin_port}"
    fi

    if [[ -n "${old_tunnel}" && -n "${old_host}" ]]; then
      if [[ -z "${old_target}" ]]; then
        old_target="127.0.0.1:${old_port}"
      fi
      old_payload="$($PYTHON - "${old_tunnel}" "${old_host}" "${old_target}" <<'PY'
import json
import sys
tunnel_id, hostname, target = sys.argv[1:4]
print(json.dumps({
    "tunnel_id": tunnel_id,
    "hostname": hostname,
    "target": target,
    "enabled": False,
}))
PY
)"
      api_post "${CONTROL_API_BASE}/api/routes" "${old_payload}" >/dev/null 2>/dev/null || true
      api_delete "${CONTROL_API_BASE}/api/tunnels/${old_tunnel}" >/dev/null || true
    fi

    if [[ "${state_dir}" == "${STATE_ROOT}/"* ]]; then
      rm -rf "${state_dir}" || true
    fi
  done < "${tmp_file}"
  rm -f "${tmp_file}"
}

parse_package_name() {
  local file="$1"
  $PYTHON - "${file}" <<'PY'
import json
import os
import sys

path = sys.argv[1]
if not os.path.exists(path):
    print("")
    raise SystemExit(0)
try:
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    v = obj.get("name", "")
    if isinstance(v, str):
        print(v)
    else:
        print("")
except Exception:
    print("")
PY
}

detect_start_cmd() {
  local pkg_file="$1"
  local port="$2"
  $PYTHON - "${pkg_file}" "${port}" <<'PY'
import json
import os
import sys

pkg_file, port = sys.argv[1], sys.argv[2]
if not os.path.exists(pkg_file):
    print("")
    raise SystemExit(0)
try:
    with open(pkg_file, "r", encoding="utf-8") as f:
        obj = json.load(f)
except Exception:
    print("")
    raise SystemExit(0)

scripts = obj.get("scripts", {}) if isinstance(obj, dict) else {}
if not isinstance(scripts, dict):
    scripts = {}

if "start" in scripts:
    print(f"npm run start -- -p {port}")
elif "preview" in scripts:
    print(f"npm run preview -- --host 127.0.0.1 --port {port}")
elif "dev" in scripts:
    print(f"npm run dev -- --host 127.0.0.1 --port {port}")
else:
    print("")
PY
}

port_from_file() {
  local f="$1"
  [[ -f "${f}" ]] || return 1
  sed -nE 's/^[[:space:]]*(export[[:space:]]+)?PORT[[:space:]]*=[[:space:]]*"?([0-9]{2,5})"?[[:space:]]*$/\2/p' "${f}" | head -n1
}

detect_platform() {
  local os raw_arch os_key arch_key
  os="$(uname -s 2>/dev/null || echo unknown)"
  raw_arch="$(uname -m 2>/dev/null || echo unknown)"

  case "${os}" in
    Darwin) os_key="darwin" ;;
    Linux) os_key="linux" ;;
    MINGW*|MSYS*|CYGWIN*) os_key="windows" ;;
    *)
      if [[ "${OS:-}" == "Windows_NT" ]]; then
        os_key="windows"
      else
        os_key="unknown"
      fi
      ;;
  esac

  case "${raw_arch}" in
    x86_64|amd64) arch_key="amd64" ;;
    arm64|aarch64) arch_key="arm64" ;;
    *) arch_key="unknown" ;;
  esac

  if [[ "${os_key}" == "darwin" && "${arch_key}" != "amd64" && "${arch_key}" != "arm64" ]]; then
    echo "unsupported platform: ${os}/${raw_arch}" >&2
    return 1
  fi
  if [[ "${os_key}" == "linux" && "${arch_key}" != "amd64" ]]; then
    echo "unsupported platform: ${os}/${raw_arch}" >&2
    return 1
  fi
  if [[ "${os_key}" == "windows" && "${arch_key}" != "amd64" ]]; then
    echo "unsupported platform: ${os}/${raw_arch}" >&2
    return 1
  fi
  if [[ "${os_key}" == "unknown" || "${arch_key}" == "unknown" ]]; then
    echo "unsupported platform: ${os}/${raw_arch}" >&2
    return 1
  fi

  echo "${os_key}-${arch_key}"
}

ensure_agent_binary() {
  local platform asset release_base url tmp
  platform="$(detect_platform)"
  AGENT_EXT=""
  if [[ "${platform}" == windows-* ]]; then
    AGENT_EXT=".exe"
  fi

  AGENT_GITHUB_REPO="${AGENT_GITHUB_REPO:-ChangfengHU/tunneling}"
  AGENT_VERSION="${AGENT_VERSION:-latest}"
  AGENT_RELEASE_BASE="${AGENT_RELEASE_BASE:-https://github.com/${AGENT_GITHUB_REPO}/releases}"
  AGENT_DIR="${AGENT_DIR:-${HOME}/.tunneling/bin}"
  mkdir -p "${AGENT_DIR}"

  AGENT_BIN="${AGENT_BIN:-${AGENT_DIR}/agent${AGENT_EXT}}"
  FORCE_AGENT_DOWNLOAD="${FORCE_AGENT_DOWNLOAD:-0}"

  if [[ "${FORCE_AGENT_DOWNLOAD}" != "1" && -f "${AGENT_BIN}" ]]; then
    if [[ "${AGENT_EXT}" == ".exe" || -x "${AGENT_BIN}" ]]; then
      return 0
    fi
  fi

  asset="agent-${platform}${AGENT_EXT}"
  if [[ "${AGENT_VERSION}" == "latest" ]]; then
    url="${AGENT_RELEASE_BASE}/latest/download/${asset}"
  else
    url="${AGENT_RELEASE_BASE}/download/${AGENT_VERSION}/${asset}"
  fi

  echo "[agent] downloading ${asset}"
  tmp="${AGENT_BIN}.tmp"
  rm -f "${tmp}"
  curl -fL --retry 3 --retry-delay 1 -o "${tmp}" "${url}"
  mv "${tmp}" "${AGENT_BIN}"
  chmod +x "${AGENT_BIN}" || true
  echo "[agent] ready: ${AGENT_BIN}"
}

is_pid_running() {
  local pid="$1"
  [[ -n "${pid}" ]] || return 1
  kill -0 "${pid}" >/dev/null 2>&1
}

stop_by_pid_file() {
  local file="$1"
  if [[ ! -f "${file}" ]]; then
    return 0
  fi
  local pid
  pid="$(cat "${file}" 2>/dev/null || true)"
  if is_pid_running "${pid}"; then
    kill "${pid}" >/dev/null 2>&1 || true
    sleep 1
    if is_pid_running "${pid}"; then
      kill -9 "${pid}" >/dev/null 2>&1 || true
    fi
  fi
  rm -f "${file}"
}

pid_on_tcp_port() {
  local port="$1"
  if ! command -v lsof >/dev/null 2>&1; then
    return 1
  fi
  lsof -ti "tcp:${port}" 2>/dev/null | head -n1
}

stop_by_tcp_port() {
  local port="$1"
  local pid
  pid="$(pid_on_tcp_port "${port}" || true)"
  if [[ -n "${pid}" ]]; then
    kill "${pid}" >/dev/null 2>&1 || true
    sleep 1
    if is_pid_running "${pid}"; then
      kill -9 "${pid}" >/dev/null 2>&1 || true
    fi
  fi
}

start_runner() {
  local runner="$1"
  local pid_file="$2"
  local log_file="$3"
  nohup "${runner}" >>"${log_file}" 2>&1 &
  echo $! >"${pid_file}"
}

wait_http_ok() {
  local url="$1"
  local max_try="${2:-30}"
  local i
  for ((i=1; i<=max_try; i++)); do
    if curl -fsS "${url}" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  return 1
}

wait_agent_connected() {
  local max_try="${1:-30}"
  local i
  local status
  for ((i=1; i<=max_try; i++)); do
    status="$(curl -fsS "${AGENT_STATUS_URL}" 2>/dev/null || true)"
    if [[ -n "${status}" ]] && grep -q '"connected":true' <<<"${status}"; then
      return 0
    fi
    sleep 1
  done
  return 1
}

write_runner_scripts() {
  cat >"${APP_RUNNER}" <<EOF_APP
#!/usr/bin/env bash
set -euo pipefail
export PATH='${PATH_VALUE}'
export PORT='${PROJECT_PORT}'
export PROJECT_PORT='${PROJECT_PORT}'
cd '${PROJECT_DIR}'
exec ${START_CMD}
EOF_APP
  chmod +x "${APP_RUNNER}"

  cat >"${AGENT_RUNNER}" <<EOF_AGENT
#!/usr/bin/env bash
set -euo pipefail
export PATH='${PATH_VALUE}'
exec '${AGENT_BIN}' \\
  -server '${AGENT_SERVER}' \\
  -token '${TUNNEL_TOKEN}' \\
  -route-sync-url '${AGENT_ROUTE_SYNC_URL}' \\
  -tunnel-id '${TUNNEL_ID}' \\
  -tunnel-token '${TUNNEL_TOKEN}' \\
  -admin-addr '${AGENT_ADMIN_ADDR}' \\
  -config '${AGENT_CONFIG}'
EOF_AGENT
  chmod +x "${AGENT_RUNNER}"
}

require_cmd curl
# Detect python3 or python (python 2 not supported; script requires python 3)
if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1 && python -c "import sys; assert sys.version_info[0]==3" 2>/dev/null; then
  PYTHON=python
else
  echo "ERROR: python3 (or python pointing to Python 3) is required" >&2
  exit 1
fi
require_cmd node
require_cmd npm

PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"
_pkg_name="$(parse_package_name "${PROJECT_DIR}/package.json" || true)"
if [[ -n "${PROJECT_NAME:-}" ]]; then
  PROJECT_NAME="${PROJECT_NAME}"
elif [[ -n "${cli_project_name}" ]]; then
  PROJECT_NAME="${cli_project_name}"
else
  PROJECT_NAME="${_pkg_name:-$(basename "${PROJECT_DIR}")}"
fi

if [[ -n "${PROJECT_PORT:-}" ]]; then
  PROJECT_PORT="${PROJECT_PORT}"
elif [[ -n "${cli_project_port}" ]]; then
  PROJECT_PORT="${cli_project_port}"
elif [[ -z "${PROJECT_PORT:-}" ]]; then
  if [[ -f "${PROJECT_DIR}/.tunnel-port" ]]; then
    PROJECT_PORT="$(head -n1 "${PROJECT_DIR}/.tunnel-port" | tr -d '[:space:]')"
  else
    PROJECT_PORT="$(port_from_file "${PROJECT_DIR}/.env.local" || true)"
    if [[ -z "${PROJECT_PORT}" ]]; then
      PROJECT_PORT="$(port_from_file "${PROJECT_DIR}/.env" || true)"
    fi
    PROJECT_PORT="${PROJECT_PORT:-3000}"
  fi
fi

if [[ -n "${USER_ID:-}" ]]; then
  USER_ID="${USER_ID}"
elif [[ -n "${cli_user_id}" ]]; then
  USER_ID="${cli_user_id}"
else
  USER_ID="$(id -un 2>/dev/null || whoami || echo u-local)"
fi
if [[ -n "${BASE_DOMAIN:-}" ]]; then
  BASE_DOMAIN="${BASE_DOMAIN}"
elif [[ -n "${cli_base_domain}" ]]; then
  BASE_DOMAIN="${cli_base_domain}"
else
  BASE_DOMAIN="vyibc.com"
fi
CONTROL_API_BASE="${CONTROL_API_BASE:-http://152.32.214.95:3002/control}"
PUBLIC_SCHEME="${PUBLIC_SCHEME:-https}"
DOMAIN_MODE="${DOMAIN_MODE:-fixed}"
if [[ -n "${SUBDOMAIN:-}" ]]; then
  SUBDOMAIN="${SUBDOMAIN}"
elif [[ -n "${cli_subdomain}" ]]; then
  SUBDOMAIN="${cli_subdomain}"
else
  SUBDOMAIN=""
fi
FORCE_NEW_DOMAIN="${FORCE_NEW_DOMAIN:-0}"

if [[ -n "${BUILD_CMD:-}" ]]; then
  BUILD_CMD="${BUILD_CMD}"
elif [[ -n "${cli_build_cmd}" ]]; then
  BUILD_CMD="${cli_build_cmd}"
else
  BUILD_CMD="npm run build"
fi

if [[ -n "${cli_start_sh}" ]]; then
  START_SH="${cli_start_sh}"
elif [[ -n "${START_SH:-}" ]]; then
  START_SH="${START_SH}"
else
  START_SH=""
fi

if [[ -n "${START_SH}" ]]; then
  if [[ "${START_SH}" != /* ]]; then
    START_SH="${PROJECT_DIR}/${START_SH}"
  fi
  if [[ ! -f "${START_SH}" ]]; then
    echo "ERROR: START_SH not found: ${START_SH}" >&2
    exit 1
  fi
  START_CMD="bash $(shell_quote "${START_SH}") $(shell_quote "${PROJECT_PORT}")"
elif [[ -n "${cli_start_cmd}" ]]; then
  START_CMD="${cli_start_cmd}"
elif [[ -n "${START_CMD:-}" ]]; then
  START_CMD="${START_CMD}"
else
  START_CMD="$(detect_start_cmd "${PROJECT_DIR}/package.json" "${PROJECT_PORT}")"
  if [[ -z "${START_CMD}" ]]; then
    START_CMD="npm run start -- -p ${PROJECT_PORT}"
  fi
fi

if [[ -n "${cli_skip_build}" ]]; then
  SKIP_BUILD="1"
else
  SKIP_BUILD="${SKIP_BUILD:-0}"
fi

AGENT_SERVER="${AGENT_SERVER:-ws://152.32.214.95/connect}"
AGENT_ROUTE_SYNC_URL="${AGENT_ROUTE_SYNC_URL:-http://152.32.214.95/_tunnel/agent/routes}"
TARGET_HOST="${TARGET_HOST:-127.0.0.1}"
TARGET="${TARGET:-${TARGET_HOST}:${PROJECT_PORT}}"
PATH_VALUE="${PATH_VALUE:-/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin}"

PROJECT_SLUG="$(sanitize_dns_label "${PROJECT_NAME}")"
USER_SLUG="$(sanitize_dns_label "${USER_ID}")"
PROJECT_KEY="$(sanitize_key "${USER_SLUG}-${PROJECT_SLUG}-${PROJECT_PORT}")"

if [[ -z "${PROJECT_SLUG}" ]]; then
  echo "ERROR: PROJECT_NAME is invalid" >&2
  exit 1
fi
if [[ -z "${USER_SLUG}" ]]; then
  echo "ERROR: USER_ID is invalid" >&2
  exit 1
fi
if [[ ! "${PROJECT_PORT}" =~ ^[0-9]{2,5}$ ]]; then
  echo "ERROR: PROJECT_PORT is invalid: ${PROJECT_PORT}" >&2
  exit 1
fi
if [[ "${DOMAIN_MODE}" != "fixed" && "${DOMAIN_MODE}" != "random" ]]; then
  echo "ERROR: DOMAIN_MODE must be fixed or random" >&2
  exit 1
fi
if [[ "${PUBLIC_SCHEME}" != "https" && "${PUBLIC_SCHEME}" != "http" ]]; then
  echo "ERROR: PUBLIC_SCHEME must be https or http" >&2
  exit 1
fi

STATE_ROOT="${STATE_ROOT:-${HOME}/.tunneling/projects}"
STATE_DIR="${STATE_ROOT}/${PROJECT_KEY}"
STATE_FILE="${STATE_DIR}/state.json"
APP_LOG="${STATE_DIR}/app.log"
AGENT_LOG="${STATE_DIR}/agent.log"
APP_PID_FILE="${STATE_DIR}/app.pid"
AGENT_PID_FILE="${STATE_DIR}/agent.pid"
APP_RUNNER="${STATE_DIR}/run-app.sh"
AGENT_RUNNER="${STATE_DIR}/run-agent.sh"
AGENT_CONFIG="${STATE_DIR}/agent-config.json"

hash_num="$(echo -n "${PROJECT_KEY}" | cksum | awk '{print $1}')"
default_admin_port=$((17000 + (hash_num % 1000)))
AGENT_ADMIN_PORT="${AGENT_ADMIN_PORT:-${default_admin_port}}"
AGENT_ADMIN_ADDR="${AGENT_ADMIN_ADDR:-127.0.0.1:${AGENT_ADMIN_PORT}}"
AGENT_STATUS_URL="http://${AGENT_ADMIN_ADDR}/api/status"

mkdir -p "${STATE_DIR}"

if [[ "${cmd}" == "stop" ]]; then
  if [[ -f "${STATE_FILE}" ]]; then
    stop_tunnel_id="$(state_get tunnel_id || true)"
    stop_hostname="$(state_get hostname || true)"
    stop_target="$(state_get target || true)"
    if [[ -z "${stop_target}" ]]; then
      stop_target="${TARGET}"
    fi
    if [[ -n "${stop_tunnel_id}" && -n "${stop_hostname}" ]]; then
      stop_payload="$($PYTHON - "${stop_tunnel_id}" "${stop_hostname}" "${stop_target}" <<'PY'
import json
import sys
tunnel_id, hostname, target = sys.argv[1:4]
print(json.dumps({
    "tunnel_id": tunnel_id,
    "hostname": hostname,
    "target": target,
    "enabled": False,
}))
PY
)"
      api_post "${CONTROL_API_BASE}/api/routes" "${stop_payload}" >/dev/null || true
    fi
  fi
  stop_by_pid_file "${APP_PID_FILE}"
  stop_by_pid_file "${AGENT_PID_FILE}"
  stop_by_tcp_port "${PROJECT_PORT}"
  stop_by_tcp_port "${AGENT_ADMIN_PORT}"
  echo "[OK] stopped: ${PROJECT_KEY}"
  exit 0
fi

if [[ "${cmd}" == "status" ]]; then
  echo "project_key=${PROJECT_KEY}"
  if [[ -f "${STATE_FILE}" ]]; then
    echo "state_file=${STATE_FILE}"
    echo "hostname=$(state_get hostname || true)"
    echo "public_url=$(state_get public_url || true)"
    echo "tunnel_id=$(state_get tunnel_id || true)"
  else
    echo "state_file not found: ${STATE_FILE}"
  fi
  if [[ -f "${APP_PID_FILE}" ]]; then
    pid="$(cat "${APP_PID_FILE}" 2>/dev/null || true)"
    echo "app_pid=${pid} running=$(is_pid_running "${pid}" && echo yes || echo no)"
  else
    pid="$(pid_on_tcp_port "${PROJECT_PORT}" || true)"
    [[ -n "${pid}" ]] && echo "app_pid=${pid} running=yes (by-port)"
  fi
  if [[ -f "${AGENT_PID_FILE}" ]]; then
    pid="$(cat "${AGENT_PID_FILE}" 2>/dev/null || true)"
    echo "agent_pid=${pid} running=$(is_pid_running "${pid}" && echo yes || echo no)"
  else
    pid="$(pid_on_tcp_port "${AGENT_ADMIN_PORT}" || true)"
    [[ -n "${pid}" ]] && echo "agent_pid=${pid} running=yes (by-port)"
  fi
  echo "local_app:"
  curl -sS -o /dev/null -w "code=%{http_code} ttfb=%{time_starttransfer}s total=%{time_total}s\n" "http://127.0.0.1:${PROJECT_PORT}/" || true
  echo "agent:"
  curl -sS "${AGENT_STATUS_URL}" || true
  echo
  if [[ -f "${STATE_FILE}" ]]; then
    url="$(state_get public_url || true)"
    if [[ -n "${url}" ]]; then
      echo "public:"
      curl -sS -o /dev/null -w "code=%{http_code} ttfb=%{time_starttransfer}s total=%{time_total}s\n" "${url}" || true
    fi
  fi
  exit 0
fi

if [[ "${cmd}" != "start" ]]; then
  usage
  exit 1
fi

if [[ ! -d "${PROJECT_DIR}" ]]; then
  echo "ERROR: PROJECT_DIR not found: ${PROJECT_DIR}" >&2
  exit 1
fi

ensure_agent_binary

# ---------------------------------------------------------------
# Machine-level shared tunnel + shared agent
# All projects on the same machine share ONE tunnel and ONE agent.
# Machine ID is generated once and stored permanently.
# ---------------------------------------------------------------
MACHINE_DIR="${HOME}/.tunneling"
MACHINE_ID_FILE="${MACHINE_DIR}/machine_id"
MACHINE_STATE_FILE="${MACHINE_DIR}/machine_state.json"
MACHINE_AGENT_DIR="${MACHINE_DIR}/machine-agent"
MACHINE_AGENT_LOG="${MACHINE_AGENT_DIR}/agent.log"
MACHINE_AGENT_PID="${MACHINE_AGENT_DIR}/agent.pid"
MACHINE_AGENT_CONFIG="${MACHINE_AGENT_DIR}/config.json"
MACHINE_AGENT_RUNNER="${MACHINE_AGENT_DIR}/run-agent.sh"
MACHINE_AGENT_ADMIN_ADDR="127.0.0.1:17000"
MACHINE_AGENT_ADMIN_PORT="17000"
MACHINE_AGENT_STATUS_URL="http://${MACHINE_AGENT_ADMIN_ADDR}/api/status"

mkdir -p "${MACHINE_DIR}" "${MACHINE_AGENT_DIR}"

# Generate a stable machine ID (once only)
if [[ ! -f "${MACHINE_ID_FILE}" ]]; then
  $PYTHON -c "import uuid; print(str(uuid.uuid4()))" > "${MACHINE_ID_FILE}"
fi
MACHINE_ID="$(cat "${MACHINE_ID_FILE}" | tr -d '[:space:]')"

# Read a field from machine state file
machine_state_read() {
  local key="$1"
  [[ -f "${MACHINE_STATE_FILE}" ]] || return 1
  $PYTHON - "${MACHINE_STATE_FILE}" "${key}" <<'PY'
import json, sys, os
f, k = sys.argv[1], sys.argv[2]
if not os.path.exists(f): raise SystemExit(1)
d = json.load(open(f))
v = d.get(k, "")
if not v: raise SystemExit(1)
print(v)
PY
}

# Write full machine state
machine_state_write() {
  # Args: tunnel_id tunnel_token
  $PYTHON - "${MACHINE_STATE_FILE}" "${MACHINE_ID}" "${USER_ID}" \
    "$1" "$2" "${MACHINE_AGENT_ADMIN_ADDR}" <<'PY'
import json, sys, os
from datetime import datetime, timezone
f, machine_id, user_id, tunnel_id, tunnel_token, agent_admin_addr = sys.argv[1:]
os.makedirs(os.path.dirname(os.path.abspath(f)), exist_ok=True)
data = {"machine_id": machine_id, "user_id": user_id,
        "tunnel_id": tunnel_id, "tunnel_token": tunnel_token,
        "agent_admin_addr": agent_admin_addr,
        "updated_at": datetime.now(timezone.utc).isoformat()}
open(f, "w").write(json.dumps(data, indent=2))
PY
}

# Check if machine agent is alive
is_machine_agent_running() {
  # Check by PID file
  local pid
  pid="$(cat "${MACHINE_AGENT_PID}" 2>/dev/null | tr -d '[:space:]' || true)"
  if [[ -n "${pid}" ]] && is_pid_running "${pid}"; then
    return 0
  fi
  # Fallback: check if something is listening on the admin port
  local port_pid
  port_pid="$(pid_on_tcp_port "${MACHINE_AGENT_ADMIN_PORT}" || true)"
  if [[ -n "${port_pid}" ]]; then
    echo "${port_pid}" > "${MACHINE_AGENT_PID}"
    return 0
  fi
  return 1
}

# Write machine agent runner script
write_machine_agent_runner() {
  local tid="$1" ttoken="$2"
  cat > "${MACHINE_AGENT_RUNNER}" <<EOF_RUNNER
#!/usr/bin/env bash
set -euo pipefail
export PATH='${PATH_VALUE}'
exec '${AGENT_BIN}' \\
  -server '${AGENT_SERVER}' \\
  -token '${ttoken}' \\
  -route-sync-url '${AGENT_ROUTE_SYNC_URL}' \\
  -tunnel-id '${tid}' \\
  -tunnel-token '${ttoken}' \\
  -admin-addr '${MACHINE_AGENT_ADMIN_ADDR}' \\
  -config '${MACHINE_AGENT_CONFIG}'
EOF_RUNNER
  chmod +x "${MACHINE_AGENT_RUNNER}"
}

TUNNEL_ID=""
TUNNEL_TOKEN=""
HOSTNAME=""
PUBLIC_URL=""

# Read machine-level shared tunnel (always takes priority over per-project state)
SHARED_TUNNEL_ID="$(machine_state_read tunnel_id || true)"
SHARED_TUNNEL_TOKEN="$(machine_state_read tunnel_token || true)"

if [[ -n "${SHARED_TUNNEL_ID}" && -n "${SHARED_TUNNEL_TOKEN}" ]]; then
  TUNNEL_ID="${SHARED_TUNNEL_ID}"
  TUNNEL_TOKEN="${SHARED_TUNNEL_TOKEN}"
  echo "[tunnel] using machine tunnel: ${TUNNEL_ID}"
elif [[ -f "${STATE_FILE}" && "${FORCE_NEW_DOMAIN}" != "1" ]]; then
  # Fallback: legacy per-project state (migration path)
  TUNNEL_ID="$(state_get tunnel_id || true)"
  TUNNEL_TOKEN="$(state_get tunnel_token || true)"
  HOSTNAME="$(state_get hostname || true)"
  PUBLIC_URL="$(state_get public_url || true)"
fi

# If machine_state.json doesn't exist yet but we already have a tunnel_id
# (from legacy state.json), pin it as the machine tunnel now so all
# subsequent projects on this machine share the same tunnel.
if [[ -z "${SHARED_TUNNEL_ID}" && -n "${TUNNEL_ID}" && -n "${TUNNEL_TOKEN}" ]]; then
  machine_state_write "${TUNNEL_ID}" "${TUNNEL_TOKEN}"
  echo "[tunnel] pinned machine tunnel: ${TUNNEL_ID}"
fi

if [[ "${DOMAIN_MODE}" == "fixed" ]]; then
  if [[ -z "${SUBDOMAIN}" ]]; then
    SUBDOMAIN="${PROJECT_SLUG}-${USER_SLUG}"
  fi
  SUBDOMAIN="$(sanitize_dns_label "${SUBDOMAIN}")"
  if [[ -z "${SUBDOMAIN}" ]]; then
    echo "ERROR: SUBDOMAIN invalid" >&2
    exit 1
  fi
  HOSTNAME="${SUBDOMAIN}.${BASE_DOMAIN}"
  PUBLIC_URL="${PUBLIC_SCHEME}://${HOSTNAME}"
fi

if [[ "${DOMAIN_MODE}" == "fixed" ]]; then
  cleanup_other_ports_for_same_project
fi

created_tunnel_id=""
if [[ -z "${TUNNEL_ID}" || -z "${TUNNEL_TOKEN}" ]]; then
  # No machine tunnel yet — create one and save it
  if [[ "${DOMAIN_MODE}" == "fixed" ]]; then
    payload="$($PYTHON - "${USER_SLUG}-machine" <<'PY'
import json, sys
name = sys.argv[1]
print(json.dumps({"name": name}))
PY
)"
    resp="$(api_post "${CONTROL_API_BASE}/api/tunnels" "${payload}")"
    TUNNEL_ID="$(echo "${resp}" | json_get tunnel.id)"
    TUNNEL_TOKEN="$(echo "${resp}" | json_get tunnel.token)"
    created_tunnel_id="${TUNNEL_ID}"
    machine_state_write "${TUNNEL_ID}" "${TUNNEL_TOKEN}"
    echo "[tunnel] created new machine tunnel: ${TUNNEL_ID}"
  else
    payload="$($PYTHON - "${USER_ID}" "${PROJECT_NAME}" "${TARGET}" "${BASE_DOMAIN}" <<'PY'
import json
import sys
user_id, project, target, base_domain = sys.argv[1:5]
print(json.dumps({
    "user_id": user_id,
    "project": project,
    "target": target,
    "base_domain": base_domain,
}))
PY
)"
    resp="$(api_post "${CONTROL_API_BASE}/api/sessions/register" "${payload}")"
    TUNNEL_ID="$(echo "${resp}" | json_get tunnel.id)"
    TUNNEL_TOKEN="$(echo "${resp}" | json_get tunnel.token)"
    HOSTNAME="$(echo "${resp}" | json_get route.hostname)"
    PUBLIC_URL="$(echo "${resp}" | json_get public_url)"
    machine_state_write "${TUNNEL_ID}" "${TUNNEL_TOKEN}"
    echo "[tunnel] created new machine tunnel: ${TUNNEL_ID}"
  fi
fi

if [[ -z "${HOSTNAME}" ]]; then
  echo "ERROR: hostname is empty" >&2
  exit 1
fi
PUBLIC_URL="${PUBLIC_SCHEME}://${HOSTNAME}"

payload="$($PYTHON - "${TUNNEL_ID}" "${HOSTNAME}" "${TARGET}" <<'PY'
import json
import sys
tunnel_id, hostname, target = sys.argv[1:4]
print(json.dumps({
    "tunnel_id": tunnel_id,
    "hostname": hostname,
    "target": target,
    "enabled": True,
    "force": True,
}))
PY
)"

if ! api_post "${CONTROL_API_BASE}/api/routes" "${payload}" >/dev/null; then
  if [[ -n "${created_tunnel_id}" ]]; then
    api_delete "${CONTROL_API_BASE}/api/tunnels/${created_tunnel_id}" || true
  fi
  echo "ERROR: failed to upsert route (${HOSTNAME} -> ${TARGET})" >&2
  exit 1
fi

echo "[1/5] build project"
cd "${PROJECT_DIR}"
if [[ "${SKIP_BUILD}" != "1" ]]; then
  eval "${BUILD_CMD}" >/dev/null
fi

echo "[2/5] write runners"
write_runner_scripts

echo "[3/5] restart local app + ensure machine agent"
stop_by_pid_file "${APP_PID_FILE}"
stop_by_tcp_port "${PROJECT_PORT}"
start_runner "${APP_RUNNER}" "${APP_PID_FILE}" "${APP_LOG}"

# Machine-agent: start only if not already running
if is_machine_agent_running; then
  echo "[machine-agent] already running (pid=$(cat "${MACHINE_AGENT_PID}" 2>/dev/null || echo '?'))"
else
  echo "[machine-agent] starting..."
  write_machine_agent_runner "${TUNNEL_ID}" "${TUNNEL_TOKEN}"
  # Stop any stale process on the admin port
  stop_by_tcp_port "${MACHINE_AGENT_ADMIN_PORT}"
  start_runner "${MACHINE_AGENT_RUNNER}" "${MACHINE_AGENT_PID}" "${MACHINE_AGENT_LOG}"
fi

echo "[4/5] wait local app"
if ! wait_http_ok "http://127.0.0.1:${PROJECT_PORT}/" 60; then
  echo "ERROR: app not ready on ${PROJECT_PORT}" >&2
  tail -n 80 "${APP_LOG}" || true
  exit 1
fi

real_app_pid="$(pid_on_tcp_port "${PROJECT_PORT}" || true)"
if [[ -n "${real_app_pid}" ]]; then
  echo "${real_app_pid}" >"${APP_PID_FILE}"
fi

echo "[5/5] wait machine agent"
if ! wait_http_ok "${MACHINE_AGENT_STATUS_URL}" 25; then
  echo "ERROR: machine agent admin not ready at ${MACHINE_AGENT_ADMIN_ADDR}" >&2
  tail -n 80 "${MACHINE_AGENT_LOG}" || true
  exit 1
fi
# Override AGENT_STATUS_URL so wait_agent_connected uses the machine agent
AGENT_STATUS_URL="${MACHINE_AGENT_STATUS_URL}"
if ! wait_agent_connected 25; then
  echo "WARN: machine agent started but not connected yet" >&2
fi

real_agent_pid="$(pid_on_tcp_port "${MACHINE_AGENT_ADMIN_PORT}" || true)"
if [[ -n "${real_agent_pid}" ]]; then
  echo "${real_agent_pid}" >"${MACHINE_AGENT_PID}"
fi

state_write

echo "[DONE]"
echo "project: ${PROJECT_NAME}"
echo "hostname: ${HOSTNAME}"
echo "public_url: ${PUBLIC_URL}"
echo "tunnel_id: ${TUNNEL_ID}"
echo "target: http://${TARGET}"
curl -sS -o /dev/null -w "public_probe code=%{http_code} ttfb=%{time_starttransfer}s total=%{time_total}s\n" "${PUBLIC_URL}" || true
echo "state_file: ${STATE_FILE}"
echo "app_log: ${APP_LOG}"
echo "agent_log: ${MACHINE_AGENT_LOG}"
