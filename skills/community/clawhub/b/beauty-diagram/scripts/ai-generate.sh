#!/usr/bin/env bash
# Generate a Mermaid diagram from a text prompt, then beautify to SVG.
# Always writes BOTH the .mmd source and the .svg render — the source is
# what the user iterates on; the SVG is the final artifact.
#
# Usage:  ./ai-generate.sh "user signup with email verification" docs/signup
#
# Requires: bd auth login with a Pro/Premium key that has the ai:write scope.
set -euo pipefail

PROMPT=${1:?usage: $0 "<prompt>" <out-stem>}
STEM=${2:?usage: $0 "<prompt>" <out-stem>}

MMD="${STEM}.mmd"
SVG="${STEM}.svg"

echo "→ generating Mermaid source for: $PROMPT"
npx --yes @beauty-diagram/cli ai generate "$PROMPT" --out "$MMD"

echo "→ beautifying $MMD"
npx --yes @beauty-diagram/cli beautify "$MMD" --out "$SVG"

echo "✓ wrote $MMD (editable source) and $SVG (presentation render)"
