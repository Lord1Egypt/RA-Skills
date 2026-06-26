#!/usr/bin/env bash
set -euo pipefail

infer_skill_root() {
  local script_dir
  script_dir="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  (cd "$script_dir/.." && pwd)
}

SKILL_ROOT="${DPP_SKILL_ROOT:-$(infer_skill_root)}"
RUNTIME_DIR="${DPP_RUNTIME_DIR:-${SKILL_ROOT}/runtime}"
WORKDIR="${DPP_WORKDIR:-$(pwd)}"
PYTHON_BIN="${DPP_PYTHON_BIN:-${SKILL_ROOT}/.venv/bin/python}"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "error: missing virtualenv python at ${PYTHON_BIN}; run scripts/bootstrap_runtime.sh first" >&2
  exit 1
fi

if [[ ! -d "${RUNTIME_DIR}/src/dpp_storyboard" ]]; then
  echo "error: bundled runtime not found at ${RUNTIME_DIR}" >&2
  exit 1
fi

if [[ ! -d "${WORKDIR}" ]]; then
  echo "error: workspace directory not found: ${WORKDIR}" >&2
  exit 1
fi

export PYTHONPATH="${RUNTIME_DIR}/src${PYTHONPATH:+:${PYTHONPATH}}"
if [[ -f "${WORKDIR}/.env" ]]; then
  export DPP_DOTENV_PATH="${WORKDIR}/.env"
fi
cd "${WORKDIR}"
exec "${PYTHON_BIN}" -m dpp_storyboard "$@"
