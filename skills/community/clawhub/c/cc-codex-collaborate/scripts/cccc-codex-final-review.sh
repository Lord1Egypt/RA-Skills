#!/usr/bin/env bash
# Run Codex final review after all milestones are complete.
# Must pass before task can be marked DONE.
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

# 2. Build context bundle
CONTEXT="$($SCRIPT_DIR/cccc-build-context.sh)"
STAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
OUT="docs/cccc/reviews/final/final-review-$STAMP.json"
PROMPT="docs/cccc/runtime/final-review-prompt-$STAMP.md"

mkdir -p docs/cccc/reviews/final docs/cccc/runtime

# 3. Create final review prompt
cat > "$PROMPT" <<'EOF2'
# Final Review Request

You are Codex, an independent read-only reviewer. Perform a final review of the completed task.

## Review Checklist

1. Are all milestones marked as completed in the milestone backlog?
2. Was each milestone reviewed by Codex with status = pass?
3. Are there any remaining risks or unresolved issues?
4. Did the implementation stay within scope?
5. Are there any untested or unverified changes?
6. Are there any secret, wallet, API key, production, or real-money risks remaining?
7. Is the final diff clean and well-structured?
8. Are there any TODOs or placeholder code left?

## Output Format

Return JSON with:
```json
{
  "status": "pass" | "fail_fixable" | "needs_human" | "unsafe",
  "summary": "Brief summary of review outcome",
  "issues": ["List of any remaining issues"],
  "risks": ["List of any remaining risks"],
  "recommendations": ["Optional next steps"]
}
```

---

EOF2

cat "$CONTEXT" >> "$PROMPT"

# 4. Update state: running final review
python3 - "$STATE" <<'PY'
import json
from pathlib import Path
p = Path('docs/cccc/state.json')
try:
    data = json.loads(p.read_text())
except Exception:
    data = {}
data['codex_final_review_status'] = 'running'
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
PY

# 5. Run Codex review
CLI_CMD="$(jq -r '.codex.cli_command // "codex"' docs/cccc/config.json 2>/dev/null || echo "codex")"

SUCCESS=false
REVIEW_STATUS="invalid"

# Use a simple schema for final review
SCHEMA='{"type":"object","properties":{"status":{"type":"string"},"summary":{"type":"string"},"issues":{"type":"array"},"risks":{"type":"array"},"recommendations":{"type":"array"}},"required":["status"]}'

if "$CLI_CMD" exec \
  --cd "$ROOT" \
  --sandbox read-only \
  --output-schema-json "$SCHEMA" \
  --output-last-message "$OUT" \
  - < "$PROMPT" 2>/dev/null; then
  SUCCESS=true
fi

# 6. Parse result and update state
if $SUCCESS && [[ -f "$OUT" ]]; then
  REVIEW_STATUS="$(jq -r '.status // "invalid"' "$OUT" 2>/dev/null || echo "invalid")"

  python3 - "$STATE" "$OUT" "$REVIEW_STATUS" <<'PY'
import json, sys
from pathlib import Path
p = Path('docs/cccc/state.json')
try:
    data = json.loads(p.read_text())
except Exception:
    data = {}

out_file = sys.argv[1] if len(sys.argv) > 1 else ''
status = sys.argv[2] if len(sys.argv) > 2 else 'invalid'

data['codex_final_review_status'] = status
data['last_codex_final_review_file'] = out_file

if status != 'pass':
    data['status'] = 'PAUSED_FOR_HUMAN'
    data['pause_reason'] = f'Codex final review requires attention: {status}'

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
data['codex_final_review_status'] = 'unavailable'
data['status'] = 'PAUSED_FOR_CODEX'
data['codex_unavailable_reason'] = 'Codex execution failed or output missing.'
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
PY
  echo "ERROR: Codex final review failed or output missing." >&2
  exit 1
fi

echo "Codex final review complete: $OUT"
echo "Status: $REVIEW_STATUS"

if [[ "$REVIEW_STATUS" != "pass" ]]; then
  exit 1
fi