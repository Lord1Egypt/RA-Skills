#!/usr/bin/env bash
# Clicks Protocol — Query tool (zero dependencies, just curl + jq)
# Uses the HTTP MCP Server at mcp.clicksprotocol.xyz

set -euo pipefail

MCP_URL="https://mcp.clicksprotocol.xyz/mcp"

call_mcp() {
  local tool="$1"
  shift
  local args="$*"
  
  local response
  response=$(curl -s -X POST "$MCP_URL" \
    -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$tool\",\"arguments\":$args}}")
  
  local error
  error=$(echo "$response" | jq -r '.error.message // empty' 2>/dev/null)
  if [ -n "$error" ]; then
    echo "Error: $error" >&2
    return 1
  fi
  
  local is_error
  is_error=$(echo "$response" | jq -r '.result.isError // false' 2>/dev/null)
  local text
  text=$(echo "$response" | jq -r '.result.content[0].text' 2>/dev/null)
  
  if [ "$is_error" = "true" ]; then
    echo "Error: $text" >&2
    return 1
  fi
  
  # Try to pretty-print if it's JSON, otherwise print raw
  echo "$text" | jq . 2>/dev/null || echo "$text"
}

usage() {
  cat <<EOF
Clicks Protocol — Query Tool

Usage: $(basename "$0") <command> [args]

Commands:
  yield-info                        Current APY rates and protocol info
  agent-info <address>              Agent registration, balance, yield split
  simulate <amount> <address>       Preview payment split (liquid vs yield)
  referral <address>                Referral network stats and earnings
  info                              Protocol overview (contracts, docs, links)

Examples:
  $(basename "$0") yield-info
  $(basename "$0") agent-info 0xABC123...
  $(basename "$0") simulate 1000 0xABC123...
  $(basename "$0") referral 0xABC123...
EOF
}

case "${1:-}" in
  yield-info|yield|apy)
    call_mcp "clicks_get_yield_info" '{}'
    ;;
  agent-info|agent|status)
    [ -z "${2:-}" ] && { echo "Usage: $0 agent-info <address>" >&2; exit 1; }
    call_mcp "clicks_get_agent_info" "{\"agent_address\":\"$2\"}"
    ;;
  simulate|split|preview)
    [ -z "${2:-}" ] || [ -z "${3:-}" ] && { echo "Usage: $0 simulate <amount_usdc> <address>" >&2; exit 1; }
    call_mcp "clicks_simulate_split" "{\"amount\":\"$2\",\"agent_address\":\"$3\"}"
    ;;
  referral|ref|network)
    [ -z "${2:-}" ] && { echo "Usage: $0 referral <address>" >&2; exit 1; }
    call_mcp "clicks_get_referral_stats" "{\"agent_address\":\"$2\"}"
    ;;
  info|about)
    curl -s "$MCP_URL" \
      -H "Content-Type: application/json" \
      -X POST \
      -d '{"jsonrpc":"2.0","id":1,"method":"resources/read","params":{"uri":"clicks://info"}}' \
      | jq -r '.result.contents[0].text' 2>/dev/null
    ;;
  -h|--help|help|"")
    usage
    ;;
  *)
    echo "Unknown command: $1" >&2
    usage >&2
    exit 1
    ;;
esac
