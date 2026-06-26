#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ASSET_SCRIPT="${SKILL_ROOT}/assets/project-tunnel.sh"
TARGET_SCRIPT="${PROJECT_DIR}/project-tunnel.sh"

if [[ ! -d "${PROJECT_DIR}" ]]; then
  echo "ERROR: project dir not found: ${PROJECT_DIR}" >&2
  exit 1
fi

if [[ ! -f "${ASSET_SCRIPT}" ]]; then
  echo "ERROR: bundled script not found: ${ASSET_SCRIPT}" >&2
  exit 1
fi

cp "${ASSET_SCRIPT}" "${TARGET_SCRIPT}"
chmod +x "${TARGET_SCRIPT}"

echo "[OK] installed ${TARGET_SCRIPT}"
