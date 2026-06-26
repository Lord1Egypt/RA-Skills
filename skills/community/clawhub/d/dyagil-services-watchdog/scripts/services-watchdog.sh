#!/usr/bin/env bash
# services-watchdog.sh — שומר על שלוש השירותים של דייוויד בחיים
# רץ דרך cron כל 2 דקות. אם משהו נפל — מקים אותו ומדווח בטלגרם.
#
# שלושת השירותים:
#   1) sahi-diet      → ~/projects/sahi-diet/src/bot.js          (Runbot)
#   2) sahi-mind      → ~/projects/sahi-mind/src/index.js        (טלגרם משימות)
#   3) mission-control→ ~/projects/mission-control/server.js     (port 4321)
#
# רישום: ~/.openclaw/workspace/logs/watchdog.log

set -u

WORKSPACE="$HOME/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"
LOG="$LOG_DIR/watchdog.log"
STATE_DIR="$WORKSPACE/memory"
STATE_FILE="$STATE_DIR/watchdog-state.json"
mkdir -p "$LOG_DIR" "$STATE_DIR"

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
log() { echo "[$(ts)] $*" >> "$LOG"; }

# rotate log if it grows past 1 MB
if [ -f "$LOG" ] && [ "$(stat -c%s "$LOG" 2>/dev/null || echo 0)" -gt 1048576 ]; then
  mv "$LOG" "$LOG.1"
fi

notify_telegram() {
  local msg="$1"
  local token
  token=$(grep -E '^TELEGRAM_BOT_TOKEN=' "$WORKSPACE/projects/sahi-diet/.env" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'")
  [ -z "$token" ] && return 0
  local chat_id="6034574482"  # David
  curl -s --max-time 10 -X POST "https://api.telegram.org/bot${token}/sendMessage" \
    -d "chat_id=${chat_id}" \
    -d "text=${msg}" \
    -d "parse_mode=HTML" >/dev/null 2>&1 || true
}

# returns 0 if up, 1 if down
check_diet() {
  pgrep -f "node src/bot.js" >/dev/null 2>&1
}
restart_diet() {
  cd "$WORKSPACE/projects/sahi-diet" || return 1
  systemd-run --user --scope --quiet --unit="sahi-diet-$(date +%s%N)" \
    --setenv=PATH="$PATH" \
    --setenv=HOME="$HOME" \
    bash -c 'cd '"$WORKSPACE"'/projects/sahi-diet && set -a && [ -f .env ] && . ./.env; set +a; exec nohup node src/bot.js >> logs/bot.log 2>&1 < /dev/null' &
  disown 2>/dev/null || true
  sleep 3
  check_diet
}

check_mind() {
  pgrep -f "sahi-mind/src/index" >/dev/null 2>&1 || pgrep -f "node src/index.js" >/dev/null 2>&1
}
restart_mind() {
  cd "$WORKSPACE/projects/sahi-mind" || return 1
  systemd-run --user --scope --quiet --unit="sahi-mind-$(date +%s%N)" \
    --setenv=PATH="$PATH" \
    --setenv=HOME="$HOME" \
    bash -c 'cd '"$WORKSPACE"'/projects/sahi-mind && set -a && [ -f .env ] && . ./.env; set +a; exec nohup node src/index.js >> logs/mind.log 2>&1 < /dev/null' &
  disown 2>/dev/null || true
  sleep 3
  check_mind
}

check_mc() {
  # port + process — שניהם חייבים להיות
  ss -tln 2>/dev/null | grep -q ":4321 " && pgrep -f "mission-control/server.js" >/dev/null 2>&1 || \
    pgrep -f "node server.js" >/dev/null 2>&1 && ss -tln 2>/dev/null | grep -q ":4321 "
}
restart_mc() {
  cd "$WORKSPACE/projects/mission-control" || return 1
  # Run inside a transient scope. The child loads its own .env via a wrapper
  # shell (`set -a; . ./.env; set +a`) so we don't need to hard-code every key
  # the server expects (MC_USER, MC_PASS, OPENAI_API_KEY, GCAL_CLIENT_ID, ...).
  systemd-run --user --scope --quiet --unit="mission-control-$(date +%s%N)" \
    --setenv=PATH="$PATH" \
    --setenv=HOME="$HOME" \
    bash -c 'cd '"$WORKSPACE"'/projects/mission-control && set -a && [ -f .env ] && . ./.env; set +a; exec nohup node server.js >> logs/mc.log 2>&1 < /dev/null' &
  disown 2>/dev/null || true
  sleep 4
  check_mc
}

services=(diet mind mc)
labels_diet="Runbot (sahi-diet)"
labels_mind="Sahi-Mind"
labels_mc="Mission Control"

down_list=()
recovered_list=()
failed_list=()

for svc in "${services[@]}"; do
  if check_$svc; then
    continue
  fi
  label_var="labels_$svc"; label="${!label_var}"
  log "DOWN: $label — attempting restart"
  down_list+=("$label")
  if restart_$svc; then
    log "RECOVERED: $label"
    recovered_list+=("$label")
  else
    log "FAILED: $label could not be restarted"
    failed_list+=("$label")
  fi
done

# notify only when something changed
if [ ${#recovered_list[@]} -gt 0 ] || [ ${#failed_list[@]} -gt 0 ]; then
  msg="🐶 <b>Watchdog</b>%0A"
  if [ ${#recovered_list[@]} -gt 0 ]; then
    msg+="✅ הוקמו: $(IFS=, ; echo "${recovered_list[*]}")%0A"
  fi
  if [ ${#failed_list[@]} -gt 0 ]; then
    msg+="❌ נכשל: $(IFS=, ; echo "${failed_list[*]}")%0A"
  fi
  notify_telegram "$msg"
fi

# heartbeat state (for diagnostics)
{
  printf '{"last_run":"%s","up":{"diet":%s,"mind":%s,"mc":%s}}' \
    "$(ts)" \
    "$(check_diet && echo true || echo false)" \
    "$(check_mind && echo true || echo false)" \
    "$(check_mc && echo true || echo false)"
} > "$STATE_FILE"

exit 0
