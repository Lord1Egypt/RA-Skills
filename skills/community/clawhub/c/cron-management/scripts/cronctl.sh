#!/bin/bash
# cronctl.sh — OpenClaw Cron Job Manager
# Usage: cronctl <command> [args]

set -euo pipefail

JOB_NAME="${2:-}"

# Colors for output (disabled if not tty)
if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BLUE='\033[0;34m'
  NC='\033[0m' # No Color
else
  RED='' GREEN='' YELLOW='' BLUE='' NC=''
fi

# ─── Helpers ─────────────────────────────────────────────────────────

die() { echo -e "${RED}Error: $1${NC}" >&2; exit 1; }
info() { echo -e "${BLUE}$1${NC}"; }
success() { echo -e "${GREEN}$1${NC}"; }
warn() { echo -e "${YELLOW}$1${NC}"; }

# Fetch all jobs as JSON
fetch_jobs() {
  local json
  json=$(openclaw cron list --json 2>/dev/null)
  if [ -z "$json" ] || [[ "$json" != \{* ]]; then
    die "Failed to fetch cron jobs. Is OpenClaw running?"
  fi
  echo "$json"
}

# Get job ID from name (fuzzy match)
get_job_id() {
  local name="$1"
  local id
  id=$(fetch_jobs | jq -r --arg name "$name" '
    .jobs[] | select(.name | test($name; "i")) | .id
  ' | head -1)
  if [ -z "$id" ]; then
    die "No job found matching '$name'"
  fi
  echo "$id"
}

# ─── Commands ────────────────────────────────────────────────────────

cmd_list() {
  local jobs_json
  jobs_json=$(fetch_jobs)

  echo -e "${BLUE}Cron Jobs:${NC}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "$jobs_json" | jq -r '.jobs[] |
    (if .enabled then "✅" else "❌" end) as $status |
    (if .state.lastRunStatus == "error" then " 🔥" elif .state.lastRunStatus == "skipped" then " ⏸️" else "" end) as $alert |
    "\($status)\($alert) \(.name)"
  '

  local total enabled disabled
  total=$(echo "$jobs_json" | jq '.jobs | length')
  enabled=$(echo "$jobs_json" | jq '[.jobs[] | select(.enabled)] | length')
  disabled=$(echo "$jobs_json" | jq '[.jobs[] | select(.enabled | not)] | length')

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo -e "Total: $total | ${GREEN}Enabled: $enabled${NC} | ${RED}Disabled: $disabled${NC}"

  if [ -f /tmp/cron-paused ]; then
    warn "⚠️  MAINTENANCE MODE ACTIVE (since $(cat /tmp/cron-paused))"
  fi
}

cmd_show() {
  [ -z "$JOB_NAME" ] && die "Usage: cronctl show <job-name>"
  local id
  id=$(get_job_id "$JOB_NAME")
  openclaw cron get "$id" --json | jq .
}

cmd_pause() {
  [ -z "$JOB_NAME" ] && die "Usage: cronctl pause <job-name>"
  local id
  id=$(get_job_id "$JOB_NAME")
  info "Pausing '$JOB_NAME' ($id)..."
  openclaw cron update "$id" '{"enabled": false}'
  success "Paused '$JOB_NAME'"
}

cmd_resume() {
  [ -z "$JOB_NAME" ] && die "Usage: cronctl resume <job-name>"
  local id
  id=$(get_job_id "$JOB_NAME")
  info "Resuming '$JOB_NAME' ($id)..."
  openclaw cron update "$id" '{"enabled": true}'
  success "Resumed '$JOB_NAME'"
}

cmd_pause_all() {
  info "Pausing all cron jobs..."
  local jobs_json
  jobs_json=$(fetch_jobs)
  local count
  count=$(echo "$jobs_json" | jq '[.jobs[] | select(.enabled)] | length')

  echo "$jobs_json" | jq -r '.jobs[] | select(.enabled) | .id' | while read -r id; do
    openclaw cron update "$id" '{"enabled": false}' 2>/dev/null || true
  done

  success "Paused $count jobs"
}

cmd_resume_all() {
  info "Resuming all cron jobs..."
  local jobs_json
  jobs_json=$(fetch_jobs)
  local count
  count=$(echo "$jobs_json" | jq '[.jobs[] | select(.enabled | not)] | length')

  echo "$jobs_json" | jq -r '.jobs[] | select(.enabled | not) | .id' | while read -r id; do
    openclaw cron update "$id" '{"enabled": true}' 2>/dev/null || true
  done

  success "Resumed $count jobs"
}

cmd_maintenance() {
  case "${JOB_NAME:-}" in
    on)
      date -Iseconds > /tmp/cron-paused
      success "Maintenance mode ENABLED — all jobs will skip on next run"
      ;;
    off)
      if [ -f /tmp/cron-paused ]; then
        rm /tmp/cron-paused
        success "Maintenance mode DISABLED — jobs will run normally"
      else
        warn "Maintenance mode was not active"
      fi
      ;;
    *)
      if [ -f /tmp/cron-paused ]; then
        warn "Maintenance mode is ACTIVE (since $(cat /tmp/cron-paused))"
      else
        info "Maintenance mode is inactive"
      fi
      ;;
  esac
}

cmd_status() {
  local jobs_json
  jobs_json=$(fetch_jobs)

  local total enabled disabled failing skipped
  total=$(echo "$jobs_json" | jq '.jobs | length')
  enabled=$(echo "$jobs_json" | jq '[.jobs[] | select(.enabled)] | length')
  disabled=$(echo "$jobs_json" | jq '[.jobs[] | select(.enabled | not)] | length')
  failing=$(echo "$jobs_json" | jq '[.jobs[] | select(.state.consecutiveErrors > 0)] | length')
  skipped=$(echo "$jobs_json" | jq '[.jobs[] | select(.state.consecutiveSkipped > 5)] | length')

  echo -e "${BLUE}Cron Health Dashboard${NC}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo -e "Total jobs:     $total"
  echo -e "Enabled:        ${GREEN}$enabled${NC}"
  echo -e "Disabled:       ${RED}$disabled${NC}"
  echo -e "Failing (now):  ${RED}$failing${NC}"
  echo -e "Skipped >5x:    ${YELLOW}$skipped${NC}"

  if [ "$failing" -gt 0 ]; then
    echo ""
    warn "Failing jobs:"
    echo "$jobs_json" | jq -r '.jobs[] | select(.state.consecutiveErrors > 0) |
      "  🔥 \(.name) — \(.state.consecutiveErrors) consecutive errors (last: \(.state.lastError // "unknown"))"
    '
  fi

  if [ "$disabled" -gt 0 ]; then
    echo ""
    warn "Disabled jobs:"
    echo "$jobs_json" | jq -r '.jobs[] | select(.enabled | not) |
      "  ❌ \(.name)"
    '
  fi

  if [ -f /tmp/cron-paused ]; then
    echo ""
    warn "⚠️  MAINTENANCE MODE ACTIVE since $(cat /tmp/cron-paused)"
  fi
}

cmd_health() {
  [ -z "$JOB_NAME" ] && die "Usage: cronctl health <job-name>"
  local id
  id=$(get_job_id "$JOB_NAME")
  local job_json
  job_json=$(openclaw cron get "$id" --json 2>/dev/null)

  if [ -z "$job_json" ] || [[ "$job_json" != \{* ]]; then
    die "Failed to get job details"
  fi

  echo -e "${BLUE}Health: $JOB_NAME${NC}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "$job_json" | jq -r '
    "Status: \(.enabled | if . then "✅ Enabled" else "❌ Disabled" end)",
    "Last run: \(.state.lastRunAtMs // 0 | todate)",
    "Last status: \(.state.lastRunStatus // "never run")",
    "Consecutive errors: \(.state.consecutiveErrors // 0)",
    "Consecutive skipped: \(.state.consecutiveSkipped // 0)",
    "Next run: \(.state.nextRunAtMs // 0 | todate)",
    "",
    "Last error: \(.state.lastError // "none")"
  '
}

cmd_help() {
  cat << 'EOF'
Usage: cronctl <command> [args]

Commands:
  list                    List all jobs with status
  show <name>            Show detailed job info
  pause <name>           Disable a single job
  resume <name>          Re-enable a single job
  pause-all              Disable ALL jobs
  resume-all             Re-enable ALL jobs
  maintenance [on|off]   Toggle maintenance mode (or show status)
  status                 Health dashboard
  health <name>          Show run history and diagnostics
  help                   Show this help

Examples:
  cronctl status                    # Quick overview
  cronctl pause cloudy-blog-writer  # Pause one job
  cronctl maintenance on            # Emergency stop
  cronctl health beads-executor     # Check failures
EOF
}

# ─── Main ────────────────────────────────────────────────────────────

COMMAND="${1:-help}"

case "$COMMAND" in
  list)           cmd_list ;;
  show)           cmd_show ;;
  pause)          cmd_pause ;;
  resume)         cmd_resume ;;
  pause-all)      cmd_pause_all ;;
  resume-all)     cmd_resume_all ;;
  maintenance)    cmd_maintenance ;;
  status)         cmd_status ;;
  health)         cmd_health ;;
  help|--help|-h) cmd_help ;;
  *)              die "Unknown command: $COMMAND. Run 'cronctl help' for usage." ;;
esac
