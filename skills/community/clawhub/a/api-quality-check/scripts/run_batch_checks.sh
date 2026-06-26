#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "Usage: $0 <providers.json> <output-dir> [prompts.json]" >&2
  exit 2
fi

CONFIGS_JSON="$1"
OUT_DIR="$2"
PROMPTS_JSON="${3:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APIQ="$SCRIPT_DIR/api_quality_check.py"

LT_BASE_RUNS="${APIQ_LT_BASE_RUNS:-12}"
LT_DETECT_RUNS="${APIQ_LT_DETECT_RUNS:-6}"
LT_TOP_LOGPROBS="${APIQ_LT_TOP_LOGPROBS:-10}"
LT_PERMUTATIONS="${APIQ_LT_PERMUTATIONS:-200}"
B3_CANDIDATES="${APIQ_B3_CANDIDATES:-120}"
B3_DISCOVERY_REPEATS="${APIQ_B3_DISCOVERY_REPEATS:-3}"
B3_KEEP_COUNT="${APIQ_B3_KEEP_COUNT:-5}"
B3_REFERENCE_SAMPLES="${APIQ_B3_REFERENCE_SAMPLES:-12}"
B3_DETECTION_REPEATS="${APIQ_B3_DETECTION_REPEATS:-5}"
B3_MIN_STABLE_COUNT="${APIQ_B3_MIN_STABLE_COUNT:-2}"
B3_MIN_STABLE_RATIO="${APIQ_B3_MIN_STABLE_RATIO:-0.35}"
B3_CONFIRM_PASSES="${APIQ_B3_CONFIRM_PASSES:-1}"
B3_SEED="${APIQ_B3_SEED:-42}"

mkdir -p "$OUT_DIR"

SMOKE_JSON="$OUT_DIR/batch-smoke.json"
SMOKE_HTML="$OUT_DIR/batch-smoke.html"
LT_READY_JSON="$OUT_DIR/providers.lt-ready.json"
B3_READY_JSON="$OUT_DIR/providers.b3it-ready.json"

python "$APIQ" batch-smoke \
  --configs "$CONFIGS_JSON" \
  --output "$SMOKE_JSON" \
  --html-output "$SMOKE_HTML"

python - "$CONFIGS_JSON" "$SMOKE_JSON" "$LT_READY_JSON" "$B3_READY_JSON" <<'PY'
import json
import sys
from pathlib import Path

configs_path, smoke_path, lt_out, b3_out = sys.argv[1:5]
configs_raw = json.loads(Path(configs_path).read_text(encoding="utf-8"))
configs = configs_raw["configs"] if isinstance(configs_raw, dict) else configs_raw
smoke = json.loads(Path(smoke_path).read_text(encoding="utf-8"))
results = smoke.get("results", [])

cfg_by_name = {}
cfg_by_index = {}
for idx, item in enumerate(configs, start=1):
    label = item.get("name") or item.get("label") or item.get("model_id") or f"config-{idx}"
    cfg_by_name[label] = item
    cfg_by_index[idx] = item

lt_ready = []
b3_ready = []
for item in results:
    cfg = cfg_by_name.get(item.get("name")) or cfg_by_index.get(item.get("index"))
    if not cfg:
        continue
    if item.get("b3it_supported"):
        b3_ready.append(cfg)
    if item.get("lt_supported"):
        lt_ready.append(cfg)

Path(lt_out).write_text(json.dumps({"configs": lt_ready}, ensure_ascii=False, indent=2), encoding="utf-8")
Path(b3_out).write_text(json.dumps({"configs": b3_ready}, ensure_ascii=False, indent=2), encoding="utf-8")
PY

LT_COUNT="$(python - "$LT_READY_JSON" <<'PY'
import json, sys
from pathlib import Path
data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
print(len(data.get('configs', [])))
PY
)"

B3_COUNT="$(python - "$B3_READY_JSON" <<'PY'
import json, sys
from pathlib import Path
data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
print(len(data.get('configs', [])))
PY
)"

if [[ "$LT_COUNT" -gt 0 ]]; then
  LT_BASE_ARGS=(
    batch-lt-baseline
    --configs "$LT_READY_JSON"
    --output-dir "$OUT_DIR/lt-baselines"
    --output "$OUT_DIR/batch-lt-baselines.json"
    --html-output "$OUT_DIR/batch-lt-baselines.html"
    --runs-per-prompt "$LT_BASE_RUNS"
    --top-logprobs "$LT_TOP_LOGPROBS"
  )
  if [[ -n "$PROMPTS_JSON" ]]; then
    LT_BASE_ARGS+=(--prompts "$PROMPTS_JSON")
  fi
  python "$APIQ" "${LT_BASE_ARGS[@]}"
  python "$APIQ" batch-lt-detect \
    --configs "$LT_READY_JSON" \
    --baseline-manifest "$OUT_DIR/batch-lt-baselines.json" \
    --output "$OUT_DIR/batch-lt-report.json" \
    --html-output "$OUT_DIR/batch-lt-report.html" \
    --runs-per-prompt "$LT_DETECT_RUNS" \
    --top-logprobs "$LT_TOP_LOGPROBS" \
    --permutations "$LT_PERMUTATIONS"
fi

if [[ "$B3_COUNT" -gt 0 ]]; then
  python "$APIQ" batch-b3it-baseline \
    --configs "$B3_READY_JSON" \
    --output-dir "$OUT_DIR/b3it-baselines" \
    --output "$OUT_DIR/batch-b3it-baselines.json" \
    --html-output "$OUT_DIR/batch-b3it-baselines.html" \
    --candidate-count "$B3_CANDIDATES" \
    --discovery-repeats "$B3_DISCOVERY_REPEATS" \
    --keep-count "$B3_KEEP_COUNT" \
    --reference-samples "$B3_REFERENCE_SAMPLES" \
    --seed "$B3_SEED"
  python "$APIQ" batch-b3it-detect \
    --configs "$B3_READY_JSON" \
    --baseline-manifest "$OUT_DIR/batch-b3it-baselines.json" \
    --output "$OUT_DIR/batch-b3it-report.json" \
    --html-output "$OUT_DIR/batch-b3it-report.html" \
    --detection-repeats "$B3_DETECTION_REPEATS" \
    --min-stable-count "$B3_MIN_STABLE_COUNT" \
    --min-stable-ratio "$B3_MIN_STABLE_RATIO" \
    --confirm-passes "$B3_CONFIRM_PASSES"
fi

python - "$OUT_DIR" "$LT_COUNT" "$B3_COUNT" <<'PY'
import html
import json
import sys
from pathlib import Path

out_dir = Path(sys.argv[1])
lt_count = int(sys.argv[2])
b3_count = int(sys.argv[3])

def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

smoke = load_json(out_dir / "batch-smoke.json") or {}
lt_report = load_json(out_dir / "batch-lt-report.json") or {}
b3_report = load_json(out_dir / "batch-b3it-report.json") or {}

cards = [
    ("Smoke", "Capability gate for all endpoints.", "batch-smoke.html", smoke.get("total_configs"), smoke.get("lt_supported_count")),
    ("LT-lite", "Logprob-tracking drift detection for LT-ready endpoints.", "batch-lt-report.html", lt_count, lt_report.get("changed_count")),
    ("B3IT-lite", "Support-set drift detection for first-token outputs.", "batch-b3it-report.html", b3_count, b3_report.get("changed_count")),
]

def card_html(title, body, href, total, changed):
    exists = (out_dir / href).exists()
    badge = "Ready" if exists else "Missing"
    badge_class = "good" if exists else "warn"
    stats = []
    if total is not None:
        stats.append(f"<span>Total: {html.escape(str(total))}</span>")
    if changed is not None:
        stats.append(f"<span>Changed: {html.escape(str(changed))}</span>")
    cta = f"<a class='link' href='./{html.escape(href)}'>Open report</a>" if exists else "<span class='link disabled'>Not generated</span>"
    return (
        "<div class='card'>"
        f"<div class='top'><h2>{html.escape(title)}</h2><span class='badge {badge_class}'>{html.escape(badge)}</span></div>"
        f"<p>{html.escape(body)}</p>"
        f"<div class='stats'>{''.join(f'<span class=\"stat\">{s}</span>' for s in stats)}</div>"
        f"{cta}"
        "</div>"
    )

summary = [
    ("Smoke checked", smoke.get("total_configs", 0)),
    ("LT-ready", smoke.get("lt_supported_count", 0)),
    ("B3IT-ready", smoke.get("b3it_supported_count", 0)),
    ("LT changed", lt_report.get("changed_count", 0) if lt_report else 0),
    ("B3IT changed", b3_report.get("changed_count", 0) if b3_report else 0),
]

html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>API Quality Index</title>
  <style>
    :root {{
      --bg: #f6f7f9;
      --card: #ffffff;
      --line: #e5e7eb;
      --text: #111827;
      --muted: #6b7280;
      --good: #d1fae5;
      --good-text: #065f46;
      --warn: #fef3c7;
      --warn-text: #92400e;
      --accent: #2563eb;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--text); }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 24px; }}
    h1, h2 {{ margin: 0; }}
    p {{ color: var(--muted); }}
    .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 20px 0 24px; }}
    .summary .item, .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 16px; }}
    .summary .value {{ font-size: 24px; font-weight: 700; margin-top: 6px; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}
    .top {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 10px; }}
    .badge {{ display: inline-flex; border-radius: 999px; padding: 4px 10px; font-size: 12px; font-weight: 700; }}
    .badge.good {{ background: var(--good); color: var(--good-text); }}
    .badge.warn {{ background: var(--warn); color: var(--warn-text); }}
    .stats {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 16px; }}
    .stat {{ background: #eff6ff; color: #1e3a8a; border-radius: 999px; padding: 4px 10px; font-size: 12px; }}
    .link {{ display: inline-block; text-decoration: none; color: white; background: var(--accent); border-radius: 10px; padding: 10px 14px; font-weight: 600; }}
    .link.disabled {{ background: #cbd5e1; color: #475569; }}
    .raw-links {{ margin-top: 24px; }}
    .raw-links a {{ color: var(--accent); text-decoration: none; margin-right: 12px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>API Quality Reports</h1>
    <p>Unified entry page for smoke, LT-lite, and B3IT-lite outputs produced by run_batch_checks.sh.</p>
    <div class="summary">
      {''.join(f"<div class='item'><div>{html.escape(label)}</div><div class='value'>{html.escape(str(value))}</div></div>" for label, value in summary)}
    </div>
    <div class="cards">
      {''.join(card_html(*card) for card in cards)}
    </div>
    <div class="raw-links">
      <a href="./batch-smoke.json">batch-smoke.json</a>
      <a href="./providers.lt-ready.json">providers.lt-ready.json</a>
      <a href="./providers.b3it-ready.json">providers.b3it-ready.json</a>
      <a href="./batch-lt-baselines.json">batch-lt-baselines.json</a>
      <a href="./batch-lt-report.json">batch-lt-report.json</a>
      <a href="./batch-b3it-baselines.json">batch-b3it-baselines.json</a>
      <a href="./batch-b3it-report.json">batch-b3it-report.json</a>
    </div>
  </div>
</body>
</html>"""

(out_dir / "index.html").write_text(html_text, encoding="utf-8")
PY

echo "Smoke report: $SMOKE_JSON"
echo "Smoke HTML:   $SMOKE_HTML"
echo "LT-ready:     $LT_READY_JSON ($LT_COUNT configs)"
echo "B3IT-ready:   $B3_READY_JSON ($B3_COUNT configs)"
echo "Index HTML:   $OUT_DIR/index.html"
echo "Output dir:   $OUT_DIR"
