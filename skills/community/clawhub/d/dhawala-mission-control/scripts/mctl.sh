#!/usr/bin/env bash
# Mission Control - System health aggregator for autonomous agents
# Collects status from daemons, cron, services, resources in one shot.
set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
RESET='\033[0m'

JSON_MODE=false
SECTION=""

usage() {
  cat <<EOF
Usage: mctl [options] [command]

Commands:
  status        Full system status (default)
  agents        List running agent processes
  health        Resource health (CPU, RAM, disk, GPU)
  cron          Cron job status
  services      Systemd service checks
  logs [name]   Recent logs for a service/agent
  restart <name> Restart a systemd service

Options:
  --json        Output as JSON
  -h, --help    Show this help
EOF
  exit 0
}

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON_MODE=true; shift ;;
    -h|--help) usage ;;
    status|agents|health|cron|services|logs|restart) SECTION="$1"; shift; break ;;
    *) echo "Unknown: $1"; usage ;;
  esac
done

EXTRA_ARG="${1:-}"

# --- Collectors ---

collect_agents() {
  local agents=()
  # OpenClaw daemon
  if pgrep -f "openclaw daemon" >/dev/null 2>&1; then
    local pid
    pid=$(pgrep -f "openclaw daemon" | head -1)
    local uptime_info
    uptime_info=$(ps -p "$pid" -o etime= 2>/dev/null | xargs)
    agents+=("{\"name\":\"openclaw-daemon\",\"pid\":$pid,\"uptime\":\"$uptime_info\",\"status\":\"running\"}")
  fi
  # OpenClaw gateway
  if pgrep -f "openclaw gateway" >/dev/null 2>&1; then
    local pid
    pid=$(pgrep -f "openclaw gateway" | head -1)
    local uptime_info
    uptime_info=$(ps -p "$pid" -o etime= 2>/dev/null | xargs)
    agents+=("{\"name\":\"openclaw-gateway\",\"pid\":$pid,\"uptime\":\"$uptime_info\",\"status\":\"running\"}")
  fi
  # Node/python agents (generic detection - skip kernel threads and this script)
  while IFS= read -r line; do
    local pid name uptime_info
    pid=$(echo "$line" | awk '{print $1}')
    name=$(echo "$line" | awk '{for(i=2;i<=NF;i++) printf $i" "; print ""}' | sed 's/ *$//' | head -c 60)
    # Skip kernel threads (enclosed in brackets) and self
    [[ "$name" =~ ^\[ ]] && continue
    [[ "$name" =~ mctl\.sh ]] && continue
    uptime_info=$(ps -p "$pid" -o etime= 2>/dev/null | xargs)
    agents+=("{\"name\":\"$(echo "$name" | sed 's/"/\\"/g')\",\"pid\":$pid,\"uptime\":\"$uptime_info\",\"status\":\"running\"}")
  done < <(pgrep -af "(agent|daemon|worker|aoms)" 2>/dev/null | grep -v "grep\|mctl\|pgrep" | head -20 || true)

  if $JSON_MODE; then
    echo "[$(IFS=,; echo "${agents[*]:-}")]}]" | sed 's/\]}]/]/'
  else
    if [ ${#agents[@]} -eq 0 ]; then
      echo -e "  ${YELLOW}No agent processes detected${RESET}"
    else
      for a in "${agents[@]}"; do
        local name pid uptime_val
        name=$(echo "$a" | grep -oP '"name":"[^"]*"' | cut -d'"' -f4)
        pid=$(echo "$a" | grep -oP '"pid":[0-9]*' | cut -d: -f2)
        uptime_val=$(echo "$a" | grep -oP '"uptime":"[^"]*"' | cut -d'"' -f4)
        echo -e "  ${GREEN}*${RESET} ${BOLD}$name${RESET}  PID=$pid  uptime=$uptime_val"
      done
    fi
  fi
}

collect_health() {
  local cpu_count mem_total mem_avail mem_pct disk_used disk_total disk_pct load
  cpu_count=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "?")
  load=$(cat /proc/loadavg 2>/dev/null | awk '{print $1, $2, $3}' || uptime | awk -F'load average:' '{print $2}' | xargs)

  if command -v free >/dev/null 2>&1; then
    mem_total=$(free -m | awk '/^Mem:/{print $2}')
    mem_avail=$(free -m | awk '/^Mem:/{print $7}')
    mem_pct=$(( (mem_total - mem_avail) * 100 / mem_total ))
  else
    mem_total="?"
    mem_avail="?"
    mem_pct="?"
  fi

  disk_info=$(df -h / 2>/dev/null | awk 'NR==2{print $3, $2, $5}')
  disk_used=$(echo "$disk_info" | awk '{print $1}')
  disk_total=$(echo "$disk_info" | awk '{print $2}')
  disk_pct=$(echo "$disk_info" | awk '{print $3}' | tr -d '%')

  # GPU (NVIDIA)
  local gpu_info=""
  if command -v nvidia-smi >/dev/null 2>&1; then
    gpu_info=$(nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
  fi

  if $JSON_MODE; then
    local gpu_json="null"
    if [ -n "$gpu_info" ]; then
      local vram_used vram_total gpu_util
      vram_used=$(echo "$gpu_info" | cut -d',' -f1 | xargs)
      vram_total=$(echo "$gpu_info" | cut -d',' -f2 | xargs)
      gpu_util=$(echo "$gpu_info" | cut -d',' -f3 | xargs)
      gpu_json="{\"vram_used_mb\":$vram_used,\"vram_total_mb\":$vram_total,\"gpu_util_pct\":$gpu_util}"
    fi
    cat <<JSONEOF
{"cpus":$cpu_count,"load":"$load","mem_total_mb":$mem_total,"mem_avail_mb":$mem_avail,"mem_pct":$mem_pct,"disk_used":"$disk_used","disk_total":"$disk_total","disk_pct":$disk_pct,"gpu":$gpu_json}
JSONEOF
  else
    # Color-code percentages
    local mem_color="$GREEN" disk_color="$GREEN"
    [ "$mem_pct" != "?" ] && [ "$mem_pct" -gt 80 ] && mem_color="$RED"
    [ "$mem_pct" != "?" ] && [ "$mem_pct" -gt 60 ] && [ "$mem_pct" -le 80 ] && mem_color="$YELLOW"
    [ -n "$disk_pct" ] && [ "$disk_pct" -gt 85 ] && disk_color="$RED"
    [ -n "$disk_pct" ] && [ "$disk_pct" -gt 70 ] && [ "$disk_pct" -le 85 ] && disk_color="$YELLOW"

    echo -e "  CPUs: ${BOLD}$cpu_count${RESET}  Load: $load"
    echo -e "  RAM:  ${mem_color}${mem_pct}%${RESET} used  (${mem_avail}MB free / ${mem_total}MB total)"
    echo -e "  Disk: ${disk_color}${disk_pct}%${RESET} used  ($disk_used / $disk_total)"

    if [ -n "$gpu_info" ]; then
      local vram_used vram_total gpu_util
      vram_used=$(echo "$gpu_info" | cut -d',' -f1 | xargs)
      vram_total=$(echo "$gpu_info" | cut -d',' -f2 | xargs)
      gpu_util=$(echo "$gpu_info" | cut -d',' -f3 | xargs)
      echo -e "  VRAM: ${vram_used}MB / ${vram_total}MB  GPU: ${gpu_util}%"
    fi
  fi
}

collect_cron() {
  if command -v openclaw >/dev/null 2>&1; then
    if $JSON_MODE; then
      local raw
      raw=$(openclaw cron list --json 2>/dev/null || true)
      if echo "$raw" | python3 -m json.tool >/dev/null 2>&1; then
        echo "$raw"
      else
        echo "[]"
      fi
    else
      openclaw cron list 2>/dev/null || echo -e "  ${YELLOW}No openclaw cron jobs found${RESET}"
    fi
  else
    if $JSON_MODE; then
      echo "[]"
    else
      echo -e "  ${YELLOW}openclaw CLI not found${RESET}"
    fi
  fi
}

collect_services() {
  local services=("openclaw-gateway" "openclaw-daemon")
  if $JSON_MODE; then
    local items=()
    for svc in "${services[@]}"; do
      local active
      active=$(systemctl is-active "$svc" 2>/dev/null | head -1 || true)
      active="${active:-not-found}"
      items+=("{\"name\":\"$svc\",\"status\":\"$active\"}")
    done
    echo "[$(IFS=,; echo "${items[*]}")]"
  else
    for svc in "${services[@]}"; do
      local active
      active=$(systemctl is-active "$svc" 2>/dev/null | head -1 || true)
      active="${active:-not-found}"
      local color="$GREEN"
      [ "$active" != "active" ] && color="$YELLOW"
      [ "$active" = "failed" ] && color="$RED"
      echo -e "  ${color}[$active]${RESET} $svc"
    done
    # Also check listening ports
    echo ""
    echo -e "  ${BOLD}Listening ports:${RESET}"
    ss -ltnp 2>/dev/null | grep -E "LISTEN" | awk '{printf "    %s  %s\n", $4, $6}' | head -15 || \
      echo -e "    ${YELLOW}Could not query ports${RESET}"
  fi
}

show_logs() {
  local name="${EXTRA_ARG:-openclaw-daemon}"
  if systemctl is-active "$name" >/dev/null 2>&1 || systemctl is-failed "$name" >/dev/null 2>&1; then
    journalctl -u "$name" --no-pager -n 50 --since "1 hour ago" 2>/dev/null || \
      echo "No journalctl logs for $name"
  else
    # Try openclaw logs
    if command -v openclaw >/dev/null 2>&1; then
      openclaw logs --tail 50 2>/dev/null || echo "No logs found for $name"
    else
      echo "Service '$name' not found and openclaw CLI not available"
    fi
  fi
}

do_restart() {
  local name="${EXTRA_ARG:-}"
  if [ -z "$name" ]; then
    echo "Usage: mctl restart <service-name>"
    exit 1
  fi
  echo -e "${YELLOW}Restarting $name...${RESET}"
  sudo systemctl restart "$name" 2>/dev/null && \
    echo -e "${GREEN}Restarted $name${RESET}" || \
    echo -e "${RED}Failed to restart $name${RESET}"
}

# --- Main ---

full_status() {
  if $JSON_MODE; then
    local tmpdir
    tmpdir=$(mktemp -d)
    collect_agents > "$tmpdir/agents.json"
    collect_health > "$tmpdir/health.json"
    collect_cron > "$tmpdir/cron.json"
    collect_services > "$tmpdir/services.json"
    TMPDIR_MCTL="$tmpdir" python3 -c "
import json, os
d = os.environ['TMPDIR_MCTL']
def load(f):
    try:
        with open(os.path.join(d, f)) as fh:
            return json.load(fh)
    except Exception:
        return []
print(json.dumps({
    'timestamp': '$(date -Iseconds)',
    'agents': load('agents.json'),
    'health': load('health.json'),
    'cron': load('cron.json'),
    'services': load('services.json')
}, indent=2))
"
    rm -rf "$tmpdir"
  else
    echo ""
    echo -e "${CYAN}${BOLD}=== MISSION CONTROL ===${RESET}"
    echo -e "${CYAN}$(date)${RESET}"
    echo ""
    echo -e "${BOLD}--- Agents ---${RESET}"
    collect_agents
    echo ""
    echo -e "${BOLD}--- Resources ---${RESET}"
    collect_health
    echo ""
    echo -e "${BOLD}--- Cron Jobs ---${RESET}"
    collect_cron
    echo ""
    echo -e "${BOLD}--- Services ---${RESET}"
    collect_services
    echo ""

    # OpenClaw status if available
    if command -v openclaw >/dev/null 2>&1; then
      echo -e "${BOLD}--- OpenClaw ---${RESET}"
      openclaw status 2>/dev/null | head -10 || echo -e "  ${YELLOW}Could not query openclaw status${RESET}"
      echo ""
    fi
  fi
}

case "${SECTION:-status}" in
  status)   full_status ;;
  agents)   if ! $JSON_MODE; then echo -e "\n${BOLD}--- Agents ---${RESET}"; fi; collect_agents ;;
  health)   if ! $JSON_MODE; then echo -e "\n${BOLD}--- Resources ---${RESET}"; fi; collect_health ;;
  cron)     if ! $JSON_MODE; then echo -e "\n${BOLD}--- Cron Jobs ---${RESET}"; fi; collect_cron ;;
  services) if ! $JSON_MODE; then echo -e "\n${BOLD}--- Services ---${RESET}"; fi; collect_services ;;
  logs)     show_logs ;;
  restart)  do_restart ;;
  *)        usage ;;
esac
