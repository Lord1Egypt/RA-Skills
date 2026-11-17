#!/usr/bin/env bash
# Install an APK and verify it actually runs:
# version, launch, focus, pid, logcat, screenshot.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/adb.sh
. "$HERE/lib/adb.sh"
[ -f "$HERE/../config.sh" ] && . "$HERE/../config.sh"

APK="${1:-}"
[ -n "$APK" ] && [ -f "$APK" ] || { echo "usage: $0 path/to/app.apk" >&2; exit 2; }

OUT_DIR="${OUT_DIR:-$HERE/../out}"
mkdir -p "$OUT_DIR"

DEV="$(cat "$HERE/../.adb-device" 2>/dev/null || true)"
[ -n "$DEV" ] || { echo "no device; run adb-connect.sh first" >&2; exit 1; }

STAGE="$APK"
if [ -n "${ADB_REMOTE_HOST:-}" ]; then
  STAGE="/tmp/$(basename "$APK")"
  scp -q -o BatchMode=yes "$APK" "$ADB_REMOTE_HOST:$STAGE"
  echo "staged APK on $ADB_REMOTE_HOST:$STAGE"
fi

PKG="${PACKAGE_ID:-}"
ACT="${LAUNCH_ACTIVITY:-}"

echo "== install =="
adb_call -s "$DEV" install -r "$STAGE" | sed 's/^/  /'

if [ -z "$PKG" ] || [ -z "$ACT" ]; then
  if command -v aapt2 >/dev/null 2>&1; then
    BADGING="$(aapt2 dump badging "$APK" 2>/dev/null || true)"
    [ -z "$PKG" ] && PKG="$(printf '%s\n' "$BADGING" | sed -n "s/^package: name='\([^']*\)'.*/\1/p" | head -1)"
    [ -z "$ACT" ] && ACT="$(printf '%s\n' "$BADGING" | sed -n "s/.*launchable-activity: name='\([^']*\)'.*/\1/p" | head -1)"
  fi
fi
[ -n "$PKG" ] || { echo "set PACKAGE_ID in config.sh (could not read it from the APK)" >&2; exit 1; }
echo "  package: $PKG"

echo "== installed metadata =="
adb_call -s "$DEV" shell dumpsys package "$PKG" \
  | grep -E 'versionName|versionCode|targetSdk|firstInstallTime|lastUpdateTime' | head -6 | sed 's/^/  /'

if [ -n "$ACT" ]; then
  echo "== launch =="
  adb_call -s "$DEV" shell input keyevent 224 >/dev/null 2>&1 || true   # wake display
  adb_call -s "$DEV" shell svc power stayon true >/dev/null 2>&1 || true
  adb_call -s "$DEV" shell input keyevent 3 >/dev/null 2>&1 || true      # HOME
  sleep 2
  adb_call -s "$DEV" shell am start -n "$PKG/$ACT" | sed 's/^/  /'
  sleep 5

  echo "== focus (must be our package) =="
  FOCUS="$(adb_text -s "$DEV" shell dumpsys window | grep -i mCurrentFocus | head -2 || true)"
  printf '%s\n' "$FOCUS" | sed 's/^/  /'
  printf '%s\n' "$FOCUS" | grep -q "$PKG" || echo "  WARNING: $PKG does not hold focus (lockscreen? crash?)"

  echo "== process =="
  PID="$(adb_text -s "$DEV" shell pidof "$PKG" || true)"
  echo "  pid: ${PID:-<none>}"
fi

echo "== crashes in logcat =="
adb_call -s "$DEV" logcat -d -t 400 | grep -iE "AndroidRuntime|FATAL EXCEPTION|$PKG" | tail -10 | sed 's/^/  /' || echo "  (clean)"

echo "== screenshot =="
SHOT="$OUT_DIR/screen.png"
capture_to_file "$SHOT" "/tmp/adb-verify-screen.png" -s "$DEV" exec-out screencap -p
if [ -f "$SHOT" ]; then
  SZ=$(wc -c < "$SHOT")
  echo "  saved $SHOT ($SZ bytes)"
  if [ "$SZ" -lt 30000 ]; then
    echo "  WARNING: suspiciously small — some OEM lockscreens hand back a cached"
    echo "           black framebuffer. Wake the device, dismiss, retry."
  fi
fi
echo "DONE"
