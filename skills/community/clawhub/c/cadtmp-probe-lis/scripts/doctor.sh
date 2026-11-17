#!/usr/bin/env bash
# cad-file-reader 环境体检（只读分档结论，不自动安装）。
# 用法：scripts/doctor.sh [--json-only|--md-only|--no-write] [--out-dir 目录]
set -uo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN=""
for candidate in \
  "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 \
  "$(command -v python3 || true)"
do
  if [[ -n "${candidate}" && -x "${candidate}" ]]; then
    PYTHON_BIN="${candidate}"
    break
  fi
done
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "❌ python3 缺失（需要 Python 3.10+）" >&2; exit 1
fi
exec "${PYTHON_BIN}" "${SKILL_DIR}/scripts/doctor.py" "$@"
