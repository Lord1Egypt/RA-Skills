#!/bin/bash
# Smoke test for commodities skill (prints first 20 lines)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
# Run with a common Yahoo commodity ticker; output may vary by connectivity.
uv run "$SCRIPT_DIR/src/main.py" CL=F 2>&1 | head -n 20
