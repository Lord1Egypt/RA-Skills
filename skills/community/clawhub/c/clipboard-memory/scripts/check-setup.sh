#!/bin/sh
# clipmem skill — setup health check
#
# Verifies that clipmem is installed, its database is healthy, the watcher
# daemon has recent captures, and (optionally) the OpenClaw integration is
# wired up.
#
# Usage:
#   scripts/check-setup.sh
#   scripts/check-setup.sh --json
#   scripts/check-setup.sh --help
#
# Exit codes:
#   0  all required checks passed
#   1  watcher stale: clipmem is installed and healthy but nothing captured
#      recently and no background service is running
#   2  binary missing: clipmem is not on PATH
#   3  doctor/service status failed or status JSON could not be parsed
#   64 invalid command-line usage

set -u

JSON_MODE=0

usage() {
  cat <<'EOF'
Usage: scripts/check-setup.sh [--json] [--help]

Verify that clipmem is installed, its SQLite archive is healthy, and a
background watcher has captured something recently.

Options:
  --json   Emit structured JSON to stdout instead of human-oriented text
  --help   Show this help text and exit

Exit codes:
  0  all required checks passed
  1  watcher stale (no recent captures and no running background service)
  2  clipmem missing from PATH
  3  doctor/service status failed or status JSON could not be parsed
  64 invalid command-line usage
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --json)
      JSON_MODE=1
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      printf 'Error: unknown argument: %s\n\n' "$1" >&2
      usage >&2
      exit 64
      ;;
  esac
  shift
done

if [ "$JSON_MODE" -eq 1 ] || [ ! -t 1 ] || [ -n "${NO_COLOR:-}" ]; then
  red()    { printf '%s\n' "$*"; }
  yellow() { printf '%s\n' "$*"; }
  green()  { printf '%s\n' "$*"; }
else
  red()    { printf '\033[31m%s\033[0m\n' "$*"; }
  yellow() { printf '\033[33m%s\033[0m\n' "$*"; }
  green()  { printf '\033[32m%s\033[0m\n' "$*"; }
fi

CLIPMEM_PRESENT="0"
DOCTOR_OK=""
FTS5_AVAILABLE=""
HOMEBREW_RUNNING=""
HOMEBREW_LOADED=""
LAUNCHAGENT_RUNNING=""
LAUNCHAGENT_LOADED=""
STALE=""
RECENT_CAPTURE_WITHIN_LAST_HOUR=""
CONFLICT=""
OPENCLAW_DOCTOR_OK=""
VERSION=""
SUMMARY=""
DETAILS=""

emit_json_and_exit() {
  JSON_EXIT_CODE="$1"
  SUMMARY="$2"
  export JSON_EXIT_CODE SUMMARY
  export CLIPMEM_PRESENT DOCTOR_OK FTS5_AVAILABLE HOMEBREW_RUNNING HOMEBREW_LOADED
  export LAUNCHAGENT_RUNNING LAUNCHAGENT_LOADED STALE RECENT_CAPTURE_WITHIN_LAST_HOUR
  export CONFLICT OPENCLAW_DOCTOR_OK VERSION DETAILS

  python3 - <<'PYJSON'
import json
import os

def parse_boolish(value):
    if value in (None, '', '-1'):
        return None
    return value == '1'

data = {
    'ok': os.environ.get('JSON_EXIT_CODE') == '0',
    'exit_code': int(os.environ.get('JSON_EXIT_CODE', '0')),
    'summary': os.environ.get('SUMMARY', ''),
    'details': os.environ.get('DETAILS') or None,
    'clipmem_present': parse_boolish(os.environ.get('CLIPMEM_PRESENT')),
    'doctor_ok': parse_boolish(os.environ.get('DOCTOR_OK')),
    'fts5_available': parse_boolish(os.environ.get('FTS5_AVAILABLE')),
    'homebrew_running': parse_boolish(os.environ.get('HOMEBREW_RUNNING')),
    'homebrew_loaded': parse_boolish(os.environ.get('HOMEBREW_LOADED')),
    'launchagent_running': parse_boolish(os.environ.get('LAUNCHAGENT_RUNNING')),
    'launchagent_loaded': parse_boolish(os.environ.get('LAUNCHAGENT_LOADED')),
    'stale': parse_boolish(os.environ.get('STALE')),
    'recent_capture_within_last_hour': parse_boolish(os.environ.get('RECENT_CAPTURE_WITHIN_LAST_HOUR')),
    'conflict': parse_boolish(os.environ.get('CONFLICT')),
    'openclaw_doctor_ok': parse_boolish(os.environ.get('OPENCLAW_DOCTOR_OK')),
    'version': os.environ.get('VERSION') or None,
}
print(json.dumps(data, indent=2, sort_keys=True))
PYJSON
  exit "$JSON_EXIT_CODE"
}

fail() {
  if [ "$JSON_MODE" -eq 1 ]; then
    emit_json_and_exit "$2" "$1"
  fi
  red "FAIL: $1"
  exit "$2"
}

if ! command -v clipmem >/dev/null 2>&1; then
  CLIPMEM_PRESENT="0"
  fail "clipmem is not on PATH. Install via 'brew install tristanmanchester/tap/clipmem' or 'cargo install clipmem'." 2
fi

CLIPMEM_PRESENT="1"
VERSION=$(clipmem --version 2>/dev/null || true)
if [ "$JSON_MODE" -eq 0 ]; then
  green "OK: ${VERSION:-clipmem present}"
fi

DOCTOR_OUT=$(clipmem doctor --json 2>&1)
DOCTOR_STATUS=$?
if [ "$DOCTOR_STATUS" -ne 0 ]; then
  DOCTOR_OK="0"
  DETAILS="$DOCTOR_OUT"
  if [ "$JSON_MODE" -eq 1 ]; then
    emit_json_and_exit 3 "clipmem doctor failed"
  fi
  red "FAIL: clipmem doctor exited ${DOCTOR_STATUS}"
  printf '%s\n' "$DOCTOR_OUT" >&2
  exit 3
fi

DOCTOR_OK="1"
if [ "$JSON_MODE" -eq 0 ]; then
  green "OK: clipmem doctor exited cleanly"
fi

if printf '%s' "$DOCTOR_OUT" | grep -Eq '"fts5_create_virtual_table_ok"[[:space:]]*:[[:space:]]*true'; then
  FTS5_AVAILABLE="1"
  if [ "$JSON_MODE" -eq 0 ]; then
    green "OK: FTS5 available"
  fi
else
  FTS5_AVAILABLE="0"
  if [ "$JSON_MODE" -eq 0 ]; then
    yellow "WARN: FTS5 not available; --mode fts will fail. Use --mode literal."
  fi
fi

STATUS_OUT=$(clipmem service status --json 2>&1)
STATUS_CODE=$?
if [ "$STATUS_CODE" -ne 0 ]; then
  DETAILS="$STATUS_OUT"
  if [ "$JSON_MODE" -eq 1 ]; then
    emit_json_and_exit 3 "clipmem service status failed"
  fi
  red "FAIL: clipmem service status exited ${STATUS_CODE}"
  printf '%s\n' "$STATUS_OUT" >&2
  exit 3
fi

STATUS_VARS=$(
  printf '%s' "$STATUS_OUT" | python3 -c "import json,sys; data=json.load(sys.stdin); print('homebrew_running=%d' % (1 if data['homebrew']['running'] else 0)); print('homebrew_loaded=%d' % (1 if data['homebrew']['loaded'] else 0)); print('launchagent_running=%d' % (1 if data['launchagent']['running'] else 0)); print('launchagent_loaded=%d' % (1 if data['launchagent']['loaded'] else 0)); print('stale=%d' % (1 if data['stale'] else 0)); fresh=data.get('recent_capture_within_last_hour'); print('recent_capture_within_last_hour=%s' % ('-1' if fresh is None else ('1' if fresh else '0'))); print('conflict=%d' % (1 if data.get('conflict') else 0))"
) || {
  DETAILS="$STATUS_OUT"
  if [ "$JSON_MODE" -eq 1 ]; then
    emit_json_and_exit 3 "could not parse clipmem service status JSON"
  fi
  red "FAIL: could not parse clipmem service status JSON"
  printf '%s\n' "$STATUS_OUT" >&2
  exit 3
}

eval "$STATUS_VARS"
HOMEBREW_RUNNING="$homebrew_running"
HOMEBREW_LOADED="$homebrew_loaded"
LAUNCHAGENT_RUNNING="$launchagent_running"
LAUNCHAGENT_LOADED="$launchagent_loaded"
STALE="$stale"
RECENT_CAPTURE_WITHIN_LAST_HOUR="$recent_capture_within_last_hour"
CONFLICT="$conflict"

if [ "$JSON_MODE" -eq 0 ]; then
  if [ "${homebrew_running}" -eq 1 ]; then
    green "OK: Homebrew service homebrew.mxcl.clipmem is running"
  elif [ "${homebrew_loaded}" -eq 1 ]; then
    yellow "WARN: Homebrew service homebrew.mxcl.clipmem is loaded but not running"
  fi

  if [ "${launchagent_running}" -eq 1 ]; then
    green "OK: LaunchAgent io.openclaw.clipmem.watch is running"
  elif [ "${launchagent_loaded}" -eq 1 ]; then
    yellow "WARN: LaunchAgent io.openclaw.clipmem.watch is loaded but not running"
  fi

  if [ "${homebrew_running}" -eq 0 ] && [ "${homebrew_loaded}" -eq 0 ] \
     && [ "${launchagent_running}" -eq 0 ] && [ "${launchagent_loaded}" -eq 0 ]; then
    yellow "WARN: no clipmem background service is loaded"
    yellow "      Run: clipmem setup"
    yellow "      Or:  brew services start clipmem"
  fi

  if [ "${recent_capture_within_last_hour}" -eq 1 ]; then
    green "OK: clipboard capture observed in the last hour"
  elif [ "${recent_capture_within_last_hour}" -eq 0 ]; then
    yellow "WARN: no clipboard captures in the last hour"
  fi

  if [ "${conflict}" -eq 1 ]; then
    yellow "WARN: both Homebrew and direct LaunchAgent services are installed"
    yellow "      Remove one with: brew services stop clipmem"
    yellow "      Or:              clipmem service uninstall"
  fi
fi

if clipmem agents openclaw --help >/dev/null 2>&1; then
  if clipmem agents openclaw doctor >/dev/null 2>&1; then
    OPENCLAW_DOCTOR_OK="1"
    if [ "$JSON_MODE" -eq 0 ]; then
      green "OK: clipmem agents openclaw doctor passed"
    fi
  else
    OPENCLAW_DOCTOR_OK="0"
    if [ "$JSON_MODE" -eq 0 ]; then
      yellow "WARN: clipmem agents openclaw doctor reported issues; run it directly for details"
    fi
  fi
fi

if [ "${STALE}" -eq 1 ]; then
  SUMMARY="STALE: no recent captures and no background watcher is running. Run 'clipmem setup' or 'brew services start clipmem' and retry."
  if [ "$JSON_MODE" -eq 1 ]; then
    emit_json_and_exit 1 "$SUMMARY"
  fi
  red "$SUMMARY"
  exit 1
fi

SUMMARY="All checks passed."
if [ "$JSON_MODE" -eq 1 ]; then
  emit_json_and_exit 0 "$SUMMARY"
fi
green "$SUMMARY"
exit 0
