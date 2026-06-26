#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if [ $# -lt 1 ]; then
  cat <<'EOF'
Usage:
  .pi/skills/ak-data-daily-timeout-report/run.sh day   --date-bjt YYYY-MM-DD --job-type AmazonListingJob [--config path] [extra args]
  .pi/skills/ak-data-daily-timeout-report/run.sh trend --start-date-bjt YYYY-MM-DD --end-date-bjt YYYY-MM-DD --job-type AmazonListingJob [--config path] [extra args]

Examples:
  .pi/skills/ak-data-daily-timeout-report/run.sh day --date-bjt 2026-04-05 --job-type AmazonListingJob
  .pi/skills/ak-data-daily-timeout-report/run.sh day --date-bjt 2026-04-05 --job-type AmazonListingJob --example-scope crawler_timeout --example-type overtime_total --example-market au --example-limit 5
  .pi/skills/ak-data-daily-timeout-report/run.sh trend --start-date-bjt 2026-04-01 --end-date-bjt 2026-04-05 --job-type AmazonListingJob
EOF
  exit 1
fi

MODE="$1"
shift

case "$MODE" in
  day)
    exec python3 "$ROOT_DIR/scripts/data/run_daily_timeout_report.py" "$@"
    ;;
  trend)
    exec python3 "$ROOT_DIR/scripts/data/run_daily_timeout_trend_report.py" "$@"
    ;;
  *)
    echo "Unsupported mode: $MODE" >&2
    exit 2
    ;;
esac
