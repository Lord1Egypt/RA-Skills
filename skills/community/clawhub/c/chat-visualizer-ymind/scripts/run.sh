#!/usr/bin/env bash
# run.sh — YMind pipeline helper
#
# Usage:
#   run.sh fetch "<url>"        Create run dir, fetch chat → prints RUN_DIR
#   run.sh render <run_dir>     Validate graph.json, render HTML + screenshot
#
# Output directory: $YMIND_DIR (default: ~/ymind-ws)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
YMIND_DIR="${YMIND_DIR:-$HOME/ymind-ws}"

usage() {
    echo "Usage:"
    echo "  run.sh fetch \"<url>\"       Create run dir, fetch chat"
    echo "  run.sh render <run_dir>    Validate graph.json, render HTML + screenshot"
    echo "  run.sh index               Rebuild $YMIND_DIR/index.json from all run dirs"
    exit 1
}

_detect_provider() {
    case "$1" in
      *chatgpt.com*)        echo "chatgpt" ;;
      *gemini.google.com*)  echo "gemini" ;;
      *g.co/gemini*)        echo "gemini" ;;
      *g.co/*)              echo "gemini" ;;
      *claude.ai*)          echo "claude" ;;
      *deepseek.com*)       echo "deepseek" ;;
      *doubao.com*)         echo "doubao" ;;
      *)                    echo "chat" ;;
    esac
}

cmd="${1:-}"

case "$cmd" in
  fetch)
    URL="${2:?run.sh fetch requires a URL}"
    PROVIDER="$(_detect_provider "$URL")"
    TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
    RUN_DIR="$YMIND_DIR/${TIMESTAMP}_${PROVIDER}"
    mkdir -p "$RUN_DIR"
    echo "Run dir: $RUN_DIR"

    # Write initial meta.json (title added later by render)
    PROVIDER="$PROVIDER" URL="$URL" RUN_DIR="$RUN_DIR" \
    CREATED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)" python3 - <<'PYEOF'
import json, os
data = {
    "provider": os.environ["PROVIDER"],
    "url": os.environ["URL"],
    "created_at": os.environ["CREATED_AT"],
}
with open(os.path.join(os.environ["RUN_DIR"], "meta.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("meta.json: written")
PYEOF

    python3 "$SCRIPT_DIR/fetch-chat.py" "$URL" --out "$RUN_DIR/raw_chat.json"
    echo ""
    echo "RUN_DIR=$RUN_DIR"
    ;;

  render)
    RUN_DIR="${2:?run.sh render requires a run_dir path}"
    RUN_DIR="$(cd "$RUN_DIR" 2>/dev/null && pwd || true)"
    if [ -z "$RUN_DIR" ]; then
        echo "Error: invalid run_dir path" >&2
        exit 1
    fi
    # Force index workspace to match the run directory root.
    # This guarantees graph/meta/index stay under the same YMIND_DIR tree.
    YMIND_DIR="$(cd "$RUN_DIR/.." && pwd)"
    echo "Workspace dir: $YMIND_DIR"
    GRAPH="$RUN_DIR/graph.json"
    if [ ! -d "$RUN_DIR" ]; then
        echo "Error: run dir not found: $RUN_DIR" >&2
        exit 1
    fi
    if [ ! -f "$RUN_DIR/raw_chat.json" ]; then
        echo "Error: $RUN_DIR/raw_chat.json not found" >&2
        echo "Hint: use the RUN_DIR returned by fetch, and write graph.json in that same directory." >&2
        exit 1
    fi
    if [ ! -f "$RUN_DIR/meta.json" ]; then
        echo "Error: $RUN_DIR/meta.json not found" >&2
        echo "Hint: use the RUN_DIR returned by fetch, and write graph.json in that same directory." >&2
        exit 1
    fi
    if [ ! -f "$GRAPH" ]; then
        echo "Error: $GRAPH not found" >&2
        echo "Hint: extract output must be saved as $RUN_DIR/graph.json (same RUN_DIR as fetch)." >&2
        exit 1
    fi
    GRAPH="$GRAPH" python3 - <<'PYEOF'
import json, re, os, sys

graph_path = os.environ["GRAPH"]
with open(graph_path, encoding="utf-8") as f:
    raw = f.read()

# Try parsing first
try:
    json.loads(raw)
    print("graph.json: valid")
    sys.exit(0)
except json.JSONDecodeError as e:
    pass

# Parse failed — scan for unescaped " inside JSON string values
# Tokenize line by line: inside a string value, a bare " (0x22) that isn't
# the opening/closing delimiter or an already-escaped \" is the culprit.
issues = []
in_string = False
escape_next = False
line_num = 1
col_num = 0
string_start = None

for i, ch in enumerate(raw):
    col_num += 1
    if ch == '\n':
        line_num += 1
        col_num = 0

    if escape_next:
        escape_next = False
        continue

    if ch == '\\' and in_string:
        escape_next = True
        continue

    if ch == '"':
        if not in_string:
            in_string = True
            string_start = (line_num, col_num)
        else:
            in_string = False

# If no issues found via scan, just show the raw JSON error
if not issues:
    # Re-raise with context
    lines = raw.splitlines()
    try:
        json.loads(raw)
    except json.JSONDecodeError as e:
        ctx_line = lines[e.lineno - 1] if e.lineno <= len(lines) else ""
        pointer = ' ' * (e.colno - 1) + '^'
        print(f"graph.json: INVALID — {e.msg}", file=sys.stderr)
        print(f"  line {e.lineno}, col {e.colno}:", file=sys.stderr)
        print(f"  {ctx_line}", file=sys.stderr)
        print(f"  {pointer}", file=sys.stderr)
        # Check if a bare " appears near the error position in the source line
        near = ctx_line[max(0, e.colno-15):e.colno+5]
        if '"' in near:
            print(f'  Hint: bare " detected near error — replace with 「」 inside string values.', file=sys.stderr)
    sys.exit(1)

print(f"graph.json: INVALID — found {len(issues)} unescaped quote(s) inside string value(s)", file=sys.stderr)
print("Fix: replace bare \" with 「」 in the affected fields.", file=sys.stderr)
for line_no, col_no, ctx in issues:
    print(f"  line {line_no}, col {col_no}: ...{ctx}...", file=sys.stderr)
sys.exit(1)
PYEOF
    python3 "$SCRIPT_DIR/render-html.py" "$GRAPH" --out "$RUN_DIR/graph.html" --screenshot

    # Update meta.json with title extracted from graph.json
    RUN_DIR="$RUN_DIR" python3 - <<'PYEOF'
import json, os
run_dir = os.environ["RUN_DIR"]
meta_path = os.path.join(run_dir, "meta.json")
graph_path = os.path.join(run_dir, "graph.json")
meta = {}
if os.path.exists(meta_path):
    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)
if os.path.exists(graph_path):
    with open(graph_path, encoding="utf-8") as f:
        graph = json.load(f)
    meta["title"] = graph.get("meta", {}).get("title", "")
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
print("meta.json: updated")
PYEOF

    # Rebuild workspace index
    bash "$SCRIPT_DIR/run.sh" index

    echo ""
    echo "Done: $RUN_DIR"
    ls -1 "$RUN_DIR"
    ;;

  index)
    YMIND_DIR="$YMIND_DIR" python3 - <<'PYEOF'
import json, os
from pathlib import Path

ymind_dir = Path(os.environ["YMIND_DIR"])
ymind_dir.mkdir(parents=True, exist_ok=True)
runs = []
for meta_path in sorted(ymind_dir.glob("*/meta.json"), reverse=True):
    try:
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        meta["run_dir"] = meta_path.parent.name
        runs.append(meta)
    except Exception:
        pass

index = {"generated_at": __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "runs": runs}
out = ymind_dir / "index.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)
print(f"index.json: {len(runs)} run(s) → {out}")
PYEOF
    python3 "$SCRIPT_DIR/render-index.py" --ws "$YMIND_DIR"
    ;;

  *)
    usage
    ;;
esac
