#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SCRIPT="$SCRIPT_DIR/backup.sh"
CRON_NAME="${CRON_NAME:-OpenClaw Daily Backup}"
CRON_EXPR="${CRON_EXPR:-0 4 * * *}"
CRON_TZ="${CRON_TZ:-}"

warn() { printf 'WARNING: %s\n' "$*" >&2; }
info() { printf '%s\n' "$*"; }
die() { warn "$*"; exit 1; }

command -v openclaw >/dev/null 2>&1 || die "openclaw CLI is required"
command -v python3 >/dev/null 2>&1 || die "python3 is required"
[ -x "$BACKUP_SCRIPT" ] || die "Backup script is not executable: $BACKUP_SCRIPT"

SYSTEM_EVENT="Run the scheduled OpenClaw backup now by executing: bash '$BACKUP_SCRIPT'. Default to operational-only mode unless Don explicitly requested encrypted secrets backup. After completion, report the manifest path, operational archive path, and whether verification is needed."

EXISTING_ID="$(openclaw cron list --json | python3 - "$CRON_NAME" <<'PY'
import json, sys
name = sys.argv[1]
try:
    data = json.load(sys.stdin)
except Exception:
    print('')
    raise SystemExit(0)
for job in data.get('jobs', []):
    if job.get('name') == name:
        print(job.get('id') or '')
        break
PY
)"

if [ -n "$EXISTING_ID" ]; then
  info "Replacing existing cron: $CRON_NAME ($EXISTING_ID)"
  openclaw cron delete "$EXISTING_ID" >/dev/null
else
  info "Creating cron: $CRON_NAME"
fi

if [ -n "$CRON_TZ" ]; then
  RESULT="$(openclaw cron create --json --name "$CRON_NAME" --cron "$CRON_EXPR" --tz "$CRON_TZ" --system-event "$SYSTEM_EVENT")"
else
  RESULT="$(openclaw cron create --json --name "$CRON_NAME" --cron "$CRON_EXPR" --system-event "$SYSTEM_EVENT")"
fi

printf '%s\n' "$RESULT"

NEXT_RUN="$(printf '%s' "$RESULT" | python3 -c 'import json,sys; data=json.load(sys.stdin); print(data.get("job",{}).get("nextRunAtMs") or data.get("nextRunAt") or "")')"
if [ -z "$NEXT_RUN" ]; then
  warn "Cron created, but nextRunAtMs/nextRunAt was not returned. Verify with: openclaw cron list"
else
  info "Verified next run marker: $NEXT_RUN"
fi

info "Note: Existing cron entries with the same name are replaced instead of duplicated."
