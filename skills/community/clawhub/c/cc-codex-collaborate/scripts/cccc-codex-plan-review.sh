#!/usr/bin/env bash
# Run Codex adversarial plan review.
# Must succeed before implementation can start.
# Never silently continue on failure.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/cccc-common.sh"

ROOT="$(cccc_repo_root)"
cd "$ROOT"
cccc_init_dirs

STATE="docs/cccc/state.json"
SKILL_DIR="$(cccc_skill_dir)"

# 1. Check Codex availability
if ! "$SCRIPT_DIR/cccc-codex-check.sh"; then
  echo "Codex unavailable. Pausing."
  # State already updated by cccc-codex-check.sh
  exit 1
fi

# 2. Build context bundle
CONTEXT="$($SCRIPT_DIR/cccc-build-context.sh)"
STAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
OUT="docs/cccc/reviews/plan/plan-review-$STAMP.json"
PROMPT="docs/cccc/runtime/plan-review-prompt-$STAMP.md"

mkdir -p docs/cccc/reviews/plan docs/cccc/runtime

cat > "$PROMPT" <<EOF2
$(cat "$SKILL_DIR/prompts/codex-plan-adversarial-review.md")

---

# Context Bundle

$(cat "$CONTEXT")
EOF2

# 3. Update state: running review
python3 - "$STATE" <<'PY'
import json
from pathlib import Path
p = Path('docs/cccc/state.json')
try:
    data = json.loads(p.read_text())
except Exception:
    data = {}
data['codex_plan_review_status'] = 'running'
data['updated_at'] = data.get('updated_at', '')
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
PY

# 4. Run Codex review
CLI_CMD="$(jq -r '.codex.cli_command // "codex"' docs/cccc/config.json 2>/dev/null || echo "codex")"

SUCCESS=false
REVIEW_STATUS="invalid"
REASON=""

if "$CLI_CMD" exec \
  --cd "$ROOT" \
  --sandbox read-only \
  --output-schema "$SKILL_DIR/schemas/codex-plan-review.schema.json" \
  --output-last-message "$OUT" \
  - < "$PROMPT" 2>/dev/null; then
  SUCCESS=true
fi

# 5. Parse result and update state
if $SUCCESS && [[ -f "$OUT" ]]; then
  # Parse the review JSON
  REVIEW_STATUS="$(jq -r '.status // "invalid"' "$OUT" 2>/dev/null || echo "invalid")"

  python3 - "$STATE" "$OUT" "$REVIEW_STATUS" <<'PY'
import json
from pathlib import Path
p = Path('docs/cccc/state.json')
try:
    data = json.loads(p.read_text())
except Exception:
    data = {}

out_file = sys.argv[1] if len(sys.argv) > 1 else ''
status = sys.argv[2] if len(sys.argv) > 2 else 'invalid'

data['codex_plan_review_status'] = status
data['last_codex_plan_review_file'] = out_file

if status == 'pass' or status == 'approved':
    data['roadmap_status'] = 'codex_approved'
else:
    data['roadmap_status'] = 'codex_rejected'
    if status in ('needs_human', 'fail_unclear'):
        data['status'] = 'PAUSED_FOR_HUMAN'
        data['pause_reason'] = 'Codex plan review needs human decision.'
    elif status == 'unsafe':
        data['status'] = 'PAUSED_FOR_HUMAN'
        data['pause_reason'] = 'Codex flagged plan as unsafe.'

p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
PY
else
  # Codex failed or output missing
  python3 - "$STATE" <<'PY'
import json
from pathlib import Path
p = Path('docs/cccc/state.json')
try:
    data = json.loads(p.read_text())
except Exception:
    data = {}
data['codex_plan_review_status'] = 'unavailable'
data['status'] = 'PAUSED_FOR_CODEX'
data['codex_unavailable_reason'] = 'Codex execution failed or output missing.'
data['roadmap_status'] = 'codex_failed'
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
PY
  echo "ERROR: Codex review failed or output missing." >&2
  exit 1
fi

echo "Codex plan review complete: $OUT"
echo "Status: $REVIEW_STATUS"

if [[ "$REVIEW_STATUS" != "pass" && "$REVIEW_STATUS" != "approved" ]]; then
  exit 1
fi