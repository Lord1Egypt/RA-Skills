#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Collect mostly read-only OpenClaw security diagnostics.

Usage:
  collect_openclaw_audit.sh --out DIR

The script writes a timestamped folder inside DIR:
  DIR/openclaw-audit-<UTC timestamp>/

Safety:
- Does not run any --fix operations.
- Avoids copying credential files.
- Collects shareable CLI diagnostics plus basic host/network metadata.
- Review outputs before sharing externally.

Examples:
  bash "{baseDir}/scripts/collect_openclaw_audit.sh" --out ./openclaw-audit
EOF
}

OUT_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)
      OUT_DIR="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "${OUT_DIR}" ]]; then
  echo "Missing --out <dir>" >&2
  usage >&2
  exit 2
fi

TS="$(date -u +"%Y%m%dT%H%M%SZ")"
ROOT="${OUT_DIR%/}/openclaw-audit-${TS}"
mkdir -p "${ROOT}"

log() { echo "[collect] $*"; }

write_note() {
  local name="$1"; shift
  printf '%s
' "$*" > "${ROOT}/${name}.txt"
}

run_cmd() {
  local name="$1"; shift
  local file="${ROOT}/${name}.txt"
  log "Running: $*"
  {
    echo "$ $*"
    "$@"
  } > "${file}" 2>&1 || {
    echo "[warn] command failed (continuing): $*" >> "${file}"
    return 0
  }
}

run_cmd_maybe_sudo() {
  local name="$1"; shift
  local file="${ROOT}/${name}.txt"
  if command -v sudo >/dev/null 2>&1; then
    log "Running (sudo -n): $*"
    {
      echo "$ sudo -n $*"
      sudo -n "$@"
    } > "${file}" 2>&1 || {
      echo "[info] sudo not available without password (skipped): $*" >> "${file}"
      return 0
    }
  else
    echo "[info] sudo not installed; skipped: $*" > "${file}"
  fi
}

# Host basics
run_cmd "host_whoami" whoami
run_cmd "host_uname" uname -a

if command -v sw_vers >/dev/null 2>&1; then
  run_cmd "host_sw_vers" sw_vers
  if [[ -x /usr/libexec/ApplicationFirewall/socketfilterfw ]]; then
    run_cmd "macos_firewall_state" /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
    run_cmd "macos_firewall_stealth" /usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode
  fi
  run_cmd "macos_filevault" fdesetup status
fi

if [[ -f /etc/os-release ]]; then
  run_cmd "host_os_release" cat /etc/os-release
fi

# Network listeners
if command -v lsof >/dev/null 2>&1; then
  run_cmd "net_lsof_listen" lsof -nP -iTCP -sTCP:LISTEN
elif command -v ss >/dev/null 2>&1; then
  run_cmd "net_ss_listen" ss -ltnp
elif command -v netstat >/dev/null 2>&1; then
  run_cmd "net_netstat_listen" netstat -anv
fi

# Linux firewall snapshot (best-effort)
if [[ -f /etc/os-release ]]; then
  run_cmd_maybe_sudo "linux_ufw_status" ufw status verbose
  run_cmd_maybe_sudo "linux_nft_ruleset" nft list ruleset
  run_cmd_maybe_sudo "linux_iptables_rules" iptables -S
fi

# Docker / container clues
if command -v docker >/dev/null 2>&1; then
  run_cmd "docker_ps" docker ps --format 'table {{.Names}}	{{.Image}}	{{.Ports}}'
  run_cmd "docker_compose_ps" docker compose ps
  run_cmd "docker_port_openclaw_gateway_18789" docker port openclaw-gateway 18789
fi

if command -v podman >/dev/null 2>&1; then
  run_cmd "podman_ps" podman ps --format 'table {{.Names}}	{{.Image}}	{{.Ports}}'
fi

if ! command -v openclaw >/dev/null 2>&1; then
  write_note "openclaw_missing" "openclaw not found on PATH; collected host-level data only."
  (
    cd "${ROOT}"
    find . -maxdepth 1 -type f -printf '%f\n' | sort > manifest.txt
  )
  log "openclaw missing; collected host info only"
  exit 0
fi

# OpenClaw core diagnostics
run_cmd "openclaw_version" openclaw --version
run_cmd "openclaw_status_all" openclaw status --all
run_cmd "openclaw_status_deep" openclaw status --deep
run_cmd "openclaw_doctor" openclaw doctor
run_cmd "openclaw_gateway_status" openclaw gateway status
run_cmd "openclaw_gateway_probe_json" openclaw gateway probe --json
run_cmd "openclaw_channels_status_probe" openclaw channels status --probe
run_cmd "openclaw_health_json" openclaw health --json
run_cmd "openclaw_security_audit_json" openclaw security audit --json
run_cmd "openclaw_security_audit_deep_json" openclaw security audit --deep --json

# Backup readiness (read-only dry runs)
run_cmd "openclaw_backup_create_dry_run_json" openclaw backup create --dry-run --json
run_cmd "openclaw_backup_only_config_dry_run_json" openclaw backup create --only-config --dry-run --json

# Safe targeted config reads
run_cmd "openclaw_config_gateway_bind" openclaw config get gateway.bind
run_cmd "openclaw_config_gateway_auth_mode" openclaw config get gateway.auth.mode
run_cmd "openclaw_config_gateway_auth_allow_tailscale" openclaw config get gateway.auth.allowTailscale
run_cmd "openclaw_config_gateway_controlui_allowed_origins" openclaw config get gateway.controlUi.allowedOrigins
run_cmd "openclaw_config_gateway_trusted_proxies" openclaw config get gateway.trustedProxies
run_cmd "openclaw_config_gateway_allow_real_ip_fallback" openclaw config get gateway.allowRealIpFallback
run_cmd "openclaw_config_discovery_mdns_mode" openclaw config get discovery.mdns.mode
run_cmd "openclaw_config_session_dm_scope" openclaw config get session.dmScope
run_cmd "openclaw_config_tools_profile" openclaw config get tools.profile
run_cmd "openclaw_config_tools_fs_workspace_only" openclaw config get tools.fs.workspaceOnly
run_cmd "openclaw_config_tools_exec_security" openclaw config get tools.exec.security
run_cmd "openclaw_config_tools_elevated_enabled" openclaw config get tools.elevated.enabled
run_cmd "openclaw_config_channels_defaults_dm_policy" openclaw config get channels.defaults.dmPolicy
run_cmd "openclaw_config_channels_defaults_group_policy" openclaw config get channels.defaults.groupPolicy
run_cmd "openclaw_config_logging_redact_sensitive" openclaw config get logging.redactSensitive

# Supply-chain visibility
run_cmd "openclaw_skills_eligible_json" openclaw skills list --eligible --json
run_cmd "openclaw_plugins_list_json" openclaw plugins list --json

# State directory metadata (do not copy secrets)
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
if [[ -d "${STATE_DIR}" ]]; then
  run_cmd "openclaw_state_ls" ls -la "${STATE_DIR}"
  if command -v stat >/dev/null 2>&1; then
    run_cmd "openclaw_state_stat" stat "${STATE_DIR}" "${STATE_DIR}/openclaw.json"
  fi
fi

(
  cd "${ROOT}"
  find . -maxdepth 1 -type f -printf '%f
' | sort > manifest.txt
)

log "Done. Output: ${ROOT}"
