#!/bin/bash
set -e

echo "BOT install: local Python dependencies only."
echo "Recommended: run inside a virtual environment."
echo "Example:"
echo "  python3 -m venv .venv && source .venv/bin/activate"

pip install -r requirements.txt

echo "Install complete."
