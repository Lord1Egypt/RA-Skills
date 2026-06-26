#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "Usage: $0 <provider.json> <output-root> [label]" >&2
  exit 2
fi

CONFIG_JSON="$1"
OUTPUT_ROOT="$2"
LABEL_OVERRIDE="${3:-}"

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
RUN_DATE="${APIQ_RUN_DATE:-$(date +%F)}"

if [[ ! -f "$CONFIG_JSON" ]]; then
  echo "Config file not found: $CONFIG_JSON" >&2
  exit 1
fi

readarray -t META < <(python3 - "$CONFIG_JSON" "$LABEL_OVERRIDE" <<'PY'
import json
import re
import sys
from pathlib import Path

cfg_path = Path(sys.argv[1])
override = sys.argv[2].strip()
cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

def slugify(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip())
    text = re.sub(r"-{2,}", "-", text).strip("-._")
    return text or "config"

label = override or cfg.get("name") or cfg.get("model_id") or cfg.get("base_url") or cfg_path.stem
print(label)
print(slugify(label))
PY
)

LABEL="${META[0]}"
LABEL_SLUG="${META[1]}"

TARGET_ROOT="$OUTPUT_ROOT/$LABEL_SLUG"
BASELINE_DIR="$TARGET_ROOT/baselines"
RUNS_DIR="$TARGET_ROOT/runs"
RUN_DIR="$RUNS_DIR/$RUN_DATE"

mkdir -p "$BASELINE_DIR" "$RUN_DIR"
cp "$CONFIG_JSON" "$RUN_DIR/provider.json"

SMOKE_JSON="$RUN_DIR/smoke.json"
SMOKE_HTML="$RUN_DIR/smoke.html"
LT_BASELINE_JSON="$BASELINE_DIR/lt-baseline.json"
LT_BASELINE_HTML="$BASELINE_DIR/lt-baseline.html"
B3_BASELINE_JSON="$BASELINE_DIR/b3it-baseline.json"
B3_BASELINE_HTML="$BASELINE_DIR/b3it-baseline.html"
LT_DETECT_JSON="$RUN_DIR/lt-detect.json"
LT_DETECT_HTML="$RUN_DIR/lt-detect.html"
B3_DETECT_JSON="$RUN_DIR/b3it-detect.json"
B3_DETECT_HTML="$RUN_DIR/b3it-detect.html"
SUMMARY_JSON="$RUN_DIR/summary.json"
SUMMARY_HTML="$RUN_DIR/index.html"
LATEST_TXT="$TARGET_ROOT/latest-run.txt"

python3 "$APIQ" smoke \
  --config "$CONFIG_JSON" \
  --output "$SMOKE_JSON" \
  --html-output "$SMOKE_HTML"

readarray -t CAPS < <(python3 - "$SMOKE_JSON" <<'PY'
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print("true" if data.get("b3it_supported") else "false")
print("true" if data.get("lt_supported") else "false")
print(data.get("recommended_detector", "unknown"))
PY
)

B3_SUPPORTED="${CAPS[0]}"
LT_SUPPORTED="${CAPS[1]}"
RECOMMENDED="${CAPS[2]}"

b3_baseline_needs_refresh="false"
if [[ -f "$B3_BASELINE_JSON" ]]; then
  b3_baseline_needs_refresh="$(python3 - "$B3_BASELINE_JSON" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
try:
    data = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    print("true")
    raise SystemExit(0)

border_inputs = data.get("border_inputs") or []
has_threshold = isinstance(data.get("stable_support_threshold"), dict)
has_reference_stable = all(isinstance(item.get("reference_stable_support"), list) for item in border_inputs if isinstance(item, dict))
print("false" if has_threshold and has_reference_stable else "true")
PY
)"
fi

if [[ "$LT_SUPPORTED" == "true" && ! -f "$LT_BASELINE_JSON" ]]; then
  python3 "$APIQ" lt-baseline \
    --config "$CONFIG_JSON" \
    --output "$LT_BASELINE_JSON" \
    --html-output "$LT_BASELINE_HTML" \
    --runs-per-prompt "$LT_BASE_RUNS" \
    --top-logprobs "$LT_TOP_LOGPROBS"
fi

if [[ "$B3_SUPPORTED" == "true" && ( ! -f "$B3_BASELINE_JSON" || "$b3_baseline_needs_refresh" == "true" ) ]]; then
  python3 "$APIQ" b3it-baseline \
    --config "$CONFIG_JSON" \
    --output "$B3_BASELINE_JSON" \
    --html-output "$B3_BASELINE_HTML" \
    --candidate-count "$B3_CANDIDATES" \
    --discovery-repeats "$B3_DISCOVERY_REPEATS" \
    --keep-count "$B3_KEEP_COUNT" \
    --reference-samples "$B3_REFERENCE_SAMPLES" \
    --seed "$B3_SEED"
fi

if [[ "$LT_SUPPORTED" == "true" && -f "$LT_BASELINE_JSON" ]]; then
  python3 "$APIQ" lt-detect \
    --config "$CONFIG_JSON" \
    --baseline "$LT_BASELINE_JSON" \
    --output "$LT_DETECT_JSON" \
    --html-output "$LT_DETECT_HTML" \
    --runs-per-prompt "$LT_DETECT_RUNS" \
    --top-logprobs "$LT_TOP_LOGPROBS" \
    --permutations "$LT_PERMUTATIONS"
fi

if [[ "$B3_SUPPORTED" == "true" && -f "$B3_BASELINE_JSON" ]]; then
  python3 "$APIQ" b3it-detect \
    --config "$CONFIG_JSON" \
    --baseline "$B3_BASELINE_JSON" \
    --output "$B3_DETECT_JSON" \
    --html-output "$B3_DETECT_HTML" \
    --detection-repeats "$B3_DETECTION_REPEATS" \
    --min-stable-count "$B3_MIN_STABLE_COUNT" \
    --min-stable-ratio "$B3_MIN_STABLE_RATIO" \
    --confirm-passes "$B3_CONFIRM_PASSES"
fi

python3 - "$LABEL" "$RUN_DATE" "$RUN_DIR" "$BASELINE_DIR" "$SMOKE_JSON" "$LT_DETECT_JSON" "$B3_DETECT_JSON" "$SUMMARY_JSON" "$SUMMARY_HTML" <<'PY'
import html
import json
import sys
from pathlib import Path

label, run_date, run_dir, baseline_dir, smoke_json, lt_json, b3_json, summary_json, summary_html = sys.argv[1:10]
run_dir = Path(run_dir)
baseline_dir = Path(baseline_dir)

def load(path_str: str):
    path = Path(path_str)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

smoke = load(smoke_json) or {}
lt = load(lt_json)
b3 = load(b3_json)

summary = {
    "label": label,
    "run_date": run_date,
    "run_dir": str(run_dir),
    "baseline_dir": str(baseline_dir),
    "smoke": {
        "b3it_supported": smoke.get("b3it_supported"),
        "lt_supported": smoke.get("lt_supported"),
        "recommended_detector": smoke.get("recommended_detector"),
        "first_token_text": smoke.get("first_token_text"),
        "first_token_error": smoke.get("first_token_error"),
        "logprob_error": smoke.get("logprob_error"),
    },
    "lt_detect": {
        "ran": lt is not None,
        "overall_changed": None if lt is None else lt.get("overall_changed"),
        "changed_prompts": None if lt is None else lt.get("changed_prompts"),
        "total_prompts": None if lt is None else lt.get("total_prompts"),
    },
    "b3it_detect": {
        "ran": b3 is not None,
        "overall_changed": None if b3 is None else b3.get("overall_changed"),
        "changed_prompts": None if b3 is None else b3.get("changed_prompts"),
        "total_prompts": None if b3 is None else b3.get("total_prompts"),
        "stopped_early": None if b3 is None else b3.get("stopped_early"),
    },
}
Path(summary_json).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

cards = [
    {
        "title": "Smoke",
        "status": "Ready",
        "href": "smoke.html",
        "meta": [
            f"B3IT supported: {smoke.get('b3it_supported')}",
            f"LT supported: {smoke.get('lt_supported')}",
            f"Recommended: {smoke.get('recommended_detector')}",
        ],
    },
    {
        "title": "LT Detect",
        "status": "Ready" if lt is not None else "Skipped",
        "href": "lt-detect.html",
        "meta": [] if lt is None else [
            f"Overall changed: {lt.get('overall_changed')}",
            f"Changed prompts: {lt.get('changed_prompts')}",
            f"Total prompts: {lt.get('total_prompts')}",
        ],
    },
    {
        "title": "B3IT Detect",
        "status": "Ready" if b3 is not None else "Skipped",
        "href": "b3it-detect.html",
        "meta": [] if b3 is None else [
            f"Overall changed: {b3.get('overall_changed')}",
            f"Changed prompts: {b3.get('changed_prompts')}",
            f"Stopped early: {b3.get('stopped_early')}",
        ],
    },
]

def render_card(card):
    href = card["href"]
    path = run_dir / href
    cta = f"<a class='link' href='./{html.escape(href)}'>Open report</a>" if path.exists() else "<span class='link disabled'>Not generated</span>"
    meta = "".join(f"<li>{html.escape(item)}</li>" for item in card["meta"])
    return (
        "<section class='card'>"
        f"<div class='row'><h2>{html.escape(card['title'])}</h2><span class='badge'>{html.escape(card['status'])}</span></div>"
        f"<ul>{meta}</ul>"
        f"{cta}"
        "</section>"
    )

html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(label)} | {html.escape(run_date)}</title>
  <style>
    :root {{
      --bg: #f4f4ef;
      --card: #fffdf8;
      --line: #ddd6c8;
      --text: #1d1a16;
      --muted: #6b645c;
      --accent: #0f766e;
      --badge: #efe7da;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Georgia, "Times New Roman", serif; background: linear-gradient(180deg, #f7f1e6 0%, var(--bg) 100%); color: var(--text); }}
    .wrap {{ max-width: 980px; margin: 0 auto; padding: 28px; }}
    .hero {{ margin-bottom: 22px; }}
    h1, h2 {{ margin: 0; }}
    p {{ color: var(--muted); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }}
    .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 18px; padding: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.04); }}
    .row {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; }}
    .badge {{ background: var(--badge); border-radius: 999px; padding: 4px 10px; font-size: 12px; }}
    ul {{ margin: 0 0 14px 18px; padding: 0; color: var(--muted); }}
    li {{ margin: 6px 0; }}
    .link {{ display: inline-block; text-decoration: none; background: var(--accent); color: #fff; border-radius: 10px; padding: 10px 14px; }}
    .link.disabled {{ background: #b8b1a6; color: #fff; }}
    .files {{ margin-top: 22px; }}
    .files a {{ color: var(--accent); text-decoration: none; margin-right: 12px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <h1>{html.escape(label)}</h1>
      <p>Daily API quality snapshot for {html.escape(run_date)}.</p>
    </div>
    <div class="grid">
      {''.join(render_card(card) for card in cards)}
    </div>
    <div class="files">
      <a href="./summary.json">summary.json</a>
      <a href="./provider.json">provider.json</a>
      <a href="./smoke.json">smoke.json</a>
      <a href="./lt-detect.json">lt-detect.json</a>
      <a href="./b3it-detect.json">b3it-detect.json</a>
    </div>
  </div>
</body>
</html>"""
Path(summary_html).write_text(html_text, encoding="utf-8")
PY

printf '%s\n' "$RUN_DIR" > "$LATEST_TXT"

echo "Label:            $LABEL"
echo "Run date:         $RUN_DATE"
echo "Recommended:      $RECOMMENDED"
echo "Run directory:    $RUN_DIR"
echo "Summary JSON:     $SUMMARY_JSON"
echo "Summary HTML:     $SUMMARY_HTML"
echo "Latest pointer:   $LATEST_TXT"
