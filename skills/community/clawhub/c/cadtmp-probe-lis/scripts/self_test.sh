#!/usr/bin/env bash
# cad-file-reader 统一自测/回归闭环入口。
# 用法：scripts/self_test.sh [--manifest <真图清单.json>] [其他 self_test.py 参数]
set -uo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN=""
for candidate in \
  "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 \
  "$(command -v python3 || true)"
do
  if [[ -n "${candidate}" && -x "${candidate}" ]]; then PYTHON_BIN="${candidate}"; break; fi
done
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "❌ python3 缺失（需要 Python 3.10+）" >&2; exit 1
fi
PYTHONPYCACHEPREFIX=/tmp/cad-pycache exec "${PYTHON_BIN}" "${SKILL_DIR}/scripts/self_test.py" "$@"
