#!/usr/bin/env bash
set -euo pipefail

ENV_DIR="${1:-.venv-bilibili-audio-transcribe}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REQ_FILE="${SCRIPT_DIR}/requirements.txt"

python3 -m venv "${ENV_DIR}"
# shellcheck disable=SC1090
source "${ENV_DIR}/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r "${REQ_FILE}"

echo "Python env ready: ${ENV_DIR}"
echo "Next: source \"${ENV_DIR}/bin/activate\" && python ${SCRIPT_DIR}/transcribe_bilibili.py --help"
