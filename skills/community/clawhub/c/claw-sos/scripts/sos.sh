#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# SOS - OpenClaw Recovery Menu v6
# ═══════════════════════════════════════════════════════════════
# WHAT: Emergency recovery tool for when your OpenClaw bot
#       stops responding on Telegram/Discord/etc.
# WHERE: /root/sos.sh (shortcut: just type "sos")
# WHEN: Use when the bot doesn't reply on Telegram
# HOW: SSH into the machine, run "sos", pick an option
#
# AUTOFIX: Run "sos auto" to skip the menu — it will diagnose
#          and fix everything automatically, escalating step by
#          step until the bot is back.
#
# LOG: Every action is logged to ~/.openclaw/backups/sos.log
#      The bot can check this to see what happened while it was down.
#
# OPTIONS EXPLAINED:
#   1) Check status    — Just look, don't touch. Shows if gateway is
#                        running, RAM, disk, version. Safe to run anytime.
#   2) Restart         — Graceful restart. Like turning off and on.
#                        Fixes 90% of issues. Wait 30s after.
#   3) Force kill      — When restart hangs. Kills the process hard
#                        then starts fresh. Wait 30s after.
#   4) Rollback        — Go back to the previous version if an update
#                        broke things. Restores config backup too.
#   5) View logs       — See what happened before the crash.
#                        Look for ERROR or FATAL lines.
#   6) Full diagnostic — Everything at once: Telegram, RAM, disk,
#                        sessions, process memory. Good for reporting.
#   7) Backup config   — Save current config before doing something risky.
#                        Always do this before manual changes.
#   8) Self-test       — Verify this script itself works. Run it after
#                        updates to make sure SOS is still functional.
#   9) Nuclear         — Last resort. Kills EVERYTHING and starts over.
#                        Requires typing YES in caps. Use only if
#                        options 2 and 3 both failed.
#  10) Autofix         — Hands-free repair. Runs diagnostics, then
#                        tries fixes in order: doctor → restart →
#                        force kill → nuclear. Stops as soon as
#                        gateway is healthy. Also: sos auto
#  11) Network check   — Test DNS, internet, and Telegram API
#                        connectivity. Run this if autofix fails —
#                        the problem might be the network, not OpenClaw.
#  12) Telegram test   — Send a real test message through Telegram
#                        to verify end-to-end delivery works.
# ═══════════════════════════════════════════════════════════════

export TERM="${TERM:-xterm}"
set -uo pipefail

SOS_VERSION="6.1.1"
OS_TYPE="linux"
[[ "$(uname -s)" == "Darwin" ]] && OS_TYPE="macos"

BOLD='\033[1m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
DIM='\033[2m'
NC='\033[0m'

# === Auto-detect paths ===
OC_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
OC_CONFIG="$OC_HOME/openclaw.json"
BACKUP_DIR="$OC_HOME/backups"
LOG_FILE="$BACKUP_DIR/sos.log"
mkdir -p "$BACKUP_DIR"

# === Cross-platform helpers ===
get_avail_ram_mb() {
  if [[ "$OS_TYPE" == "macos" ]]; then
    local pagesize=$(sysctl -n hw.pagesize)
    local free_pages=$(vm_stat | awk '/Pages free:/{gsub(/\./,"",$3); print $3}')
    local inactive_pages=$(vm_stat | awk '/Pages inactive:/{gsub(/\./,"",$3); print $3}')
    echo $(( (free_pages + inactive_pages) * pagesize / 1024 / 1024 ))
  else
    free -m | awk '/Mem:/{print $7}'
  fi
}

get_avail_disk_mb() {
  if [[ "$OS_TYPE" == "macos" ]]; then
    df -m / | awk 'NR==2{print $4}'
  else
    df / --output=avail -BM | tail -1 | tr -d ' M'
  fi
}

show_ram() {
  if [[ "$OS_TYPE" == "macos" ]]; then
    local total_bytes=$(sysctl -n hw.memsize)
    local total_gb=$(echo "scale=1; $total_bytes / 1073741824" | bc 2>/dev/null || echo "unknown")
    echo "Total RAM: ${total_gb}GB"
    vm_stat | head -8
  else
    free -h | head -2
  fi
}

show_ram_full() {
  if [[ "$OS_TYPE" == "macos" ]]; then
    local total_bytes=$(sysctl -n hw.memsize)
    local total_gb=$(echo "scale=1; $total_bytes / 1073741824" | bc 2>/dev/null || echo "unknown")
    echo "Total RAM: ${total_gb}GB"
    vm_stat
  else
    free -h
  fi
}

drop_caches() {
  if [[ "$OS_TYPE" == "macos" ]]; then
    if command -v purge &>/dev/null; then
      purge 2>/dev/null || true
    else
      echo -e "${DIM}purge not available (needs Xcode CLI tools)${NC}"
    fi
  else
    sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true
  fi
}

clean_disk() {
  if [[ "$OS_TYPE" == "macos" ]]; then
    npm cache clean --force &>/dev/null || true
    find /tmp -type f -mtime +1 -delete 2>/dev/null || true
  else
    journalctl --vacuum-size=50M &>/dev/null || true
    npm cache clean --force &>/dev/null || true
    find /tmp -type f -mtime +1 -delete 2>/dev/null || true
  fi
}

check_dns() {
  if command -v host &>/dev/null; then
    timeout 5 host google.com &>/dev/null
  elif command -v dig &>/dev/null; then
    timeout 5 dig google.com +short &>/dev/null
  elif command -v nslookup &>/dev/null; then
    timeout 5 nslookup google.com &>/dev/null
  else
    # Fallback: try a DNS-dependent curl
    timeout 5 curl -sf http://google.com -o /dev/null 2>/dev/null
  fi
}

show_logs() {
  local lines="${1:-50}"
  if [[ "$OS_TYPE" == "macos" ]]; then
    log show --predicate 'process == "openclaw-gateway"' --last 5m --style syslog 2>/dev/null | tail -"$lines" \
      || tail -"$lines" "$OC_HOME/logs/gateway.log" 2>/dev/null \
      || echo "No logs found anywhere."
  else
    journalctl --user -u openclaw-gateway -n "$lines" --no-pager 2>/dev/null \
      || journalctl -u openclaw-gateway -n "$lines" --no-pager 2>/dev/null \
      || tail -"$lines" "$OC_HOME/logs/gateway.log" 2>/dev/null \
      || echo "No logs found anywhere."
  fi
}

daemon_reload() {
  if [[ "$OS_TYPE" == "macos" ]]; then
    : # no-op on macOS
  else
    systemctl --user daemon-reload 2>/dev/null || systemctl daemon-reload 2>/dev/null || true
  fi
}

has_whiptail() {
  command -v whiptail &>/dev/null || command -v dialog &>/dev/null
}

get_whiptail_cmd() {
  if command -v whiptail &>/dev/null; then
    echo "whiptail"
  elif command -v dialog &>/dev/null; then
    echo "dialog"
  else
    echo ""
  fi
}

# === Logging ===
log() {
  local level="$1"
  shift
  local msg="$*"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S UTC')
  echo "[$timestamp] [$level] $msg" >> "$LOG_FILE"
}

log_start() {
  log "INFO" "=== SOS session started by $(whoami) from $(who am i 2>/dev/null | awk '{print $NF}' || echo 'local') ==="
  log "INFO" "OpenClaw version: $(get_version), Service: $(detect_service)"
}

# === Auto-detect service type ===
detect_service() {
  if [[ "$OS_TYPE" == "macos" ]]; then
    if launchctl list 2>/dev/null | grep -q openclaw; then
      echo "launchctl"
    else
      echo "none"
    fi
  else
    if systemctl --user is-active openclaw-gateway &>/dev/null; then
      echo "user"
    elif systemctl is-active openclaw-gateway &>/dev/null; then
      echo "system"
    else
      echo "none"
    fi
  fi
}

svc_cmd() {
  local action=$1
  local svc_type=$(detect_service)
  if [[ "$action" == "start" && "$svc_type" == "none" ]]; then
    if [[ "$OS_TYPE" == "macos" ]]; then
      # Check for plist even if not currently loaded
      if ls ~/Library/LaunchAgents/*openclaw* &>/dev/null 2>&1 || ls /Library/LaunchDaemons/*openclaw* &>/dev/null 2>&1; then
        svc_type="launchctl"
      fi
    else
      if systemctl --user cat openclaw-gateway &>/dev/null; then
        svc_type="user"
      elif systemctl cat openclaw-gateway &>/dev/null; then
        svc_type="system"
      fi
    fi
  fi
  log "ACTION" "svc_cmd $action (detected: $svc_type)"
  case $svc_type in
    user)   systemctl --user $action openclaw-gateway ;;
    system) systemctl $action openclaw-gateway ;;
    launchctl)
      local plist=$(ls ~/Library/LaunchAgents/*openclaw* /Library/LaunchDaemons/*openclaw* 2>/dev/null | head -1)
      local svc_label=$(basename "$plist" .plist 2>/dev/null || echo "com.openclaw.gateway")
      case $action in
        start)
          launchctl load "$plist" 2>/dev/null || true
          launchctl kickstart -k "gui/$(id -u)/$svc_label" 2>/dev/null || true
          echo "Started via launchctl."
          ;;
        stop)
          launchctl kill SIGTERM "gui/$(id -u)/$svc_label" 2>/dev/null \
            || launchctl unload "$plist" 2>/dev/null || true
          echo "Stopped via launchctl."
          ;;
        restart)
          launchctl kill SIGTERM "gui/$(id -u)/$svc_label" 2>/dev/null || true
          sleep 2
          launchctl unload "$plist" 2>/dev/null || true
          launchctl load "$plist" 2>/dev/null || true
          echo "Restarted via launchctl."
          ;;
        status)
          launchctl list "$svc_label" 2>/dev/null || echo "Not loaded."
          ;;
      esac
      ;;
    none)
      echo -e "${RED}No service found. Trying manual...${NC}"
      log "WARN" "No service found, falling back to manual"
      if [[ "$action" == "start" || "$action" == "restart" ]]; then
        local OC_BIN=$(which openclaw 2>/dev/null || echo "/usr/lib/node_modules/openclaw/dist/index.js")
        nohup node "$OC_BIN" gateway --port 18789 &>/dev/null &
        echo "Started manually (PID $!)"
        log "INFO" "Started manually PID $!"
      elif [[ "$action" == "stop" ]]; then
        kill $(pgrep -f openclaw-gateway) 2>/dev/null && echo "Stopped." || echo "Nothing to stop."
      elif [[ "$action" == "status" ]]; then
        ps aux | grep openclaw-gateway | grep -v grep || echo "Not running."
      fi
      ;;
  esac
}

get_version() {
  openclaw --version 2>/dev/null | grep -oP '\d{4}\.\d+\.\d+' || echo "unknown"
}

# === Health check: returns 0 if gateway is alive ===
is_healthy() {
  if ! pgrep -f openclaw-gateway &>/dev/null; then
    return 1
  fi
  local status_out=$(timeout 15 openclaw status 2>&1 || true)
  if echo "$status_out" | grep -q "Telegram.*ON.*OK"; then
    return 0
  fi
  if echo "$status_out" | grep -q "active (running)"; then
    return 0
  fi
  return 1
}

# === Network check ===
check_network() {
  echo -e "${YELLOW}=== Network Diagnostics ===${NC}"
  echo -e "${DIM}Testing connectivity layer by layer...${NC}\n"
  local all_ok=true

  # DNS
  echo -ne "  DNS resolution...        "
  if check_dns; then
    echo -e "${GREEN}✓ OK${NC}"
  else
    echo -e "${RED}✗ FAILED — DNS is broken${NC}"
    echo -e "    ${DIM}Try: cat /etc/resolv.conf${NC}"
    echo -e "    ${DIM}Fix: echo 'nameserver 1.1.1.1' > /etc/resolv.conf${NC}"
    all_ok=false
  fi

  # Internet (HTTPS)
  echo -ne "  Internet (HTTPS)...      "
  if timeout 5 curl -sf https://www.google.com -o /dev/null 2>/dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
  else
    echo -e "${RED}✗ FAILED — no internet or HTTPS blocked${NC}"
    echo -e "    ${DIM}Try: ping 1.1.1.1${NC}"
    all_ok=false
  fi

  # Telegram API
  echo -ne "  Telegram API...          "
  if timeout 5 curl -sf https://api.telegram.org -o /dev/null 2>/dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
  else
    echo -e "${RED}✗ FAILED — can't reach Telegram${NC}"
    echo -e "    ${DIM}Telegram might be blocked or rate-limited${NC}"
    all_ok=false
  fi

  # Anthropic API
  echo -ne "  Anthropic API...         "
  if timeout 5 curl -sf https://api.anthropic.com -o /dev/null 2>/dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
  else
    echo -e "${YELLOW}⚠ Unreachable (may need auth — not necessarily broken)${NC}"
  fi

  # OpenAI API
  echo -ne "  OpenAI API...            "
  if timeout 5 curl -sf https://api.openai.com -o /dev/null 2>/dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
  else
    echo -e "${YELLOW}⚠ Unreachable (may need auth)${NC}"
  fi

  # Latency
  echo -ne "  Latency (Telegram)...    "
  local latency=$(timeout 5 curl -sf -o /dev/null -w "%{time_total}" https://api.telegram.org 2>/dev/null || echo "timeout")
  if [[ "$latency" != "timeout" ]]; then
    local ms=$(echo "$latency * 1000" | bc 2>/dev/null || echo "$latency")
    echo -e "${CYAN}${ms}ms${NC}"
  else
    echo -e "${RED}timeout${NC}"
  fi

  echo ""
  if $all_ok; then
    echo -e "${GREEN}Network is fine — the problem is not connectivity.${NC}"
    log "INFO" "Network check: all OK"
  else
    echo -e "${RED}Network issues found! Fix those before restarting.${NC}"
    log "WARN" "Network check: issues found"
  fi
}

# === Telegram test message ===
telegram_test() {
  echo -e "${YELLOW}=== Telegram Test Message ===${NC}"
  echo -e "${DIM}Sends a real message through the bot to verify delivery.${NC}\n"

  # Extract bot token from config
  local token=$(python3 -c "
import json
try:
    c = json.load(open('$OC_CONFIG'))
    t = c.get('channels',{}).get('telegram',{}).get('token','')
    print(t)
except: pass
" 2>/dev/null)

  if [[ -z "$token" ]]; then
    echo -e "${RED}✗ Can't find Telegram token in config${NC}"
    log "WARN" "Telegram test: no token found"
    return 1
  fi
  echo -e "  Token: ${CYAN}${token:0:8}...${token: -4}${NC}"

  # Get chat ID — try to find from recent updates or config
  echo -ne "  Enter chat ID to test (or press Enter to auto-detect): "
  read -r chat_id

  if [[ -z "$chat_id" ]]; then
    # Try to get from recent updates
    chat_id=$(timeout 5 curl -sf "https://api.telegram.org/bot${token}/getUpdates?limit=1" 2>/dev/null \
      | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['result'][-1]['message']['chat']['id'])" 2>/dev/null || echo "")
    if [[ -z "$chat_id" ]]; then
      echo -e "${RED}✗ Can't auto-detect chat ID. Please enter manually.${NC}"
      echo -ne "  Chat ID: "
      read -r chat_id
    else
      echo -e "  Auto-detected: ${CYAN}${chat_id}${NC}"
    fi
  fi

  if [[ -z "$chat_id" ]]; then
    echo -e "${RED}✗ No chat ID — can't send test${NC}"
    return 1
  fi

  local timestamp=$(date '+%Y-%m-%d %H:%M:%S UTC')
  local msg="🔧 SOS Test Message | $timestamp | This confirms Telegram delivery is working."

  echo -e "\n  Sending test message..."
  local result=$(timeout 10 curl -sf -X POST "https://api.telegram.org/bot${token}/sendMessage" \
    -d "chat_id=${chat_id}" -d "text=${msg}" 2>/dev/null)

  if echo "$result" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok']" 2>/dev/null; then
    echo -e "  ${GREEN}✓ Message sent successfully!${NC}"
    echo -e "  ${DIM}Check Telegram — you should see the test message.${NC}"
    log "INFO" "Telegram test: sent to $chat_id"
  else
    echo -e "  ${RED}✗ Send failed!${NC}"
    echo -e "  ${DIM}Response: ${result:-no response}${NC}"
    log "WARN" "Telegram test: FAILED to $chat_id"
  fi
}

# === Autofix ===
autofix() {
  echo -e "${RED}╔══════════════════════════════════════════════════════╗${NC}"
  echo -e "${RED}║         🔧  AUTOFIX MODE — Hands-free repair        ║${NC}"
  echo -e "${RED}╚══════════════════════════════════════════════════════╝${NC}"
  echo ""
  log "AUTOFIX" "=== Autofix started ==="

  # ----------------------------------------------------------
  # Step 0: Diagnose
  # ----------------------------------------------------------
  echo -e "${YELLOW}Step 0/7: Diagnosing...${NC}"
  local proc_running=false
  local ram_ok=true
  local disk_ok=true
  local avail_ram=$(get_avail_ram_mb)
  local avail_disk=$(get_avail_disk_mb)

  if pgrep -f openclaw-gateway &>/dev/null; then
    proc_running=true
    echo -e "  Process: ${GREEN}running${NC} (PID $(pgrep -f openclaw-gateway | head -1))"
    local rss=$(ps aux | grep openclaw-gateway | grep -v grep | awk '{print int($6/1024)}' | head -1)
    echo -e "  Memory usage: ${CYAN}${rss}MB${NC}"
  else
    echo -e "  Process: ${RED}NOT running${NC}"
  fi

  if [[ $avail_ram -lt 150 ]]; then
    ram_ok=false
    echo -e "  RAM: ${RED}CRITICAL — only ${avail_ram}MB free${NC}"
    log "AUTOFIX" "RAM critical: ${avail_ram}MB"
  else
    echo -e "  RAM: ${GREEN}${avail_ram}MB available${NC}"
  fi

  if [[ $avail_disk -lt 200 ]]; then
    disk_ok=false
    echo -e "  Disk: ${RED}CRITICAL — only ${avail_disk}MB free${NC}"
    log "AUTOFIX" "Disk critical: ${avail_disk}MB"
  else
    echo -e "  Disk: ${GREEN}${avail_disk}MB free${NC}"
  fi
  echo ""

  # ----------------------------------------------------------
  # Step 0.5: Fix resource issues
  # ----------------------------------------------------------
  if ! $ram_ok; then
    echo -e "${YELLOW}Step 0.5: Clearing RAM...${NC}"
    drop_caches
    if [[ "$OS_TYPE" != "macos" ]]; then
      journalctl --vacuum-time=1d &>/dev/null || true
    fi
    log "AUTOFIX" "Cleared caches to free RAM"
    echo -e "  RAM now: ${CYAN}$(get_avail_ram_mb)MB${NC}"
    echo ""
  fi

  if ! $disk_ok; then
    echo -e "${YELLOW}Step 0.5: Clearing disk space...${NC}"
    clean_disk
    log "AUTOFIX" "Cleared disk space"
    echo -e "  Disk now: ${CYAN}$(get_avail_disk_mb)MB${NC}"
    echo ""
  fi

  # ----------------------------------------------------------
  # Step 1: Network check
  # ----------------------------------------------------------
  echo -e "${YELLOW}Step 1/7: Checking network...${NC}"
  local net_ok=true
  if ! timeout 5 curl -sf https://api.telegram.org -o /dev/null 2>/dev/null; then
    echo -e "  ${RED}✗ Can't reach Telegram API!${NC}"
    log "AUTOFIX" "Network: Telegram API unreachable"
    if ! check_dns; then
      echo -e "  ${RED}✗ DNS is broken too${NC}"
      echo -e "  ${YELLOW}Attempting DNS fix...${NC}"
      cp /etc/resolv.conf /etc/resolv.conf.bak 2>/dev/null || true
      echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf
      log "AUTOFIX" "Fixed DNS (set 1.1.1.1 + 8.8.8.8)"
      sleep 2
      if timeout 5 curl -sf https://api.telegram.org -o /dev/null 2>/dev/null; then
        echo -e "  ${GREEN}✓ DNS fix worked!${NC}"
      else
        echo -e "  ${RED}✗ Still can't reach internet — network problem, not OpenClaw${NC}"
        echo -e "\n${RED}⚠ Fix the network first. No point restarting without internet.${NC}"
        log "AUTOFIX" "FAILED — network issue, not OpenClaw"
        return 1
      fi
    else
      echo -e "  ${YELLOW}DNS works but Telegram blocked — might be temporary${NC}"
      net_ok=false
    fi
  else
    echo -e "  ${GREEN}✓ Network OK (Telegram API reachable)${NC}"
  fi
  echo ""

  # ----------------------------------------------------------
  # Step 2: Doctor fix
  # ----------------------------------------------------------
  echo -e "${YELLOW}Step 2/7: Running openclaw doctor --fix...${NC}"
  echo -e "  ${DIM}Fixes config issues, permissions, and known problems.${NC}"
  log "AUTOFIX" "Running openclaw doctor --fix"
  local doctor_out=$(timeout 30 openclaw doctor --fix --non-interactive 2>&1 || true)
  if echo "$doctor_out" | grep -qi "fix\|repair\|corrected\|applied"; then
    echo -e "  ${GREEN}✓ Doctor found and fixed issues${NC}"
    log "AUTOFIX" "Doctor applied fixes"
  elif echo "$doctor_out" | grep -qi "error\|fail"; then
    echo -e "  ${YELLOW}⚠ Doctor had errors (continuing anyway)${NC}"
    log "AUTOFIX" "Doctor errors: $(echo "$doctor_out" | tail -3)"
  else
    echo -e "  ${GREEN}✓ Doctor: nothing to fix${NC}"
    log "AUTOFIX" "Doctor: clean"
  fi
  echo ""

  # ----------------------------------------------------------
  # Step 3: Quick health check
  # ----------------------------------------------------------
  echo -e "${YELLOW}Step 3/7: Quick health check...${NC}"
  if is_healthy; then
    echo -e "  ${GREEN}✓ Gateway is healthy! Nothing to fix.${NC}"
    log "AUTOFIX" "Already healthy — no action needed"
    echo -e "\n${GREEN}Bot is running fine. Try messaging on Telegram.${NC}"
    return 0
  fi
  echo -e "  ${RED}✗ Not healthy. Starting repair sequence...${NC}"
  echo ""

  # ----------------------------------------------------------
  # Step 4: Graceful restart
  # ----------------------------------------------------------
  echo -e "${YELLOW}Step 4/7: Trying graceful restart...${NC}"
  echo -e "  ${DIM}This fixes ~90% of problems.${NC}"
  log "AUTOFIX" "Attempting graceful restart"
  svc_cmd restart 2>/dev/null || true
  echo -e "  Waiting 15 seconds..."
  sleep 15
  if is_healthy; then
    echo -e "  ${GREEN}✓ Fixed! Gateway is back.${NC}"
    log "AUTOFIX" "FIXED by graceful restart"
    echo -e "\n${GREEN}✅ Bot is back! Wait 15 more seconds then message on Telegram.${NC}"
    return 0
  fi
  echo -e "  ${RED}✗ Still down. Escalating...${NC}"
  echo ""

  # ----------------------------------------------------------
  # Step 5: Force kill + restart
  # ----------------------------------------------------------
  echo -e "${YELLOW}Step 5/7: Force killing and restarting...${NC}"
  echo -e "  ${DIM}Killing hung processes and starting fresh.${NC}"
  log "AUTOFIX" "Attempting force kill + restart"
  kill -9 $(pgrep -f openclaw-gateway) 2>/dev/null || true
  sleep 3
  svc_cmd start 2>/dev/null || true
  echo -e "  Waiting 15 seconds..."
  sleep 15
  if is_healthy; then
    echo -e "  ${GREEN}✓ Fixed! Gateway is back.${NC}"
    log "AUTOFIX" "FIXED by force kill + restart"
    echo -e "\n${GREEN}✅ Bot is back! Wait 15 more seconds then message on Telegram.${NC}"
    return 0
  fi
  echo -e "  ${RED}✗ Still down. Escalating...${NC}"
  echo ""

  # ----------------------------------------------------------
  # Step 6: Nuclear
  # ----------------------------------------------------------
  echo -e "${YELLOW}Step 6/7: Nuclear restart (killing all openclaw processes)...${NC}"
  echo -e "  ${DIM}Full process cleanup and systemd reload.${NC}"
  log "AUTOFIX" "Attempting nuclear restart"
  kill -9 $(pgrep -f openclaw) 2>/dev/null || true
  sleep 3
  daemon_reload
  svc_cmd start 2>/dev/null || true
  echo -e "  Waiting 20 seconds..."
  sleep 20
  if is_healthy; then
    echo -e "  ${GREEN}✓ Fixed! Gateway is back.${NC}"
    log "AUTOFIX" "FIXED by nuclear restart"
    echo -e "\n${GREEN}✅ Bot is back! Wait 15 more seconds then message on Telegram.${NC}"
    return 0
  fi
  echo -e "  ${RED}✗ Still down after nuclear.${NC}"
  echo ""

  # ----------------------------------------------------------
  # Step 7: Give up
  # ----------------------------------------------------------
  echo -e "${RED}Step 7/7: Autofix exhausted all options.${NC}"
  echo ""
  echo -e "${YELLOW}What to try manually:${NC}"
  if [[ "$OS_TYPE" == "macos" ]]; then
    echo -e "  ${CYAN}a)${NC} Check logs:  ${DIM}log show --predicate 'process == \"openclaw-gateway\"' --last 10m${NC}"
  else
    echo -e "  ${CYAN}a)${NC} Check logs:  ${DIM}journalctl --user -u openclaw-gateway -n 100 --no-pager${NC}"
  fi
  echo -e "  ${CYAN}b)${NC} Check config: ${DIM}cat $OC_CONFIG | python3 -m json.tool${NC}"
  echo -e "     ${DIM}(If JSON is invalid: cp $BACKUP_DIR/pre-update-*.json $OC_CONFIG)${NC}"
  echo -e "  ${CYAN}c)${NC} Rollback:    ${DIM}sos → option 4${NC}"
  echo -e "  ${CYAN}d)${NC} Full reinstall:"
  echo -e "     ${DIM}npm install -g openclaw@$(get_version)${NC}"
  echo -e "     ${DIM}openclaw gateway install --force${NC}"
  if [[ "$OS_TYPE" == "macos" ]]; then
    echo -e "     ${DIM}sos → option 2 (restart)${NC}"
  else
    echo -e "     ${DIM}systemctl --user restart openclaw-gateway${NC}"
  fi
  echo ""
  echo -e "${RED}If nothing works: https://discord.com/invite/clawd${NC}"
  log "AUTOFIX" "FAILED — all repair attempts exhausted"
  return 1
}

# === Self-test ===
self_test() {
  local ok=true
  echo -e "${YELLOW}Running self-test...${NC}"
  log "ACTION" "Self-test started"

  if ! command -v openclaw &>/dev/null; then
    echo -e "${RED}✗ openclaw binary not found in PATH${NC}"; ok=false
  else
    echo -e "${GREEN}✓ openclaw binary found${NC}"
  fi

  if [[ ! -f "$OC_CONFIG" ]]; then
    echo -e "${RED}✗ Config not found at $OC_CONFIG${NC}"; ok=false
  else
    echo -e "${GREEN}✓ Config file exists ($(du -h "$OC_CONFIG" | cut -f1))${NC}"
  fi

  local svc_type=$(detect_service)
  if [[ "$svc_type" == "none" ]]; then
    echo -e "${YELLOW}⚠ No systemd service detected (manual mode)${NC}"
  else
    echo -e "${GREEN}✓ Service type: $svc_type${NC}"
  fi

  local backup_count=$(ls $BACKUP_DIR/pre-update-*.json 2>/dev/null | wc -l)
  echo -e "${GREEN}✓ Backups available: $backup_count${NC}"

  local avail_mb=$(get_avail_disk_mb)
  if [[ $avail_mb -lt 500 ]]; then
    echo -e "${RED}✗ Low disk space: ${avail_mb}MB free${NC}"; ok=false
  else
    echo -e "${GREEN}✓ Disk space OK: ${avail_mb}MB free${NC}"
  fi

  local avail_ram=$(get_avail_ram_mb)
  if [[ $avail_ram -lt 200 ]]; then
    echo -e "${RED}✗ Low RAM: ${avail_ram}MB available${NC}"; ok=false
  else
    echo -e "${GREEN}✓ RAM OK: ${avail_ram}MB available${NC}"
  fi

  if [[ -w "$LOG_FILE" ]] || touch "$LOG_FILE" 2>/dev/null; then
    echo -e "${GREEN}✓ Log file writable${NC}"
  else
    echo -e "${RED}✗ Can't write to log file${NC}"; ok=false
  fi

  if is_healthy; then
    echo -e "${GREEN}✓ Health check: gateway is healthy${NC}"
  else
    echo -e "${YELLOW}⚠ Health check: gateway not healthy${NC}"
  fi

  # Quick network test
  if timeout 5 curl -sf https://api.telegram.org -o /dev/null 2>/dev/null; then
    echo -e "${GREEN}✓ Network: Telegram API reachable${NC}"
  else
    echo -e "${RED}✗ Network: can't reach Telegram API${NC}"; ok=false
  fi

  if $ok; then
    echo -e "\n${GREEN}All checks passed ✅${NC}"
    log "INFO" "Self-test: ALL PASSED"
  else
    echo -e "\n${RED}Some checks failed ❌${NC}"
    log "WARN" "Self-test: SOME FAILED"
  fi
}

# === Handle CLI flags ===
if [[ "${1:-}" == "--version" || "${1:-}" == "-v" ]]; then
  echo "SOS v${SOS_VERSION}"
  exit 0
fi

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  # Print the header comment block
  sed -n '2,/^[^#]/p' "$0" | grep '^#' | sed 's/^# \?//'
  exit 0
fi

# === Handle CLI shortcuts ===
if [[ "${1:-}" == "auto" || "${1:-}" == "autofix" || "${1:-}" == "fix" ]]; then
  log_start
  log "ACTION" "Autofix triggered via CLI: $1"
  autofix
  log "INFO" "=== SOS session ended ==="
  exit $?
fi

if [[ "${1:-}" == "net" || "${1:-}" == "network" ]]; then
  log_start
  log "ACTION" "Network check via CLI"
  check_network
  log "INFO" "=== SOS session ended ==="
  exit 0
fi

if [[ "${1:-}" == "test" || "${1:-}" == "tg" ]]; then
  log_start
  log "ACTION" "Telegram test via CLI"
  telegram_test
  log "INFO" "=== SOS session ended ==="
  exit $?
fi

# === Whiptail menu (arrow keys, temp file for compatibility) ===
whiptail_menu() {
  local ver=$(get_version)
  local svc=$(detect_service)
  local tmpfile=$(mktemp)
  local _wt=$(get_whiptail_cmd)

  $_wt --title " SOS Recovery Menu v6 " \
    --default-item "AUTOFIX" \
    --menu "  Version: $ver | Service: $svc\n\n  Use arrow keys, Enter to select:" 22 60 13 \
    "AUTOFIX"  "Diagnose + fix automatically" \
    "status"   "Check status (look, don't touch)" \
    "restart"  "Restart gateway" \
    "force"    "Force kill + restart" \
    "rollback" "Rollback to backup" \
    "logs"     "View last 50 logs" \
    "diag"     "Full diagnostics" \
    "backup"   "Backup config NOW" \
    "selftest" "Self-test" \
    "nuclear"  "NUCLEAR (last resort!)" \
    "network"  "Network check" \
    "telegram" "Telegram test message" \
    "exit"     "Exit" \
    2>"$tmpfile"

  local rc=$?
  local choice=$(cat "$tmpfile")
  rm -f "$tmpfile"

  [[ $rc -ne 0 ]] && { echo "0"; return; }

  case "$choice" in
    AUTOFIX)  echo "10" ;;
    status)   echo "1" ;;
    restart)  echo "2" ;;
    force)    echo "3" ;;
    rollback) echo "4" ;;
    logs)     echo "5" ;;
    diag)     echo "6" ;;
    backup)   echo "7" ;;
    selftest) echo "8" ;;
    nuclear)  echo "9" ;;
    network)  echo "11" ;;
    telegram) echo "12" ;;
    exit)     echo "0" ;;
    *)        echo "0" ;;
  esac
}

# === Fallback text menu ===
text_menu() {
  local CURRENT_VER=$(get_version)
  local LAST_BACKUP=$(ls -t $BACKUP_DIR/pre-update-*.json 2>/dev/null | head -1 | xargs basename 2>/dev/null || echo "none")

  # All display to stderr so $() only captures the final choice
  {
    clear
    echo -e "${RED}╔══════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║         🚨  SOS RECOVERY MENU  v6                   ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════╝${NC}"
    echo -e "  Version: ${GREEN}${CURRENT_VER}${NC} | Service: ${GREEN}$(detect_service)${NC}"
    echo -e "  Backup: ${CYAN}${LAST_BACKUP}${NC}"
    echo -e "  Log: ${DIM}${LOG_FILE}${NC}"
    echo ""
    echo -e "${GREEN} ↵)${NC} 🔧 AUTOFIX           ${DIM}— just press Enter (recommended!)${NC}"
    echo ""
    echo -e "${CYAN} 1)${NC} Check status         ${DIM}— just look, don't touch${NC}"
    echo -e "${CYAN} 2)${NC} Restart gateway      ${DIM}— graceful restart, fixes most issues${NC}"
    echo -e "${CYAN} 3)${NC} Force kill + restart  ${DIM}— when restart hangs${NC}"
    echo -e "${CYAN} 4)${NC} Rollback to backup   ${DIM}— undo a bad update${NC}"
    echo -e "${CYAN} 5)${NC} View logs            ${DIM}— gateway + SOS action log${NC}"
    echo -e "${CYAN} 6)${NC} Full diagnostics     ${DIM}— TG, RAM, disk, sessions, everything${NC}"
    echo -e "${CYAN} 7)${NC} Backup config NOW    ${DIM}— save before doing something risky${NC}"
    echo -e "${CYAN} 8)${NC} Self-test            ${DIM}— verify this script works${NC}"
    echo -e "${RED} 9)${NC} ☢️  Nuclear            ${DIM}— kill everything, last resort only${NC}"
    echo -e "${CYAN}11)${NC} Network check        ${DIM}— test DNS, internet, Telegram API${NC}"
    echo -e "${CYAN}12)${NC} Telegram test        ${DIM}— send a real test message${NC}"
    echo -e "${CYAN} 0)${NC} Exit"
    echo ""
    echo -e "${DIM}Tip: just press Enter, or run 'sos auto'. Shortcuts: sos net | sos tg | sos fix${NC}"
    echo ""
    echo -ne "${BOLD}Pick an option [Enter = autofix]: ${NC}"
  } >&2
  read -r opt
  echo "${opt:-10}"
}

# === Pick menu mode: whiptail/dialog if TTY + available, else text ===
pick_menu() {
  if [[ -t 0 && -t 1 ]] && has_whiptail; then
    whiptail_menu
  else
    text_menu
  fi
}

# === Main Menu Loop ===
while true; do
  log_start

  # Whiptail/dialog needs direct terminal access — no subshell $()
  if [[ -t 0 && -t 1 ]] && has_whiptail; then
    local_tmpfile=$(mktemp)
    _wt=$(get_whiptail_cmd)
    $_wt --title " SOS Recovery Menu v6 " \
      --default-item "AUTOFIX" \
      --menu "  Version: $(get_version) | Service: $(detect_service)\n\n  Use arrow keys, Enter to select:" 22 60 13 \
      "AUTOFIX"  "Diagnose + fix automatically" \
      "status"   "Check status (look, don't touch)" \
      "restart"  "Restart gateway" \
      "force"    "Force kill + restart" \
      "rollback" "Rollback to backup" \
      "logs"     "View last 50 logs" \
      "diag"     "Full diagnostics" \
      "backup"   "Backup config NOW" \
      "selftest" "Self-test" \
      "nuclear"  "NUCLEAR (last resort!)" \
      "network"  "Network check" \
      "telegram" "Telegram test message" \
      "exit"     "Exit" \
      2>"$local_tmpfile"
    local_rc=$?
    local_choice=$(cat "$local_tmpfile")
    rm -f "$local_tmpfile"
    if [[ $local_rc -ne 0 ]]; then
      opt="0"
    else
      case "$local_choice" in
        AUTOFIX)  opt="10" ;; status)   opt="1" ;; restart)  opt="2" ;;
        force)    opt="3" ;;  rollback) opt="4" ;; logs)     opt="5" ;;
        diag)     opt="6" ;;  backup)   opt="7" ;; selftest) opt="8" ;;
        nuclear)  opt="9" ;;  network)  opt="11" ;; telegram) opt="12" ;;
        exit)     opt="0" ;;  *)        opt="0" ;;
      esac
    fi
  else
    opt=$(text_menu)
  fi

  [[ "$opt" == "255" ]] && exit 0

  log "ACTION" "User selected option: $opt"

  case $opt in
    10|auto|autofix|fix)
      autofix
      ;;
    1)
      echo -e "\n${YELLOW}=== Service ===${NC}"
      svc_cmd status
      echo -e "\n${YELLOW}=== Process ===${NC}"
      ps aux | grep openclaw-gateway | grep -v grep || echo -e "${RED}Not running!${NC}"
      echo -e "\n${YELLOW}=== Version ===${NC}"
      get_version
      echo -e "\n${YELLOW}=== RAM ===${NC}"
      show_ram
      echo -e "\n${YELLOW}=== Disk ===${NC}"
      df -h / | tail -1
      log "INFO" "Status check completed"
      ;;
    2)
      echo -e "\n${YELLOW}Restarting gateway...${NC}"
      echo -e "${DIM}This takes ~10 seconds. Bot will be back in ~30s.${NC}"
      svc_cmd restart
      sleep 5
      svc_cmd status
      echo -e "\n${GREEN}Done. Wait 30 seconds then message on Telegram.${NC}"
      log "INFO" "Restart completed"
      ;;
    3)
      echo -e "\n${RED}Force killing all gateway processes...${NC}"
      echo -e "${DIM}Use this when option 2 hangs or doesn't work.${NC}"
      kill -9 $(pgrep -f openclaw-gateway) 2>/dev/null || true
      log "WARN" "Force killed gateway process"
      sleep 3
      echo -e "${YELLOW}Starting fresh...${NC}"
      svc_cmd start
      sleep 5
      svc_cmd status
      echo -e "\n${GREEN}Done. Wait 30 seconds then message on Telegram.${NC}"
      log "INFO" "Force restart completed"
      ;;
    4)
      echo -e "\n${DIM}Rollback = go back to the previous working version + config.${NC}"
      LAST_BACKUP_PATH=$(ls -t $BACKUP_DIR/pre-update-*.json 2>/dev/null | head -1)
      LAST_VER_PATH=$(ls -t $BACKUP_DIR/pre-update-*.version 2>/dev/null | head -1)
      if [[ -z "${LAST_BACKUP_PATH:-}" ]]; then
        echo -e "${RED}No backup found!${NC}"
        echo -e "${DIM}Enter the version number you want (e.g. 2026.3.7):${NC}"
        echo -ne "> "
        read -r ROLLBACK_VER
        log "WARN" "No backup found, manual version entry: $ROLLBACK_VER"
      else
        ROLLBACK_VER=$(cat "$LAST_VER_PATH" 2>/dev/null || "")
        echo -e "Backup found: ${CYAN}$(basename $LAST_BACKUP_PATH)${NC}"
        echo -e "Will rollback to version: ${CYAN}${ROLLBACK_VER:-unknown}${NC}"
        if [[ -z "${ROLLBACK_VER:-}" ]]; then
          echo -e "${DIM}Version file missing. Enter the version:${NC}"
          echo -ne "> "
          read -r ROLLBACK_VER
        fi
      fi
      echo -ne "${RED}Rollback to ${ROLLBACK_VER}? (y/N): ${NC}"
      read -r confirm
      if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
        log "ACTION" "Rollback started to version $ROLLBACK_VER"
        echo -e "${YELLOW}Step 1/4: Installing openclaw@${ROLLBACK_VER}...${NC}"
        if ! npm install -g openclaw@${ROLLBACK_VER}; then
          echo -e "${RED}npm install failed! Aborting.${NC}"
          log "ERROR" "npm install failed for $ROLLBACK_VER"
        else
          echo -e "${YELLOW}Step 2/4: Reinstalling gateway service...${NC}"
          openclaw gateway install --force
          if [[ -n "${LAST_BACKUP_PATH:-}" ]]; then
            echo -e "${YELLOW}Step 3/4: Restoring config backup...${NC}"
            cp "$LAST_BACKUP_PATH" "$OC_CONFIG"
          else
            echo -e "${YELLOW}Step 3/4: No config to restore (skipped).${NC}"
          fi
          echo -e "${YELLOW}Step 4/4: Restarting...${NC}"
          svc_cmd restart
          sleep 5
          echo -e "${GREEN}Rolled back to: $(get_version)${NC}"
          echo -e "${GREEN}Wait 30 seconds then message on Telegram.${NC}"
          log "INFO" "Rollback completed to $(get_version)"
        fi
      else
        echo "Cancelled."
        log "INFO" "Rollback cancelled by user"
      fi
      ;;
    5)
      echo -e "\n${YELLOW}Last 50 gateway log lines:${NC}"
      echo -e "${DIM}Look for lines with ERROR, FATAL, or crash/exit messages.${NC}\n"
      show_logs 50
      echo -e "\n${YELLOW}=== SOS action log (last 20 entries) ===${NC}"
      echo -e "${DIM}These are YOUR previous SOS actions:${NC}\n"
      tail -20 "$LOG_FILE" 2>/dev/null || echo "No SOS log yet."
      log "INFO" "Viewed logs"
      ;;
    6)
      echo -e "\n${DIM}Full system check — takes a few seconds...${NC}"
      echo -e "\n${YELLOW}=== Telegram ===${NC}"
      openclaw status 2>&1 | grep -A2 "Telegram" || echo "Can't check"
      echo -e "\n${YELLOW}=== Sessions ===${NC}"
      openclaw status 2>&1 | grep "Sessions" | head -1 || echo "Can't check"
      echo -e "\n${YELLOW}=== RAM ===${NC}"
      show_ram_full
      echo -e "\n${YELLOW}=== OpenClaw Process ===${NC}"
      ps aux | grep openclaw-gateway | grep -v grep | awk '{printf "RSS: %.0fMB | CPU: %s%%\n", $6/1024, $3}' || echo "Not running"
      echo -e "\n${YELLOW}=== Disk ===${NC}"
      du -sh "$OC_HOME/" 2>/dev/null
      df -h / | tail -1
      echo -e "\n${YELLOW}=== Node.js ===${NC}"
      node --version 2>/dev/null || echo "node not found!"
      echo -e "\n${YELLOW}=== Uptime ===${NC}"
      uptime
      log "INFO" "Full diagnostics completed"
      ;;
    7)
      echo -e "${DIM}Saving a snapshot of the current config + version...${NC}"
      TIMESTAMP=$(date +%Y%m%d-%H%M%S)
      cp "$OC_CONFIG" "$BACKUP_DIR/pre-update-${TIMESTAMP}.json"
      echo "$CURRENT_VER" > "$BACKUP_DIR/pre-update-${TIMESTAMP}.version"
      echo -e "${GREEN}Backed up:${NC}"
      echo "  Config → $BACKUP_DIR/pre-update-${TIMESTAMP}.json"
      echo "  Version → $CURRENT_VER"
      ls -t $BACKUP_DIR/pre-update-*.json 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null
      ls -t $BACKUP_DIR/pre-update-*.version 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null
      echo -e "${GREEN}Old backups cleaned (keeping last 5).${NC}"
      log "INFO" "Manual backup created: pre-update-${TIMESTAMP}"
      ;;
    8)
      self_test
      ;;
    9)
      echo -e "\n${RED}☢️  NUCLEAR OPTION${NC}"
      echo -e "${DIM}This kills ALL openclaw processes, reloads systemd, and starts fresh.${NC}"
      echo -e "${DIM}Use ONLY if options 2 and 3 both failed.${NC}"
      echo -ne "Type ${RED}YES${NC} to confirm (anything else = cancel): "
      read -r confirm
      if [[ "$confirm" == "YES" ]]; then
        log "CRITICAL" "Nuclear option activated"
        echo -e "${RED}Killing everything...${NC}"
        kill -9 $(pgrep -f openclaw) 2>/dev/null || true
        sleep 3
        echo -e "${YELLOW}Reloading service manager...${NC}"
        daemon_reload
        echo -e "${YELLOW}Starting gateway...${NC}"
        svc_cmd start
        sleep 5
        svc_cmd status
        echo -e "\n${GREEN}Nuked and restarted. Wait 30 seconds.${NC}"
        log "INFO" "Nuclear restart completed"
      else
        echo "Cancelled."
        log "INFO" "Nuclear cancelled by user"
      fi
      ;;
    11|net|network)
      check_network
      ;;
    12|tg|test)
      telegram_test
      ;;
    0|q|quit|exit)
      log "INFO" "SOS session ended (user exit)"
      echo "Bye."
      exit 0
      ;;
    *)
      echo "Invalid option."
      log "WARN" "Invalid option entered: $opt"
      ;;
  esac

  echo ""
  echo -ne "${DIM}Press Enter to return to menu (or 0 to exit)...${NC}"
  read -r back
  [[ "$back" == "0" || "$back" == "q" ]] && { log "INFO" "=== SOS session ended ==="; exit 0; }
done
