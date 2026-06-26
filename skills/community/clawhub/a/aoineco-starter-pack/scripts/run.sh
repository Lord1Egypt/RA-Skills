#!/usr/bin/env bash
set -euo pipefail

# Convenience wrapper: run the pack installer from the *installed* skill path.
# Usage:
#   bash skills/aoineco-starter-pack/scripts/run.sh [minimal|core|full]

MODE="${1:-core}"

# Resolve this script's directory even if called from elsewhere
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$HERE/install_pack.sh" "$MODE"
