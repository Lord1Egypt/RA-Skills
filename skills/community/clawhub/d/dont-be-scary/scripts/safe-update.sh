#!/bin/bash
# dont-be-scary — Safe OpenClaw update with snapshot + rollback + Telegram report
#
# Launch detached so the script survives gateway restart (which kills the agent):
#   nohup "$OPENCLAW_WORKSPACE_DIR/skills/dont-be-scary/scripts/safe-update.sh" </dev/null >/dev/null 2>&1 & disown
#
# Flow:
#   1. Snapshot npm package + .app bundle to /tmp/openclaw-rollback/<ts>/
#   2. Telegram: "starting"
#   3. openclaw update (restarts gateway itself)
#   4. Health check up to 180s (gateway responds on :GATEWAY_PORT)
#   5. OK   → Telegram success, prune snapshots (keep last 2)
#   6. FAIL → restore snapshot, restart gateway via launchctl, Telegram with log path
#
# Env overrides (all optional):
#   OPENCLAW_TG_CHAT_ID   — Telegram chat_id to notify (else auto-detected from openclaw.json delivery)
#   OPENCLAW_TG_BOT       — Bot account name in openclaw.json (default: "default")
#   OPENCLAW_CONFIG       — Path to openclaw.json (default: ~/.openclaw/openclaw.json)
#   OPENCLAW_NPM_DIR      — Path to npm install (default: /opt/homebrew/lib/node_modules/openclaw)
#   OPENCLAW_APP_DIR      — Path to .app bundle (default: /Applications/OpenClaw.app)
#   OPENCLAW_GATEWAY_PORT — Gateway port for health check (default: 18789)
#   OPENCLAW_PLIST        — LaunchAgent plist (default: ~/Library/LaunchAgents/ai.openclaw.gateway.plist)
#   OPENCLAW_BIN          — openclaw binary path (default: /opt/homebrew/bin/openclaw)
#   OPENCLAW_SNAP_ROOT    — Snapshot root dir (default: /tmp/openclaw-rollback)

set -u

CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
NPM_DIR="${OPENCLAW_NPM_DIR:-/opt/homebrew/lib/node_modules/openclaw}"
APP_DIR="${OPENCLAW_APP_DIR:-/Applications/OpenClaw.app}"
PLIST="${OPENCLAW_PLIST:-$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist}"
OC_BIN="${OPENCLAW_BIN:-/opt/homebrew/bin/openclaw}"
GATEWAY_PORT="${OPENCLAW_GATEWAY_PORT:-18789}"
SNAP_ROOT="${OPENCLAW_SNAP_ROOT:-/tmp/openclaw-rollback}"
TG_BOT="${OPENCLAW_TG_BOT:-default}"

TS=$(date +%Y%m%d-%H%M%S)
LOG=/tmp/openclaw-update-${TS}.log
SNAP_DIR="${SNAP_ROOT}/${TS}"

exec >>"$LOG" 2>&1

echo "===== $(date) — UPDATE START (PID $$) ====="
echo "Config: $CONFIG"
echo "NPM dir: $NPM_DIR"
echo "App dir: $APP_DIR"

# ---- Pull bot token from openclaw.json ----
BOT_TOKEN=$(python3 -c "
import json, sys
try:
    cfg = json.load(open('$CONFIG'))
    print(cfg['channels']['telegram']['accounts']['$TG_BOT']['botToken'])
except Exception as e:
    sys.stderr.write(f'config error: {e}\n')
    sys.exit(1)
" 2>/dev/null)

# ---- Pull chat_id (env override > openclaw.json delivery target > fail) ----
CHAT_ID="${OPENCLAW_TG_CHAT_ID:-}"
if [ -z "$CHAT_ID" ]; then
    CHAT_ID=$(python3 -c "
import json, sys
try:
    cfg = json.load(open('$CONFIG'))
    # Try common locations: delivery.targets[], channels.telegram.accounts.default.defaultChatId, etc.
    targets = cfg.get('delivery', {}).get('targets', [])
    for t in targets:
        if t.get('channel') == 'telegram' and t.get('to'):
            print(t['to']); sys.exit(0)
    # Fallback: defaultChatId on the bot account
    chat = cfg.get('channels', {}).get('telegram', {}).get('accounts', {}).get('$TG_BOT', {}).get('defaultChatId')
    if chat:
        print(chat); sys.exit(0)
    sys.exit(1)
except Exception:
    sys.exit(1)
" 2>/dev/null)
fi

tg() {
    local msg="$1"
    if [ -n "$BOT_TOKEN" ] && [ -n "$CHAT_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
            -d "chat_id=${CHAT_ID}" \
            --data-urlencode "text=${msg}" > /dev/null
    else
        echo "[tg] No bot token or chat_id — skipping notification: $msg"
    fi
}

health_check() {
    for i in $(seq 1 60); do
        if curl -sf -m 2 "http://localhost:${GATEWAY_PORT}/" -o /dev/null 2>&1; then
            return 0
        fi
        sleep 3
    done
    return 1
}

restart_gateway() {
    if [ -f "$PLIST" ]; then
        launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null
        sleep 3
        launchctl bootstrap "gui/$(id -u)" "$PLIST" 2>/dev/null
    else
        echo "WARN: plist not found at $PLIST, cannot restart via launchctl"
    fi
}

# ---- Preflight ----
if [ ! -x "$OC_BIN" ]; then
    echo "FATAL: openclaw binary not found at $OC_BIN"
    tg "❌ dont-be-scary: openclaw binary not found at $OC_BIN. Set OPENCLAW_BIN."
    exit 1
fi
if [ ! -d "$NPM_DIR" ]; then
    echo "FATAL: npm dir not found at $NPM_DIR"
    tg "❌ dont-be-scary: npm dir not found at $NPM_DIR. Set OPENCLAW_NPM_DIR."
    exit 1
fi

OLD_VER=$("$OC_BIN" --version 2>/dev/null | head -1)
echo "Pre-update version: $OLD_VER"

# ---- 1. Snapshot ----
echo "Creating snapshot at $SNAP_DIR..."
mkdir -p "$SNAP_DIR"
cp -R "$NPM_DIR" "$SNAP_DIR/openclaw-npm" || { echo "FAIL snapshot npm"; tg "❌ Update aborted: failed to snapshot npm package."; exit 1; }
if [ -d "$APP_DIR" ]; then
    cp -R "$APP_DIR" "$SNAP_DIR/OpenClaw.app" || { echo "FAIL snapshot app"; tg "❌ Update aborted: failed to snapshot OpenClaw.app."; exit 1; }
fi
SNAP_SIZE=$(du -sh "$SNAP_DIR" | cut -f1)
echo "Snapshot done ($SNAP_SIZE)"

tg "🔄 Updating OpenClaw from ${OLD_VER}. Snapshot saved (${SNAP_SIZE}). Pinging back in 1-2 min."

# ---- 2. Update ----
echo "Running openclaw update..."
"$OC_BIN" update --json > "/tmp/openclaw-update-${TS}.update.json" 2>&1
UPDATE_RC=$?
echo "openclaw update exit code: $UPDATE_RC"
cat "/tmp/openclaw-update-${TS}.update.json"

# ---- 3. Health check ----
echo "Waiting for gateway..."
sleep 8
if health_check; then
    NEW_VER=$("$OC_BIN" --version 2>/dev/null | head -1)
    echo "Health OK. New version: $NEW_VER"
    if [ "$OLD_VER" = "$NEW_VER" ]; then
        tg "✅ OpenClaw operational (no version change). Version: ${NEW_VER}. Nothing to update."
    else
        tg "✅ OpenClaw updated. ${OLD_VER} → ${NEW_VER}. Gateway operational."
    fi
    # Prune snapshots: keep last 2
    cd "$SNAP_ROOT" && ls -1t | tail -n +3 | xargs -I {} rm -rf "{}" 2>/dev/null
    echo "===== $(date) — UPDATE OK ====="
    exit 0
fi

# ---- 4. ROLLBACK ----
echo "Health check FAILED. Rolling back..."
launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null
sleep 3

rm -rf "$NPM_DIR"
mv "$SNAP_DIR/openclaw-npm" "$NPM_DIR"
if [ -d "$SNAP_DIR/OpenClaw.app" ]; then
    rm -rf "$APP_DIR"
    mv "$SNAP_DIR/OpenClaw.app" "$APP_DIR"
fi
rmdir "$SNAP_DIR" 2>/dev/null

restart_gateway
sleep 5

if health_check; then
    tg "⚠️ Update FAILED but rollback OK. Restored version: ${OLD_VER}. Log: ${LOG}"
    echo "===== $(date) — ROLLBACK OK ====="
    exit 1
else
    tg "🚨 CRITICAL: update failed AND rollback failed. Gateway down. Manual intervention needed. Log: ${LOG}. See references/rescue-prompt.md for Claude Code recovery prompt."
    echo "===== $(date) — ROLLBACK FAILED ====="
    exit 2
fi
