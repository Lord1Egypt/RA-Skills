#!/usr/bin/env bash
set -euo pipefail

FIXTURE="${1:-$(dirname "$0")/fixtures/weak-model-shortcut-round.txt}"

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
require 'PATCH_STATUS:'
require 'CONTINUATION_SIGNAL:'
require 'NEXT_ACTION:'
require 'CHAT_CONTINUITY:'
require 'RESUME_SNIPPET:'
require 'SELF_POSITION_STATUS:'
require 'CONSULTANT_POSITION_STATUS:'
require 'SYNTHESIS_STATUS:'

if ! grep -Fq 'SELF_POSITION_COMPACT:' "$FIXTURE"; then
  echo '[FAIL] weak-model shortcut must keep compact self-position' >&2
  exit 1
fi

if ! grep -Fq 'CONSULTANT_POSITION_COMPACT:' "$FIXTURE"; then
  echo '[FAIL] weak-model shortcut must keep compact consultant position in consultant-bearing rounds' >&2
  exit 1
fi

if ! grep -Fq 'SYNTHESIS_COMPACT:' "$FIXTURE"; then
  echo '[FAIL] weak-model shortcut must keep compact synthesis' >&2
  exit 1
fi

if grep -Fq 'LAST_CONSULTANT:' "$FIXTURE"; then
  echo '[OK] weak-model shortcut fixture passed with optional LAST_CONSULTANT'
else
  echo '[OK] weak-model shortcut fixture passed'
fi
