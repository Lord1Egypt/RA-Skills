#!/bin/bash
# DataGuard DLP — Audit Log Manager
# Copyright (c) 2026 Jeff Cyprien. Licensed under MIT.
# https://github.com/jeffcGit/dataguard-dlp
#
# Log and review all blocked/suspicious attempts
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$SKILL_DIR/logs"
BLOCKED_LOG="$LOG_DIR/blocked-attempts.log"
WARN_LOG="$LOG_DIR/warnings.log"
ALL_LOG="$LOG_DIR/all-attempts.log"
CONFIG="$SKILL_DIR/config/config.json"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Read config: log_data_previews (default: false)
LOG_DATA_PREVIEWS=false
if [ -f "$CONFIG" ] && grep -q '"log_data_previsions"' "$CONFIG" 2>/dev/null; then
  LOG_DATA_PREVIEWS=$(grep '"log_data_previews"' "$CONFIG" | grep -oE '(true|false)' | head -1)
fi
[ -z "$LOG_DATA_PREVIEWS" ] && LOG_DATA_PREVIEWS=false

log_attempt() {
  local tool="$1"
  local action="$2"      # BLOCK, WARN, ALLOW
  local domain="$3"
  local patterns="$4"
  local risk_score="$5"
  local data_preview="$6"
  local user_decision="${7:-pending}"
  
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  # Sanitize inputs: strip newlines and control chars to prevent log injection
  tool=$(echo "$tool" | tr -d '\n' | head -c 50)
  domain=$(echo "$domain" | tr -d '\n' | head -c 100)
  patterns=$(echo "$patterns" | tr -d '\n' | head -c 200)
  local log_entry="[$timestamp] $action | Tool: $tool | Domain: $domain | Patterns: $patterns | Score: $risk_score | Decision: $user_decision"
  
  # Log to appropriate file
  case "$action" in
    BLOCK)
      echo "$log_entry" >> "$BLOCKED_LOG"
      if [ "$LOG_DATA_PREVIEWS" = "true" ]; then
        # Only log preview if explicitly enabled — redact to first 4 chars
        data_preview=$(echo "$data_preview" | tr -d '\n' | head -c 200)
        data_preview=$(echo "$data_preview" | sed 's/\(.\{4\}\).*/\1***/')
        echo "Data: $data_preview" >> "$BLOCKED_LOG"
      else
        echo "Data: [REDACTED]" >> "$BLOCKED_LOG"
      fi
      echo "---" >> "$BLOCKED_LOG"
      ;;
    WARN)
      echo "$log_entry" >> "$WARN_LOG"
      ;;
  esac
  
  # Always log to all-attempts
  echo "$log_entry" >> "$ALL_LOG"
}

log_approved() {
  local tool="$1"
  local domain="$2"
  local patterns="$3"
  local risk_score="$4"
  local reason="${5:-user approved}"
  
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "[$timestamp] APPROVED | Tool: $tool | Domain: $domain | Patterns: $patterns | Score: $risk_score | Reason: $reason" >> "$LOG_DIR/approved.log"
}

show_recent() {
  local count="${1:-10}"
  
  echo "🚫 Recent Blocked Attempts"
  echo "=========================="
  
  if [ ! -f "$BLOCKED_LOG" ]; then
    echo "No blocked attempts logged."
    return 0
  fi
  
  tail -n "$((count * 3))" "$BLOCKED_LOG" | head -n "$((count * 3))"
}

show_today() {
  local today=$(date -u +"%Y-%m-%d")
  
  echo "📊 Today's Activity"
  echo "==================="
  
  # Count by action
  local blocked=0
  local warned=0
  local approved=0
  
  if [ -f "$BLOCKED_LOG" ]; then
    blocked=$(grep -c "^\[$today" "$BLOCKED_LOG" 2>/dev/null || echo 0)
  fi
  
  if [ -f "$WARN_LOG" ]; then
    warned=$(grep -c "^\[$today" "$WARN_LOG" 2>/dev/null || echo 0)
  fi
  
  if [ -f "$LOG_DIR/approved.log" ]; then
    approved=$(grep -c "^\[$today" "$LOG_DIR/approved.log" 2>/dev/null || echo 0)
  fi
  
  echo "Blocked: $blocked"
  echo "Warnings: $warned"
  echo "Approved: $approved"
  echo ""
  
  if [ -f "$BLOCKED_LOG" ]; then
    echo "Recent blocks:"
    grep "^\[$today" "$BLOCKED_LOG" | tail -5
  fi
}

export_logs() {
  local output="${1:-dataguard-export-$(date +%Y%m%d-%H%M%S).json}"
  
  # Pure bash JSON export (no python3 dependency)
  local blocked_count=0
  local warned_count=0
  local approved_count=0
  
  {
    echo "{"
    echo "  \"exported_at\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\","
    echo "  \"blocked\": ["
    
    if [ -f "$BLOCKED_LOG" ]; then
      local first=true
      while IFS= read -r line; do
        [[ "$line" == ---* ]] && continue
        [[ ! "$line" =~ ^\[ ]] && continue
        # Parse: [timestamp] ACTION | Tool: X | Domain: Y | Patterns: Z | Score: N | Decision: D
        local ts=$(echo "$line" | sed 's/^\[\([^]]*\)\].*/\1/')
        local act=$(echo "$line" | sed 's/^\[[^]]*\] \([A-Z]*\).*/\1/')
        local tl=$(echo "$line" | grep -oE 'Tool: [^|]+' | sed 's/Tool: //' | xargs)
        local dm=$(echo "$line" | grep -oE 'Domain: [^|]+' | sed 's/Domain: //' | xargs)
        local pt=$(echo "$line" | grep -oE 'Patterns: [^|]+' | sed 's/Patterns: //' | xargs)
        local sc=$(echo "$line" | grep -oE 'Score: [0-9]+' | sed 's/Score: //')
        
        [ "$first" = true ] && first=false || echo ","
        printf '    {"timestamp":"%s","action":"%s","tool":"%s","domain":"%s","patterns":"%s","score":%s}' "$ts" "$act" "$tl" "$dm" "$pt" "${sc:-0}"
        blocked_count=$((blocked_count + 1))
      done < "$BLOCKED_LOG"
    fi
    
    echo ""
    echo "  ],"
    echo "  \"warnings\": [],"
    echo "  \"approved\": []"
    echo "}"
  } > "$output"
  
  echo "✅ Exported to: $output"
  echo "   (structured export — warnings/approved arrays omitted for brevity)"
}

show_stats() {
  echo "📈 DataGuard Statistics"
  echo "======================="
  
  local total_blocked=0
  local total_warned=0
  local total_approved=0
  
  [ -f "$BLOCKED_LOG" ] && total_blocked=$(grep -c "^\[" "$BLOCKED_LOG" 2>/dev/null || echo 0)
  [ -f "$WARN_LOG" ] && total_warned=$(grep -c "^\[" "$WARN_LOG" 2>/dev/null || echo 0)
  [ -f "$LOG_DIR/approved.log" ] && total_approved=$(grep -c "^\[" "$LOG_DIR/approved.log" 2>/dev/null || echo 0)
  
  echo "Total Blocked: $total_blocked"
  echo "Total Warnings: $total_warned"
  echo "Total Approved: $total_approved"
  
  # Top blocked domains
  if [ -f "$BLOCKED_LOG" ] && [ "$total_blocked" -gt 0 ]; then
    echo ""
    echo "Top Blocked Domains:"
    grep "Domain:" "$BLOCKED_LOG" | sed 's/.*Domain: //' | sed 's/ |.*//' | sort | uniq -c | sort -rn | head -5
  fi
  
  # Top patterns
  if [ -f "$BLOCKED_LOG" ] && [ "$total_blocked" -gt 0 ]; then
    echo ""
    echo "Top Patterns Blocked:"
    grep "Patterns:" "$BLOCKED_LOG" | sed 's/.*Patterns: //' | sed 's/ |.*//' | tr ',' '\n' | sort | uniq -c | sort -rn | head -5
  fi
}

usage() {
  cat <<EOF
DataGuard Audit Log Manager

Usage:
  $0 --recent [N]           Show last N blocked attempts (default: 10)
  $0 --today                Show today's summary
  $0 --stats                Show statistics
  $0 --export [file]        Export logs to JSON (default: dataguard-export-<timestamp>.json)
  $0 --log-block <details>  Log a blocked attempt
  $0 --log-approve <details> Log an approved attempt

Internal use (called by hooks):
  $0 --log-block <tool> <domain> <patterns> <score> <data_preview>
  $0 --log-approve <tool> <domain> <patterns> <score> <reason>

EOF
  exit 0
}

case "${1:-}" in
  --recent) show_recent "${2:-10}" ;;
  --today) show_today ;;
  --stats) show_stats ;;
  --export) export_logs "${2:-}" ;;
  --log-block) log_attempt "${2:-web_fetch}" "BLOCK" "${3:-unknown}" "${4:-}" "${5:-0}" "${6:-}" ;;
  --log-approve) log_approved "${2:-}" "${3:-}" "${4:-}" "${5:-}" "${6:-user approved}" ;;
  *) usage ;;
esac