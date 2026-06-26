#!/usr/bin/env bash
# OpenClaw Gateway Resilience Guard
# Keeps the OpenClaw gateway/channel alive with layered probes and guarded restarts.

set -u

WATCHDOG_VERSION="1.4.4"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

CONFIG_DIR="${XDG_CONFIG_HOME:-${HOME}/.config}/openclaw-gateway-watchdog"
CONFIG_FILE="${WATCHDOG_CONFIG:-${CONFIG_DIR}/watchdog.env}"
STATE_DIR="${XDG_STATE_HOME:-${HOME}/.local/state}/openclaw-gateway-watchdog"
LOG_FILE="${WATCHDOG_LOG_FILE:-${STATE_DIR}/watchdog.log}"
RUNTIME_BASE="${XDG_RUNTIME_DIR:-/tmp}"
RUNTIME_DIR="${RUNTIME_BASE}/openclaw-gateway-watchdog"
LOCK_DIR="${RUNTIME_DIR}/lock"

# Defaults are intentionally useful out of the box. Users can override them in
# ~/.config/openclaw-gateway-watchdog/watchdog.env or environment variables.
GATEWAY_SERVICE="${GATEWAY_SERVICE:-openclaw-gateway}"
GATEWAY_HEALTH_URL="${GATEWAY_HEALTH_URL:-http://127.0.0.1:18789/healthz}"
GATEWAY_HOST="${GATEWAY_HOST:-127.0.0.1}"
GATEWAY_PORT="${GATEWAY_PORT:-18789}"
CHANNEL_URL="${CHANNEL_URL:-https://ilinkai.weixin.qq.com}"
NETWORK_URLS="${NETWORK_URLS:-https://www.baidu.com https://www.qq.com https://api.weixin.qq.com}"
RESTART_COMMAND="${RESTART_COMMAND:-}"
OPENCLAW_NATIVE_PROBES="${OPENCLAW_NATIVE_PROBES:-auto}"
OPENCLAW_HEALTH_TIMEOUT_MS="${OPENCLAW_HEALTH_TIMEOUT_MS:-12000}"
OPENCLAW_GATEWAY_STRICT="${OPENCLAW_GATEWAY_STRICT:-0}"
OPENCLAW_CHANNELS_PROBE="${OPENCLAW_CHANNELS_PROBE:-1}"
OPENCLAW_DIAG_ENABLED="${OPENCLAW_DIAG_ENABLED:-1}"
OPENCLAW_DIAG_INTERVAL="${OPENCLAW_DIAG_INTERVAL:-300}"
OPENCLAW_LOG_SCAN_ENABLED="${OPENCLAW_LOG_SCAN_ENABLED:-1}"
OPENCLAW_LOG_LIMIT="${OPENCLAW_LOG_LIMIT:-200}"
OPENCLAW_LOG_SIGNAL_LIMIT="${OPENCLAW_LOG_SIGNAL_LIMIT:-40}"
OPENCLAW_LOG_TIMEOUT_MS="${OPENCLAW_LOG_TIMEOUT_MS:-15000}"
OPENCLAW_LOG_WARN_PATTERNS="${OPENCLAW_LOG_WARN_PATTERNS:-fetch failed|fetch timeout|LLM idle timeout|model silent|chat/completions|providerRuntimeFailureKind|ECONNRESET|ECONNREFUSED|ETIMEDOUT|ENOTFOUND|socket hang up|TLS|CERT_|proxy|429|rate limit|quota|unauthorized|invalid api key|embedded abort settle timed out|embedded run failover decision|memory-core: narrative generation ended with status=timeout|dreaming.*timeout|health-monitor|event loop|degraded|restartPending|session expired|errcode=-14|Monitor.*stopped|monitor.*ended|config hot reload|config change detected|cron.*error|task.*failed}"
OPENCLAW_DIAG_ACTION="${OPENCLAW_DIAG_ACTION:-log}"
OPENCLAW_DIAG_FAILURES_BEFORE_ACTION="${OPENCLAW_DIAG_FAILURES_BEFORE_ACTION:-2}"
OPENCLAW_DIAG_COMMAND="${OPENCLAW_DIAG_COMMAND:-}"
DASHBOARD_ENABLED="${DASHBOARD_ENABLED:-1}"
DASHBOARD_HOST="${DASHBOARD_HOST:-127.0.0.1}"
DASHBOARD_PORT="${DASHBOARD_PORT:-18790}"
DASHBOARD_ACTIONS_ENABLED="${DASHBOARD_ACTIONS_ENABLED:-0}"
DASHBOARD_TOKEN="${DASHBOARD_TOKEN:-}"
DASHBOARD_DIR="${DASHBOARD_DIR:-${SCRIPT_DIR}/dashboard}"
DASHBOARD_PYTHON="${DASHBOARD_PYTHON:-}"
MODEL_PROBE_ENABLED="${MODEL_PROBE_ENABLED:-0}"
MODEL_EDGE_PROBE_ENABLED="${MODEL_EDGE_PROBE_ENABLED:-1}"
MODEL_PROBE_INTERVAL="${MODEL_PROBE_INTERVAL:-1800}"
MODEL_PROBE_TIMEOUT="${MODEL_PROBE_TIMEOUT:-120}"
MODEL_PROBE_FAILURES_BEFORE_ACTION="${MODEL_PROBE_FAILURES_BEFORE_ACTION:-2}"
MODEL_PROBE_ACTION="${MODEL_PROBE_ACTION:-log}"
MODEL_PROBE_COMMAND="${MODEL_PROBE_COMMAND:-}"
MODEL_PROBE_MODEL="${MODEL_PROBE_MODEL:-}"
MODEL_PROBE_THINKING="${MODEL_PROBE_THINKING:-off}"
MODEL_PROBE_SESSION_ID="${MODEL_PROBE_SESSION_ID:-watchdog-model-probe}"
MODEL_PROBE_MESSAGE="${MODEL_PROBE_MESSAGE:-Reply with exactly OK.}"

BASE_INTERVAL="${BASE_INTERVAL:-60}"
NIGHT_INTERVAL="${NIGHT_INTERVAL:-300}"
MAX_INTERVAL="${MAX_INTERVAL:-1800}"
CONNECT_TIMEOUT="${CONNECT_TIMEOUT:-5}"
MAX_TIME="${MAX_TIME:-10}"
CHANNEL_FAILURES_BEFORE_RESTART="${CHANNEL_FAILURES_BEFORE_RESTART:-2}"
SUCCESS_COUNT_TO_RESET="${SUCCESS_COUNT_TO_RESET:-5}"
MAX_RESTARTS_PER_HOUR="${MAX_RESTARTS_PER_HOUR:-6}"
POST_RESTART_SLEEP="${POST_RESTART_SLEEP:-30}"

if [ -f "$CONFIG_FILE" ]; then
  # shellcheck disable=SC1090
  . "$CONFIG_FILE"
fi

mkdir -p "$STATE_DIR" "$RUNTIME_DIR" "$(dirname "$LOG_FILE")"

cleanup() {
  rmdir "$LOCK_DIR" 2>/dev/null || true
}

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "Another watchdog instance is already running: $LOCK_DIR" >&2
  exit 0
fi
trap cleanup EXIT INT TERM

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$LOG_FILE"
}

rotate_log_if_needed() {
  local max_bytes="${MAX_LOG_BYTES:-1048576}"
  [ -f "$LOG_FILE" ] || return 0
  local size
  size=$(wc -c <"$LOG_FILE" 2>/dev/null || echo 0)
  if [ "${size:-0}" -gt "$max_bytes" ]; then
    mv "$LOG_FILE" "${LOG_FILE}.1" 2>/dev/null || : >"$LOG_FILE"
    log "LOG: rotated because it exceeded ${max_bytes} bytes"
  fi
}

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

native_probes_enabled() {
  case "${OPENCLAW_NATIVE_PROBES:-auto}" in
    0|false|False|FALSE|off|Off|OFF|no|No|NO) return 1 ;;
    *) return 0 ;;
  esac
}

probe_output_has() {
  local file="$1"
  local pattern="$2"
  [ -f "$file" ] && grep -Eiq "$pattern" "$file"
}

log_probe_tail() {
  local label="$1"
  local file="$2"
  [ -f "$file" ] || return 0
  local line
  line=$(grep -Eiv '^[[:space:]]*$' "$file" | head -n 1 | cut -c 1-220)
  [ -n "$line" ] && log "${label}: ${line}"
}

probe_output_is_unsupported() {
  local file="$1"
  probe_output_has "$file" 'unknown command|unknown option|unknown argument|unrecognized option|not recognized|invalid command'
}

run_openclaw_probe() {
  local label="$1"
  local outfile="$2"
  shift 2
  "$@" >"$outfile" 2>&1
}

check_openclaw_gateway_rpc() {
  native_probes_enabled || return 2
  have_cmd openclaw || return 2

  local out_file="${STATE_DIR}/last-openclaw-gateway-status.json"
  if run_openclaw_probe "gateway status" "$out_file" \
    openclaw gateway status --json --require-rpc --timeout "$OPENCLAW_HEALTH_TIMEOUT_MS"; then
    if probe_output_has "$out_file" '"ok"[[:space:]]*:[[:space:]]*false'; then
      log "OPENCLAW GATEWAY FAIL: gateway status reported ok=false"
      log_probe_tail "OPENCLAW GATEWAY DETAIL" "$out_file"
      return 1
    fi
    if probe_output_has "$out_file" '"degraded"[[:space:]]*:[[:space:]]*true'; then
      log "OPENCLAW GATEWAY WARN: gateway RPC probe is reachable but degraded"
      [ "${OPENCLAW_GATEWAY_STRICT:-0}" = "1" ] && return 1
    fi
    return 0
  fi

  local rc=$?
  if [ "${OPENCLAW_NATIVE_PROBES:-auto}" = "auto" ] && probe_output_is_unsupported "$out_file"; then
    log "OPENCLAW GATEWAY WARN: native gateway status probe is unsupported; falling back to local probes"
    return 2
  fi
  log "OPENCLAW GATEWAY WARN: openclaw gateway status --require-rpc failed (rc=${rc}); falling back to local probes"
  log_probe_tail "OPENCLAW GATEWAY DETAIL" "$out_file"
  return 2
}

check_openclaw_health_snapshot() {
  native_probes_enabled || return 2
  have_cmd openclaw || return 2

  local out_file="${STATE_DIR}/last-openclaw-health.json"
  if run_openclaw_probe "health" "$out_file" \
    openclaw health --json --verbose --timeout "$OPENCLAW_HEALTH_TIMEOUT_MS"; then
    if probe_output_has "$out_file" '"ok"[[:space:]]*:[[:space:]]*false'; then
      log "OPENCLAW CHANNEL FAIL: health snapshot reported ok=false"
      log_probe_tail "OPENCLAW HEALTH DETAIL" "$out_file"
      return 1
    fi
    return 0
  fi

  local rc=$?
  if [ "${OPENCLAW_NATIVE_PROBES:-auto}" = "auto" ] && probe_output_is_unsupported "$out_file"; then
    log "OPENCLAW CHANNEL WARN: native health probe is unsupported; falling back to URL probes"
    return 2
  fi
  log "OPENCLAW CHANNEL FAIL: openclaw health live probe failed (rc=${rc})"
  log_probe_tail "OPENCLAW HEALTH DETAIL" "$out_file"
  return 1
}

check_openclaw_status_deep() {
  native_probes_enabled || return 2
  have_cmd openclaw || return 2

  local out_file="${STATE_DIR}/last-openclaw-status-deep.txt"
  if run_openclaw_probe "status deep" "$out_file" \
    openclaw status --deep; then
    if probe_output_has "$out_file" 'logged[ -]?out|loggedOut|disconnected|unhealthy|healthy[[:space:]]*:[[:space:]]*false|probe[[:space:]-]*failed|status[[:space:]]*:[[:space:]]*(409|410|411|412|413|414|415|500|501|502|503|504|515)|timeout'; then
      log "OPENCLAW CHANNEL FAIL: status --deep contains failure keywords"
      log_probe_tail "OPENCLAW STATUS DETAIL" "$out_file"
      return 1
    fi
    return 0
  fi

  local rc=$?
  if [ "${OPENCLAW_NATIVE_PROBES:-auto}" = "auto" ] && probe_output_is_unsupported "$out_file"; then
    log "OPENCLAW CHANNEL WARN: status --deep is unsupported; falling back to other probes"
    return 2
  fi
  log "OPENCLAW CHANNEL FAIL: openclaw status --deep failed (rc=${rc})"
  log_probe_tail "OPENCLAW STATUS DETAIL" "$out_file"
  return 1
}

check_openclaw_channels_status() {
  native_probes_enabled || return 2
  have_cmd openclaw || return 2
  [ "${OPENCLAW_CHANNELS_PROBE:-1}" = "1" ] || return 2

  local out_file="${STATE_DIR}/last-openclaw-channels-status.txt"
  if run_openclaw_probe "channels status" "$out_file" \
    openclaw channels status --probe; then
    if probe_output_has "$out_file" 'logged[ -]?out|loggedOut|disconnected|unhealthy|healthy[[:space:]]*:[[:space:]]*false|probe[[:space:]-]*failed|status[[:space:]]*:[[:space:]]*(409|410|411|412|413|414|415|500|501|502|503|504|515)|timeout'; then
      log "OPENCLAW CHANNEL FAIL: channels status contains failure keywords"
      log_probe_tail "OPENCLAW CHANNEL DETAIL" "$out_file"
      return 1
    fi
    return 0
  fi

  local rc=$?
  if [ "${OPENCLAW_NATIVE_PROBES:-auto}" = "auto" ] && probe_output_is_unsupported "$out_file"; then
    log "OPENCLAW CHANNEL WARN: native channels probe is unsupported; falling back to URL probes"
    return 2
  fi
  log "OPENCLAW CHANNEL FAIL: openclaw channels status --probe failed (rc=${rc})"
  log_probe_tail "OPENCLAW CHANNEL DETAIL" "$out_file"
  return 1
}

http_probe() {
  local url="$1"
  local code
  code=$(curl -L -sS -o /dev/null -w '%{http_code}' \
    --connect-timeout "$CONNECT_TIMEOUT" --max-time "$MAX_TIME" "$url" 2>/dev/null || printf '000')

  case "$code" in
    2??|3??|4??) return 0 ;;
    *) return 1 ;;
  esac
}

tcp_probe() {
  [ -n "${GATEWAY_HOST:-}" ] || return 1
  [ -n "${GATEWAY_PORT:-}" ] || return 1
  ( : >"/dev/tcp/${GATEWAY_HOST}/${GATEWAY_PORT}" ) >/dev/null 2>&1
}

systemd_user_available() {
  have_cmd systemctl && systemctl --user status >/dev/null 2>&1
}

service_unit_name() {
  case "$GATEWAY_SERVICE" in
    *.service) printf '%s\n' "$GATEWAY_SERVICE" ;;
    *) printf '%s.service\n' "$GATEWAY_SERVICE" ;;
  esac
}

gateway_unit_exists() {
  local unit
  systemd_user_available || return 1
  unit=$(service_unit_name)
  [ "$(systemctl --user show "$unit" -p LoadState --value 2>/dev/null || echo not-found)" != "not-found" ]
}

gateway_unit_active() {
  systemd_user_available || return 1
  systemctl --user is-active --quiet "$GATEWAY_SERVICE" >/dev/null 2>&1
}

check_gateway() {
  local native_status=2
  check_openclaw_gateway_rpc
  native_status=$?
  case "$native_status" in
    0) return 0 ;;
    1) return 1 ;;
  esac

  if [ -n "${GATEWAY_HEALTH_URL:-}" ] && http_probe "$GATEWAY_HEALTH_URL"; then
    return 0
  fi

  if tcp_probe; then
    return 0
  fi

  if gateway_unit_exists; then
    if gateway_unit_active; then
      log "GATEWAY WARN: service is active, but local health/port probe failed"
      return 2
    fi
    log "GATEWAY FAIL: service ${GATEWAY_SERVICE} is not active"
    return 1
  fi

  if have_cmd pgrep && pgrep -f 'openclaw.*gateway' >/dev/null 2>&1; then
    log "GATEWAY WARN: process exists, but local health/port probe failed"
    return 2
  fi

  log "GATEWAY FAIL: no healthy gateway detected"
  return 1
}

check_channel() {
  local native_status=2
  check_openclaw_health_snapshot
  native_status=$?
  case "$native_status" in
    0) return 0 ;;
    1)
      check_openclaw_status_deep >/dev/null 2>&1 || true
      check_openclaw_channels_status >/dev/null 2>&1 || true
      return 1
      ;;
    2)
      check_openclaw_status_deep
      native_status=$?
      [ "$native_status" -eq 0 ] && return 0
      [ "$native_status" -eq 1 ] && return 1
      check_openclaw_channels_status
      native_status=$?
      [ "$native_status" -eq 0 ] && return 0
      [ "$native_status" -eq 1 ] && return 1
      ;;
  esac

  http_probe "$CHANNEL_URL"
}

check_network() {
  local success=0
  local total=0
  local url

  for url in $NETWORK_URLS; do
    total=$((total + 1))
    if http_probe "$url"; then
      success=$((success + 1))
    fi
  done

  if [ "$success" -gt 0 ]; then
    return 0
  fi

  log "NETWORK FAIL: all ${total} network probes failed"
  return 1
}

model_probe_enabled() {
  case "${MODEL_PROBE_ENABLED:-0}" in
    1|true|True|TRUE|on|On|ON|yes|Yes|YES) return 0 ;;
    *) return 1 ;;
  esac
}

diag_enabled() {
  case "${OPENCLAW_DIAG_ENABLED:-1}" in
    0|false|False|FALSE|off|Off|OFF|no|No|NO) return 1 ;;
    *) return 0 ;;
  esac
}

log_scan_enabled() {
  case "${OPENCLAW_LOG_SCAN_ENABLED:-1}" in
    0|false|False|FALSE|off|Off|OFF|no|No|NO) return 1 ;;
    *) return 0 ;;
  esac
}

dashboard_enabled() {
  case "${DASHBOARD_ENABLED:-1}" in
    0|false|False|FALSE|off|Off|OFF|no|No|NO) return 1 ;;
    *) return 0 ;;
  esac
}

dashboard_actions_enabled() {
  case "${DASHBOARD_ACTIONS_ENABLED:-1}" in
    1|true|True|TRUE|on|On|ON|yes|Yes|YES) return 0 ;;
    *) return 1 ;;
  esac
}

model_edge_probe_enabled() {
  case "${MODEL_EDGE_PROBE_ENABLED:-1}" in
    0|false|False|FALSE|off|Off|OFF|no|No|NO) return 1 ;;
    *) return 0 ;;
  esac
}

json_field() {
  local file="$1"
  local key="$2"
  grep -Eo "\"${key}\"[[:space:]]*:[[:space:]]*\"[^\"]+\"" "$file" 2>/dev/null |
    head -n 1 |
    sed -E "s/.*\"${key}\"[[:space:]]*:[[:space:]]*\"([^\"]+)\".*/\\1/"
}

model_probe_due() {
  local now="$1"
  local last="$2"
  [ "$last" -eq 0 ] && return 0
  [ "$((now - last))" -ge "${MODEL_PROBE_INTERVAL:-1800}" ]
}

interval_due() {
  local now="$1"
  local last="$2"
  local interval="$3"
  [ "$last" -eq 0 ] && return 0
  [ "$((now - last))" -ge "$interval" ]
}

dashboard_pid_file() {
  printf '%s/dashboard.pid' "$STATE_DIR"
}

find_dashboard_python() {
  if [ -n "${DASHBOARD_PYTHON:-}" ] && have_cmd "$DASHBOARD_PYTHON"; then
    printf '%s\n' "$DASHBOARD_PYTHON"
    return 0
  fi
  if have_cmd python3; then
    printf '%s\n' "python3"
    return 0
  fi
  if have_cmd python; then
    printf '%s\n' "python"
    return 0
  fi
  return 1
}

dashboard_alive() {
  local pid_file
  local pid
  pid_file="$(dashboard_pid_file)"
  [ -f "$pid_file" ] || return 1
  pid="$(cat "$pid_file" 2>/dev/null || true)"
  [ -n "$pid" ] || return 1
  kill -0 "$pid" 2>/dev/null
}

start_dashboard() {
  dashboard_enabled || return 0
  dashboard_alive && return 0
  [ -f "${DASHBOARD_DIR}/server.py" ] || {
    log "DASHBOARD WARN: ${DASHBOARD_DIR}/server.py not found; dashboard disabled for this run"
    DASHBOARD_ENABLED=0
    return 0
  }

  local python_bin
  python_bin="$(find_dashboard_python 2>/dev/null || true)"
  [ -n "$python_bin" ] || {
    log "DASHBOARD WARN: python3/python not found; dashboard disabled for this run"
    DASHBOARD_ENABLED=0
    return 0
  }

  local actions="0"
  dashboard_actions_enabled && actions="1"
  WATCHDOG_STATE_DIR="$STATE_DIR" \
  WATCHDOG_CONFIG_FILE="$CONFIG_FILE" \
  WATCHDOG_DASHBOARD_HOST="$DASHBOARD_HOST" \
  WATCHDOG_DASHBOARD_PORT="$DASHBOARD_PORT" \
  WATCHDOG_DASHBOARD_ACTIONS_ENABLED="$actions" \
  WATCHDOG_DASHBOARD_TOKEN="$DASHBOARD_TOKEN" \
    nohup "$python_bin" "${DASHBOARD_DIR}/server.py" >>"${STATE_DIR}/dashboard.log" 2>&1 &
  printf '%s\n' "$!" >"$(dashboard_pid_file)"
  log "DASHBOARD: http://${DASHBOARD_HOST}:${DASHBOARD_PORT}"
}

log_signal_categories() {
  local file="$1"
  local categories=""
  [ -s "$file" ] || return 0

  if probe_output_has "$file" 'fetch failed|fetch timeout|LLM idle timeout|model silent|chat/completions|providerRuntimeFailureKind.*timeout'; then
    categories="${categories},provider_timeout"
  fi
  if probe_output_has "$file" 'ECONNRESET|ECONNREFUSED|ETIMEDOUT|ENOTFOUND|socket hang up|TLS|CERT_|proxy'; then
    categories="${categories},proxy_or_network"
  fi
  if probe_output_has "$file" '429|rate limit|too many requests|quota'; then
    categories="${categories},provider_rate_limit"
  fi
  if probe_output_has "$file" '401|403|unauthorized|forbidden|invalid api key|auth'; then
    categories="${categories},provider_auth"
  fi
  if probe_output_has "$file" 'embedded abort settle timed out'; then
    categories="${categories},abort_stuck"
  fi
  if probe_output_has "$file" 'memory-core: narrative generation ended with status=timeout|dreaming.*timeout'; then
    categories="${categories},memory_dream_timeout"
  fi
  if probe_output_has "$file" 'restartPending|session expired|errcode=-14|Monitor.*stopped|monitor.*ended'; then
    categories="${categories},channel_session"
  fi
  if probe_output_has "$file" 'event loop|degraded|health-monitor'; then
    categories="${categories},gateway_degraded"
  fi
  if probe_output_has "$file" 'config hot reload|config change detected'; then
    categories="${categories},config_reload"
  fi
  if probe_output_has "$file" 'cron.*error|task.*failed|run failover decision'; then
    categories="${categories},task_runtime"
  fi
  if probe_output_has "$file" '\bwarn\b|\bwarning\b|\berror\b|\bfailed\b|\btimeout\b'; then
    categories="${categories},openclaw_warning"
  fi

  categories="${categories#,}"
  [ -n "$categories" ] && printf '%s\n' "$categories"
}

scan_openclaw_logs() {
  log_scan_enabled || return 2
  have_cmd openclaw || return 2

  local log_file="${STATE_DIR}/last-openclaw-logs.txt"
  local signals_file="${STATE_DIR}/last-openclaw-log-signals.txt"
  local categories_file="${STATE_DIR}/last-openclaw-log-signal-categories.txt"
  local fingerprint_file="${STATE_DIR}/last-openclaw-log-signals.cksum"
  local fingerprint=""
  local previous=""
  local matches=0
  local categories=""

  openclaw logs --plain --limit "$OPENCLAW_LOG_LIMIT" --timeout "$OPENCLAW_LOG_TIMEOUT_MS" >"$log_file" 2>&1 || return 2
  grep -Ei "(${OPENCLAW_LOG_WARN_PATTERNS})|\\b(warn|warning|error|failed|timeout)\\b" "$log_file" 2>/dev/null | tail -n "$OPENCLAW_LOG_SIGNAL_LIMIT" >"$signals_file" || true
  [ -s "$signals_file" ] || return 0

  fingerprint=$(cksum "$signals_file" 2>/dev/null | awk '{print $1 ":" $2}')
  previous=$(cat "$fingerprint_file" 2>/dev/null || true)
  [ "$fingerprint" = "$previous" ] && return 0
  printf '%s\n' "$fingerprint" >"$fingerprint_file"

  matches=$(wc -l <"$signals_file" 2>/dev/null || echo 0)
  categories=$(log_signal_categories "$signals_file")
  [ -n "$categories" ] || categories="unknown"
  printf '%s\n' "$categories" >"$categories_file"
  log "OPENCLAW LOG WARN: categories=${categories} matches=${matches} fingerprint=${fingerprint}"
  log_probe_tail "OPENCLAW LOG DETAIL" "$signals_file"
  return 1
}

run_openclaw_diagnostics() {
  diag_enabled || return 2
  native_probes_enabled || return 2
  have_cmd openclaw || return 2

  local degraded=0
  local signals=0
  local summary_file="${STATE_DIR}/last-openclaw-diagnostics.jsonl"
  local gateway_file="${STATE_DIR}/last-openclaw-gateway-status.json"
  local health_file="${STATE_DIR}/last-openclaw-health.json"
  local models_file="${STATE_DIR}/last-openclaw-model-status.json"
  local status_file="${STATE_DIR}/last-openclaw-status-deep.txt"
  local categories_file="${STATE_DIR}/last-openclaw-log-signal-categories.txt"
  local categories="none"

  openclaw gateway status --json --require-rpc --timeout "$OPENCLAW_HEALTH_TIMEOUT_MS" >"$gateway_file" 2>&1 || true
  openclaw health --json --verbose --timeout "$OPENCLAW_HEALTH_TIMEOUT_MS" >"$health_file" 2>&1 || true
  openclaw models status --json >"$models_file" 2>&1 || true
  openclaw status --deep --no-color >"$status_file" 2>&1 || true

  if probe_output_has "$health_file" '"degraded"[[:space:]]*:[[:space:]]*true|"ok"[[:space:]]*:[[:space:]]*false'; then
    degraded=1
    log "OPENCLAW DIAG WARN: health snapshot reports degraded or not ok"
    log_probe_tail "OPENCLAW HEALTH DETAIL" "$health_file"
  fi
  if probe_output_has "$models_file" '"fallbacks"[[:space:]]*:[[:space:]]*\[\]'; then
    log "OPENCLAW DIAG INFO: no model fallbacks configured"
  fi

  scan_openclaw_logs
  case "$?" in
    1)
      signals=1
      categories=$(cat "$categories_file" 2>/dev/null || printf 'unknown')
      ;;
  esac

  printf '{"ts":"%s","healthDegraded":%s,"newLogSignals":%s,"categories":"%s"}\n' \
    "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$degraded" "$signals" "$categories" >>"$summary_file"

  if [ "$degraded" -eq 1 ] || [ "$signals" -eq 1 ]; then
    return 1
  fi
  return 0
}

handle_diag_failure() {
  local failures="$1"
  if [ "$failures" -lt "${OPENCLAW_DIAG_FAILURES_BEFORE_ACTION:-2}" ]; then
    return 0
  fi

  if ! check_network; then
    log "OPENCLAW DIAG SAFEGUARD: general network probes failed; skip diagnostic action"
    return 0
  fi

  case "${OPENCLAW_DIAG_ACTION:-log}" in
    restart)
      log "OPENCLAW DIAG ACTION: restart gateway after ${failures} consecutive diagnostic warnings"
      restart_gateway || true
      ;;
    command)
      if [ -n "${OPENCLAW_DIAG_COMMAND:-}" ]; then
        log "OPENCLAW DIAG ACTION: ${OPENCLAW_DIAG_COMMAND}"
        sh -c "$OPENCLAW_DIAG_COMMAND" >>"$LOG_FILE" 2>&1 || log "OPENCLAW DIAG ACTION FAIL: command returned non-zero"
      else
        log "OPENCLAW DIAG ACTION WARN: OPENCLAW_DIAG_ACTION=command but OPENCLAW_DIAG_COMMAND is empty"
      fi
      ;;
    log|*)
      log "OPENCLAW DIAG ACTION: log-only after ${failures} consecutive diagnostic warnings"
      ;;
  esac
}

probe_model_api_edge() {
  model_edge_probe_enabled || return 2
  have_cmd openclaw || return 2
  have_cmd curl || return 2

  local status_file="${STATE_DIR}/last-openclaw-model-status.json"
  local provider_file="${STATE_DIR}/last-openclaw-model-provider.json"
  local model="${MODEL_PROBE_MODEL:-}"
  local provider=""
  local base_url=""
  local metrics=""
  local rc=0

  if [ -z "$model" ]; then
    openclaw models status --json >"$status_file" 2>&1 || return 2
    model=$(json_field "$status_file" "defaultModel")
  fi
  [ -n "$model" ] || return 2
  case "$model" in
    */*) provider="${model%%/*}" ;;
    *) return 2 ;;
  esac

  openclaw config get "models.providers.${provider}" >"$provider_file" 2>&1 || return 2
  base_url=$(json_field "$provider_file" "baseUrl")
  [ -n "$base_url" ] || return 2

  metrics=$(curl -L -sS -o /dev/null \
    -w 'code=%{http_code} dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} start=%{time_starttransfer} total=%{time_total}' \
    --connect-timeout "$CONNECT_TIMEOUT" --max-time "$MAX_TIME" "$base_url" 2>&1)
  rc=$?
  printf '%s\n' "$metrics" >"${STATE_DIR}/last-model-api-edge-probe.txt"

  if [ "$rc" -eq 0 ] && printf '%s' "$metrics" | grep -Eq 'code=(2|3|4)[0-9][0-9]'; then
    log "MODEL API EDGE OK: provider=${provider} model=${model} base=${base_url} ${metrics}"
    return 0
  fi

  log "MODEL API EDGE FAIL: provider=${provider} model=${model} base=${base_url} rc=${rc} ${metrics}"
  return 1
}

run_model_probe() {
  model_probe_enabled || return 2
  have_cmd openclaw || {
    log "MODEL PROBE WARN: openclaw CLI not found; skip model probe"
    return 2
  }

  local out_file="${STATE_DIR}/last-openclaw-model-probe.json"
  local history_file="${STATE_DIR}/model-probe-history.jsonl"
  local started
  local ended
  local duration
  local rc
  local status
  local provider
  local model
  local args

  started=$(date '+%s')
  probe_model_api_edge >/dev/null 2>&1 || true
  args=(agent --session-id "$MODEL_PROBE_SESSION_ID" --thinking "$MODEL_PROBE_THINKING" --timeout "$MODEL_PROBE_TIMEOUT" --json --message "$MODEL_PROBE_MESSAGE")
  if [ -n "${MODEL_PROBE_MODEL:-}" ]; then
    args=(agent --session-id "$MODEL_PROBE_SESSION_ID" --model "$MODEL_PROBE_MODEL" --thinking "$MODEL_PROBE_THINKING" --timeout "$MODEL_PROBE_TIMEOUT" --json --message "$MODEL_PROBE_MESSAGE")
  fi

  openclaw "${args[@]}" >"$out_file" 2>&1
  rc=$?
  ended=$(date '+%s')
  duration=$((ended - started))

  status=$(json_field "$out_file" "status")
  provider=$(json_field "$out_file" "provider")
  model=$(json_field "$out_file" "model")
  [ -n "$provider" ] || provider="unknown"
  [ -n "$model" ] || model="${MODEL_PROBE_MODEL:-configured-default}"

  if [ "$rc" -eq 0 ] && [ "$status" = "ok" ]; then
    log "MODEL PROBE OK: provider=${provider} model=${model} duration=${duration}s session=${MODEL_PROBE_SESSION_ID}"
    printf '{"ts":"%s","status":"ok","provider":"%s","model":"%s","durationSeconds":%s}\n' \
      "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$provider" "$model" "$duration" >>"$history_file"
    return 0
  fi

  local reason="failed"
  if probe_output_has "$out_file" 'timeout|timed out|idle timeout|fetch timeout'; then
    reason="timeout"
  elif probe_output_has "$out_file" 'rate limit|429|too many requests'; then
    reason="rate_limited"
  elif probe_output_has "$out_file" '401|403|unauthorized|forbidden|invalid api key|auth'; then
    reason="auth"
  elif probe_output_has "$out_file" 'Model override .* not allowed'; then
    reason="config"
  fi

  log "MODEL PROBE FAIL: reason=${reason} rc=${rc} provider=${provider} model=${model} duration=${duration}s timeout=${MODEL_PROBE_TIMEOUT}s"
  log_probe_tail "MODEL PROBE DETAIL" "$out_file"
  printf '{"ts":"%s","status":"fail","reason":"%s","provider":"%s","model":"%s","durationSeconds":%s,"exitCode":%s}\n' \
    "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$reason" "$provider" "$model" "$duration" "$rc" >>"$history_file"
  return 1
}

handle_model_probe_failure() {
  local failures="$1"
  if [ "$failures" -lt "${MODEL_PROBE_FAILURES_BEFORE_ACTION:-2}" ]; then
    return 0
  fi

  if ! check_network; then
    log "MODEL PROBE SAFEGUARD: general network probes failed; skip model action"
    return 0
  fi

  case "${MODEL_PROBE_ACTION:-log}" in
    restart)
      log "MODEL PROBE ACTION: restart gateway after ${failures} consecutive model probe failures"
      restart_gateway || true
      ;;
    command)
      if [ -n "${MODEL_PROBE_COMMAND:-}" ]; then
        log "MODEL PROBE ACTION: ${MODEL_PROBE_COMMAND}"
        sh -c "$MODEL_PROBE_COMMAND" >>"$LOG_FILE" 2>&1 || log "MODEL PROBE ACTION FAIL: command returned non-zero"
      else
        log "MODEL PROBE ACTION WARN: MODEL_PROBE_ACTION=command but MODEL_PROBE_COMMAND is empty"
      fi
      ;;
    log|*)
      log "MODEL PROBE ACTION: log-only after ${failures} consecutive model probe failures"
      ;;
  esac
}

restart_count_file() {
  printf '%s/restarts.%s' "$STATE_DIR" "$(date '+%Y%m%d%H')"
}

can_restart_now() {
  local file
  file=$(restart_count_file)
  local count=0
  [ -f "$file" ] && count=$(cat "$file" 2>/dev/null || echo 0)
  [ "${count:-0}" -lt "$MAX_RESTARTS_PER_HOUR" ]
}

record_restart() {
  local file
  file=$(restart_count_file)
  local count=0
  [ -f "$file" ] && count=$(cat "$file" 2>/dev/null || echo 0)
  printf '%s\n' "$((count + 1))" >"$file"
  find "$STATE_DIR" -name 'restarts.*' -type f -mtime +2 -exec rm -f {} + 2>/dev/null || true
}

restart_gateway() {
  if ! can_restart_now; then
    log "CIRCUIT OPEN: restart limit reached (${MAX_RESTARTS_PER_HOUR}/hour); skip restart"
    return 1
  fi

  if [ -n "${RESTART_COMMAND:-}" ]; then
    log "ACTION: ${RESTART_COMMAND}"
    if sh -c "$RESTART_COMMAND" >>"$LOG_FILE" 2>&1; then
      record_restart
      return 0
    fi
    log "ACTION FAIL: restart command returned non-zero"
    return 1
  fi

  if gateway_unit_exists; then
    log "ACTION: systemctl --user restart ${GATEWAY_SERVICE}"
    if systemctl --user restart "$GATEWAY_SERVICE" >>"$LOG_FILE" 2>&1; then
      record_restart
      return 0
    fi
    log "ACTION FAIL: systemd restart failed"
    return 1
  fi

  if have_cmd openclaw; then
    log "ACTION: openclaw gateway restart"
    if openclaw gateway restart >>"$LOG_FILE" 2>&1; then
      record_restart
      return 0
    fi
    log "ACTION FAIL: openclaw gateway restart failed"
    return 1
  fi

  log "ACTION FAIL: set RESTART_COMMAND in ${CONFIG_FILE}; no restart method found"
  return 1
}

backoff_interval() {
  local failures="$1"
  local interval="$BASE_INTERVAL"
  local i=1
  while [ "$i" -lt "$failures" ]; do
    interval=$((interval * 2))
    i=$((i + 1))
    [ "$interval" -ge "$MAX_INTERVAL" ] && break
  done
  [ "$interval" -gt "$MAX_INTERVAL" ] && interval="$MAX_INTERVAL"
  printf '%s\n' "$interval"
}

sleep_interval() {
  local hour
  hour=$(date '+%H')
  hour=$((10#$hour))
  if [ "$hour" -ge 1 ] && [ "$hour" -lt 8 ]; then
    printf '%s\n' "$NIGHT_INTERVAL"
  else
    printf '%s\n' "$BASE_INTERVAL"
  fi
}

main() {
  local fail_count=0
  local success_count=0
  local model_fail_count=0
  local diag_fail_count=0
  local last_diag_at=0
  local last_model_probe_at=0
  local gw_status=0
  local now=0
  local wait_for=0

  log "START: OpenClaw Gateway Resilience Guard ${WATCHDOG_VERSION}"
  log "CONFIG: ${CONFIG_FILE}"
  log "TARGET: channel=${CHANNEL_URL} health=${GATEWAY_HEALTH_URL} service=${GATEWAY_SERVICE} native=${OPENCLAW_NATIVE_PROBES} diag=${OPENCLAW_DIAG_ENABLED} model_probe=${MODEL_PROBE_ENABLED} dashboard=${DASHBOARD_ENABLED}"
  start_dashboard

  while true; do
    rotate_log_if_needed
    start_dashboard
    now=$(date '+%s')

    check_gateway
    gw_status=$?
    if [ "$gw_status" -eq 1 ]; then
      fail_count=$((fail_count + 1))
      success_count=0
      log "CRITICAL: gateway appears down; restarting immediately"
      restart_gateway || true
      sleep "$POST_RESTART_SLEEP"
      continue
    fi

    if diag_enabled && interval_due "$now" "$last_diag_at" "$OPENCLAW_DIAG_INTERVAL"; then
      last_diag_at="$now"
      run_openclaw_diagnostics
      case "$?" in
        0) diag_fail_count=0 ;;
        1)
          diag_fail_count=$((diag_fail_count + 1))
          handle_diag_failure "$diag_fail_count"
          ;;
      esac
    fi

    if model_probe_enabled && model_probe_due "$now" "$last_model_probe_at"; then
      last_model_probe_at="$now"
      run_model_probe
      case "$?" in
        0) model_fail_count=0 ;;
        1)
          model_fail_count=$((model_fail_count + 1))
          handle_model_probe_failure "$model_fail_count"
          ;;
      esac
    fi

    if check_channel; then
      if [ "$fail_count" -gt 0 ]; then
        success_count=$((success_count + 1))
        if [ "$success_count" -ge "$SUCCESS_COUNT_TO_RESET" ]; then
          log "RECOVERED: ${SUCCESS_COUNT_TO_RESET} consecutive channel probes succeeded; failure count reset"
          fail_count=0
          success_count=0
        else
          log "RECOVERING: channel probe succeeded (${success_count}/${SUCCESS_COUNT_TO_RESET})"
        fi
      fi
      sleep "$(sleep_interval)"
      continue
    fi

    fail_count=$((fail_count + 1))
    success_count=0
    log "CHANNEL FAIL: ${CHANNEL_URL} failed (${fail_count}/${CHANNEL_FAILURES_BEFORE_RESTART})"

    if ! check_network; then
      log "SAFEGUARD: looks like global network trouble; wait without restarting gateway"
      sleep "$BASE_INTERVAL"
      continue
    fi

    if [ "$fail_count" -lt "$CHANNEL_FAILURES_BEFORE_RESTART" ]; then
      sleep "$BASE_INTERVAL"
      continue
    fi

    wait_for=$(backoff_interval "$fail_count")
    log "BACKOFF: network is reachable; will re-check channel in ${wait_for}s before restart"
    sleep "$wait_for"

    if check_channel; then
      log "RECOVERED: channel came back before restart"
      fail_count=0
      continue
    fi

    restart_gateway || true
    sleep "$POST_RESTART_SLEEP"
  done
}

main "$@"
