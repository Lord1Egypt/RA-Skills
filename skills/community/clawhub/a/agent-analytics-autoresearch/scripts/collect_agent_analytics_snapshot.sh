#!/usr/bin/env bash
set -u

if [ "$#" -lt 3 ]; then
  printf 'Usage: %s <project_slug> <primary_event> <proxy_event> [output_dir]\n' "$0" >&2
  exit 2
fi

PROJECT_SLUG="$1"
PRIMARY_EVENT="$2"
PROXY_EVENT="$3"
OUTPUT_DIR="${4:-data/$(date +%F)}"

mkdir -p "$OUTPUT_DIR"

run_snapshot_command() {
  output_file="$1"
  shift
  "$@" > "$output_file" 2>&1
  command_status=$?
  perl -i -pe 's/\e\[[0-9;]*m//g' "$output_file" 2>/dev/null || true
  if [ "$command_status" -ne 0 ]; then
    printf '\ncommand_exit_code: %s\n' "$command_status" >> "$output_file"
  fi
}

run_snapshot_command "$OUTPUT_DIR/insights.txt" \
  npx --yes @agent-analytics/cli@0.5.31 insights "$PROJECT_SLUG" --period 7d
run_snapshot_command "$OUTPUT_DIR/pages.txt" \
  npx --yes @agent-analytics/cli@0.5.31 pages "$PROJECT_SLUG" --since 7d
run_snapshot_command "$OUTPUT_DIR/funnel.txt" \
  npx --yes @agent-analytics/cli@0.5.31 funnel "$PROJECT_SLUG" \
  --steps "page_view,$PROXY_EVENT,$PRIMARY_EVENT" \
  --since 7d
run_snapshot_command "$OUTPUT_DIR/${PROXY_EVENT}-events.txt" \
  npx --yes @agent-analytics/cli@0.5.31 events "$PROJECT_SLUG" \
  --event "$PROXY_EVENT" \
  --days 7 \
  --limit 50
run_snapshot_command "$OUTPUT_DIR/${PRIMARY_EVENT}-events.txt" \
  npx --yes @agent-analytics/cli@0.5.31 events "$PROJECT_SLUG" \
  --event "$PRIMARY_EVENT" \
  --days 7 \
  --limit 50
run_snapshot_command "$OUTPUT_DIR/experiments.txt" \
  npx --yes @agent-analytics/cli@0.5.31 experiments list "$PROJECT_SLUG"

printf 'Saved Agent Analytics snapshot to %s\n' "$OUTPUT_DIR"
