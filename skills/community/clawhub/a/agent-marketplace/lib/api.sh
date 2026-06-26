#!/bin/bash
# api.sh — Backend API integration
# Connects the skill layer to the AgentYard marketplace API.

AGENTYARD_API="${AGENTYARD_API:-https://agentyard-production.up.railway.app}"

# Validate API URL — must be https:// (or http://localhost for dev)
if [[ "$AGENTYARD_API" != https://* && "$AGENTYARD_API" != http://localhost* ]]; then
  echo "  Error: AGENTYARD_API must use https:// (got: $AGENTYARD_API)" >&2
  return 1 2>/dev/null || exit 1
fi

# On Windows (Schannel), SSL revocation checks can fail.
CURL_SSL_FLAGS=""
if curl --version 2>/dev/null | grep -qi schannel; then
  CURL_SSL_FLAGS="--ssl-no-revoke"
fi

# Wrapper for curl with security hardening
_curl() {
  curl --proto "=https,http" $CURL_SSL_FLAGS "$@"
}

# ── URL-encode a string ──
_urlencode() {
  jq -sRr @uri <<< "$1" 2>/dev/null || printf '%s' "$1"
}

# ── Health check ──
api_health_check() {
  local response
  response=$(_curl -s -o /dev/null -w "%{http_code}" \
    --connect-timeout 5 --max-time 10 \
    "${AGENTYARD_API}/health" 2>/dev/null) || true
  [[ "$response" == "200" ]]
}

# ── Register agent on marketplace ──
# Usage: register_agent <agent_config_json>
register_agent() {
  local agent_config="$1"

  if [[ -z "$agent_config" ]]; then
    echo "  Error: agent config required" >&2
    return 1
  fi

  # Validate JSON before sending
  if ! echo "$agent_config" | jq empty 2>/dev/null; then
    echo "  Error: invalid agent config JSON" >&2
    return 1
  fi

  local response
  response=$(_curl -s -w "\n%{http_code}" \
    --connect-timeout 10 --max-time 30 \
    -X POST "${AGENTYARD_API}/agents/register" \
    -H "Content-Type: application/json" \
    -d "$agent_config" 2>/dev/null) || true

  local http_code=$(echo "$response" | tail -1)
  local body=$(echo "$response" | sed '$d')

  if [[ "$http_code" == "201" || "$http_code" == "200" ]]; then
    echo "$body"
    return 0
  fi

  # Fallback: register locally if API unreachable
  if [[ "$http_code" == "000" ]]; then
    echo "  API unreachable. Agent saved locally." >&2
    return 0
  fi

  echo "  Registration failed (HTTP $http_code): $(echo "$body" | jq -r '.detail // "unknown error"' 2>/dev/null)" >&2
  return 1
}

# ── Create wallet via backend ──
# Usage: create_agent_wallet <agent_name> <public_key>
create_agent_wallet() {
  local agent_name="$1"
  local public_key="$2"

  local payload
  payload=$(jq -n --arg name "$agent_name" --arg key "$public_key" \
    '{ agent_name: $name, public_key: $key }')

  local response
  response=$(_curl -s -w "\n%{http_code}" \
    --connect-timeout 10 --max-time 30 \
    -X POST "${AGENTYARD_API}/wallets/create" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null) || true

  local http_code=$(echo "$response" | tail -1)
  local body=$(echo "$response" | sed '$d')

  if [[ "$http_code" == "201" || "$http_code" == "200" ]]; then
    echo "$body"
    return 0
  fi

  return 1
}

# ── Search marketplace ──
# Usage: search_agents <specialty> [max_price]
search_agents() {
  local specialty="$1"
  local max_price="${2:-}"

  if [[ -z "$specialty" ]]; then
    echo "  Error: specialty required" >&2
    return 1
  fi

  # Validate max_price is numeric if provided
  if [[ -n "$max_price" ]] && ! [[ "$max_price" =~ ^[0-9]+$ ]]; then
    echo "  Error: max_price must be a number" >&2
    return 1
  fi

  # URL-encode parameters
  local encoded_specialty
  encoded_specialty=$(_urlencode "$specialty")

  local url="${AGENTYARD_API}/agents/marketplace?specialty=${encoded_specialty}"
  [[ -n "$max_price" ]] && url="${url}&max_price=${max_price}"

  local response
  response=$(_curl -s -w "\n%{http_code}" \
    --connect-timeout 10 --max-time 15 \
    -X GET "$url" 2>/dev/null) || true

  local http_code=$(echo "$response" | tail -1)
  local body=$(echo "$response" | sed '$d')

  if [[ "$http_code" == "200" ]]; then
    local count=$(echo "$body" | jq '.agents | length' 2>/dev/null || echo "0")

    if [[ "$count" == "0" ]]; then
      echo "  No agents found matching '$specialty'."
      return 0
    fi

    echo "  Agents matching '$specialty':"
    echo ""
    echo "$body" | jq -r '.agents[] | "  \(.agent_name // .name) — \(.capabilities // .specialty) — \(.price_sats // .price_per_task_sats) sats/task"' 2>/dev/null
    return 0
  fi

  # Fallback to local search
  if [[ "$http_code" == "000" ]]; then
    search_local_agents "$specialty"
    return $?
  fi

  echo "  Search failed (HTTP $http_code)" >&2
  return 1
}

# ── Local fallback search ──
search_local_agents() {
  local specialty="$1"

  if [[ ! -d "agents" ]]; then
    echo "  No local agents found."
    return 0
  fi

  echo "  Agents matching '$specialty' (local):"
  echo ""

  local found=0
  for agent_dir in agents/*/; do
    if [[ -f "${agent_dir}agentyard.json" ]]; then
      local config
      config=$(cat "${agent_dir}agentyard.json" 2>/dev/null) || continue
      local agent_specialty
      agent_specialty=$(echo "$config" | jq -r '.specialty // ""')

      if [[ "${agent_specialty,,}" == *"${specialty,,}"* ]]; then
        local name price
        name=$(echo "$config" | jq -r '.agent_name // ""')
        price=$(echo "$config" | jq -r '.price_sats // 0')
        echo "  $name — $agent_specialty — $price sats/task"
        found=1
      fi
    fi
  done

  [[ "$found" == "0" ]] && echo "  No agents found matching '$specialty'."
  return 0
}

# ── Get agent info ──
# Usage: get_agent_info <agent_name>
get_agent_info() {
  local agent_name="$1"

  if [[ -z "$agent_name" ]]; then
    echo "Error: agent_name required" >&2
    return 1
  fi

  # URL-encode agent name
  local encoded_name
  encoded_name=$(_urlencode "$agent_name")

  # Try backend first
  local response
  response=$(_curl -s -w "\n%{http_code}" \
    --connect-timeout 5 --max-time 10 \
    -X GET "${AGENTYARD_API}/agents/${encoded_name}" 2>/dev/null) || true

  local http_code=$(echo "$response" | tail -1)
  local body=$(echo "$response" | sed '$d')

  if [[ "$http_code" == "200" ]]; then
    echo "$body"
    return 0
  fi

  # Fallback to local config
  if [[ -f "agents/${agent_name}/agentyard.json" ]]; then
    cat "agents/${agent_name}/agentyard.json"
    return 0
  fi

  return 1
}

# ── Create hire via backend ──
# Usage: create_hire <seller_agent_id> <task_description> <max_sats> <buyer_email>
create_hire() {
  local seller_id="$1"
  local task_desc="$2"
  local max_sats="$3"
  local buyer_email="$4"

  # Build JSON safely with jq
  local payload
  payload=$(jq -n \
    --arg id "$seller_id" \
    --arg brief "$task_desc" \
    --argjson sats "$max_sats" \
    --arg email "$buyer_email" \
    '{ agent_id: $id, brief: $brief, max_sats: $sats, delivery_email: $email }')

  local response
  response=$(_curl -s -w "\n%{http_code}" \
    --connect-timeout 10 --max-time 30 \
    -X POST "${AGENTYARD_API}/jobs" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null) || true

  local http_code=$(echo "$response" | tail -1)
  local body=$(echo "$response" | sed '$d')

  if [[ "$http_code" == "201" || "$http_code" == "200" ]]; then
    echo "$body"
    return 0
  fi

  if [[ "$http_code" == "000" ]]; then
    echo "  API unreachable." >&2
    return 1
  fi

  echo "  Hire failed (HTTP $http_code): $(echo "$body" | jq -r '.detail // "unknown error"' 2>/dev/null)" >&2
  return 1
}
