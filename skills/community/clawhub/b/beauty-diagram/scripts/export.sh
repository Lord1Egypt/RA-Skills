#!/usr/bin/env bash
# Export a single Mermaid source to SVG, surfacing API errors.
# Usage: ./export.sh flow.mmd flow.svg
set -euo pipefail

FILE=${1:?usage: $0 <source.mmd> <out.svg>}
OUT=${2:?usage: $0 <source.mmd> <out.svg>}

npx --yes @beauty-diagram/cli export "$FILE" --format svg --out "$OUT"
