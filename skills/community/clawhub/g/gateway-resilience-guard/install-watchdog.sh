#!/usr/bin/env bash
# Install OpenClaw Gateway Resilience Guard for the current Linux/WSL/macOS user.

set -euo pipefail

SERVICE_NAME="gateway-watchdog"
PLIST_LABEL="ai.clawhub.gateway-resilience-guard"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
INSTALL_DIR="${INSTALL_DIR:-${HOME}/.local/share/openclaw-gateway-watchdog}"
CONFIG_DIR="${XDG_CONFIG_HOME:-${HOME}/.config}/openclaw-gateway-watchdog"
STATE_DIR="${XDG_STATE_HOME:-${HOME}/.local/state}/openclaw-gateway-watchdog"
CONFIG_FILE="${CONFIG_DIR}/watchdog.env"
SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"
SERVICE_FILE="${SYSTEMD_USER_DIR}/${SERVICE_NAME}.service"
LAUNCH_AGENTS_DIR="${HOME}/Library/LaunchAgents"
PLIST_FILE="${LAUNCH_AGENTS_DIR}/${PLIST_LABEL}.plist"

CHANNEL_URL="${CHANNEL_URL:-}"
GATEWAY_SERVICE="${GATEWAY_SERVICE:-}"
GATEWAY_HEALTH_URL="${GATEWAY_HEALTH_URL:-}"
RESTART_COMMAND="${RESTART_COMMAND:-}"
YES=0
NO_START=0

usage() {
  cat <<'USAGE'
Usage:
  bash install-watchdog.sh [options]

Platforms:
  Linux/WSL: installs a user systemd service or direct-run fallback.
  macOS:     installs a LaunchAgent.
  Windows:   use install-watchdog.ps1 from PowerShell instead.

Options:
  --yes                         Non-interactive install with defaults.
  --no-start                    Install files/service but do not start it.
  --channel-url URL             Main channel URL to probe.
  --gateway-service NAME        systemd user service name, default auto/openclaw-gateway.
  --health-url URL              Local gateway health URL, default http://127.0.0.1:18789/healthz.
  --restart-command COMMAND     Explicit command used to restart gateway.
  --install-dir DIR             Override install directory.
  -h, --help                    Show this help.
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --yes|-y) YES=1 ;;
    --no-start) NO_START=1 ;;
    --channel-url) CHANNEL_URL="${2:?missing URL}"; shift ;;
    --gateway-service|--service) GATEWAY_SERVICE="${2:?missing service name}"; shift ;;
    --health-url) GATEWAY_HEALTH_URL="${2:?missing URL}"; shift ;;
    --restart-command) RESTART_COMMAND="${2:?missing command}"; shift ;;
    --install-dir) INSTALL_DIR="${2:?missing dir}"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

case "$(uname -s 2>/dev/null || echo unknown)" in
  MINGW*|MSYS*|CYGWIN*)
    echo "Please run install-watchdog.ps1 from PowerShell on Windows, or run this installer inside WSL/Linux/macOS." >&2
    exit 1
    ;;
esac

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

systemd_user_available() {
  have_cmd systemctl && systemctl --user status >/dev/null 2>&1
}

unit_exists() {
  local unit="$1"
  local service_unit
  systemd_user_available || return 1
  case "$unit" in
    *.service) service_unit="$unit" ;;
    *) service_unit="${unit}.service" ;;
  esac
  [ "$(systemctl --user show "$service_unit" -p LoadState --value 2>/dev/null || echo not-found)" != "not-found" ]
}

detect_gateway_service() {
  local candidate
  for candidate in openclaw-gateway openclaw.gateway openclaw; do
    if unit_exists "$candidate"; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  printf '%s\n' "openclaw-gateway"
}

default_restart_command() {
  local service="$1"
  if unit_exists "$service"; then
    printf 'systemctl --user restart %s\n' "$service"
  elif have_cmd openclaw; then
    printf '%s\n' 'openclaw gateway restart'
  else
    printf 'systemctl --user restart %s\n' "$service"
  fi
}

prompt_default() {
  local prompt="$1"
  local default="$2"
  local answer=""

  if [ "$YES" -eq 1 ] || [ ! -t 0 ]; then
    printf '%s\n' "$default"
    return 0
  fi

  printf '%s [%s]: ' "$prompt" "$default" >&2
  read -r answer || answer=""
  if [ -n "$answer" ]; then
    printf '%s\n' "$answer"
  else
    printf '%s\n' "$default"
  fi
}

require_cmd() {
  if ! have_cmd "$1"; then
    echo "Missing dependency: $1" >&2
    exit 1
  fi
}

xml_escape() {
  printf '%s' "$1" | sed \
    -e 's/&/\&amp;/g' \
    -e 's/</\&lt;/g' \
    -e 's/>/\&gt;/g' \
    -e 's/"/\&quot;/g'
}

generate_token() {
  if have_cmd openssl; then
    openssl rand -hex 24
    return 0
  fi
  if [ -r /dev/urandom ]; then
    od -An -N24 -tx1 /dev/urandom | tr -d ' \n'
    printf '\n'
    return 0
  fi
  printf '%s-%s-%s\n' "$(date '+%s')" "$$" "$RANDOM"
}

require_cmd curl

GATEWAY_SERVICE="${GATEWAY_SERVICE:-$(detect_gateway_service)}"
CHANNEL_URL="${CHANNEL_URL:-$(prompt_default "Channel probe URL" "https://ilinkai.weixin.qq.com")}"
GATEWAY_HEALTH_URL="${GATEWAY_HEALTH_URL:-$(prompt_default "Local gateway health URL" "http://127.0.0.1:18789/healthz")}"
RESTART_COMMAND="${RESTART_COMMAND:-$(default_restart_command "$GATEWAY_SERVICE")}"

mkdir -p "$INSTALL_DIR" "$CONFIG_DIR" "$STATE_DIR"
install -m 0755 "${SCRIPT_DIR}/gateway-watchdog.sh" "${INSTALL_DIR}/gateway-watchdog.sh"
install -m 0755 "${SCRIPT_DIR}/uninstall-watchdog.sh" "${INSTALL_DIR}/uninstall-watchdog.sh"
install -m 0644 "${SCRIPT_DIR}/gateway-watchdog.ps1" "${INSTALL_DIR}/gateway-watchdog.ps1" 2>/dev/null || true
install -m 0644 "${SCRIPT_DIR}/install-watchdog.ps1" "${INSTALL_DIR}/install-watchdog.ps1" 2>/dev/null || true
install -m 0644 "${SCRIPT_DIR}/uninstall-watchdog.ps1" "${INSTALL_DIR}/uninstall-watchdog.ps1" 2>/dev/null || true
[ -f "${SCRIPT_DIR}/README.md" ] && install -m 0644 "${SCRIPT_DIR}/README.md" "${INSTALL_DIR}/README.md"
[ -f "${SCRIPT_DIR}/README.zh-CN.md" ] && install -m 0644 "${SCRIPT_DIR}/README.zh-CN.md" "${INSTALL_DIR}/README.zh-CN.md"
if [ -d "${SCRIPT_DIR}/dashboard" ]; then
  rm -rf "${INSTALL_DIR}/dashboard"
  cp -R "${SCRIPT_DIR}/dashboard" "${INSTALL_DIR}/dashboard"
fi

if [ ! -f "$CONFIG_FILE" ]; then
  DASHBOARD_TOKEN_VALUE="$(generate_token)"
  cat >"$CONFIG_FILE" <<EOF
# OpenClaw Gateway Watchdog config.
# Re-run install-watchdog.sh with flags or edit this file to override defaults.
GATEWAY_SERVICE="${GATEWAY_SERVICE}"
GATEWAY_HEALTH_URL="${GATEWAY_HEALTH_URL}"
GATEWAY_HOST="127.0.0.1"
GATEWAY_PORT="18789"
CHANNEL_URL="${CHANNEL_URL}"
NETWORK_URLS="https://www.baidu.com https://www.qq.com https://api.weixin.qq.com"
RESTART_COMMAND="${RESTART_COMMAND}"
OPENCLAW_NATIVE_PROBES="auto"
OPENCLAW_HEALTH_TIMEOUT_MS="12000"
OPENCLAW_GATEWAY_STRICT="0"
OPENCLAW_CHANNELS_PROBE="1"
OPENCLAW_DIAG_ENABLED="1"
OPENCLAW_DIAG_INTERVAL="300"
OPENCLAW_LOG_SCAN_ENABLED="1"
OPENCLAW_LOG_LIMIT="200"
OPENCLAW_LOG_SIGNAL_LIMIT="40"
OPENCLAW_LOG_TIMEOUT_MS="15000"
OPENCLAW_LOG_WARN_PATTERNS="fetch failed|fetch timeout|LLM idle timeout|model silent|chat/completions|providerRuntimeFailureKind|ECONNRESET|ECONNREFUSED|ETIMEDOUT|ENOTFOUND|socket hang up|TLS|CERT_|proxy|429|rate limit|quota|unauthorized|invalid api key|embedded abort settle timed out|embedded run failover decision|memory-core: narrative generation ended with status=timeout|dreaming.*timeout|health-monitor|event loop|degraded|restartPending|session expired|errcode=-14|Monitor.*stopped|monitor.*ended|config hot reload|config change detected|cron.*error|task.*failed"
OPENCLAW_DIAG_ACTION="log"
OPENCLAW_DIAG_FAILURES_BEFORE_ACTION="2"
OPENCLAW_DIAG_COMMAND=""
DASHBOARD_ENABLED="1"
DASHBOARD_HOST="127.0.0.1"
DASHBOARD_PORT="18790"
DASHBOARD_ACTIONS_ENABLED="1"
DASHBOARD_TOKEN="${DASHBOARD_TOKEN_VALUE}"
DASHBOARD_DIR="${INSTALL_DIR}/dashboard"
MODEL_PROBE_ENABLED="0"
MODEL_EDGE_PROBE_ENABLED="1"
MODEL_PROBE_INTERVAL="1800"
MODEL_PROBE_TIMEOUT="120"
MODEL_PROBE_FAILURES_BEFORE_ACTION="2"
MODEL_PROBE_ACTION="log"
MODEL_PROBE_COMMAND=""
MODEL_PROBE_MODEL=""
MODEL_PROBE_THINKING="off"
MODEL_PROBE_SESSION_ID="watchdog-model-probe"
MODEL_PROBE_MESSAGE="Reply with exactly OK."
BASE_INTERVAL="60"
NIGHT_INTERVAL="300"
MAX_INTERVAL="1800"
CHANNEL_FAILURES_BEFORE_RESTART="2"
SUCCESS_COUNT_TO_RESET="5"
MAX_RESTARTS_PER_HOUR="6"
EOF
else
  echo "Keeping existing config: ${CONFIG_FILE}"
fi

if [ "$(uname -s 2>/dev/null || echo unknown)" = "Darwin" ]; then
  mkdir -p "$LAUNCH_AGENTS_DIR"
  cat >"$PLIST_FILE" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$(xml_escape "$PLIST_LABEL")</string>
  <key>ProgramArguments</key>
  <array>
    <string>$(xml_escape "${INSTALL_DIR}/gateway-watchdog.sh")</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>WATCHDOG_CONFIG</key>
    <string>$(xml_escape "$CONFIG_FILE")</string>
  </dict>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$(xml_escape "${STATE_DIR}/launchd.out.log")</string>
  <key>StandardErrorPath</key>
  <string>$(xml_escape "${STATE_DIR}/launchd.err.log")</string>
</dict>
</plist>
EOF
  if [ "$NO_START" -eq 0 ]; then
    uid=$(id -u)
    launchctl bootout "gui/${uid}" "$PLIST_FILE" >/dev/null 2>&1 || true
    launchctl bootstrap "gui/${uid}" "$PLIST_FILE"
    launchctl enable "gui/${uid}/${PLIST_LABEL}" >/dev/null 2>&1 || true
    launchctl kickstart -k "gui/${uid}/${PLIST_LABEL}" >/dev/null 2>&1 || true
  fi
  echo "Installed macOS LaunchAgent: ${PLIST_LABEL}"
  echo "Status:  launchctl print gui/$(id -u)/${PLIST_LABEL}"
  echo "Logs:    tail -f ${STATE_DIR}/watchdog.log"
else
  mkdir -p "$SYSTEMD_USER_DIR"
  cat >"$SERVICE_FILE" <<EOF
[Unit]
Description=OpenClaw Gateway Resilience Guard
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
Environment=WATCHDOG_CONFIG=${CONFIG_FILE}
ExecStart=${INSTALL_DIR}/gateway-watchdog.sh
Restart=always
RestartSec=20

[Install]
WantedBy=default.target
EOF

  if systemd_user_available; then
    systemctl --user daemon-reload
    systemctl --user enable "$SERVICE_NAME"
    if [ "$NO_START" -eq 0 ]; then
      systemctl --user restart "$SERVICE_NAME"
    fi
    echo "Installed systemd user service: ${SERVICE_NAME}"
    echo "Status:  systemctl --user status ${SERVICE_NAME}"
    echo "Logs:    journalctl --user -u ${SERVICE_NAME} -f"
  else
    echo "User systemd is not available. Installing direct-run fallback."
    if [ "$NO_START" -eq 0 ]; then
      nohup "${INSTALL_DIR}/gateway-watchdog.sh" >>"${STATE_DIR}/bootstrap.log" 2>&1 &
      printf '%s\n' "$!" >"${STATE_DIR}/watchdog.pid"
      echo "Started fallback process with PID $(cat "${STATE_DIR}/watchdog.pid")."
    fi
    echo "For automatic start after reboot, enable user systemd in WSL/Linux and re-run this installer."
  fi
fi

echo ""
echo "Config:  ${CONFIG_FILE}"
echo "Log:     ${STATE_DIR}/watchdog.log"
echo "Dashboard: http://127.0.0.1:18790"
echo "Remove:  bash ${INSTALL_DIR}/uninstall-watchdog.sh"
