#!/usr/bin/env bash
set -euo pipefail

infer_skill_root() {
  local script_dir
  script_dir="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  (cd "$script_dir/.." && pwd)
}

SKILL_ROOT="${DPP_SKILL_ROOT:-$(infer_skill_root)}"
RUNTIME_DIR="${DPP_RUNTIME_DIR:-${SKILL_ROOT}/runtime}"
VENV_DIR="${DPP_VENV_DIR:-${SKILL_ROOT}/.venv}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 is required" >&2
  exit 1
fi

if [[ ! -f "${RUNTIME_DIR}/pyproject.toml" ]]; then
  echo "error: bundled runtime not found at ${RUNTIME_DIR}; rebuild the skill bundle first" >&2
  exit 1
fi

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/python" -m pip install -e "${RUNTIME_DIR}[dev]"

"${VENV_DIR}/bin/python" - <<'PY'
import bytedtos
import dotenv
import pydantic
import volcenginesdkarkruntime

print("python deps ok")
PY

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "error: ffmpeg is required" >&2
  exit 1
fi

ffmpeg -version >/dev/null
echo "runtime bootstrap ok"
