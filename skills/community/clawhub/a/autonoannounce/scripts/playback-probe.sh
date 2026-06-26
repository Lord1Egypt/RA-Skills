#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
BACKEND="${1:-auto}"

if [[ "$BACKEND" == "auto" || -z "$BACKEND" ]]; then
  BACKEND="$($ROOT/skills/autonoannounce/scripts/backend-detect.sh || echo none)"
fi

list_mpv_devices() {
  if ! command -v mpv >/dev/null 2>&1; then return 0; fi
  mpv --no-config --audio-device=help --idle=yes --force-window=no 2>&1 \
    | awk '/^  [^ ]/ {print $1}' \
    | sed 's/:$//' \
    | sed 's/^/device:/' || true
}

case "$BACKEND" in
  mpv)
    echo "backend:mpv"
    list_mpv_devices
    ;;
  ffplay)
    echo "backend:ffplay"
    ;;
  paplay)
    echo "backend:paplay"
    ;;
  afplay)
    echo "backend:afplay"
    ;;
  powershell-soundplayer)
    echo "backend:powershell-soundplayer"
    ;;
  none|"")
    echo "backend:none"
    ;;
  *)
    echo "backend:$BACKEND"
    ;;
esac
