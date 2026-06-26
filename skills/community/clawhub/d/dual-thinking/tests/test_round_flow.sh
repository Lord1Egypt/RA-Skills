#!/usr/bin/env bash
set -euo pipefail

FIXTURE="${1:-$(dirname "$0")/fixtures/sample-round-block.txt}"

require() {
  local needle="$1"
  if ! grep -Fq "$needle" "$FIXTURE"; then
    echo "[FAIL] missing field: $needle" >&2
    exit 1
  fi
}

require 'ROUND:'
require 'TOPIC:'
require 'MODE:'
require 'SESSION:'
require 'DECISION:'
require 'NEXT_ACTION:'
require 'CHAT_CONTINUITY:'
require 'VALIDATION_STATUS:'
require 'RESUME_SNIPPET:'

ROUND_NUM="$(awk '/^ROUND:/{print $2; exit}' "$FIXTURE")"
CHAT_CONTINUITY="$(awk -F': ' '/^CHAT_CONTINUITY:/{print $2; exit}' "$FIXTURE")"
ORCHESTRATOR_MODE="$(awk -F': ' '/^ORCHESTRATOR_MODE:/{print $2; exit}' "$FIXTURE")"

if [[ "$ORCHESTRATOR_MODE" == "api" || "$ORCHESTRATOR_MODE" == "multi" ]]; then
  require 'SELF_POSITION_STATUS:'
  require 'CONSULTANT_POSITION_STATUS:'
  require 'SYNTHESIS_STATUS:'

  status_block="$(awk '
    BEGIN { after_resume=0; capture=0 }
    /^RESUME_SNIPPET:/ { after_resume=1; next }
    after_resume && /^[^[:space:]].*: / {
      if ($0 ~ /^SELF_POSITION_STATUS:/ || $0 ~ /^CONSULTANT_POSITION_STATUS:/ || $0 ~ /^SYNTHESIS_STATUS:/) {
        print $0
        capture++
        if (capture == 3) exit
      } else {
        print "__BREAK__"
        exit
      }
    }
    after_resume { next }
  ' "$FIXTURE")"

  expected=$'SELF_POSITION_STATUS:\nCONSULTANT_POSITION_STATUS:\nSYNTHESIS_STATUS:'
  normalized="$(printf '%s\n' "$status_block" | sed 's/:.*/:/')"

  if [[ "$normalized" != "$expected" ]]; then
    echo '[FAIL] consultant-bearing status fields must be the first top-level fields after RESUME_SNIPPET and appear in exact order' >&2
    exit 1
  fi
fi

if [[ -n "$ROUND_NUM" ]] && [[ "$ROUND_NUM" -gt 1 ]] && [[ "$CHAT_CONTINUITY" == "new" ]]; then
  echo '[FAIL] round 2+ cannot default to a new chat' >&2
  exit 1
fi

if grep -Fq 'PATCH_STATUS: applied' "$FIXTURE"; then
  require 'PATCH_MANIFEST:'
fi

VALIDATION_STATUS="$(awk -F': ' '/^VALIDATION_STATUS:/{print $2; exit}' "$FIXTURE")"
PUBLISH_STATUS="$(awk -F': ' '/^PUBLISH_STATUS:/{print $2; exit}' "$FIXTURE")"

case "$VALIDATION_STATUS" in
  passed|failed|blocked) ;;
  *)
    echo '[FAIL] VALIDATION_STATUS must be passed|failed|blocked' >&2
    exit 1
    ;;
esac

if [[ "$PUBLISH_STATUS" == "Packaged" || "$PUBLISH_STATUS" == "Published" ]]; then
  if [[ "$VALIDATION_STATUS" != "passed" ]]; then
    echo '[FAIL] packaged/published requires VALIDATION_STATUS: passed' >&2
    exit 1
  fi
fi

if grep -Fq 'CONTINUATION_SIGNAL: stop' "$FIXTURE"; then
  if grep -Fq 'PATCH_STATUS: proposed' "$FIXTURE"; then
    echo '[FAIL] stop signal cannot coexist with unapplied proposed patch' >&2
    exit 1
  fi
fi

echo '[OK] round flow fixture passed'
