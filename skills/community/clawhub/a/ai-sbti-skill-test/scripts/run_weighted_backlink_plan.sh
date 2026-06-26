#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${AI_SBTI_SKILL_TEST_ENV_FILE:-/root/.openclaw/workspace/.secrets/ai-sbti-skill-test.env}"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

SITE_URL="${SITE_URL:-https://aisbti.com}"
INPUT_CSV="${INPUT_CSV:-/root/.openclaw/workspace/ops/aisbti-seo/backlink-prospects.csv}"
RELAY_MAP_CSV="${RELAY_MAP_CSV:-}"
OUTPUT_MD="${OUTPUT_MD:-/root/.openclaw/workspace/ops/aisbti-seo/weighted-backlink-plan.md}"
OUTPUT_JSON="${OUTPUT_JSON:-/root/.openclaw/workspace/ops/aisbti-seo/weighted-backlink-plan.json}"
MIN_SCORE="${MIN_SCORE:-35}"
TOP_N="${TOP_N:-40}"
MONEY_KEYWORDS="${MONEY_KEYWORDS:-sbti test,screaming bird test indicator,sbti personality test}"

mkdir -p "$(dirname "$OUTPUT_MD")" "$(dirname "$OUTPUT_JSON")"

cmd=(
  python3 "$SKILL_DIR/scripts/build_weighted_backlink_plan.py"
  --site-url "$SITE_URL"
  --input-csv "$INPUT_CSV"
  --output-md "$OUTPUT_MD"
  --output-json "$OUTPUT_JSON"
  --min-score "$MIN_SCORE"
  --top-n "$TOP_N"
)

if [[ -n "$RELAY_MAP_CSV" && -f "$RELAY_MAP_CSV" ]]; then
  cmd+=(--relay-map "$RELAY_MAP_CSV")
fi

IFS=',' read -r -a kw_array <<< "$MONEY_KEYWORDS"
for kw in "${kw_array[@]}"; do
  trimmed="$(echo "$kw" | sed 's/^ *//;s/ *$//')"
  if [[ -n "$trimmed" ]]; then
    cmd+=(--money-keyword "$trimmed")
  fi
done

"${cmd[@]}"
