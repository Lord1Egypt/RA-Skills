#!/usr/bin/env bash
# PDF 图纸识图候选（本机分流 + 本地 OCR）。
set -euo pipefail
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
  echo "Python 3 not found; cannot run PDF reader." >&2
  exit 1
fi
exec "${PYTHON_BIN}" "${SKILL_DIR}/scripts/cad_pdf_ocr.py" "$@"
