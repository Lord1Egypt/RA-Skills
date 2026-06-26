#!/usr/bin/env bash
# Beautify all .mmd files in a directory, writing a sibling .svg.
# Usage: ./beautify.sh docs/diagrams
set -euo pipefail

DIR=${1:-docs/diagrams}
THEME=${THEME:-modern}

for f in "$DIR"/*.mmd; do
  [ -f "$f" ] || continue
  out="${f%.mmd}.svg"
  echo "→ $f"
  npx --yes @beauty-diagram/cli beautify "$f" --theme "$THEME" --out "$out"
done
