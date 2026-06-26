#!/usr/bin/env bash
set -euo pipefail

PKG_NAME="${AIHEAL_NPM_PACKAGE:-aihealingmecli}"
CACHE_DIR="${AIHEAL_NPM_CACHE_DIR:-${TMPDIR:-/tmp}/aiheal-cli-npm-cache-${UID}}"

run_cli_checks() {
  local -a cli_cmd=("$@")

  echo "[smoke] verifying command tree: ${cli_cmd[*]}"
  "${cli_cmd[@]}" --help >/dev/null
  "${cli_cmd[@]}" auth --help >/dev/null
  "${cli_cmd[@]}" audio --help >/dev/null
  "${cli_cmd[@]}" chat --help >/dev/null

  echo "[smoke] verifying config envelope"
  "${cli_cmd[@]}" config get >/dev/null

  if [[ "${RUN_NETWORK_SMOKE:-0}" == "1" ]]; then
    echo "[smoke] running network smoke against configured apiBase"
    "${cli_cmd[@]}" audio list --limit 1 --sort newest >/dev/null
  fi
}

if command -v aiheal >/dev/null 2>&1; then
  echo "[smoke] using global aiheal binary"
  run_cli_checks aiheal
else
  mkdir -p "${CACHE_DIR}"
  echo "[smoke] using npx package ${PKG_NAME}"
  run_cli_checks env NPM_CONFIG_CACHE="${CACHE_DIR}" npx -y -p "${PKG_NAME}" aiheal
fi

echo "[smoke] done"
