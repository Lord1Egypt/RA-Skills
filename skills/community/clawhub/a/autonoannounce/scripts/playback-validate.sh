#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
CFG="$ROOT/config/tts-queue.json"
BACKEND="${1:-}"
DEVICE="${2:-}"

if [[ -f "$CFG" && ( -z "$BACKEND" || -z "$DEVICE" ) ]]; then
  mapfile -t vals < <(python3 - "$CFG" <<'PY'
import json,sys
try:
  c=json.load(open(sys.argv[1]))
  p=c.get('playback',{})
  print(p.get('backend','auto'))
  print(p.get('device',''))
except Exception:
  print('auto')
  print('')
PY
)
  [[ -z "$BACKEND" ]] && BACKEND="${vals[0]:-auto}"
  [[ -z "$DEVICE" ]] && DEVICE="${vals[1]:-}"
fi

if [[ -z "$BACKEND" || "$BACKEND" == "auto" ]]; then
  BACKEND="$($ROOT/skills/autonoannounce/scripts/backend-detect.sh || true)"
fi

ok=true
reason=""

case "$BACKEND" in
  mpv|ffplay|paplay|afplay)
    if ! command -v "$BACKEND" >/dev/null 2>&1; then
      ok=false; reason="backend_binary_missing"
    fi
    ;;
  powershell-soundplayer)
    if ! command -v powershell >/dev/null 2>&1 && ! command -v pwsh >/dev/null 2>&1; then
      ok=false; reason="powershell_missing"
    fi
    ;;
  none|"")
    ok=false; reason="no_backend_detected"
    ;;
  *)
    if ! command -v "$BACKEND" >/dev/null 2>&1; then
      ok=false; reason="custom_backend_missing"
    fi
    ;;
esac

if $ok && [[ "$BACKEND" == "mpv" && -n "$DEVICE" ]]; then
  if ! mpv --no-config --audio-device=help --idle=yes --force-window=no 2>&1 | awk '{print $1}' | tr -d ':' | grep -Fxq "$DEVICE"; then
    ok=false
    reason="configured_device_not_found"
  fi
fi

cat <<EOF
{"ok":$ok,"backend":"$BACKEND","device":"$DEVICE","reason":"$reason"}
EOF

$ok || exit 1
