#!/bin/bash
# Agent Fuel — Autonomous wallet balance monitor & auto top-up
# Requires: mp (MoonPay CLI) installed and wallet created
# Usage: ./agent-fuel.sh [--daemon]

set -euo pipefail

CONFIG_FILE="${AGENT_FUEL_CONFIG:-$HOME/clawd/.secrets/agent-fuel.json}"
LOG_FILE="${AGENT_FUEL_LOG:-$HOME/clawd/memory/agent-fuel.log}"
STATE_FILE="${AGENT_FUEL_STATE:-/tmp/agent-fuel-state.json}"

# Defaults
CHAIN="base"
CURRENCY="USDC"
MIN_BALANCE="5.00"
TOP_UP_AMOUNT="20.00"
MAX_DAILY_SPEND="100.00"
ALERT_THRESHOLD="2.00"
WALLET_NAME="agent-fuel"
CHECK_INTERVAL=300  # 5 minutes
NOTIFY_CMD=""  # optional: telegram notification command

# Load config if exists
load_config() {
  if [[ -f "$CONFIG_FILE" ]]; then
    CHAIN=$(jq -r '.chain // "base"' "$CONFIG_FILE")
    CURRENCY=$(jq -r '.currency // "USDC"' "$CONFIG_FILE")
    MIN_BALANCE=$(jq -r '.minBalance // "5.00"' "$CONFIG_FILE")
    TOP_UP_AMOUNT=$(jq -r '.topUpAmount // "20.00"' "$CONFIG_FILE")
    MAX_DAILY_SPEND=$(jq -r '.maxDailySpend // "100.00"' "$CONFIG_FILE")
    ALERT_THRESHOLD=$(jq -r '.alertThreshold // "2.00"' "$CONFIG_FILE")
    WALLET_NAME=$(jq -r '.walletName // "agent-fuel"' "$CONFIG_FILE")
    CHECK_INTERVAL=$(jq -r '.checkInterval // 300' "$CONFIG_FILE")
    NOTIFY_CMD=$(jq -r '.notifyCmd // ""' "$CONFIG_FILE")
  fi
}

# Get wallet address for chain
get_wallet_address() {
  mp wallet list --json 2>/dev/null | jq -r ".[0].addresses.${CHAIN} // empty"
}

# Get current balance in USD
get_balance() {
  local addr
  addr=$(get_wallet_address)
  if [[ -z "$addr" ]]; then
    echo "-1"
    return
  fi
  
  local balances
  balances=$(mp token balance list --wallet "$addr" --chain "$CHAIN" --json 2>/dev/null)
  
  # Find target currency balance, default 0 if not found
  local found
  found=$(echo "$balances" | jq -r "
    [.items[]? | select(.symbol == \"$CURRENCY\" or (.symbol | ascii_downcase) == (\"$CURRENCY\" | ascii_downcase))] | 
    if length > 0 then .[0].balance else \"0\" end
  " 2>/dev/null)
  echo "${found:-0}"
}

# Get today's total spend from state
get_daily_spend() {
  local today
  today=$(date +%Y-%m-%d)
  if [[ -f "$STATE_FILE" ]]; then
    local state_date
    state_date=$(jq -r '.date // ""' "$STATE_FILE" 2>/dev/null)
    if [[ "$state_date" == "$today" ]]; then
      jq -r '.totalSpent // 0' "$STATE_FILE"
      return
    fi
  fi
  echo "0"
}

# Log transaction to state
log_spend() {
  local amount="$1"
  local reason="$2"
  local today
  today=$(date +%Y-%m-%d)
  local now
  now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  
  local current_spend
  current_spend=$(get_daily_spend)
  local new_total
  new_total=$(echo "$current_spend + $amount" | bc)
  
  # Update state file
  local txs="[]"
  if [[ -f "$STATE_FILE" ]] && [[ "$(jq -r '.date' "$STATE_FILE" 2>/dev/null)" == "$today" ]]; then
    txs=$(jq '.transactions // []' "$STATE_FILE")
  fi
  
  jq -n \
    --arg date "$today" \
    --arg total "$new_total" \
    --argjson txs "$txs" \
    --arg ts "$now" \
    --arg amt "$amount" \
    --arg rsn "$reason" \
    '{date: $date, totalSpent: ($total|tonumber), transactions: ($txs + [{timestamp: $ts, amount: ($amt|tonumber), reason: $rsn}])}' \
    > "$STATE_FILE"
}

# Send notification
notify() {
  local msg="$1"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $msg" >> "$LOG_FILE"
  
  if [[ -n "$NOTIFY_CMD" ]]; then
    eval "$NOTIFY_CMD '$msg'" 2>/dev/null || true
  fi
  
  echo "$msg"
}

# Top up via MoonPay
do_topup() {
  local daily_spend
  daily_spend=$(get_daily_spend)
  
  # Check daily limit
  local would_spend
  would_spend=$(echo "$daily_spend + $TOP_UP_AMOUNT" | bc)
  local over
  over=$(echo "$would_spend > $MAX_DAILY_SPEND" | bc)
  
  if [[ "$over" == "1" ]]; then
    notify "⚠️ AGENT FUEL: Daily spend limit would be exceeded (\$$daily_spend + \$$TOP_UP_AMOUNT > \$$MAX_DAILY_SPEND). Manual top-up needed."
    return 1
  fi
  
  notify "⛽ AGENT FUEL: Topping up \$$TOP_UP_AMOUNT $CURRENCY on $CHAIN..."
  
  # Map currency+chain to MoonPay token code
  local currency_lower
  currency_lower=$(echo "$CURRENCY" | tr '[:upper:]' '[:lower:]')
  local token_code
  case "${currency_lower}_${CHAIN}" in
    usdc_base) token_code="usdc_base" ;;
    usdc_ethereum) token_code="usdc" ;;
    usdc_solana) token_code="usdc_sol" ;;
    usdt_tron) token_code="usdt_trx" ;;
    eth_*) token_code="eth" ;;
    sol_*) token_code="sol" ;;
    *) token_code="${currency_lower}_${CHAIN}" ;;
  esac
  
  # MoonPay buy — returns checkout URL for fiat purchase
  local result
  result=$(mp buy \
    --token "$token_code" \
    --amount "$TOP_UP_AMOUNT" \
    --wallet "$(get_wallet_address)" \
    2>&1) || {
    notify "❌ AGENT FUEL: Top-up failed: $result"
    return 1
  }
  
  log_spend "$TOP_UP_AMOUNT" "auto-top-up"
  notify "✅ AGENT FUEL: Top-up initiated. $result"
  return 0
}

# x402 request wrapper
x402_request() {
  local url="$1"
  shift
  
  mp x402 request --url "$url" --wallet "$WALLET_NAME" --chain "$CHAIN" --json "$@" 2>&1
}

# Main check cycle
check() {
  load_config
  
  local balance
  balance=$(get_balance)
  
  if [[ "$balance" == "-1" ]]; then
    notify "❌ AGENT FUEL: Could not check balance. Wallet '$WALLET_NAME' not found."
    return 1
  fi
  
  local below_alert
  below_alert=$(echo "$balance < $ALERT_THRESHOLD" | bc 2>/dev/null || echo "0")
  local below_min
  below_min=$(echo "$balance < $MIN_BALANCE" | bc 2>/dev/null || echo "0")
  
  if [[ "$below_alert" == "1" ]]; then
    notify "🚨 AGENT FUEL: CRITICAL — Balance \$$balance below alert threshold \$$ALERT_THRESHOLD"
  fi
  
  if [[ "$below_min" == "1" ]]; then
    notify "⛽ AGENT FUEL: Balance \$$balance below minimum \$$MIN_BALANCE. Auto top-up..."
    do_topup
    return $?
  fi
  
  echo "✅ Balance: \$$balance $CURRENCY ($CHAIN) — OK"
  return 0
}

# Daemon mode
daemon() {
  notify "🚀 AGENT FUEL: Daemon started. Checking every ${CHECK_INTERVAL}s"
  notify "   Chain: $CHAIN | Currency: $CURRENCY | Min: \$$MIN_BALANCE | Top-up: \$$TOP_UP_AMOUNT"
  
  while true; do
    check || true
    sleep "$CHECK_INTERVAL"
  done
}

# CLI
case "${1:-check}" in
  check)
    load_config
    check
    ;;
  daemon|--daemon)
    load_config
    daemon
    ;;
  balance)
    load_config
    balance=$(get_balance)
    echo "$balance $CURRENCY ($CHAIN)"
    ;;
  topup|top-up)
    load_config
    do_topup
    ;;
  x402)
    load_config
    shift
    x402_request "$@"
    ;;
  status)
    load_config
    echo "=== Agent Fuel Status ==="
    echo "Wallet: $WALLET_NAME"
    echo "Chain: $CHAIN"
    echo "Currency: $CURRENCY"
    echo "Min Balance: \$$MIN_BALANCE"
    echo "Top-up Amount: \$$TOP_UP_AMOUNT"
    echo "Max Daily Spend: \$$MAX_DAILY_SPEND"
    echo "Today's Spend: \$$(get_daily_spend)"
    echo "Current Balance: \$$(get_balance) $CURRENCY"
    ;;
  *)
    echo "Usage: agent-fuel.sh [check|daemon|balance|topup|x402|status]"
    exit 1
    ;;
esac
