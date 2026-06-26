#!/usr/bin/env bash
set -euo pipefail

REMOTE_SKILL_URL="${REMOTE_SKILL_URL:-https://www.shitskills.net/skill.md}"
PROBE_MODE="${PROBE_MODE:-warn}"
PROBE_ATTEMPTS="${PROBE_ATTEMPTS:-3}"
PROBE_SLEEP_SECONDS="${PROBE_SLEEP_SECONDS:-2}"
CONNECT_TIMEOUT="${CONNECT_TIMEOUT:-10}"
MAX_TIME="${MAX_TIME:-30}"

last_error=""

for attempt in $(seq 1 "$PROBE_ATTEMPTS"); do
  echo "[task4-probe] attempt $attempt/$PROBE_ATTEMPTS"

  if curl --fail --silent --show-error --location \
    --connect-timeout "$CONNECT_TIMEOUT" \
    --max-time "$MAX_TIME" \
    --head "$REMOTE_SKILL_URL" >/dev/null 2>"/tmp/task4-probe-head.err"; then
    if remote_body="$(curl --fail --silent --show-error --location \
      --connect-timeout "$CONNECT_TIMEOUT" \
      --max-time "$MAX_TIME" \
      "$REMOTE_SKILL_URL" 2>"/tmp/task4-probe-body.err")"; then
      if printf '%s' "$remote_body" | rg -qi '(^---)|(^# )|(name:)|(description:)|(skill)'; then
        echo "[task4-probe] remote live skill healthy"
        exit 0
      fi
      last_error="content probe did not match skill-like shape"
    else
      last_error="$(cat /tmp/task4-probe-body.err 2>/dev/null || true)"
    fi
  else
    last_error="$(cat /tmp/task4-probe-head.err 2>/dev/null || true)"
  fi

  if [[ "$attempt" -lt "$PROBE_ATTEMPTS" ]]; then
    sleep "$PROBE_SLEEP_SECONDS"
  fi
done

echo "[task4-probe] remote live skill probe failed after $PROBE_ATTEMPTS attempts" >&2
if [[ -n "$last_error" ]]; then
  echo "[task4-probe] last error: $last_error" >&2
fi
echo "[task4-probe] Task 4 native flow should be treated as unavailable until this probe passes" >&2

if [[ "$PROBE_MODE" == "strict" ]]; then
  exit 1
fi

exit 0
