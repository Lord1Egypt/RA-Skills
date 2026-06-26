#!/bin/bash
# DataGuard DLP — Domain Allowlist Manager
# Copyright (c) 2026 Jeff Cyprien. Licensed under MIT.
# https://github.com/jeffcGit/dataguard-dlp
#
# Manage approved domains for outbound data transfer
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
ALLOWLIST="$SKILL_DIR/config/domain-allowlist.txt"
BLOCKLIST="$SKILL_DIR/config/domain-blocklist.txt"

# Ensure files exist
mkdir -p "$SKILL_DIR/config"
touch "$ALLOWLIST" "$BLOCKLIST"

# Default allowed domains (built-in)
DEFAULT_ALLOWED=(
  "api.openai.com"
  "api.anthropic.com"
  "api.brave.com"
  "search.brave.com"
  "docs.openclaw.ai"
  "clawhub.ai"
  "github.com"
  "api.github.com"
  "raw.githubusercontent.com"
  "npmjs.com"
  "registry.npmjs.org"
)

# Default blocked domains (high risk)
DEFAULT_BLOCKED=(
  "pastebin.com"
  "hastebin.com"
  "transfer.sh"
  "0x0.st"
  "webhook.site"
  "requestbin.net"
  "pipedream.com"
  "temp-mail.org"
  "guerrillamail.com"
  "10minutemail.com"
)

usage() {
  cat <<EOF
DataGuard Domain Allowlist Manager

Usage:
  $0 --list              List allowed domains
  $0 --blocked            List blocked domains
  $0 --check <domain>     Check if domain is allowed
  $0 --add <domain>       Add domain to allowlist (requires approval)
  $0 --remove <domain>    Remove domain from allowlist
  $0 --init               Initialize with defaults

EOF
  exit 0
}

list_allowed() {
  echo "✅ ALLOWED DOMAINS"
  echo "=================="
  echo ""
  echo "Built-in defaults:"
  for d in "${DEFAULT_ALLOWED[@]}"; do
    echo "  $d"
  done
  echo ""
  echo "User-added:"
  if [ -s "$ALLOWLIST" ]; then
    cat "$ALLOWLIST" | sort -u
  else
    echo "  (none)"
  fi
}

list_blocked() {
  echo "🚫 BLOCKED DOMAINS"
  echo "=================="
  echo ""
  echo "Built-in defaults:"
  for d in "${DEFAULT_BLOCKED[@]}"; do
    echo "  $d"
  done
  echo ""
  echo "User-added:"
  if [ -s "$BLOCKLIST" ]; then
    cat "$BLOCKLIST" | sort -u
  else
    echo "  (none)"
  fi
}

check_domain() {
  local domain="$1"
  
  # Check if in default allowed
  for d in "${DEFAULT_ALLOWED[@]}"; do
    if [ "$domain" = "$d" ] || [[ "$domain" == *".$d" ]]; then
      echo "✅ ALLOWED (default): $domain"
      return 0
    fi
  done
  
  # Check if in user allowlist
  if grep -qxF "$domain" "$ALLOWLIST" 2>/dev/null; then
    echo "✅ ALLOWED (user): $domain"
    return 0
  fi
  
  # Check if in default blocked
  for d in "${DEFAULT_BLOCKED[@]}"; do
    if [ "$domain" = "$d" ] || [[ "$domain" == *".$d" ]]; then
      echo "🚫 BLOCKED (high risk): $domain"
      return 1
    fi
  done
  
  # Check if in user blocklist
  if grep -qxF "$domain" "$BLOCKLIST" 2>/dev/null; then
    echo "🚫 BLOCKED (user): $domain"
    return 1
  fi
  
  # Unknown domain
  echo "⚠️  UNKNOWN: $domain"
  echo "   This domain is not in allowlist or blocklist."
  echo "   Requires user approval for data transfer."
  return 2
}

add_domain() {
  local domain="$1"
  
  # Validate domain format
  if ! echo "$domain" | grep -qE '^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*$'; then
    echo "❌ Invalid domain format: $domain"
    exit 1
  fi
  
  # Check if already allowed
  for d in "${DEFAULT_ALLOWED[@]}"; do
    if [ "$domain" = "$d" ]; then
      echo "✅ Already allowed (built-in): $domain"
      return 0
    fi
  done
  
  if grep -qxF "$domain" "$ALLOWLIST" 2>/dev/null; then
    echo "✅ Already allowed: $domain"
    return 0
  fi
  
  echo "$domain" >> "$ALLOWLIST"
  sort -u "$ALLOWLIST" -o "$ALLOWLIST"
  echo "✅ Added to allowlist: $domain"
  echo ""
  echo "⚠️  NOTE: This domain is now allowed for all outbound data."
  echo "   Make sure you trust this domain."
}

remove_domain() {
  local domain="$1"
  
  # Check if in user allowlist
  if ! grep -qxF "$domain" "$ALLOWLIST" 2>/dev/null; then
    echo "❌ Domain not in user allowlist: $domain"
    exit 1
  fi
  
  # Remove domain
  grep -vxF "$domain" "$ALLOWLIST" > "$ALLOWLIST.tmp" 2>/dev/null || true
  mv "$ALLOWLIST.tmp" "$ALLOWLIST" 2>/dev/null || true
  
  echo "✅ Removed from allowlist: $domain"
}

init_defaults() {
  echo "Initializing DataGuard domain lists..."
  
  # Create config directory
  mkdir -p "$SKILL_DIR/config"
  
  # Initialize empty allowlist (defaults are hardcoded)
  touch "$ALLOWLIST"
  
  # Initialize empty blocklist (defaults are hardcoded)
  touch "$BLOCKLIST"
  
  echo "✅ Initialized with default domains"
  echo ""
  list_allowed
}

# Main
case "${1:-}" in
  --list) list_allowed ;;
  --blocked) list_blocked ;;
  --check) check_domain "${2:-}" ;;
  --add) add_domain "${2:-}" ;;
  --remove) remove_domain "${2:-}" ;;
  --init) init_defaults ;;
  *) usage ;;
esac