#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON:-python3}"
if [ -x "$ROOT_DIR/.venv/bin/python" ]; then
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
fi

OUT_DIR="${OUT_DIR:-data/runs/quickstart-run}"
QUERY_POOL="${QUERY_POOL:-data/query-pools/mineru-example.json}"
MODEL_CONFIG="${MODEL_CONFIG:-data/models.multi.sample.json}"
MANUAL_RESPONSES="${MANUAL_RESPONSES:-data/manual.multi.sample.json}"

"$PYTHON_BIN" scripts/validate_data.py --repo-root .
"$PYTHON_BIN" -m devtool_answer_monitor run \
  --query-pool "$QUERY_POOL" \
  --model-config "$MODEL_CONFIG" \
  --out-dir "$OUT_DIR" \
  --manual-responses "$MANUAL_RESPONSES"
"$PYTHON_BIN" scripts/generate_weekly_report.py --summary data/runs/sample-run/summary.json --output data/runs/sample-run/weekly_report.md
"$PYTHON_BIN" scripts/build_leaderboard.py --runs-root data/runs --output-dir data/leaderboards --image-output assets/leaderboard-sample.png
"$PYTHON_BIN" scripts/build_repair_trend.py

cat <<MSG
Quickstart complete.

New run:
  $OUT_DIR/raw_responses.jsonl
  $OUT_DIR/score_draft.jsonl
  $OUT_DIR/run_manifest.json

Sample report snapshot:
  data/runs/sample-run/weekly_report.md
  assets/leaderboard-sample.png
  assets/repair-trend-sample.png

If you are new here, open:
  docs/for-beginners.md
MSG
