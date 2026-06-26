#!/usr/bin/env bash
# aegis_toggle_feed.sh — Enable/disable the AEGIS 5-minute live feed cron safely.
# Usage:
#   ./aegis_toggle_feed.sh status          # print current cron status
#   ./aegis_toggle_feed.sh enable          # enable the AEGIS-feed cron
#   ./aegis_toggle_feed.sh disable         # disable the AEGIS-feed cron
#   ./aegis_toggle_feed.sh enable --minutes 60  # enable for 60 minutes then disable

CRON_ID="56addb4c-8b6a-4a72-b2f0-8cadac441971"
OPENCLAW=openclaw

set -euo pipefail

cmd=${1:-status}
shift || true

function status() {
  $OPENCLAW cron list --json | jq -r --arg id "$CRON_ID" '.entries[] | select(.id==$id) | "id:\(.id) name:\(.name) enabled:\(.enabled) schedule:\(.schedule.expr) next:\(.state.nextRunAtMs)"' || echo "AEGIS-feed not found"
}

function enable_cron() {
  echo "Enabling AEGIS-feed cron (id=$CRON_ID)" >&2
  $OPENCLAW cron enable "$CRON_ID"
}

function disable_cron() {
  echo "Disabling AEGIS-feed cron (id=$CRON_ID)" >&2
  $OPENCLAW cron disable "$CRON_ID"
}

if [ "$cmd" = "status" ]; then
  status
  exit 0
fi

if [ "$cmd" = "enable" ]; then
  # safety check: confirm manual approval unless --yes is provided
  minutes=0
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --minutes)
        minutes=$2; shift 2;;
      --yes)
        APPROVE=1; shift;;
      *) shift;;
    esac
  done

  if [ "${APPROVE-0}" != "1" ]; then
    echo "WARNING: Live feed posts frequently. Confirm you really want to enable by re-running with --yes or pass --minutes <n> to enable temporarily." >&2
    exit 2
  fi

  enable_cron

  if [ "$minutes" -gt 0 ]; then
    echo "Will auto-disable after ${minutes} minutes." >&2
    # schedule background disable
    (sleep $((minutes*60)) && $OPENCLAW cron disable "$CRON_ID" && echo "AEGIS-feed auto-disabled after ${minutes} minutes" >&2) &
  fi
  exit 0
fi

if [ "$cmd" = "disable" ]; then
  disable_cron
  exit 0
fi

echo "Usage: $0 {status|enable|disable} [--minutes N] [--yes]" >&2
exit 1
