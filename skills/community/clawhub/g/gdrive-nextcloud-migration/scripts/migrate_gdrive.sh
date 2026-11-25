#!/usr/bin/env bash
# Google Drive -> Nextcloud migration copy (rclone) + error triage report.
# Based on the Low-tech Lab "Vers un numerique souverain et resilient" procedure.
#
# Usage:
#   migrate_gdrive.sh SRC_REMOTE:PATH DST_REMOTE:PATH LOG_DIR [options]
#   migrate_gdrive.sh --report-only LOG_DIR
# Options:
#   --exclude PATTERN     pattern to skip (repeatable)
#   --dry-run             preview only, nothing transferred
#   --bwlimit RATE        bandwidth cap, e.g. 5M or "08:00,512k 23:00,off"
#   --max-transfer SIZE   stop after SIZE transferred, e.g. 10G
# Credentials: never passed here. Remotes must already exist in rclone config
# (the user runs `rclone config` once, interactively). Missing remotes are
# detected and reported before any transfer.
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage: migrate_gdrive.sh SRC_REMOTE:PATH DST_REMOTE:PATH LOG_DIR [options]
       migrate_gdrive.sh --report-only LOG_DIR
Options: --exclude PATTERN (repeatable) | --dry-run | --bwlimit RATE | --max-transfer SIZE
EOF
}

# report LOGFILE REPORTFILE -> prints counts, writes triage report;
# exits 0 when no errors, 1 otherwise.
report() {
  local log=$1 out=$2 n_long n_other
  n_long=$(grep -Ec 'trop long|too long' "$log" 2>/dev/null || true)
  n_other=$(grep -E 'ERROR' "$log" 2>/dev/null | grep -Evc 'trop long|too long' || true)
  {
    echo "== rclone error report $(date -Is) =="
    echo "log: $log"
    echo
    echo "-- Filenames too long: rename at source (or rclone moveto), then re-run copy --"
    grep -E 'trop long|too long' "$log" 2>/dev/null || echo "(none)"
    echo
    echo "-- Other errors (triage individually) --"
    grep -E 'ERROR' "$log" 2>/dev/null | grep -Ev 'trop long|too long' || echo "(none)"
  } > "$out"
  echo "errors: $((n_long + n_other)) total ($n_long name-too-long, $n_other other)"
  echo "report: $out"
  [ "$((n_long + n_other))" -eq 0 ]
}

if [ "${1:-}" = "--report-only" ]; then
  [ $# -eq 2 ] || { usage; exit 2; }
  LOG="$2/rclone_gdrive.txt"
  [ -f "$LOG" ] || { echo "no log at $LOG" >&2; exit 2; }
  report "$LOG" "$2/errors_report.txt" && exit 0 || exit 1
fi

[ $# -ge 3 ] || { usage; exit 2; }
SRC=$1 DST=$2 LOGDIR=$3; shift 3
EXCLUDES=() EXTRA=() DRY=0
while [ $# -gt 0 ]; do
  case $1 in
    --exclude) [ $# -ge 2 ] || { usage; exit 2; }; EXCLUDES+=(--exclude "$2"); shift 2 ;;
    --dry-run) DRY=1; EXTRA+=(--dry-run); shift ;;
    --bwlimit|--max-transfer) [ $# -ge 2 ] || { usage; exit 2; }; EXTRA+=("$1" "$2"); shift 2 ;;
    *) echo "unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

command -v rclone >/dev/null 2>&1 || { echo "rclone is not installed" >&2; exit 1; }

# Credentials check: remote names only, no secrets. Ask the user to run
# `rclone config` for anything missing — never configure credentials here.
CONFIGURED=$(rclone listremotes)
for spec in "$SRC" "$DST"; do
  case $spec in
    *:*)
      r=${spec%%:*}
      if ! printf '%s\n' "$CONFIGURED" | grep -qx "$r:"; then
        echo "remote '$r:' is not configured. Run: rclone config  (interactive, by you — no secrets in chat or scripts)" >&2
        exit 1
      fi
      ;;
  esac
done

mkdir -p "$LOGDIR"
LOG="$LOGDIR/rclone_gdrive.txt"
LEVEL=ERROR
if [ "$DRY" -eq 1 ]; then LEVEL=INFO; fi

rc=0
rclone copy "$SRC" "$DST" \
  --drive-export-formats ods,odt,odp \
  --drive-skip-dangling-shortcuts \
  --links \
  ${EXCLUDES[@]+"${EXCLUDES[@]}"} \
  ${EXTRA[@]+"${EXTRA[@]}"} \
  --log-level "$LEVEL" --log-file "$LOG" --progress || rc=$?

echo
if [ "$DRY" -eq 1 ]; then echo "DRY-RUN: nothing was transferred."; fi
report "$LOG" "$LOGDIR/errors_report.txt" || true
echo "rclone exit code: $rc"
exit "$rc"
