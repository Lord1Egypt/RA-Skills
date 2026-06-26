#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./run.sh 7
# Defaults:
#   day=1

DAY="${1:-1}"

if [[ -f ".env" ]]; then
  # shellcheck disable=SC1091
  source ".env"
fi

python3 tool.py --day "${DAY}"

