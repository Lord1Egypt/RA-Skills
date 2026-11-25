#!/usr/bin/env bash
set -euo pipefail

# Installs the sudo shim (sudo-shim.template.sh) at ~/.openclaw/bin/sudo, then, with
# your confirmation, puts ~/.openclaw/bin first on the PATH OpenClaw uses for commands.

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

# The real sudo is looked for in the system directories only. "command -v sudo"
# could return this shim when it is already installed and first on PATH.
REAL_SUDO=""
for candidate in /usr/bin/sudo /bin/sudo /usr/local/bin/sudo; do
  if validate_root_bin "${candidate}"; then
    REAL_SUDO="${candidate}"
    break
  fi
done
if [[ -z "${REAL_SUDO}" ]]; then
  log "Refusing to install shim: no root-owned sudo found in /usr/bin, /bin or /usr/local/bin."
  exit 1
fi

PYTHON3="$(resolve_python)"

OPENCLAW_DIR="${HOME}/.openclaw"
BIN_DIR="${OPENCLAW_DIR}/bin"
SKILL_DIR="${OPENCLAW_DIR}/workspace/skills/cyber-security-engineer"
TEMPLATE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/sudo-shim.template.sh"

if [[ ! -f "${TEMPLATE}" ]]; then
  log "Shim template not found: ${TEMPLATE}"
  exit 1
fi
if [[ ! -f "${SKILL_DIR}/scripts/guarded_privileged_exec.py" ]]; then
  log "The skill is not installed at ${SKILL_DIR}. Install it first, then run this again."
  exit 1
fi

mkdir -p "${BIN_DIR}"
chmod 700 "${OPENCLAW_DIR}" "${BIN_DIR}" || true

WRAPPER="${BIN_DIR}/sudo"
# Fill the three paths into the template, each quoted for the shell.
"${PYTHON3}" - "${TEMPLATE}" "${WRAPPER}" "${REAL_SUDO}" "${PYTHON3}" "${SKILL_DIR}" <<'PY'
import shlex
import sys

template, destination, real_sudo, python3, skill_dir = sys.argv[1:6]
with open(template, encoding="utf-8") as f:
    text = f.read()
for placeholder, value in (("@REAL_SUDO@", real_sudo), ("@PYTHON3@", python3), ("@SKILL_DIR@", skill_dir)):
    text = text.replace(placeholder, shlex.quote(value))
with open(destination, "w", encoding="utf-8") as f:
    f.write(text)
PY
chmod 700 "${WRAPPER}"

log "Installed sudo shim: ${WRAPPER}"

# Make OpenClaw find the shim before the real sudo.
#
# Preferred: OpenClaw's own setting tools.exec.pathPrepend, which puts the directory
# first on PATH for every command the gateway runs. Current OpenClaw releases start
# the gateway through a generated environment file that replaces any PATH set in the
# LaunchAgent, so editing the LaunchAgent alone no longer has any effect there.
#
# Fallback (older OpenClaw without that setting, macOS): the LaunchAgent's PATH.

confirm_change() {
  # $1 = what will be modified. Changing how OpenClaw finds sudo is persistent, so it
  # needs a clear yes: typed at a terminal, or OPENCLAW_HOOK_ASSUME_YES=1 for
  # unattended installs. With neither, nothing is changed.
  if [[ "${OPENCLAW_HOOK_ASSUME_YES:-0}" == "1" ]]; then
    return 0
  fi
  if [[ ! -t 0 ]]; then
    return 1
  fi
  local reply
  printf '[cyber-security-engineer] This will modify %s\nProceed? [y/N]: ' "$1"
  read -r reply
  [[ "${reply}" == "y" || "${reply}" == "Y" ]]
}

set_path_prepend() {
  command -v openclaw >/dev/null 2>&1 || return 1
  local merged
  # Keep any directories already configured; put the shim directory first.
  merged="$("${PYTHON3}" - "${OPENCLAW_DIR}/openclaw.json" "${BIN_DIR}" <<'PY'
import json, sys
config_path, shim_dir = sys.argv[1], sys.argv[2]
try:
    with open(config_path, encoding="utf-8") as f:
        current = json.load(f).get("tools", {}).get("exec", {}).get("pathPrepend") or []
except Exception:
    current = []
entries = [shim_dir] + [e for e in current if isinstance(e, str) and e != shim_dir]
print(json.dumps(entries))
PY
)" || return 1
  openclaw config set tools.exec.pathPrepend "${merged}" --strict-json >/dev/null 2>&1 || return 1
  openclaw config validate >/dev/null 2>&1 || return 1
}

set_launchagent_path() {
  local plist="${HOME}/Library/LaunchAgents/ai.openclaw.gateway.plist"
  [[ "$(uname -s)" == "Darwin" && -f "${plist}" && -x /usr/libexec/PlistBuddy ]] || return 1
  /usr/libexec/PlistBuddy -c "Add :EnvironmentVariables dict" "${plist}" 2>/dev/null || true
  local existing new_path
  existing="$(/usr/libexec/PlistBuddy -c "Print :EnvironmentVariables:PATH" "${plist}" 2>/dev/null || true)"
  if [[ -z "${existing}" ]]; then
    new_path="${BIN_DIR}:/usr/bin:/bin:/usr/sbin:/sbin"
    /usr/libexec/PlistBuddy -c "Add :EnvironmentVariables:PATH string ${new_path}" "${plist}" 2>/dev/null || \
      /usr/libexec/PlistBuddy -c "Set :EnvironmentVariables:PATH ${new_path}" "${plist}" 2>/dev/null || return 1
  else
    case ":${existing}:" in
      *":${BIN_DIR}:"*) ;;
      *) /usr/libexec/PlistBuddy -c "Set :EnvironmentVariables:PATH ${BIN_DIR}:${existing}" "${plist}" 2>/dev/null || return 1 ;;
    esac
  fi
}

if ! confirm_change "OpenClaw's command PATH (tools.exec.pathPrepend in ${OPENCLAW_DIR}/openclaw.json)"; then
  log "OpenClaw's command PATH was not changed (no confirmation given)."
  log "The shim is installed but OpenClaw will not use it until ${BIN_DIR} is first on that PATH."
  log "Run this installer in a terminal and answer y, or set OPENCLAW_HOOK_ASSUME_YES=1."
  exit 0
fi

if set_path_prepend; then
  log "Set tools.exec.pathPrepend so OpenClaw runs ${BIN_DIR}/sudo before the real sudo."
  log "Restart the OpenClaw gateway to apply:"
  log "  openclaw gateway restart"
elif set_launchagent_path; then
  log "This OpenClaw has no tools.exec.pathPrepend setting; added ${BIN_DIR} to the gateway LaunchAgent PATH instead."
  # A plain restart keeps the old environment; the service has to be reloaded to see the new PATH.
  log "Reload the OpenClaw gateway service to apply:"
  log "  launchctl bootout gui/\$(id -u)/ai.openclaw.gateway"
  log "  launchctl bootstrap gui/\$(id -u) ${HOME}/Library/LaunchAgents/ai.openclaw.gateway.plist"
else
  log "Could not configure OpenClaw's PATH automatically."
  log "Make sure the OpenClaw gateway runs with ${BIN_DIR} before /usr/bin on its PATH, then restart it."
fi
