#!/usr/bin/env bash
# scan.sh — Quick skill security scan wrapper
# Usage: bash scan.sh /path/to/skill [--full]
#   --full  : enable LLM analyzer (requires ANTHROPIC_API_KEY or SKILL_SCANNER_LLM_API_KEY)

set -euo pipefail

SKILL_PATH="${1:-}"
MODE="${2:-}"

if [[ -z "$SKILL_PATH" ]]; then
  echo "Usage: scan.sh /path/to/skill [--full]"
  exit 1
fi

if [[ ! -d "$SKILL_PATH" ]]; then
  echo "[error] Not a directory: $SKILL_PATH"
  exit 1
fi

SKILL_NAME=$(basename "$SKILL_PATH")

echo "============================================================"
echo "Scanning: $SKILL_NAME"
echo "Path: $SKILL_PATH"
echo "============================================================"

if [[ "$MODE" == "--full" ]]; then
  # Full scan with LLM (requires API key)
  API_KEY="${SKILL_SCANNER_LLM_API_KEY:-${ANTHROPIC_API_KEY:-}}"
  if [[ -z "$API_KEY" ]]; then
    echo "[warn] No API key found. Set ANTHROPIC_API_KEY or SKILL_SCANNER_LLM_API_KEY for LLM analysis."
    echo "[info] Falling back to behavioral scan only."
    skill-scanner scan "$SKILL_PATH" --use-behavioral --format markdown --detailed
  else
    SKILL_SCANNER_LLM_API_KEY="$API_KEY" \
    SKILL_SCANNER_LLM_MODEL="${SKILL_SCANNER_LLM_MODEL:-claude-haiku-4-5}" \
      skill-scanner scan "$SKILL_PATH" \
        --use-behavioral \
        --use-llm \
        --enable-meta \
        --llm-provider anthropic \
        --format markdown \
        --detailed
  fi
else
  # Default: static + behavioral (no API key needed)
  skill-scanner scan "$SKILL_PATH" --use-behavioral --format markdown --detailed
fi
