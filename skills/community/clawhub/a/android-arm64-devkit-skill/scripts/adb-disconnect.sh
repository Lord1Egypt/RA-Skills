#!/usr/bin/env bash
# Tear down the adb session cleanly.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/adb.sh
. "$HERE/lib/adb.sh"
[ -f "$HERE/../config.sh" ] && . "$HERE/../config.sh"

DEV="$(cat "$HERE/../.adb-device" 2>/dev/null || true)"
if [ -n "${ADB_HOST:-}" ] && [ -n "$DEV" ]; then
  echo "disconnecting $DEV"
  adb_call disconnect "$DEV" | sed 's/^/  /'
fi

if [ "${1:-}" = "--restart-server" ]; then
  echo "restarting adb server"
  adb_call kill-server || true
  adb_call start-server || true
fi

rm -f "$HERE/../.adb-device"
echo "done"
