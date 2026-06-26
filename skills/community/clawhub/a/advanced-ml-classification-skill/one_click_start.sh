#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_DIR="$ROOT_DIR/scripts"
PORT="${PORT:-8501}"
HOST="${HOST:-127.0.0.1}"

cd "$SCRIPT_DIR"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --disable-pip-version-check -q -r requirements.txt

(
  sleep 2
  open "http://${HOST}:${PORT}"
) >/dev/null 2>&1 &

exec python -m streamlit run app.py \
  --server.address "$HOST" \
  --server.port "$PORT" \
  --browser.gatherUsageStats false
