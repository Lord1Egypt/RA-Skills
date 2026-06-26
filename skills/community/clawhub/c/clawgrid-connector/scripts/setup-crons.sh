#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"
LAUNCHD_LABEL="ai.clawgrid.heartbeat"
LAUNCHD_PLIST="$HOME/Library/LaunchAgents/${LAUNCHD_LABEL}.plist"
IS_MACOS=false
[ "$(uname -s)" = "Darwin" ] && IS_MACOS=true

if [ ! -f "$CONFIG" ]; then
  echo "Config not found at $CONFIG — run setup first" >&2
  exit 1
fi

# --- Pre-flight: ensure exec approval is configured for automated sessions ---
CHECK_EXEC="$SKILL_DIR/scripts/check-exec-approval.sh"
if [ -x "$CHECK_EXEC" ]; then
  _EA_STATUS=$(bash "$CHECK_EXEC" 2>/dev/null | head -1 || echo "UNKNOWN")
  if [ "$_EA_STATUS" != "OK" ]; then
    SETUP_EXEC="$SKILL_DIR/scripts/setup-exec-approval.sh"
    if [ -x "$SETUP_EXEC" ]; then
      echo "[setup-crons] Configuring exec approval for automated sessions..."
      bash "$SETUP_EXEC" --quiet || true
    fi
  fi
fi

HB_MIN=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('heartbeat_interval_minutes', 1))" 2>/dev/null || echo 1)
HB_SEC=$((HB_MIN * 60))
NOTIFIER_CRON=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('notifier_cron_expression', '0 9,21 * * *'))" 2>/dev/null || echo "0 9,21 * * *")

# Remove ALL openclaw cron jobs matching a given name.
# openclaw cron remove requires a jobId, not a name.  We read the
# job store (jobs.json) to find matching names, then remove by jobId.
_oc_remove_by_name() {
  local name="$1"
  local oc_bin="${OPENCLAW_BIN:-openclaw}"
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

echo "=== ClawGrid Cron Setup ==="
if $IS_MACOS; then
  echo "  Platform:            macOS (using launchd for heartbeat)"
else
  echo "  Platform:            Linux (using crontab for heartbeat)"
fi
echo "  Heartbeat interval:  every ${HB_MIN} min (smart wake included)"
echo "  Notifier schedule:   ${NOTIFIER_CRON} (openclaw cron)"
echo "  Note: Task polling is now handled by heartbeat smart wake"
echo ""

# --- 1. Heartbeat scheduler (OS-specific, zero LLM cost) ---
HEARTBEAT_SCRIPT="$SKILL_DIR/scripts/heartbeat.sh"
if [ ! -f "$HEARTBEAT_SCRIPT" ]; then
  echo "[ERROR] heartbeat.sh not found at $HEARTBEAT_SCRIPT" >&2
  exit 1
fi

if $IS_MACOS; then
  # macOS: use launchd (avoids crontab Full Disk Access requirement)
  # NOTE: Do NOT use `crontab -` on macOS — it hangs in non-interactive shells.
  # Instead, use crontab <file> to remove old entries if any exist.
  _old_cron=$(crontab -l 2>/dev/null || true)
  if [ -n "$_old_cron" ] && echo "$_old_cron" | grep -q 'clawgrid-heartbeat'; then
    echo "$_old_cron" | grep -v 'clawgrid-heartbeat' > /tmp/.clawgrid-crontab-clean 2>/dev/null
    crontab /tmp/.clawgrid-crontab-clean 2>/dev/null || true
    rm -f /tmp/.clawgrid-crontab-clean
  fi
  launchctl bootout "gui/$(id -u)/$LAUNCHD_LABEL" 2>/dev/null || true

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
  echo "[OK] launchd: heartbeat every ${HB_MIN} min (${LAUNCHD_LABEL})"
else
  # Linux: use system crontab
  (crontab -l 2>/dev/null | grep -v 'clawgrid-heartbeat'; \
   echo "*/$HB_MIN * * * * /bin/bash $HEARTBEAT_SCRIPT >> /tmp/clawgrid-heartbeat.log 2>&1 # clawgrid-heartbeat") \
  | crontab -
  echo "[OK] System crontab: heartbeat every ${HB_MIN} min"
fi

# --- 2. Clean up legacy crons (replaced by heartbeat smart wake / renamed) ---
OPENCLAW_BIN=$(command -v openclaw 2>/dev/null || echo "")
if [ -z "$OPENCLAW_BIN" ]; then
  for _p in /opt/homebrew/bin/openclaw /usr/local/bin/openclaw "$HOME/.local/bin/openclaw"; do
    [ -x "$_p" ] && OPENCLAW_BIN="$_p" && break
  done
fi
if [ -z "$OPENCLAW_BIN" ]; then
  echo "[WARN] openclaw not found in PATH — skipping OpenClaw cron setup."
  echo "       Heartbeat is configured. Set up keepalive cron manually:"
  echo "       openclaw cron add --name clawgrid-keepalive ..."
  echo ""
  echo "=== Heartbeat configured, cron setup skipped ==="
  exit 0
fi

_oc_remove_by_name "clawgrid-earner"
echo "[OK] Removed legacy earner cron (now handled by heartbeat smart wake)"

# --- 3. OpenClaw cron: keepalive (remove old names + duplicates, add exactly one) ---
_oc_remove_by_name "clawgrid-notifier"
_oc_remove_by_name "clawgrid-keepalive"

IS_DURATION=$(echo "$NOTIFIER_CRON" | python3 -c "
import sys, re
v = sys.stdin.read().strip()
print('yes' if re.match(r'^\d+[mhd]$', v) else 'no')
" 2>/dev/null || echo "no")

_NOTIFY_MSG="Run: bash $SKILL_DIR/scripts/notify.sh — relay output to owner with [ClawGrid.ai] prefix. If HEARTBEAT_OK, just say HEARTBEAT_OK."

if [ "$IS_DURATION" = "yes" ]; then
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
echo "[OK] OpenClaw cron: clawgrid-keepalive ($NOTIFIER_CRON)"

echo ""
echo "=== All cron jobs configured ==="
if $IS_MACOS; then
  echo "Verify with: launchctl list | grep clawgrid  &&  openclaw cron list"
else
  echo "Verify with: crontab -l | grep clawgrid  &&  openclaw cron list"
fi
