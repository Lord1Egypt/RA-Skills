#!/usr/bin/env bash
# Install (or replace) the autonomous brainblast-fleet cron job on OpenClaw.
#
# The job is an ISOLATED COMMAND payload: it runs run-fleet.sh directly in the
# Gateway scheduler with no model call, so an unattended run can only ever submit
# proof-gated VTIs. Command cron is an operator-admin surface (requires
# operator.admin), which is exactly right for a self-hosted sourcing loop.
#
# Usage:  install-cron.sh                    # every 6 hours
#         install-cron.sh "every 4h"         # fixed interval
#         install-cron.sh "0 */12 * * *"     # cron expression (gets --tz)
# Env:    BRAINBLAST_CRON_NAME  job name (default brainblast-fleet)
#         BRAINBLAST_CRON_TZ    IANA tz for cron expressions (default UTC)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN="$SCRIPT_DIR/run-fleet.sh"
NAME="${BRAINBLAST_CRON_NAME:-brainblast-fleet}"
TZ_="${BRAINBLAST_CRON_TZ:-UTC}"
SCHED="${1:-every 6h}"

command -v openclaw >/dev/null || { echo "openclaw not found on PATH" >&2; exit 1; }
[ -x "$RUN" ] || chmod +x "$RUN"

# Replace any existing job of the same name so re-running is idempotent.
openclaw cron remove "$NAME" >/dev/null 2>&1 || true

# The schedule is positional (accepts "every 1h", "20m", ISO, or a cron expr).
# Only a cron expression (starts with a digit or *) takes a timezone.
EXTRA=()
case "$SCHED" in
  \**|[0-9]*\ *) EXTRA=(--tz "$TZ_") ;;
esac

# Command payload: no --session, no model call — pure deterministic pipeline.
# --no-deliver = the "none" delivery mode (stdout still captured in cron history).
openclaw cron create "$SCHED" \
  --name "$NAME" \
  --command "$RUN" \
  --timeout-seconds 3600 \
  --no-deliver \
  "${EXTRA[@]}"

echo
echo "Installed cron '$NAME' (schedule: $SCHED)."
echo "  openclaw cron list           # see it"
echo "  openclaw cron runs --id <id> # run history"
echo "  openclaw cron remove $NAME    # remove it"
