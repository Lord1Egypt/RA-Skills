#!/usr/bin/env bash
set -euo pipefail

RUN_NAME="${1:-$(date +%F)-growth-loop}"
RUN_DIR="${2:-autoresearch-runs/$RUN_NAME}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$RUN_DIR/data"

cp "$SKILL_DIR/references/brief-template.md" "$RUN_DIR/brief.md"
cp "$SKILL_DIR/references/final-variants-template.md" "$RUN_DIR/final_variants.md"
cp "$SKILL_DIR/references/results-header.txt" "$RUN_DIR/results.tsv"
touch "$RUN_DIR/scratch.md"

printf 'Created autoresearch run at %s\n' "$RUN_DIR"
printf 'Next: fill %s/brief.md, collect data, then run the loop.\n' "$RUN_DIR"
