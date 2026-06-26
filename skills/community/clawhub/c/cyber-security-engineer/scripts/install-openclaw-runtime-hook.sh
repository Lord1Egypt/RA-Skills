#!/usr/bin/env bash
set -euo pipefail

# Installs a sudo shim at ~/.openclaw/bin/sudo (matches live_assessment checks).
# For the shim to be used, OpenClaw's runtime PATH must include ~/.openclaw/bin
# before /usr/bin. This script attempts best-effort PATH injection for macOS
# LaunchAgent installs of the gateway.

log() {
  printf '[cyber-security-engineer] %s\n' "$*"
}

get_uid_and_perms() {
  local path="$1"
  local uid perms

  # GNU stat (Linux)
  if uid="$(stat -c '%u' "${path}" 2>/dev/null)" && perms="$(stat -c '%a' "${path}" 2>/dev/null)"; then
    printf '%s %s\n' "${uid}" "${perms}"
    return 0
  fi

  # BSD stat (macOS)
  if uid="$(stat -f '%u' "${path}" 2>/dev/null)" && perms="$(stat -f '%Lp' "${path}" 2>/dev/null)"; then
    printf '%s %s\n' "${uid}" "${perms}"
    return 0
  fi

  return 1
}

resolve_python() {
  local py
  py="$(command -v python3 || true)"
  if [[ -z "${py}" ]]; then
    log "python3 not found; cannot install shim."
    exit 1
  fi
  echo "${py}"
}

validate_root_bin() {
  local bin="$1"
  if [[ -z "${bin}" || ! -x "${bin}" ]]; then
    return 1
  fi
  # Require absolute path
  if [[ "${bin}" != /* ]]; then
    return 1
  fi
  # Resolve symlinks
  local real
  real="$(readlink -f "${bin}" 2>/dev/null || echo "${bin}")"
  if [[ ! -x "${real}" ]]; then
    return 1
  fi
  # Ensure owned by root and not writable by group/other
  local st
  st="$(get_uid_and_perms "${real}" || true)"
  if [[ -z "${st}" ]]; then
    return 1
  fi
  local uid perms
  uid="$(echo "${st}" | awk '{print $1}')"
  perms="$(echo "${st}" | awk '{print $2}')"
  # uid must be 0
  if [[ "${uid}" != "0" ]]; then
    return 1
  fi
  # perms: no group/other write
  local gow
  gow=$(( 8#${perms} & 8#022 ))
  if [[ "${gow}" -ne 0 ]]; then
    return 1
  fi
  return 0
}

REAL_SUDO="$(command -v sudo || true)"
if [[ -z "${REAL_SUDO}" ]]; then
  log "sudo not found; nothing to install."
  exit 1
fi
if ! validate_root_bin "${REAL_SUDO}"; then
  log "Refusing to install shim: sudo binary failed validation."
  exit 1
fi

PYTHON3="$(resolve_python)"

OPENCLAW_DIR="${HOME}/.openclaw"
BIN_DIR="${OPENCLAW_DIR}/bin"
SKILL_DIR_DEFAULT="${OPENCLAW_DIR}/workspace/skills/cyber-security-engineer"

mkdir -p "${BIN_DIR}"
chmod 700 "${OPENCLAW_DIR}" "${BIN_DIR}" || true

WRAPPER="${BIN_DIR}/sudo"
cat > "${WRAPPER}" <<EOF
#!/usr/bin/env bash
set -euo pipefail

REAL_SUDO_OVERRIDE="\${OPENCLAW_REAL_SUDO:-${REAL_SUDO}}"
PYTHON3_OVERRIDE="\${OPENCLAW_PYTHON3:-${PYTHON3}}"
SKILL_DIR="\${OPENCLAW_CYBER_SKILL_DIR:-${SKILL_DIR_DEFAULT}}"

# Pass-through for sudo bookkeeping.
if [[ \$# -eq 0 ]]; then
  exec "\${REAL_SUDO_OVERRIDE}"
fi
case "\${1:-}" in
  -h|--help|-V|--version|-v|-l|-k)
    exec "\${REAL_SUDO_OVERRIDE}" "\$@"
    ;;
esac

# Refuse non-interactive privilege escalation by default (safety).
if [[ ! -t 0 && "\${OPENCLAW_ALLOW_NONINTERACTIVE_SUDO:-0}" != "1" ]]; then
  echo "[cyber-security-engineer] Refusing non-interactive sudo (set OPENCLAW_ALLOW_NONINTERACTIVE_SUDO=1 to override)." >&2
  exit 2
fi

REASON="\${OPENCLAW_PRIV_REASON:-OpenClaw requested privileged execution}"
# Sanitize reason: strip shell metacharacters to prevent injection
REASON="\$(printf '%s' "\${REASON}" | tr -d '\`\$\\!;|&<>(){}' | head -c 200)"
export OPENCLAW_REAL_SUDO="\${REAL_SUDO_OVERRIDE}"
export OPENCLAW_PYTHON3="\${PYTHON3_OVERRIDE}"
exec "\${PYTHON3_OVERRIDE}" "\${SKILL_DIR}/scripts/guarded_privileged_exec.py" \
  --reason "\${REASON}" \
  --use-sudo \
  -- "\$@"
EOF
chmod 700 "${WRAPPER}"

log "Installed sudo shim: ${WRAPPER}"

if [[ "$(uname -s)" == "Darwin" ]]; then
  PLIST="${HOME}/Library/LaunchAgents/ai.openclaw.gateway.plist"
  if [[ -f "${PLIST}" ]] && command -v /usr/libexec/PlistBuddy >/dev/null 2>&1; then
    if [[ -t 0 && "${OPENCLAW_SKIP_PLIST_CONFIRM:-0}" != "1" ]]; then
      printf '[cyber-security-engineer] This will modify the gateway LaunchAgent PATH in:\n  %s\nProceed? [y/N]: ' "${PLIST}"
      read -r confirm
      if [[ "${confirm}" != "y" && "${confirm}" != "Y" ]]; then
        log "Skipped LaunchAgent PATH modification. You can add ${BIN_DIR} to PATH manually."
        log "Restart the OpenClaw gateway to apply:"
        log "  openclaw gateway restart"
        exit 0
      fi
    fi
    # Ensure EnvironmentVariables exists and prepend ~/.openclaw/bin to PATH.
    /usr/libexec/PlistBuddy -c "Add :EnvironmentVariables dict" "${PLIST}" 2>/dev/null || true
    EXISTING_PATH="$(/usr/libexec/PlistBuddy -c "Print :EnvironmentVariables:PATH" "${PLIST}" 2>/dev/null || true)"
    if [[ -z "${EXISTING_PATH}" ]]; then
      NEW_PATH="${BIN_DIR}:/usr/bin:/bin:/usr/sbin:/sbin"
      /usr/libexec/PlistBuddy -c "Add :EnvironmentVariables:PATH string ${NEW_PATH}" "${PLIST}" 2>/dev/null || \
        /usr/libexec/PlistBuddy -c "Set :EnvironmentVariables:PATH ${NEW_PATH}" "${PLIST}" 2>/dev/null || true
      log "Updated gateway LaunchAgent PATH to include ${BIN_DIR}"
    else
      case ":${EXISTING_PATH}:" in
        *":${BIN_DIR}:"*) ;;
        *)
          NEW_PATH="${BIN_DIR}:${EXISTING_PATH}"
          /usr/libexec/PlistBuddy -c "Set :EnvironmentVariables:PATH ${NEW_PATH}" "${PLIST}" 2>/dev/null || true
          log "Prepended ${BIN_DIR} to gateway LaunchAgent PATH"
          ;;
      esac
    fi
  else
    log "macOS gateway plist not found or PlistBuddy unavailable; PATH must include ${BIN_DIR} manually."
  fi
else
  log "Non-macOS: ensure the OpenClaw gateway process PATH includes ${BIN_DIR} before /usr/bin."
fi

log "Restart the OpenClaw gateway to apply:"
log "  openclaw gateway restart"
