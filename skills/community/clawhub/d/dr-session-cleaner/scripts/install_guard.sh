#!/usr/bin/env bash
set -euo pipefail

TARGET="${SESSION_GUARD_TARGET:-}"
INTERVAL_MIN=15
THRESHOLD="${SESSION_GUARD_THRESHOLD:-0.8}"
CHANNEL="${SESSION_GUARD_CHANNEL:-discord}"
GUARD_DIR="$HOME/.openclaw/session-guard"
STATE_PATH="${SESSION_GUARD_STATE:-$GUARD_DIR/state.json}"
LOG_PATH="${SESSION_GUARD_LOG:-$GUARD_DIR/guard.log}"
COOLDOWN="${SESSION_GUARD_COOLDOWN_MIN:-60}"
DRY_RUN=false

usage() {
  cat <<'EOF'
Usage: scripts/install_guard.sh --target user:123 [options]

Installs an alert-only session monitor. It never cleans, resets, or deletes sessions.
State and logs are restricted to ~/.openclaw/session-guard/.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="$2"; shift 2 ;;
    --interval) INTERVAL_MIN="$2"; shift 2 ;;
    --threshold) THRESHOLD="$2"; shift 2 ;;
    --channel) CHANNEL="$2"; shift 2 ;;
    --state) STATE_PATH="$2"; shift 2 ;;
    --log) LOG_PATH="$2"; shift 2 ;;
    --cooldown) COOLDOWN="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

shell_quote() { printf "'%s'" "${1//\'/\'\"\'\"\'}"; }

is_guard_file() {
  local candidate canonical guard_canonical
  candidate="$(realpath -m -- "$1")" || return 1
  guard_canonical="$(realpath -m -- "$GUARD_DIR")" || return 1
  [[ "$candidate" == "$guard_canonical/"* && "$candidate" != *$'\n'* ]]
}

[[ "$TARGET" =~ ^user:[0-9]{5,30}$ ]] || { echo "--target must be a Discord immutable DM target" >&2; exit 2; }
[[ "$CHANNEL" == "discord" ]] || { echo "--channel must be discord" >&2; exit 2; }
[[ "$INTERVAL_MIN" =~ ^[1-9][0-9]*$ && "$INTERVAL_MIN" -le 59 ]] || { echo "--interval must be 1-59 minutes" >&2; exit 2; }
[[ "$COOLDOWN" =~ ^[0-9]+$ ]] || { echo "--cooldown must be a non-negative integer" >&2; exit 2; }
[[ "$THRESHOLD" =~ ^(0\.[0-9]+|0?\.[0-9]+)$ ]] || { echo "--threshold must be a decimal greater than 0 and less than 1" >&2; exit 2; }
awk -v threshold="$THRESHOLD" 'BEGIN { exit !(threshold > 0 && threshold < 1) }' || { echo "--threshold must be greater than 0 and less than 1" >&2; exit 2; }
is_guard_file "$STATE_PATH" || { echo "--state must be inside ~/.openclaw/session-guard" >&2; exit 2; }
is_guard_file "$LOG_PATH" || { echo "--log must be inside ~/.openclaw/session-guard" >&2; exit 2; }

SKILL_DIR="$(cd -- "$(dirname "$0")/.." && pwd)"
SCRIPT_CMD="cd $(shell_quote "$SKILL_DIR") && python3 scripts/session_guard.py --target $(shell_quote "$TARGET") --threshold $(shell_quote "$THRESHOLD") --channel discord --state $(shell_quote "$STATE_PATH") --cooldown-min $(shell_quote "$COOLDOWN") >> $(shell_quote "$LOG_PATH") 2>&1"
CRON_EXPR="*/$INTERVAL_MIN * * * * $SCRIPT_CMD"
BEGIN_MARK="# BEGIN session-guard"
END_MARK="# END session-guard"

if $DRY_RUN; then
  printf '%s\n%s\n%s\n' "$BEGIN_MARK" "$CRON_EXPR" "$END_MARK"
  exit 0
fi

mkdir -p "$GUARD_DIR"
chmod 700 "$GUARD_DIR"
touch "$LOG_PATH"
chmod 600 "$LOG_PATH"

CURRENT_CRON="$(crontab -l 2>/dev/null | sed '/^# BEGIN session-guard$/,/^# END session-guard$/d' || true)"
{
  printf '%s\n' "$CURRENT_CRON" | grep -v '^$' || true
  printf '%s\n%s\n%s\n' "$BEGIN_MARK" "$CRON_EXPR" "$END_MARK"
} | crontab -

echo "Installed alert-only session guard (every ${INTERVAL_MIN}m)."
