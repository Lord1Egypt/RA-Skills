#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

python generate_complex_demo.py

python advanced_ml_skill.py \
  --data-path ./demo_complex.csv \
  --target-col target_label

echo
echo "Demo finished. Start frontend with:"
echo "  source .venv/bin/activate && streamlit run app.py"
