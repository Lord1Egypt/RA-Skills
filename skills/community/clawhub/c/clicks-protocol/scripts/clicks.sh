#!/usr/bin/env bash
# Clicks Protocol — Query tool (zero dependencies, just curl + jq)
# Uses the HTTP MCP Server at mcp.clicksprotocol.xyz

set -euo pipefail

MCP_URL="https://mcp.clicksprotocol.xyz/mcp"

call_mcp() {
  local tool="$1"
  shift
  local args
  if [ "$#" -gt 0 ]; then
    args="$1"
  else
    args='{}'
  fi
  
  local response
  response=$(curl -s -X POST "$MCP_URL" \
    -H "Content-Type: application/json" \
    -d "$(jq -cn --arg tool "$tool" --argjson args "$args" \
      '{jsonrpc:"2.0",id:1,method:"tools/call",params:{name:$tool,arguments:$args}}')")
  
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
    call_mcp "clicks_get_agent_info" "$(jq -cn --arg address "$2" '{agent_address:$address}')"
    ;;
  simulate|split|preview)
    [ -z "${2:-}" ] || [ -z "${3:-}" ] && { echo "Usage: $0 simulate <amount_usdc> <address>" >&2; exit 1; }
    call_mcp "clicks_simulate_split" "$(jq -cn --arg amount "$2" --arg address "$3" '{amount:$amount,agent_address:$address}')"
    ;;
  referral|ref|network)
    [ -z "${2:-}" ] && { echo "Usage: $0 referral <address>" >&2; exit 1; }
    call_mcp "clicks_get_referral_stats" "$(jq -cn --arg address "$2" '{agent_address:$address}')"
    ;;
  info|about)
    cat <<EOF
Clicks Protocol - Agent Commerce Settlement Router on Base

What it does:
1. Agent commerce software detects a USDC payment from a rail such as x402 or ACP.
2. Clicks settlement policy can keep 80% liquid for operations and route 20% to supported yield backends by default.
3. Treasury policy, attribution, receipts, and withdrawals stay explicit and auditable.
4. Operator-controlled actions stay outside this read-only ClawHub script.

Safety boundary:
- This script only calls read-only remote MCP tools.
- It never handles private keys, signs transactions, broadcasts transactions, or performs state-changing treasury actions.
- Treat all amounts as status or simulation output until a human operator separately approves and signs.

Fee: 2% on yield only, never on principal.
Attribution: Level 1 gets 40%, Level 2 gets 20%, Level 3 gets 10% of protocol fee.

Contracts: Base Mainnet (Chain ID 8453)
- ClicksRegistry: 0x23bb0Ea69b2BD2e527D5DbA6093155A6E1D0C0a3
- ClicksSplitterV4: 0xB7E0016d543bD443ED2A6f23d5008400255bf3C8
- ClicksYieldRouter: 0x053167a233d18E05Bc65a8d5F3F8808782a3EECD
- ClicksFeeV2: 0x8C4E07bBF0BDc3949eA133D636601D8ba17e0fb5
- ClicksReferral: 0x1E5Ab896D3b3A542C5E91852e221b2D849944ccC

SDK: npm install @clicks-protocol/sdk
MCP: npm install @clicks-protocol/mcp-server
Docs: https://clicksprotocol.xyz/llms.txt
EOF
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
