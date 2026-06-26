#!/bin/bash

set -euo pipefail

# Usage: deliver-gift.sh <html-file> <setup-state-file> [deploy-script]
# Example:
#   deliver-gift.sh ./workspace/gifts/2026-03-25-hello.html ./workspace/daily-gift/setup-state.json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HTML_FILE="${1:-}"
SETUP_STATE_FILE="${2:-}"
DEPLOY_SCRIPT="${3:-$SCRIPT_DIR/deploy.sh}"

if [ -z "$HTML_FILE" ] || [ -z "$SETUP_STATE_FILE" ]; then
  echo "Usage: deliver-gift.sh <html-file> <setup-state-file> [deploy-script]" >&2
  exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
  echo "HTML file not found: $HTML_FILE" >&2
  exit 1
fi

HTML_FILE_ABS="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$HTML_FILE")"

read_setup_state() {
  python3 - "$1" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])

if not path.exists():
    print(
        json.dumps(
            {
                "setup_present": 0,
                "hosting_enabled": 0,
                "provider": "",
                "domain": "",
                "warning": "setup_state_missing",
            }
        )
    )
    raise SystemExit(0)

try:
    data = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    print(
        json.dumps(
            {
                "setup_present": 1,
                "hosting_enabled": 0,
                "provider": "",
                "domain": "",
                "warning": "setup_state_invalid",
            }
        )
    )
    raise SystemExit(0)

hosting = data.get("hosting") or {}
enabled = bool(hosting.get("enabled"))
provider = str(hosting.get("provider") or "")
domain = str(hosting.get("domain") or "")
warning = ""

if enabled and (not provider or not domain):
    enabled = False
    warning = "hosting_incomplete"
elif not enabled:
    warning = "hosting_disabled"

print(
    json.dumps(
        {
            "setup_present": 1,
            "hosting_enabled": 1 if enabled else 0,
            "provider": provider,
            "domain": domain,
            "warning": warning,
        }
    )
)
PY
}

print_result() {
  python3 - "$@" <<'PY'
import json
import sys

delivery_mode, url, html_file, provider, domain, fallback_reason, warning = sys.argv[1:]
print(
    json.dumps(
        {
            "delivery_mode": delivery_mode,
            "url": url,
            "html_file": html_file,
            "provider": provider,
            "domain": domain,
            "fallback_reason": fallback_reason,
            "warning": warning,
        },
        ensure_ascii=True,
    )
)
PY
}

SETUP_STATE_JSON="$(read_setup_state "$SETUP_STATE_FILE")"
HOSTING_ENABLED="$(python3 -c 'import json,sys; print(json.loads(sys.stdin.read())["hosting_enabled"])' <<<"$SETUP_STATE_JSON")"
PROVIDER="$(python3 -c 'import json,sys; print(json.loads(sys.stdin.read())["provider"])' <<<"$SETUP_STATE_JSON")"
DOMAIN="$(python3 -c 'import json,sys; print(json.loads(sys.stdin.read())["domain"])' <<<"$SETUP_STATE_JSON")"
STATE_WARNING="$(python3 -c 'import json,sys; print(json.loads(sys.stdin.read())["warning"])' <<<"$SETUP_STATE_JSON")"

if [ "$HOSTING_ENABLED" = "1" ]; then
  if [ ! -x "$DEPLOY_SCRIPT" ]; then
    print_result "local_file" "" "$HTML_FILE_ABS" "" "" "deploy_script_not_executable" "Deploy script is missing or not executable: $DEPLOY_SCRIPT"
    exit 0
  fi

  if DEPLOY_OUTPUT="$("$DEPLOY_SCRIPT" "$HTML_FILE_ABS" "$DOMAIN" "$PROVIDER" 2>&1)"; then
    DEPLOY_URL="$(python3 -c 'import sys; lines=[line.strip() for line in sys.stdin.read().splitlines() if line.strip()]; urls=[line for line in lines if line.startswith(("http://", "https://"))]; print(urls[-1] if urls else (lines[-1] if lines else ""))' <<<"$DEPLOY_OUTPUT")"
    if [[ "$DEPLOY_URL" != http://* && "$DEPLOY_URL" != https://* ]]; then
      DEPLOY_WARNING="$(printf '%s' "$DEPLOY_OUTPUT" | python3 -c 'import sys; print(sys.stdin.read().strip().replace("\n", " | "))')"
      print_result "local_file" "" "$HTML_FILE_ABS" "" "" "deploy_output_missing_url" "$DEPLOY_WARNING"
      exit 0
    fi
    print_result "hosted_url" "$DEPLOY_URL" "$HTML_FILE_ABS" "$PROVIDER" "$DOMAIN" "" ""
    exit 0
  fi

  DEPLOY_WARNING="$(printf '%s' "$DEPLOY_OUTPUT" | python3 -c 'import sys; print(sys.stdin.read().strip().replace("\n", " | "))')"
  print_result "local_file" "" "$HTML_FILE_ABS" "" "" "deploy_failed" "$DEPLOY_WARNING"
  exit 0
fi

print_result "local_file" "" "$HTML_FILE_ABS" "" "" "$STATE_WARNING" ""
