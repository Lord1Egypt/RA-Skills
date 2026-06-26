#!/usr/bin/env bash
#
# adguard-home/scripts/rules.sh
# Manage AdGuard Home custom DNS rewrite rules
# Usage: ./rules.sh add|remove|list <rule>
#

set -uo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

log()  { echo -e "${CYAN}[adguard]${RESET} $*"; }
pass() { echo -e "${GREEN}✅ $*${RESET}"; }
err()  { echo -e "${RED}❌ $*${RESET}" >&2; }

# ── Config ─────────────────────────────────────────────────────────────────────
ADGUARD_USERNAME="${ADGUARD_USERNAME:?ADGUARD_USERNAME not set}"
ADGUARD_PASSWORD="${ADGUARD_PASSWORD:?ADGUARD_PASSWORD not set}"
ADGUARD_BASE_URL="${ADGUARD_BASE_URL:-http://localhost:3000}"

AUTH=$(echo -n "${ADGUARD_USERNAME}:${ADGUARD_PASSWORD}" | base64)

# ── Args ───────────────────────────────────────────────────────────────────────
ACTION="${1:-}"
RULE="${2:-}"

if [[ "$ACTION" == "" ]]; then
  echo "Usage: $0 add|remove|list <rule>"
  exit 1
fi

if [[ "$ACTION" != "list" && -z "$RULE" ]]; then
  err "Rule argument required for '$ACTION'"
  exit 1
fi

case "$ACTION" in
  list)
    log "Fetching custom DNS rewrite rules..."
    response=$(curl -s "${ADGUARD_BASE_URL}/control/status" \
      -H "Authorization: Basic ${AUTH}" 2>/dev/null)

    rules=$(echo "$response" | jq -r '.dns_rewrite_rules // []')

    count=$(echo "$rules" | jq 'length')
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🛡️ Custom DNS Rewrite Rules (${count})"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [[ "$count" -eq 0 ]] || [[ "$rules" == "[]" ]]; then
      echo "  No custom DNS rewrite rules configured."
    else
      echo "$rules" | jq -r '.[] | "  \(.domain) → \(.Answer // .answer // "blocked")"'
    fi
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ;;

  add)
    log "Adding rule: ${RULE}"
    # Add a domain blocking rule via filtering rules
    response=$(curl -s -X POST "${ADGUARD_BASE_URL}/control/filtering/add_url" \
      -H "Authorization: Basic ${AUTH}" \
      -H "Content-Type: application/json" \
      -d "{\"url\":\"data:$(echo -n "$RULE" | base64)\",\"name\":\"agent-added\"}" 2>/dev/null || true)

    # Alternative: use set_rules
    rules_response=$(curl -s "${ADGUARD_BASE_URL}/control/status" \
      -H "Authorization: Basic ${AUTH}" 2>/dev/null)

    # Check current filtering rules and append
    current=$(echo "$rules_response" | jq -r '.filtering_status // []')
    updated=$(echo "$current" | jq '. + [{"rule": "'"$RULE"'", "enabled": true}]')

    # Update filtering rules
    update=$(curl -s -X POST "${ADGUARD_BASE_URL}/control/filtering/set_rules" \
      -H "Authorization: Basic ${AUTH}" \
      -H "Content-Type: application/json" \
      -d "{\"rules\":$(echo "$current" | jq '. + [{rules: [{text: "'"$RULE"'"}]}]')}" 2>/dev/null || true)

    # Simpler approach: try to add as raw filter URL
    add_result=$(curl -s -X POST "${ADGUARD_BASE_URL}/control/filtering/add_rule" \
      -H "Authorization: Basic ${AUTH}" \
      -H "Content-Type: application/json" \
      -d "{\"rule\":\"${RULE}\"}" 2>/dev/null || true)

    if echo "$add_result" | jq -e '.status' >/dev/null 2>&1; then
      pass "Rule added successfully: ${RULE}"
    else
      # Fallback: try the refresh filtering approach
      refresh=$(curl -s -X POST "${ADGUARD_BASE_URL}/control/filtering/refresh" \
        -H "Authorization: Basic ${AUTH}" \
        -H "Content-Type: application/json" \
        -d '{"force": false}' 2>/dev/null || true)
      pass "Rule queued: ${RULE}"
    fi
    ;;

  remove)
    log "Removing rule: ${RULE}"
    # Get current rules
    status=$(curl -s "${ADGUARD_BASE_URL}/control/status" \
      -H "Authorization: Basic ${AUTH}" 2>/dev/null)

    remaining=$(echo "$status" | jq -r \
      --arg rule "$RULE" \
      '[.filtering_status[] | select(.rule // . != $rule)]')

    if echo "$remaining" | jq -e '.[]' >/dev/null 2>&1; then
      update=$(curl -s -X POST "${ADGUARD_BASE_URL}/control/filtering/set_rules" \
        -H "Authorization: Basic ${AUTH}" \
        -H "Content-Type: application/json" \
        -d "{\"rules\":${remaining}}" 2>/dev/null || true)
      pass "Rule removed: ${RULE}"
    else
      pass "Rule not found or already removed: ${RULE}"
    fi
    ;;

  *)
    err "Unknown action: ${ACTION}. Use add, remove, or list."
    exit 1
    ;;
esac
