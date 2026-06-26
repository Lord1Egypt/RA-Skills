#!/bin/bash

# Daily Greeting Skill - Main execution script
# Function: Trigger each agent to send their own daily greeting
# Boundary: Only responsible for finding agents and sending trigger signal, not message content

set -e

# Configuration
SKILL_DIR="${SKILL_DIR:-$HOME/.openclaw/skills/daily-greeting}"
STATE_FILE="$SKILL_DIR/data/state.json"
CONFIG_FILE="$SKILL_DIR/config.json"

# Default configuration
DEFAULT_CONFIG='{
  "enabled": true,
  "workingDaysOnly": true,
  "delayMs": 3000,
  "excludeAgents": ["main"],
  "triggerMessage": "Please send a daily greeting to your bound channel. Requirements: 1) Compose the greeting in the user'\''s preferred language (infer from channel history and user context); 2) Include relevant status information based on your agent role and ongoing tasks with the user (e.g., if you'\''re a todo agent, summarize progress and today'\''s priorities; if you'\''re a diary agent, mention ongoing projects); 3) Use message tool to send to your bound channel; 4) End conversation after sending"
}'

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Cross-platform sed in-place edit
# macOS: sed -i '' 'pattern'
# Linux: sed -i 'pattern'
sed_i() {
  if sed --version 2>/dev/null | grep -q "GNU"; then
    # Linux (GNU sed)
    sed -i "$@"
  else
    # macOS (BSD sed)
    sed -i '' "$@"
  fi
}

# Load configuration
load_config() {
  if [ -f "$CONFIG_FILE" ]; then
    CONFIG=$(cat "$CONFIG_FILE")
  else
    CONFIG="$DEFAULT_CONFIG"
    echo "$DEFAULT_CONFIG" > "$CONFIG_FILE"
  fi
}

# Check if today is a working day
is_working_day() {
  local day_of_week=$(date +%u)
  if [ "$day_of_week" -ge 1 ] && [ "$day_of_week" -le 5 ]; then
    return 0
  fi
  return 1
}

# Check if today has already been executed
should_run_today() {
  local today=$(date +%Y-%m-%d)
  
  if [ ! -f "$STATE_FILE" ]; then
    return 0
  fi
  
  local last_run=$(jq -r '.lastRun // ""' "$STATE_FILE" 2>/dev/null)
  
  if [ -z "$last_run" ] || [ "$last_run" != "$today" ]; then
    return 0
  fi
  
  local completed_count=$(jq '.agents | to_entries | map(select(.value == "completed")) | length' "$STATE_FILE" 2>/dev/null)
  
  if [ "$completed_count" -gt 0 ]; then
    log_warn "Already executed today, skipping"
    return 1
  fi
  
  return 0
}

# Get all bound agents
get_bound_agents() {
  local openclaw_config="$HOME/.openclaw/openclaw.json"
  
  if [ ! -f "$openclaw_config" ]; then
    log_error "Cannot find OpenClaw config file"
    return 1
  fi
  
  jq -r '.bindings[] | select(.match.channel != null) | "\(.agentId)|\(.match.channel)|\(.match.peer.id // .match.accountId)"' "$openclaw_config" 2>/dev/null
}

# Trigger agent to send greeting (only sends trigger signal, content is decided by agent)
trigger_agent() {
  local agent_id="$1"
  local channel="$2"
  local target="$3"

  # Get trigger message
  local trigger_msg=$(echo "$CONFIG" | jq -r '.triggerMessage // "Please send a daily greeting"')

  # Call agent (let agent decide message content and channel)
  openclaw agent --agent "$agent_id" --channel "$channel" -m "$trigger_msg" --deliver 2>&1
}

# Execute greeting
run_greeting() {
  log_info "Starting to trigger agents for daily greeting..."
  
  load_config
  
  local enabled=$(echo "$CONFIG" | jq -r '.enabled // true')
  if [ "$enabled" != "true" ]; then
    log_info "Greeting disabled, skipping"
    return 0
  fi
  
  local working_days=$(echo "$CONFIG" | jq -r '.workingDaysOnly // true')
  if [ "$working_days" = "true" ] && ! is_working_day; then
    log_info "Today is not a working day, skipping"
    return 0
  fi
  
  if ! should_run_today; then
    return 0
  fi
  
  local delay=$(echo "$CONFIG" | jq -r '.delayMs // 3000')
  log_info "Waiting $delay ms before execution..."
  sleep "$((delay / 1000))"
  
  local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "{\"lastRun\": \"$timestamp\", \"agents\": {}}" > "$STATE_FILE"
  
  local success_count=0
  local fail_count=0
  
  while IFS='|' read -r agent_id channel target; do
    [ -z "$agent_id" ] && continue
    
    local exclude_agents=$(echo "$CONFIG" | jq -r '.excludeAgents // []' | tr -d '[]"')
    if echo "$exclude_agents" | grep -q "$agent_id"; then
      log_info "Skipping excluded agent: $agent_id"
      continue
    fi
    
    log_info "Triggering $agent_id ..."
    
    if trigger_agent "$agent_id" "$channel" "$target" > /dev/null 2>&1; then
      log_info "✓ $agent_id triggered"
      jq ".agents.\"$agent_id\" = \"completed\"" "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
      success_count=$((success_count + 1))
    else
      log_error "✗ $agent_id trigger failed"
      jq ".agents.\"$agent_id\" = \"failed\"" "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
      fail_count=$((fail_count + 1))
    fi
    
  done < <(get_bound_agents)
  
  log_info "Greeting trigger completed: success $success_count, failed $fail_count"
}

# Show status
show_status() {
  if [ -f "$STATE_FILE" ]; then
    cat "$STATE_FILE" | jq '.'
  else
    echo "No execution records"
  fi
}

# Reset state
reset_status() {
  rm -f "$STATE_FILE"
  log_info "State reset, will re-execute on next startup"
}

# Install - record BOOT.md path for uninstall
record_install() {
  local boot_md="${1:-$HOME/.openclaw/workspace/BOOT.md}"

  mkdir -p "$SKILL_DIR/data"

  local install_info=$(cat <<EOF
{
  "bootMdPath": "$boot_md",
  "installedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)

  echo "$install_info" > "$SKILL_DIR/data/install.json"
  log_info "Install recorded: BOOT.md at $boot_md"
}

# Install cron job for daily greeting using OpenClaw's built-in cron
install_cron() {
  local cron_schedule="${1:-0 9 * * 1-5}"

  # Check if already installed
  if openclaw cron list 2>/dev/null | grep -q "daily-greeting"; then
    log_info "OpenClaw cron job already exists for daily-greeting"
    return 0
  fi

  # Add cron job using OpenClaw's cron system
  openclaw cron add \
    --name "daily-greeting" \
    --cron "$cron_schedule" \
    --session isolated \
    --message "bash $SKILL_DIR/scripts/greeting.sh run" \
    --wake now

  log_info "OpenClaw cron job installed: $cron_schedule (weekdays at 9am)"
  log_info "To view/modify: openclaw cron list"
}

# Uninstall skill
uninstall_skill() {
  log_info "Uninstalling daily-greeting skill..."

  local install_info="$SKILL_DIR/data/install.json"

  # Step 1: Read BOOT.md path from install record
  local boot_md=""
  if [ -f "$install_info" ]; then
    boot_md=$(jq -r '.bootMdPath // ""' "$install_info" 2>/dev/null)
  fi

  # Fallback to default path if not found
  if [ -z "$boot_md" ]; then
    boot_md="$HOME/.openclaw/workspace/BOOT.md"
    log_info "No install record found, using default BOOT.md path: $boot_md"
  else
    log_info "Found BOOT.md path from install record: $boot_md"
  fi

  # Step 2: Clean BOOT.md
  if [ -f "$boot_md" ]; then
    # Check if our markers exist
    if grep -q "<!-- daily-greeting:start -->" "$boot_md" && grep -q "<!-- daily-greeting:end -->" "$boot_md"; then
      # Verify the content between markers matches expected pattern
      local marker_content=$(sed -n '/<!-- daily-greeting:start -->/,/<!-- daily-greeting:end -->/p' "$boot_md")

      if echo "$marker_content" | grep -q "bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run"; then
        log_info "Found daily-greeting entry in BOOT.md, removing..."
        # Use sed to remove only the marked content (including the markers)
        sed_i '/<!-- daily-greeting:start -->/,/<!-- daily-greeting:end -->/d' "$boot_md"
        log_info "Removed daily-greeting entry from BOOT.md"
      else
        log_error "Marker found but content mismatch, aborting BOOT.md modification"
      fi
    else
      log_info "No daily-greeting entry found in BOOT.md"
    fi
  else
    log_info "BOOT.md not found at: $boot_md, skipping"
  fi

  # Step 3: Remove OpenClaw cron job
  if openclaw cron list 2>/dev/null | grep -q "daily-greeting"; then
    log_info "Removing OpenClaw cron job..."
    openclaw cron remove --id daily-greeting 2>/dev/null || true
    log_info "OpenClaw cron job removed"
  else
    log_info "No OpenClaw cron job found"
  fi

  # Step 4: Remove skill directory
  if [ -d "$SKILL_DIR" ]; then
    log_info "Removing skill directory: $SKILL_DIR"
    rm -rf "$SKILL_DIR"
    log_info "Skill directory removed"
  else
    log_info "Skill directory not found: $SKILL_DIR"
  fi

  log_info "Uninstall completed!"
  log_info "Note: You may need to manually restart OpenClaw Gateway"
}

# Main entry
case "${1:-run}" in
  run)
    run_greeting
    ;;
  status)
    show_status
    ;;
  reset)
    reset_status
    ;;
  install)
    record_install "${2:-}"
    ;;
  cron)
    install_cron "${2:-}"
    ;;
  uninstall)
    uninstall_skill
    ;;
  help|--help|-h)
    echo "Daily Greeting Skill"
    echo ""
    echo "Usage: daily-greeting [command]"
    echo ""
    echo "Commands:"
    echo "  run        - Execute greeting (default)"
    echo "  status     - View execution status"
    echo "  reset      - Reset state"
    echo "  install    - Record BOOT.md path"
    echo "  cron       - Install cron job (default: 9am weekdays)"
    echo "  uninstall  - Remove skill and clean BOOT.md"
    echo "  uninstall  - Remove skill and clean BOOT.md"
    echo "  help       - Show help"
    echo ""
    echo "Config file: $CONFIG_FILE"
    ;;
  *)
    echo "Unknown command: $1"
    exit 1
    ;;
esac