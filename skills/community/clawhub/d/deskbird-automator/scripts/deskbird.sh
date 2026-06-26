#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [[ -x "${SKILL_ROOT}/.venv/bin/python" ]]; then
  PYTHON_BIN="${SKILL_ROOT}/.venv/bin/python"
elif [[ -x "${SKILL_ROOT}/../.venv/bin/python" ]]; then
  PYTHON_BIN="${SKILL_ROOT}/../.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
else
  PYTHON_BIN="$(command -v python)"
fi

ENV_FILE="${DESKBIRD_ENV_FILE:-${SKILL_ROOT}/.env}"
mkdir -p "$(dirname "${ENV_FILE}")"
touch "${ENV_FILE}"

export DESKBIRD_SAFE_MODE="${DESKBIRD_SAFE_MODE:-true}"

if ! "${PYTHON_BIN}" -c "import requests" >/dev/null 2>&1; then
  echo "Fehler: Kein passendes Python mit 'requests' gefunden." >&2
  echo "Bitte im Skill-Ordner ausfuehren: python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt" >&2
  exit 2
fi

has_env_file="false"
for arg in "$@"; do
  if [[ "${arg}" == "--env-file" || "${arg}" == --env-file=* ]]; then
    has_env_file="true"
    break
  fi
done

if [[ "${has_env_file}" == "true" ]]; then
  exec "${PYTHON_BIN}" "${SCRIPT_DIR}/deskbird_tool.py" "$@"
fi

exec "${PYTHON_BIN}" "${SCRIPT_DIR}/deskbird_tool.py" "$@" --env-file "${ENV_FILE}"
