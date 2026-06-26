#!/usr/bin/env bash
# guardian.sh — OpenClaw Gateway Watchdog
# Monitors the OpenClaw gateway process, attempts graduated repairs,
# sends alerts via Telegram and/or Discord, and commits daily snapshots.
#
# Usage: guardian.sh [--config /path/to/config.env]
# All configuration via environment variables (see SKILL.md).

# Note: -e intentionally omitted — daemon must survive unexpected non-zero exits
set -uo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION — all overridable via environment
# ─────────────────────────────────────────────────────────────────────────────

GUARDIAN_CHECK_INTERVAL="${GUARDIAN_CHECK_INTERVAL:-30}"
GUARDIAN_MAX_REPAIR="${GUARDIAN_MAX_REPAIR:-3}"
GUARDIAN_COOLDOWN="${GUARDIAN_COOLDOWN:-600}"
GUARDIAN_ENABLE_ROLLBACK="${GUARDIAN_ENABLE_ROLLBACK:-false}"
GUARDIAN_LOG="${GUARDIAN_LOG:-/tmp/openclaw-guardian.log}"
GUARDIAN_WORKSPACE="${GUARDIAN_WORKSPACE:-$HOME/.openclaw/workspace}"
GUARDIAN_TELEGRAM_BOT_TOKEN="${GUARDIAN_TELEGRAM_BOT_TOKEN:-}"
GUARDIAN_TELEGRAM_CHAT_ID="${GUARDIAN_TELEGRAM_CHAT_ID:-}"
GUARDIAN_DISCORD_WEBHOOK_URL="${GUARDIAN_DISCORD_WEBHOOK_URL:-}"
OPENCLAW_PORT="${OPENCLAW_PORT:-}"

# Optional config file override (first argument)
if [[ "${1:-}" == "--config" && -n "${2:-}" ]]; then
  # shellcheck source=/dev/null
  source "$2"
fi

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

readonly LOCKFILE="/tmp/openclaw-guardian.lock"
readonly SNAPSHOT_DATE_FILE="/tmp/openclaw-guardian-last-snapshot"
readonly LOG_MAX_BYTES=1048576  # 1 MB

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────────────────────

# log_rotate — rotate log if it exceeds LOG_MAX_BYTES (keep one backup)
log_rotate() {
  if [[ -f "$GUARDIAN_LOG" ]]; then
    local size
    size=$(wc -c < "$GUARDIAN_LOG" 2>/dev/null || echo 0)
    if (( size > LOG_MAX_BYTES )); then
      mv "$GUARDIAN_LOG" "${GUARDIAN_LOG}.1"
      touch "$GUARDIAN_LOG"
    fi
  fi
}

# log <LEVEL> <message> — write timestamped line to log file and stdout
log() {
  local level="$1"
  shift
  local message="$*"
  local timestamp
  timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  local line="[${timestamp}] [${level}] ${message}"

  echo "$line" | tee -a "$GUARDIAN_LOG"
}

log_info()  { log "INFO"  "$@"; }
log_warn()  { log "WARN"  "$@"; }
log_error() { log "ERROR" "$@"; }

# ─────────────────────────────────────────────────────────────────────────────
# ALERTING
# ─────────────────────────────────────────────────────────────────────────────

# send_telegram <message> — POST to Telegram Bot API
send_telegram() {
  local message="$1"
  if [[ -z "$GUARDIAN_TELEGRAM_BOT_TOKEN" || -z "$GUARDIAN_TELEGRAM_CHAT_ID" ]]; then
    return 0
  fi
  curl -s --max-time 10 \
    -X POST \
    "https://api.telegram.org/bot${GUARDIAN_TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d "chat_id=${GUARDIAN_TELEGRAM_CHAT_ID}" \
    --data-urlencode "text=${message}" \
    -d "parse_mode=Markdown" \
    > /dev/null 2>&1 || log_warn "Telegram alert failed"
}

# send_discord <message> — POST to Discord webhook
send_discord() {
  local message="$1"
  if [[ -z "$GUARDIAN_DISCORD_WEBHOOK_URL" ]]; then
    return 0
  fi
  local payload
  if command -v jq &>/dev/null; then
    payload=$(jq -Rn --arg msg "$message" '{"content": $msg}')
  else
    # Fallback: escape backslashes, quotes, and newlines
    local escaped
    escaped=$(printf '%s' "$message" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr '\n' ' ')
    payload="{\"content\": \"${escaped}\"}"
  fi
  curl -s --max-time 10 \
    -X POST \
    -H "Content-Type: application/json" \
    -d "$payload" \
    "$GUARDIAN_DISCORD_WEBHOOK_URL" \
    > /dev/null 2>&1 || log_warn "Discord alert failed"
}

# alert <message> — send to all configured channels; log-only if none configured
alert() {
  local message="$1"
  log_info "ALERT: ${message}"

  local has_channel=false
  if [[ -n "$GUARDIAN_TELEGRAM_BOT_TOKEN" && -n "$GUARDIAN_TELEGRAM_CHAT_ID" ]]; then
    send_telegram "$(printf '🛡️ *OpenClaw Guardian*\n%s' "$message")"
    has_channel=true
  fi
  if [[ -n "$GUARDIAN_DISCORD_WEBHOOK_URL" ]]; then
    send_discord "🛡️ OpenClaw Guardian | ${message}"
    has_channel=true
  fi

  if [[ "$has_channel" == "false" ]]; then
    log_info "No alert channel configured — log-only mode"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# LOCK FILE MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────

# acquire_lock — write PID to lockfile; exit if another live instance is running
acquire_lock() {
  if [[ -f "$LOCKFILE" ]]; then
    local existing_pid
    existing_pid=$(cat "$LOCKFILE" 2>/dev/null || echo "")
    if [[ -n "$existing_pid" ]] && kill -0 "$existing_pid" 2>/dev/null; then
      echo "Another guardian instance is already running (PID ${existing_pid}). Exiting."
      exit 1
    else
      log_warn "Stale lockfile found (PID ${existing_pid:-unknown}). Removing."
      rm -f "$LOCKFILE"
    fi
  fi
  echo $$ > "$LOCKFILE"
  log_info "Lockfile acquired (PID $$)"
}

# release_lock — remove lockfile on clean exit
release_lock() {
  rm -f "$LOCKFILE"
  log_info "Lockfile released"
}

# ─────────────────────────────────────────────────────────────────────────────
# SIGNAL HANDLING
# ─────────────────────────────────────────────────────────────────────────────

# on_exit — cleanup on any signal or exit
on_exit() {
  alert "Guardian stopping (PID $$)"
  release_lock
}

trap on_exit EXIT
trap 'log_info "Received SIGTERM — shutting down"; exit 0' SIGTERM
trap 'log_info "Received SIGINT — shutting down"; exit 0' SIGINT

# ─────────────────────────────────────────────────────────────────────────────
# HEALTH CHECKING
# ─────────────────────────────────────────────────────────────────────────────

# check_cli_status — use `openclaw gateway status`; returns 0 if healthy
check_cli_status() {
  openclaw gateway status > /dev/null 2>&1
}

# detect_port — parse gateway port from `openclaw gateway status` or use OPENCLAW_PORT
detect_port() {
  if [[ -n "${OPENCLAW_PORT:-}" ]]; then
    echo "$OPENCLAW_PORT"
    return
  fi
  # Parse port from status output (looks for "port=NNNNN")
  local port
  port=$(openclaw gateway status 2>/dev/null | grep -oE 'port=[0-9]+' | head -1 | cut -d= -f2)
  if [[ -n "$port" ]]; then
    echo "$port"
  else
    echo "18789"  # fallback default
  fi
}

# check_http_health — curl the /health endpoint; returns 0 if HTTP 200
check_http_health() {
  local port
  port=$(detect_port)
  local http_code
  http_code=$(curl -s --max-time 5 -o /dev/null -w "%{http_code}" \
    "http://127.0.0.1:${port}/health" 2>/dev/null || echo "000")
  [[ "$http_code" == "200" ]]
}

# is_gateway_healthy — graduated check: CLI first, then HTTP; returns 0 if healthy
is_gateway_healthy() {
  if check_cli_status; then
    return 0
  fi
  log_warn "CLI status check failed — trying HTTP health endpoint"
  if check_http_health; then
    log_warn "CLI check failed but HTTP health OK — treating as degraded-but-alive"
    return 0
  fi
  return 1
}

# ─────────────────────────────────────────────────────────────────────────────
# REPAIR — LEVEL 1: Restart
# ─────────────────────────────────────────────────────────────────────────────

# repair_level1 — `openclaw gateway restart`; returns 0 if gateway recovers
repair_level1() {
  log_info "Repair Level 1: restarting gateway"
  alert "Attempting Level 1 repair: gateway restart"

  if openclaw gateway restart > /dev/null 2>&1; then
    log_info "Gateway restart command succeeded — waiting 30s for stabilisation"
    sleep 30
    if is_gateway_healthy; then
      log_info "Level 1 repair succeeded"
      alert "✅ Level 1 repair succeeded — gateway is back online"
      return 0
    fi
  else
    log_warn "Gateway restart command failed"
  fi

  log_warn "Level 1 repair failed"
  alert "❌ Level 1 repair failed"
  return 1
}

# ─────────────────────────────────────────────────────────────────────────────
# REPAIR — LEVEL 2: Doctor Fix
# ─────────────────────────────────────────────────────────────────────────────

# repair_level2 — `openclaw doctor --fix` then `openclaw gateway start`; returns 0 if OK
repair_level2() {
  log_info "Repair Level 2: running openclaw doctor --fix"
  alert "Attempting Level 2 repair: openclaw doctor --fix"

  openclaw doctor --fix > /dev/null 2>&1 || log_warn "doctor --fix exited non-zero (may still be useful)"
  log_info "Doctor fix done — waiting 15s then starting gateway"
  sleep 15

  if openclaw gateway start > /dev/null 2>&1; then
    log_info "Gateway start command succeeded — waiting 30s for stabilisation"
    sleep 30
    if is_gateway_healthy; then
      log_info "Level 2 repair succeeded"
      alert "✅ Level 2 repair succeeded — gateway is back online"
      return 0
    fi
  else
    log_warn "Gateway start command failed after doctor fix"
  fi

  log_warn "Level 2 repair failed"
  alert "❌ Level 2 repair failed"
  return 1
}

# ─────────────────────────────────────────────────────────────────────────────
# REPAIR — LEVEL 3: Safe Git Rollback (optional, off by default)
# ─────────────────────────────────────────────────────────────────────────────

# find_stable_commit — return the last commit SHA that is NOT an auto-backup or rollback commit
find_stable_commit() {
  cd "$GUARDIAN_WORKSPACE"
  # Skip guardian snapshot commits and any commit with "rollback" in the message
  git log --oneline -50 | grep -v -E "guardian:|rollback|auto-backup" | head -1 | awk '{print $1}'
}

# repair_level3 — stash → reset to stable commit → pop; returns 0 if gateway recovers
repair_level3() {
  if [[ "$GUARDIAN_ENABLE_ROLLBACK" != "true" ]]; then
    log_info "Level 3 rollback disabled (GUARDIAN_ENABLE_ROLLBACK=false)"
    return 1
  fi

  log_warn "Repair Level 3: safe git rollback"
  alert "⚠️ Attempting Level 3 repair: safe git rollback (GUARDIAN_ENABLE_ROLLBACK=true)"

  cd "$GUARDIAN_WORKSPACE"

  # Stash uncommitted work first — NEVER lose user changes
  local stash_result
  stash_result=$(git stash push -m "guardian: pre-rollback stash $(date '+%Y-%m-%d %H:%M:%S')" 2>&1) || true
  local stashed=false
  if echo "$stash_result" | grep -q "Saved working directory"; then
    stashed=true
    log_info "Uncommitted changes stashed: ${stash_result}"
  else
    log_info "Nothing to stash (working tree clean)"
  fi

  local stable_commit
  stable_commit=$(find_stable_commit)
  if [[ -z "$stable_commit" ]]; then
    log_error "Could not find a stable commit to roll back to"
    alert "❌ Level 3 failed: no stable commit found"
    if [[ "$stashed" == "true" ]]; then
      git stash pop 2>/dev/null || log_warn "Failed to pop stash after failed rollback — manual recovery needed"
    fi
    return 1
  fi

  log_info "Rolling back to stable commit: ${stable_commit}"

  if ! git reset --hard "$stable_commit" 2>&1; then
    log_error "git reset --hard failed"
    alert "❌ Level 3 rollback git reset failed"
    if [[ "$stashed" == "true" ]]; then
      git stash pop 2>/dev/null || log_warn "Failed to pop stash — manual recovery needed"
    fi
    return 1
  fi

  # Restore uncommitted work on top of rolled-back state
  if [[ "$stashed" == "true" ]]; then
    if git stash pop 2>/dev/null; then
      log_info "Uncommitted changes restored after rollback"
    else
      log_warn "git stash pop failed after rollback — changes remain in stash"
      alert "⚠️ Rollback completed but stash pop failed — your changes are in git stash"
    fi
  fi

  log_info "Rollback complete — restarting gateway"
  openclaw gateway restart > /dev/null 2>&1 || true
  sleep 30

  if is_gateway_healthy; then
    log_info "Level 3 repair succeeded"
    alert "✅ Level 3 rollback succeeded — gateway is back online (rolled back to ${stable_commit})"
    return 0
  fi

  log_error "Level 3 repair failed — gateway still down after rollback"
  alert "❌ Level 3 rollback failed — manual intervention required"
  return 1
}

# ─────────────────────────────────────────────────────────────────────────────
# DAILY SNAPSHOT
# ─────────────────────────────────────────────────────────────────────────────

# daily_snapshot — commit workspace once per calendar day (respects .gitignore)
daily_snapshot() {
  local today
  today=$(date '+%Y-%m-%d')
  local last_snapshot=""

  if [[ -f "$SNAPSHOT_DATE_FILE" ]]; then
    last_snapshot=$(cat "$SNAPSHOT_DATE_FILE" 2>/dev/null || echo "")
  fi

  if [[ "$last_snapshot" == "$today" ]]; then
    return 0  # Already snapped today
  fi

  if [[ ! -d "$GUARDIAN_WORKSPACE/.git" ]]; then
    log_warn "GUARDIAN_WORKSPACE is not a git repo — skipping snapshot"
    return 0
  fi

  cd "$GUARDIAN_WORKSPACE"

  # git add respects .gitignore automatically — secrets safe if .gitignored
  if git add -A 2>&1 && git diff --cached --quiet; then
    log_info "Daily snapshot: nothing to commit"
    echo "$today" > "$SNAPSHOT_DATE_FILE"
    return 0
  fi

  if git commit -m "guardian: daily snapshot ${today}" > /dev/null 2>&1; then
    log_info "Daily snapshot committed for ${today}"
    echo "$today" > "$SNAPSHOT_DATE_FILE"
  else
    log_warn "Daily snapshot commit failed (may already be clean)"
    echo "$today" > "$SNAPSHOT_DATE_FILE"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# REPAIR ORCHESTRATOR
# ─────────────────────────────────────────────────────────────────────────────

# run_repairs — graduated repair cycle; enters cooldown if all levels fail
run_repairs() {
  local repair_count=0

  alert "🔴 Gateway is DOWN — beginning repair sequence"

  while (( repair_count < GUARDIAN_MAX_REPAIR )); do
    repair_count=$((repair_count + 1))
    log_info "Repair attempt ${repair_count}/${GUARDIAN_MAX_REPAIR}"

    if repair_level1; then
      return 0
    fi

    if repair_level2; then
      return 0
    fi
  done

  # All Level 1+2 attempts exhausted
  if [[ "$GUARDIAN_ENABLE_ROLLBACK" == "true" ]]; then
    if repair_level3; then
      return 0
    fi
  fi

  log_error "All repair attempts exhausted — entering cooldown (${GUARDIAN_COOLDOWN}s)"
  alert "🚨 All repair attempts FAILED. Entering ${GUARDIAN_COOLDOWN}s cooldown. Manual intervention may be required."
  sleep "$GUARDIAN_COOLDOWN"
  log_info "Cooldown complete — resuming monitoring"
}

# ─────────────────────────────────────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────────────────────────────────────

main() {
  acquire_lock

  log_info "OpenClaw Guardian started (PID $$)"
  log_info "Config: interval=${GUARDIAN_CHECK_INTERVAL}s, max_repair=${GUARDIAN_MAX_REPAIR}, cooldown=${GUARDIAN_COOLDOWN}s, rollback=${GUARDIAN_ENABLE_ROLLBACK}"
  log_info "Workspace: ${GUARDIAN_WORKSPACE}"
  log_info "Health endpoint: http://127.0.0.1:$(detect_port)/health"

  alert "🟢 Guardian started (PID $$) — monitoring every ${GUARDIAN_CHECK_INTERVAL}s"

  local was_down=false

  while true; do
    # Rotate log if needed (once per loop iteration, not on every log() call)
    log_rotate

    # Run daily snapshot (no-op if already done today)
    daily_snapshot

    if is_gateway_healthy; then
      if [[ "$was_down" == "true" ]]; then
        log_info "Gateway has recovered — resuming normal monitoring"
        was_down=false
      else
        log_info "Gateway healthy"
      fi
    else
      log_warn "Gateway health check FAILED"
      was_down=true
      run_repairs
    fi

    sleep "$GUARDIAN_CHECK_INTERVAL"
  done
}

main "$@"
