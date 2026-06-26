#!/usr/bin/env bash
# Run Codex milestone review for current milestone.
# Must pass before milestone can be marked as completed.
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
  exit 1
fi

# 2. Get current milestone ID
MILESTONE_ID="$(jq -r '.current_milestone_id // "UNKNOWN"' "$STATE" 2>/dev/null || echo UNKNOWN)"
REVIEW_ROUND="$(jq -r '.review_round_current // 0' "$STATE" 2>/dev/null || echo 0)"

if [[ "$MILESTONE_ID" == "UNKNOWN" || "$MILESTONE_ID" == "null" ]]; then
  echo "ERROR: No current milestone set." >&2
  exit 1
fi

# 3. Build context bundle
CONTEXT="$($SCRIPT_DIR/cccc-build-context.sh)"
STAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
OUT="docs/cccc/reviews/milestones/${MILESTONE_ID}-r${REVIEW_ROUND}-${STAMP}.json"
PROMPT="docs/cccc/runtime/${MILESTONE_ID}-review-prompt-$STAMP.md"

mkdir -p docs/cccc/reviews/milestones docs/cccc/runtime

cat > "$PROMPT" <<EOF2
$(cat "$SKILL_DIR/prompts/codex-milestone-review.md")

---

# Context Bundle

$(cat "$CONTEXT")
EOF2

# 4. Update state: running review
python3 - "$STATE" "$MILESTONE_ID" <<'PY'
import json
from pathlib import Path
p = Path('docs/cccc/state.json')
try:
    data = json.loads(p.read_text())
except Exception:
    data = {}
data['current_milestone_codex_review_status'] = 'running'
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
PY

# 5. Run Codex review
CLI_CMD="$(jq -r '.codex.cli_command // "codex"' docs/cccc/config.json 2>/dev/null || echo "codex")"

SUCCESS=false
REVIEW_STATUS="invalid"

if "$CLI_CMD" exec \
  --cd "$ROOT" \
  --sandbox read-only \
  --output-schema "$SKILL_DIR/schemas/codex-milestone-review.schema.json" \
  --output-last-message "$OUT" \
  - < "$PROMPT" 2>/dev/null; then
  SUCCESS=true
fi

# 6. Parse result and update state
if $SUCCESS && [[ -f "$OUT" ]]; then
  REVIEW_STATUS="$(jq -r '.status // "invalid"' "$OUT" 2>/dev/null || echo "invalid")"

  python3 - "$STATE" "$OUT" "$MILESTONE_ID" "$REVIEW_STATUS" <<'PY'
import json, sys
from pathlib import Path
p = Path('docs/cccc/state.json')
try:
    data = json.loads(p.read_text())
except Exception:
    data = {}

out_file = sys.argv[1] if len(sys.argv) > 1 else ''
milestone_id = sys.argv[2] if len(sys.argv) > 2 else ''
status = sys.argv[3] if len(sys.argv) > 3 else 'invalid'

data['current_milestone_codex_review_status'] = status
data['current_milestone_codex_review_file'] = out_file
data['last_codex_milestone_review_file'] = out_file

if status == 'pass':
    # Milestone approved, nothing else to do here
    pass
elif status == 'fail_fixable':
    data['fix_attempts_current'] = data.get('fix_attempts_current', 0) + 1
elif status in ('needs_human', 'fail_unclear', 'unsafe', 'sensitive_operation'):
    data['status'] = 'PAUSED_FOR_HUMAN'
    data['pause_reason'] = f'Codex milestone review needs human decision: {status}'

p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
PY
else
  # Codex failed or output missing
  python3 - "$STATE" "$MILESTONE_ID" <<'PY'
import json, sys
from pathlib import Path
p = Path('docs/cccc/state.json')
try:
    data = json.loads(p.read_text())
except Exception:
    data = {}

milestone_id = sys.argv[1] if len(sys.argv) > 1 else ''
data['current_milestone_codex_review_status'] = 'unavailable'
data['status'] = 'PAUSED_FOR_CODEX'
data['codex_unavailable_reason'] = 'Codex execution failed or output missing.'
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
PY
  echo "ERROR: Codex review failed or output missing." >&2
  exit 1
fi

echo "Codex milestone review complete: $OUT"
echo "Status: $REVIEW_STATUS"
echo "Milestone: $MILESTONE_ID"

if [[ "$REVIEW_STATUS" != "pass" ]]; then
  exit 1
fi