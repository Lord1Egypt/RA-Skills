#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
REPO_DIR="$SKILL_DIR"
WRAPPER="$SCRIPT_DIR/gemini_smart_search.sh"
PYTHON_ENTRY="$SCRIPT_DIR/gemini_smart_search.py"

pass() { printf 'PASS: %s\n' "$1"; }
info() { printf 'INFO: %s\n' "$1"; }
fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }

json_assert() {
  local file="$1"
  local mode="$2"
  python3 - "$file" "$mode" <<'PY'
import json, sys
path, expected_mode = sys.argv[1], sys.argv[2]
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
required = ["ok", "query", "mode", "model_used", "fallback_chain", "display_chain", "answer", "citations", "error", "escalation"]
missing = [k for k in required if k not in data]
if missing:
    raise SystemExit(f"missing keys: {missing}")
if data["mode"] != expected_mode:
    raise SystemExit(f"unexpected mode: {data['mode']}")
if not isinstance(data["fallback_chain"], list):
    raise SystemExit("fallback_chain must be a list")
if not isinstance(data["citations"], list):
    raise SystemExit("citations must be a list")
usage = data.get("usage", {})
if usage.get("provider") != "gemini":
    raise SystemExit(f"unexpected provider: {usage.get('provider')}")
if not isinstance(usage.get("grounding"), bool):
    raise SystemExit("usage.grounding must be boolean")
error = data.get("error")
if not isinstance(error, dict):
    raise SystemExit("error must be an object in missing-key smoke mode")
if error.get("type") != "missing_api_key":
    raise SystemExit(f"unexpected error type: {error.get('type')}")
escalation = data.get("escalation")
if not isinstance(escalation, dict):
    raise SystemExit("escalation must be an object")
if escalation.get("should_open_issue") not in (False, None):
    raise SystemExit("missing-key path should not request issue creation")
print("JSON_OK")
PY
}

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

for mode in cheap balanced deep; do
  out="$TMP_DIR/$mode.json"
  set +e
  env -i PATH="$PATH" GEMINI_SMART_SEARCH_SKIP_LOCAL_ENV=1 python3 "$PYTHON_ENTRY" --query "smoke test" --mode "$mode" --json > "$out"
  status=$?
  set -e
  if [ "$status" -ne 1 ]; then
    fail "expected missing-key smoke path to exit 1 for mode=$mode; got $status"
  fi
  json_assert "$out" "$mode" >/dev/null
  pass "non-destructive JSON smoke passes for mode=$mode"
done

if git -C "$REPO_DIR" check-ignore .env.local >/dev/null 2>&1; then
  pass ".env.local is gitignored"
else
  fail ".env.local is not ignored"
fi

if [ "${LIVE_SMOKE:-0}" = "1" ]; then
  info "LIVE_SMOKE=1 set; running one live wrapper query"
  live_out="$TMP_DIR/live.json"
  "$WRAPPER" --query "BoundaryML context engineering" --mode cheap --json > "$live_out"
  python3 - "$live_out" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = json.load(f)
if not data.get('ok'):
    raise SystemExit(f"live smoke failed: {data.get('error')}")
if not data.get('model_used'):
    raise SystemExit('live smoke missing model_used')
if not isinstance(data.get('citations'), list):
    raise SystemExit('live smoke citations must be a list')
print('LIVE_OK')
PY
  pass "live wrapper smoke succeeded"
else
  info "Skipped live wrapper query. Set LIVE_SMOKE=1 to verify repo-local env loading and real API path."
fi

printf 'Smoke tests completed successfully.\n'
