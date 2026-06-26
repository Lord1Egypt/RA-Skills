#!/usr/bin/env bash
set -euo pipefail

# Heartbeat & keepalive scheduler control: start / stop / status
# Centralizes launchd (macOS) / crontab (Linux) + openclaw keepalive cron
# management.  Other scripts delegate here instead of duplicating logic.

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

LAUNCHD_LABEL="ai.clawgrid.heartbeat"
LAUNCHD_PLIST="$HOME/Library/LaunchAgents/${LAUNCHD_LABEL}.plist"
HEARTBEAT_SCRIPT="$SKILL_DIR/scripts/heartbeat.sh"
IS_MACOS=false
[ "$(uname -s)" = "Darwin" ] && IS_MACOS=true

QUIET=false
[ "${2:-}" = "--quiet" ] && QUIET=true

_log() { $QUIET || echo "$@"; }
_log_err() { $QUIET || echo "$@" >&2; }

_read_hb_min() {
  python3 -c "import json; print(json.load(open('$CONFIG')).get('heartbeat_interval_minutes', 1))" 2>/dev/null || echo 1
}

_read_notifier_cron() {
  python3 -c "import json; print(json.load(open('$CONFIG')).get('notifier_cron_expression', '0 9,21 * * *'))" 2>/dev/null || echo "0 9,21 * * *"
}

_find_openclaw_bin() {
  local oc
  oc=$(command -v openclaw 2>/dev/null || echo "")
  if [ -z "$oc" ]; then
    for _p in /opt/homebrew/bin/openclaw /usr/local/bin/openclaw "$HOME/.local/bin/openclaw"; do
      [ -x "$_p" ] && oc="$_p" && break
    done
  fi
  echo "$oc"
}

# Remove ALL openclaw cron jobs matching a given name.
# openclaw cron remove requires a jobId, not a name.
_oc_remove_by_name() {
  local name="$1"
  local oc_bin="$2"
  local jobs_file="$HOME/.openclaw/cron/jobs.json"
  [ ! -f "$jobs_file" ] && return 0
  local ids
  ids=$(python3 -c "
import json, sys
try:
    with open(sys.argv[1]) as f:
        data = json.load(f)
    jobs = data if isinstance(data, list) else []
    if isinstance(data, dict):
        jobs = data.get('jobs', [])
        if not jobs:
            jobs = [dict(jobId=k, **v) for k, v in data.items() if isinstance(v, dict)]
    for j in jobs:
        if j.get('name') == sys.argv[2]:
            jid = j.get('jobId', j.get('id', ''))
            if jid:
                print(jid)
except Exception:
    pass
" "$jobs_file" "$name" 2>/dev/null || true)
  [ -z "$ids" ] && return 0
  while IFS= read -r jid; do
    [ -n "$jid" ] && "$oc_bin" cron remove "$jid" 2>/dev/null || true
  done <<< "$ids"
}

_is_duration_format() {
  echo "$1" | python3 -c "
import sys, re
v = sys.stdin.read().strip()
print('yes' if re.match(r'^\d+[mhd]$', v) else 'no')
" 2>/dev/null || echo "no"
}

_keepalive_exists() {
  local jobs_file="$HOME/.openclaw/cron/jobs.json"
  [ ! -f "$jobs_file" ] && echo "false" && return
  python3 -c "
import json
try:
    with open('$jobs_file') as f:
        data = json.load(f)
    jobs = data if isinstance(data, list) else data.get('jobs', [])
    if not jobs and isinstance(data, dict):
        jobs = list(data.values())
    found = any(j.get('name') == 'clawgrid-keepalive' for j in jobs if isinstance(j, dict))
    print('true' if found else 'false')
except Exception:
    print('false')
" 2>/dev/null || echo "false"
}

# ── start ─────────────────────────────────────────────────────────
cmd_start() {
  if [ ! -f "$CONFIG" ]; then
    echo '{"action":"error","message":"Config not found — run setup first"}'
    exit 1
  fi
  if [ ! -f "$HEARTBEAT_SCRIPT" ]; then
    echo '{"action":"error","message":"heartbeat.sh not found"}'
    exit 1
  fi

  local HB_MIN HB_SEC scheduler
  HB_MIN=$(_read_hb_min)
  HB_SEC=$((HB_MIN * 60))

  # --- Heartbeat scheduler ---
  if $IS_MACOS; then
    scheduler="launchd"
    # Remove stale crontab entries (migrated to launchd)
    # NOTE: Do NOT use `crontab -` on macOS — it hangs in non-interactive shells.
    _old_cron=$(crontab -l 2>/dev/null || true)
    if [ -n "$_old_cron" ] && echo "$_old_cron" | grep -q 'clawgrid-heartbeat'; then
      echo "$_old_cron" | grep -v 'clawgrid-heartbeat' > /tmp/.clawgrid-crontab-clean 2>/dev/null
      crontab /tmp/.clawgrid-crontab-clean 2>/dev/null || true
      rm -f /tmp/.clawgrid-crontab-clean
    fi

    launchctl bootout "gui/$(id -u)/$LAUNCHD_LABEL" 2>/dev/null || \
      launchctl unload "$LAUNCHD_PLIST" 2>/dev/null || true

    mkdir -p "$HOME/Library/LaunchAgents"
    cat > "$LAUNCHD_PLIST" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LAUNCHD_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${HEARTBEAT_SCRIPT}</string>
    </array>
    <key>StartInterval</key>
    <integer>${HB_SEC}</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/clawgrid-heartbeat.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/clawgrid-heartbeat-err.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HOME</key>
        <string>${HOME}</string>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
PLIST
    launchctl bootstrap "gui/$(id -u)" "$LAUNCHD_PLIST" 2>/dev/null || \
      launchctl load "$LAUNCHD_PLIST" 2>/dev/null || true
  else
    scheduler="crontab"
    (crontab -l 2>/dev/null | grep -v 'clawgrid-heartbeat'; \
     echo "*/$HB_MIN * * * * /bin/bash $HEARTBEAT_SCRIPT >> /tmp/clawgrid-heartbeat.log 2>&1 # clawgrid-heartbeat") \
    | crontab -
  fi
  _log_err "[heartbeat-ctl] Heartbeat scheduler started ($scheduler, every ${HB_MIN} min)"

  # --- Keepalive cron via openclaw ---
  local OPENCLAW_BIN keepalive_schedule="none"
  OPENCLAW_BIN=$(_find_openclaw_bin)
  if [ -n "$OPENCLAW_BIN" ]; then
    # Clean up legacy names
    _oc_remove_by_name "clawgrid-earner" "$OPENCLAW_BIN"
    _oc_remove_by_name "clawgrid-notifier" "$OPENCLAW_BIN"
    _oc_remove_by_name "clawgrid-keepalive" "$OPENCLAW_BIN"

    local NOTIFIER_CRON
    NOTIFIER_CRON=$(_read_notifier_cron)
    keepalive_schedule="$NOTIFIER_CRON"

    local _NOTIFY_MSG="Run: bash $SKILL_DIR/scripts/notify.sh — relay output to owner with [ClawGrid.ai] prefix. If HEARTBEAT_OK, just say HEARTBEAT_OK."

    if [ "$(_is_duration_format "$NOTIFIER_CRON")" = "yes" ]; then
      "$OPENCLAW_BIN" cron add \
        --name "clawgrid-keepalive" \
        --every "$NOTIFIER_CRON" \
        --session isolated \
        --announce \
        --timeout-seconds 60 \
        --message "$_NOTIFY_MSG"
    else
      "$OPENCLAW_BIN" cron add \
        --name "clawgrid-keepalive" \
        --cron "$NOTIFIER_CRON" \
        --session isolated \
        --announce \
        --timeout-seconds 60 \
        --message "$_NOTIFY_MSG"
    fi
    _log_err "[heartbeat-ctl] Keepalive cron started (clawgrid-keepalive, $NOTIFIER_CRON)"
  else
    _log_err "[heartbeat-ctl] openclaw not found — keepalive cron skipped"
  fi

  echo "{\"action\":\"started\",\"heartbeat\":{\"scheduler\":\"$scheduler\",\"interval_minutes\":$HB_MIN},\"keepalive\":{\"schedule\":\"$keepalive_schedule\"}}"
}

# ── stop ──────────────────────────────────────────────────────────
cmd_stop() {
  local scheduler="unknown"

  # --- Stop heartbeat scheduler ---
  crontab -l 2>/dev/null | grep -v 'clawgrid-heartbeat' | crontab - 2>/dev/null || true
  if $IS_MACOS; then
    scheduler="launchd"
    # Try bootout (new API) first, fall back to unload (legacy API) for
    # environments where bootout lacks permission (e.g. OpenClaw exec).
    launchctl bootout "gui/$(id -u)/$LAUNCHD_LABEL" 2>/dev/null || \
      launchctl unload "$LAUNCHD_PLIST" 2>/dev/null || true
    rm -f "$LAUNCHD_PLIST"
  else
    scheduler="crontab"
  fi
  _log_err "[heartbeat-ctl] Heartbeat scheduler stopped ($scheduler)"

  # --- Stop keepalive cron ---
  local OPENCLAW_BIN
  OPENCLAW_BIN=$(_find_openclaw_bin)
  if [ -n "$OPENCLAW_BIN" ]; then
    _oc_remove_by_name "clawgrid-keepalive" "$OPENCLAW_BIN"
    _log_err "[heartbeat-ctl] Keepalive cron stopped (clawgrid-keepalive)"
  fi

  echo "{\"action\":\"stopped\",\"scheduler\":\"$scheduler\"}"
}

# ── status ────────────────────────────────────────────────────────
cmd_status() {
  local hb_running=false hb_scheduler="none" interval=0
  local ka_running=false

  if $IS_MACOS; then
    if launchctl list "$LAUNCHD_LABEL" &>/dev/null; then
      hb_running=true
      hb_scheduler="launchd"
    fi
  fi

  local HB_COUNT
  HB_COUNT=$(crontab -l 2>/dev/null | grep -c 'clawgrid-heartbeat' || true)
  if [ "$HB_COUNT" -gt 0 ]; then
    hb_running=true
    hb_scheduler="crontab"
  fi

  if [ -f "$CONFIG" ]; then
    interval=$(_read_hb_min)
  fi

  if [ "$(_keepalive_exists)" = "true" ]; then
    ka_running=true
  fi

  echo "{\"action\":\"status\",\"heartbeat\":{\"running\":$hb_running,\"scheduler\":\"$hb_scheduler\",\"interval_minutes\":$interval},\"keepalive\":{\"running\":$ka_running}}"
}

# ── dispatch ──────────────────────────────────────────────────────
case "${1:-help}" in
  start)  cmd_start ;;
  stop)   cmd_stop ;;
  status) cmd_status ;;
  help|--help|-h)
    cat << 'EOF'
heartbeat-ctl — Manage ClawGrid heartbeat scheduler & keepalive cron

Commands:
  start [--quiet]   Install heartbeat scheduler (launchd / crontab) + keepalive cron
  stop  [--quiet]   Uninstall heartbeat scheduler + keepalive cron
  status            Check if heartbeat scheduler and keepalive are running

Output: JSON on stdout, human-readable logs on stderr.
EOF
    ;;
  *) echo "{\"action\":\"error\",\"message\":\"Unknown command: $1. Use start|stop|status.\"}" ; exit 1 ;;
esac
