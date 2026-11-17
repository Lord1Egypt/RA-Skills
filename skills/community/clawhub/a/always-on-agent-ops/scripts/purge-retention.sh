#!/usr/bin/env bash
# Executes the log retention declared at the top of SKILL.md. Weekly (cr-22).
# This is the ONLY file in this skill that deletes anything the user owns.
# A retention window nobody enforces is not a retention window, it is a sentence.
#
# Scope, deliberately narrow:
#   deletes  -> regular *.log files under $OPENCLAW_HOME/logs older than N days
#   reports  -> workspace size, so unbounded growth cannot happen silently
#   never    -> a recursive delete, never a directory, never anything outside $OPENCLAW_HOME/logs
# DEFAULT IS DRY RUN: it lists what would go and deletes nothing. Deletion happens ONLY
# when PURGE_DRY_RUN is exactly "0" - set by a human after reading a dry-run list.
# Unset, empty, "false", "no", anything else = dry run. A delete switch that fails open
# on a typo is not a switch.
set -uo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$DIR/cron-message.sh"

# `-` not `:-`: an explicitly EMPTY OPENCLAW_HOME must be refused below, not silently
# replaced by the default. Only a genuinely unset variable gets the default.
HOME_DIR="${OPENCLAW_HOME-$HOME/.openclaw}"
LOG_DIR="$HOME_DIR/logs"
LOG_RETENTION_DAYS="${LOG_RETENTION_DAYS:-30}"

# Guard 1 — blocklist: paths that are never a target, whatever else is true.
case "$HOME_DIR" in
  ""|"/"|"$HOME") cron_message "cr-22-purge" "Error" "OPENCLAW_HOME resolves to an unsafe path." \
      "retention" "Set OPENCLAW_HOME to the agent home (default ~/.openclaw)." "home=${HOME_DIR:-unset}"
    exit 0 ;;
esac

# Guard 2 — POSITIVE marker. A blocklist of three paths only refuses the three paths it
# knows; everything else (a typo, a stale env var, an unrelated directory that happens to
# hold a logs/) sails through and gets deleted. Demand PROOF this is an agent home instead.
if [ ! -f "$HOME_DIR/openclaw.json" ] && [ ! -d "$HOME_DIR/agents" ]; then
  cron_message "cr-22-purge" "Error" "Not an OpenClaw home (no openclaw.json, no agents/) - refusing to delete." \
    "retention" "Point OPENCLAW_HOME at the agent home (default ~/.openclaw)." "home=$HOME_DIR"
  exit 0
fi

# Guard 3 — the window must be a plain positive integer: it is fed to `find -mtime`, and a
# junk value there is a purge with an undefined window.
case "$LOG_RETENTION_DAYS" in
  ''|*[!0-9]*|0) cron_message "cr-22-purge" "Error" "LOG_RETENTION_DAYS must be a positive integer." \
      "retention" "Set LOG_RETENTION_DAYS to a whole number of days (default 30)." "value=$LOG_RETENTION_DAYS"
    exit 0 ;;
esac

if [ ! -d "$LOG_DIR" ]; then
  cron_message "cr-22-purge" "Nothing to do" "No log directory - nothing to retain." \
    "retention" "None." "dir=$LOG_DIR"
  exit 0
fi

# -type f only: a symlink or a directory is never a candidate.
# NUL-delimited read, not `mapfile`: macOS ships bash 3.2, where mapfile does not
# exist - and this skill's whole point is a host that never gets a second chance.
stale=()
while IFS= read -r -d '' f; do
  stale+=("$f")
# -mtime +N matches "older than N+1 full 24h periods", so +30 would keep a 30-day-old file
# and make the declared 30-day window a 31-day one. -1 puts the executed window back on the
# declared number: at exactly 30 days, the file goes.
done < <(find "$LOG_DIR" -type f -name '*.log' -mtime +"$((LOG_RETENTION_DAYS - 1))" -print0 2>/dev/null)
ws_size="$(du -sh "$HOME_DIR/workspace" 2>/dev/null | cut -f1 | tr -d ' ')"
kept="$(find "$LOG_DIR" -type f -name '*.log' 2>/dev/null | wc -l | tr -d ' ')"

if [ "${#stale[@]}" -eq 0 ]; then
  cron_message "cr-22-purge" "Nothing to do" "No log older than ${LOG_RETENTION_DAYS} days." \
    "retention" "None." "kept=$kept workspace=${ws_size:-unknown}"
  exit 0
fi

if [ "${PURGE_DRY_RUN-1}" != "0" ]; then
  printf '%s\n' "${stale[@]}" >&2
  cron_message "cr-22-purge" "Human action required" "Dry run: ${#stale[@]} file(s) would be deleted, none were." \
    "retention" "Review the list (stderr), then arm with PURGE_DRY_RUN=0." "mode=dry_run days=$LOG_RETENTION_DAYS"
  exit 0
fi

deleted=0
for f in "${stale[@]}"; do
  rm -f -- "$f" && deleted=$((deleted + 1))
done

cron_message "cr-22-purge" "Done" "Deleted ${deleted}/${#stale[@]} log file(s) past retention." \
  "retention" "None." "days=$LOG_RETENTION_DAYS workspace=${ws_size:-unknown}"
exit 0
