#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/_common.sh"

TIMESTAMP="$(python3 - <<'PY'
from datetime import datetime
print(datetime.now().strftime('%Y%m%d-%H%M%S'))
PY
)"
TMP_ROOT="${TMPDIR:-/tmp}"
EVIDENCE_DIR_DEFAULT="$TMP_ROOT/clawtune-script-evidence-$TIMESTAMP"
export CLAWTUNE_EVIDENCE_DIR="${CLAWTUNE_EVIDENCE_DIR:-$EVIDENCE_DIR_DEFAULT}"
ensure_evidence_dir

"$SCRIPT_DIR/session-state.sh" init > /dev/null
append_log "run.log" "main-flow-smoke started evidence_dir=$CLAWTUNE_EVIDENCE_DIR"

"$SCRIPT_DIR/auth-bootstrap.sh" ensure | tee "$CLAWTUNE_EVIDENCE_DIR/00-auth-bootstrap.out.txt"
"$SCRIPT_DIR/generate-playlist.sh" \
  "Late Night City Walk" \
  "A moody but not too dark original playlist for walking home after overtime." \
  "late night walking after overtime, slightly emo, atmospheric, not too dark" \
  3 5 false | tee "$CLAWTUNE_EVIDENCE_DIR/01-generate-playlist.out.txt"
"$SCRIPT_DIR/create-draft.sh" \
  "A warm cinematic anniversary song based on a late-night city-walk feeling." \
  "anniversary" \
  "mandopop" \
  "zh-CN" \
  "warm" \
  "gift" \
  "We walked home together after long days and still felt close." | tee "$CLAWTUNE_EVIDENCE_DIR/02-create-draft.out.txt"
"$SCRIPT_DIR/update-draft.sh" "" "" "" "" "bright" "" "" | tee "$CLAWTUNE_EVIDENCE_DIR/03-update-draft.out.txt"
"$SCRIPT_DIR/recommend-draft.sh" | tee "$CLAWTUNE_EVIDENCE_DIR/04-recommend-draft.out.txt"
"$SCRIPT_DIR/create-order.sh" "" "A warm cinematic anniversary song with gentle late-night imagery." "CNY" | tee "$CLAWTUNE_EVIDENCE_DIR/05-create-order.out.txt"
"$SCRIPT_DIR/check-order-status.sh" | tee "$CLAWTUNE_EVIDENCE_DIR/06-check-order-status.out.txt"
"$SCRIPT_DIR/check-order-delivery.sh" | tee "$CLAWTUNE_EVIDENCE_DIR/07-check-order-delivery.out.txt"
if "$SCRIPT_DIR/check-public-result.sh" order | tee "$CLAWTUNE_EVIDENCE_DIR/08-check-public-result.out.txt"; then
  append_log "run.log" "public order result check succeeded"
else
  append_log "run.log" "public order result check failed"
fi
if "$SCRIPT_DIR/recover-order.sh" | tee "$CLAWTUNE_EVIDENCE_DIR/09-recover-order.out.txt"; then
  append_log "run.log" "recover-order succeeded"
else
  append_log "run.log" "recover-order failed"
fi
if "$SCRIPT_DIR/check-public-result.sh" playlist | tee "$CLAWTUNE_EVIDENCE_DIR/10-check-public-playlist.out.txt"; then
  append_log "run.log" "public playlist result check succeeded"
else
  append_log "run.log" "public playlist result check skipped-or-failed"
fi

save_session_snapshot
printf '%s\n' "$CLAWTUNE_EVIDENCE_DIR"
