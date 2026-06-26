#!/usr/bin/env bash
set -euo pipefail
umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
STATE_ROOT="${CADUCEUSMAIL_STATE_DIR:-${HOME}/.caduceusmail}"
INTEL_DIR="${CADUCEUSMAIL_INTEL_DIR:-${STATE_ROOT}/intel}"
ENV_FILE="${CADUCEUSMAIL_ENV_FILE:-${STATE_ROOT}/.env}"

ensure_private_dir() {
  mkdir -p "$1"
  chmod 700 "$1" 2>/dev/null || true
}

add_if_set() {
  local name="$1"
  if [[ ${!name+x} ]]; then
    ENV_MAP["$name"]="${!name}"
  fi
}

ensure_private_dir "${STATE_ROOT}"
ensure_private_dir "${INTEL_DIR}"
if [[ -f "${ENV_FILE}" ]]; then
  chmod 600 "${ENV_FILE}" 2>/dev/null || true
fi

ENTRYPOINT="$(bash "${SCRIPT_DIR}/ensure-caduceusmail.sh")"

declare -A ENV_MAP=()

for name in \
  HOME PATH USER LANG LC_ALL TERM COLORTERM NO_COLOR \
  CI DISPLAY WAYLAND_DISPLAY SSH_TTY SSH_CONNECTION SSH_CLIENT \
  TMPDIR TMP TEMP \
  ENTRA_TENANT_ID ENTRA_CLIENT_ID ENTRA_CLIENT_SECRET \
  EXCHANGE_DEFAULT_MAILBOX EXCHANGE_ORGANIZATION ORGANIZATION_DOMAIN \
  CLOUDFLARE_API_TOKEN CLOUDFLARE_ZONE_ID CF_API_TOKEN CF_ZONE_ID; do
  add_if_set "${name}"
done

while IFS='=' read -r name _; do
  case "${name}" in
    CADUCEUSMAIL_*|EMAIL_ALIAS_FABRIC_*|OPENCLAW_*)
      add_if_set "${name}"
      ;;
  esac
done < <(env)

# Run the vendored tool with a reduced environment so unrelated host secrets do not leak through.
ENV_MAP["CADUCEUSMAIL_STATE_DIR"]="${STATE_ROOT}"
ENV_MAP["CADUCEUSMAIL_INTEL_DIR"]="${INTEL_DIR}"
ENV_MAP["CADUCEUSMAIL_ENV_FILE"]="${ENV_FILE}"
ENV_MAP["CADUCEUSMAIL_ALLOW_EXTERNAL_SCRIPT_RESOLUTION"]="${CADUCEUSMAIL_ALLOW_EXTERNAL_SCRIPT_RESOLUTION:-0}"

ENV_ARGS=()
while IFS= read -r name; do
  ENV_ARGS+=("${name}=${ENV_MAP[${name}]}")
done < <(printf '%s\n' "${!ENV_MAP[@]}" | sort)

exec env -i "${ENV_ARGS[@]}" node "${ENTRYPOINT}" "$@"
