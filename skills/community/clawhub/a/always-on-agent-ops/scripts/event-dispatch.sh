#!/usr/bin/env bash
# Named-event dispatcher: maps an event to the heavy cron job(s) that handle it.
# Called by preflights when (and only when) they counted work > 0.
#
# The event name is matched against a CLOSED list hardcoded in the `case` below.
# Nothing from the caller is ever concatenated into a command: an unknown event
# exits 2. The count argument is used as display text only.
#
# Guards, in order:
#   1. mkdir lock  -> two preflights firing the same event cannot double-run it.
#      Released on RETURN, EXIT, INT and TERM, plus a TTL for locks orphaned by kill -9.
#      The lock is an EMPTY directory, so it is removed with `rmdir`, never a recursive delete:
#      rmdir refuses a symlink, a file, or a non-empty dir - it cannot delete anything else.
#   2. job exists  -> an id that is not installed is an Error line, never a silent no-op.
#   3. runningAtMs -> the job itself is already mid-run; do not stack a second turn.
#
# EDIT THE MAPPING BELOW to the job ids ACTUALLY installed (`openclaw cron list`).
# Jobs created via `openclaw cron add` get an auto-generated UUID, not the id you
# wrote in your template. Pointing at template ids = silent no-op forever.
# Deliberately NOT `set -e`: every failure must leave a status line behind.
set -uo pipefail

event="${1:-}"
count="${2:-}"
DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$DIR/cron-message.sh"

LOCK_TTL_MIN="${LOCK_TTL_MIN:-15}"   # older than this = orphaned by a kill; reclaim it
# Fed to `find -mmin`: junk there = a TTL that never fires (or always does). Fall back to 15.
case "$LOCK_TTL_MIN" in ''|*[!0-9]*|0) LOCK_TTL_MIN=15 ;; esac
LOCK_DIR=""

release_lock() {
  if [ -n "${LOCK_DIR:-}" ]; then rmdir "$LOCK_DIR" 2>/dev/null || true; fi
  LOCK_DIR=""
  return 0
}
trap release_lock EXIT INT TERM

usage() {
  cat <<'USAGE'
Usage: event-dispatch.sh <event> [count]

Events (closed list - anything else exits 2):
  work_ready      Actionable item entered the outbound queue
  review_needed   Existing work item needs a second pass
  source_changed  Upstream source of truth moved
  hourly_safety   Lightweight consistency check
USAGE
}

run_job() {
  local id="$1"
  local lock_dir="${TMPDIR:-/tmp}/openclaw-event-${id}.lock"
  local details="event=$event"
  [ -n "$count" ] && details="$details count=$count"

  # A lock older than the TTL survived a kill (daily restart, sleep, kill -9).
  # Without this, one killed run blocks the event forever while the channel
  # keeps reporting a healthy-looking "Blocked".
  if [ -d "$lock_dir" ] && [ ! -L "$lock_dir" ] \
     && [ -n "$(find "$lock_dir" -maxdepth 0 -type d -mmin +"$LOCK_TTL_MIN" 2>/dev/null)" ]; then
    rmdir "$lock_dir" 2>/dev/null || true
  fi

  if ! mkdir "$lock_dir" 2>/dev/null; then
    cron_message "dispatch" "Blocked" "A dispatch is already in flight." "$id" \
      "Wait for the current run; if it never clears: rmdir $lock_dir" "$details"
    return 0
  fi
  LOCK_DIR="$lock_dir"
  trap release_lock RETURN

  # Probe once, classify into exactly three outcomes: unknown | running | idle.
  # Do NOT assume `cron get` exits non-zero on an unknown id: some releases exit 0
  # and print prose. Anything that is not JSON carrying this job's id is `unknown`,
  # so an unparsable answer can never fall through to "idle" and fire a bogus run.
  local state="" probe="unknown"
  state="$(openclaw cron get "$id" 2>/dev/null)" || state=""
  probe="$(printf '%s' "$state" | node -e '
    let s = "";
    process.stdin.on("data", (d) => (s += d));
    process.stdin.on("end", () => {
      let j;
      try { j = JSON.parse(s); } catch { return process.stdout.write("unknown"); }
      if (!j || typeof j !== "object") return process.stdout.write("unknown");
      const job = j.job && typeof j.job === "object" ? j.job : j;
      if (!job.id) return process.stdout.write("unknown");
      const st = job.state && typeof job.state === "object" ? job.state : {};
      process.stdout.write(st.runningAtMs ? "running" : "idle");
    });
  ' 2>/dev/null || echo "unknown")"

  if [ "$probe" = "unknown" ]; then
    cron_message "dispatch" "Error" "Unknown job id - the mapping points at an id that is not installed." "$id" \
      "Run: openclaw cron list, then fix the mapping in this script." "$details"
    return 0
  fi

  if [ "$probe" = "running" ]; then
    cron_message "dispatch" "Blocked" "Job already running." "$id" \
      "Wait for the active run." "$details"
    return 0
  fi

  cron_message "dispatch" "Started" "Job requested." "$id" \
    "OpenClaw runs it now." "$details"
  if ! openclaw cron run "$id"; then
    cron_message "dispatch" "Error" "Job start failed." "$id" \
      "Check: openclaw cron get $id" "$details"
  fi
  return 0
}

case "$event" in
  work_ready)     run_job "cr-10-worker" ;;
  review_needed)  run_job "cr-30-reviewer" ;;
  source_changed) run_job "cr-30-reviewer"; run_job "cr-40-drift-watch" ;;  # one event, several jobs
  hourly_safety)  run_job "cr-40-drift-watch" ;;
  ""|-h|--help|help) usage ;;
  *) echo "Unknown event: $event" >&2; usage >&2; exit 2 ;;
esac
