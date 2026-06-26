#!/bin/bash
# DataGuard DLP — Emergency Override
# Copyright (c) 2026 Jeff Cyprien. Licensed under MIT.
# https://github.com/jeffcGit/dataguard-dlp
#
# Creates a time-limited override window for approved data transfers.
# All overrides are audit-logged with reason and expiry.
#
# SECURITY: This script is intentionally restrictive.
# - Override lasts max 5 minutes
# - Must provide a reason (logged)
# - Auto-expires regardless
# - All override activity is recorded
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OVERRIDE_FILE="$SKILL_DIR/context/override-active"
AUDIT_LOG="$SKILL_DIR/scripts/audit-log.sh"
MAX_DURATION_MINUTES=5

usage() {
  cat <<EOF
DataGuard Emergency Override

Usage:
  $0 --activate <reason>   Activate override (max ${MAX_DURATION_MINUTES} min)
  $0 --check               Check if override is active
  $0 --revoke              Revoke active override

IMPORTANT: Overrides are audit-logged and auto-expire.
Provide a clear reason — this will be recorded.

EOF
  exit 0
}

activate() {
  local reason="$1"
  
  if [ -z "$reason" ]; then
    echo "❌ ERROR: Reason is required for override activation"
    echo "Usage: $0 --activate \"<reason>\""
    exit 1
  fi
  
  # Check if already active (and not expired)
  if [ -f "$OVERRIDE_FILE" ]; then
    local stored_expiry=$(sed -n 's/^expiry_epoch=\([0-9]*\)/\1/p' "$OVERRIDE_FILE" 2>/dev/null || echo "0")
    local now_epoch=$(date -u +%s)
    if [ -n "$stored_expiry" ] && [ "$stored_expiry" -gt "$now_epoch" ] 2>/dev/null; then
      local expiry_iso=$(sed -n 's/^expiry=\(.*\)/\1/p' "$OVERRIDE_FILE" 2>/dev/null || echo "unknown")
      echo "⚠️  Override already active (expires: $expiry_iso)"
      echo "Revoke first if you need a new override."
      exit 1
    else
      # Expired — clean up before reactivating
      rm -f "$OVERRIDE_FILE"
    fi
  fi
  
  # Calculate expiry time
  local now_epoch=$(date -u +%s)
  local expiry_epoch=$((now_epoch + MAX_DURATION_MINUTES * 60))
  local expiry_iso=$(date -u -d "@$expiry_epoch" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -r "$expiry_epoch" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "unknown")
  local activated_iso=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  
  # Write override file — simple key=value format for reliable parsing
  cat > "$OVERRIDE_FILE" <<EOF
activated=$activated_iso
expiry=$expiry_iso
expiry_epoch=$expiry_epoch
reason=$reason
activated_by=manual
EOF
  
  # Restrict permissions
  chmod 600 "$OVERRIDE_FILE"
  
  # Audit log the override
  "$AUDIT_LOG" --log-approve "override" "dataguard" "EMERGENCY_OVERRIDE" "0" "$reason" 2>/dev/null || true
  
  echo "⚠️  OVERRIDE ACTIVATED"
  echo "Duration: $MAX_DURATION_MINUTES minutes"
  echo "Expires: $expiry_iso"
  echo "Reason: $reason"
  echo ""
  echo "All data transfers during this window are audit-logged."
}

check() {
  if [ ! -f "$OVERRIDE_FILE" ]; then
    echo "INACTIVE"
    return 1
  fi
  
  # Read expiry_epoch from simple key=value format
  local stored_expiry=$(sed -n 's/^expiry_epoch=\([0-9]*\)/\1/p' "$OVERRIDE_FILE" 2>/dev/null || echo "0")
  local now_epoch=$(date -u +%s)
  
  if [ -z "$stored_expiry" ] || [ "$stored_expiry" = "0" ]; then
    rm -f "$OVERRIDE_FILE"
    echo "INACTIVE"
    return 1
  fi
  
  if [ "$now_epoch" -ge "$stored_expiry" ] 2>/dev/null; then
    # Expired — clean up
    rm -f "$OVERRIDE_FILE"
    echo "EXPIRED"
    return 1
  fi
  
  local reason=$(sed -n 's/^reason=\(.*\)/\1/p' "$OVERRIDE_FILE" 2>/dev/null || echo "unknown")
  local expiry=$(sed -n 's/^expiry=\(.*\)/\1/p' "$OVERRIDE_FILE" 2>/dev/null || echo "unknown")
  
  echo "ACTIVE"
  echo "Reason: $reason"
  echo "Expires: $expiry"
  return 0
}

revoke() {
  if [ ! -f "$OVERRIDE_FILE" ]; then
    echo "No active override to revoke."
    return 0
  fi
  
  local reason=$(sed -n 's/^reason=\(.*\)/\1/p' "$OVERRIDE_FILE" 2>/dev/null || echo "unknown")
  
  rm -f "$OVERRIDE_FILE"
  
  # Audit log the revocation
  "$AUDIT_LOG" --log-approve "override" "dataguard" "OVERRIDE_REVOKED" "0" "revoked: was '$reason'" 2>/dev/null || true
  
  echo "✅ Override revoked"
}

case "${1:-}" in
  --activate) activate "${2:-}" ;;
  --check) check ;;
  --revoke) revoke ;;
  *) usage ;;
esac