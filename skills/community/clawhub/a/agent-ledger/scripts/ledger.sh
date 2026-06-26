#!/usr/bin/env bash
# Agent Ledger — track AI agent earnings and payments
# Usage: ledger.sh [add|balance|list|pay|stats|export|wallet]
set -euo pipefail

LEDGER_DIR="${AGENT_LEDGER_DIR:-$HOME/.agent-ledger}"
LEDGER_FILE="$LEDGER_DIR/ledger.jsonl"
CONFIG_FILE="$LEDGER_DIR/config.json"
mkdir -p "$LEDGER_DIR"

# Ensure config exists
[[ -f "$CONFIG_FILE" ]] || echo '{"wallet":"","rates":{}}' > "$CONFIG_FILE"

sum_amounts() {
  local status="$1"
  local total
  total=$(grep "\"status\":\"$status\"" "$LEDGER_FILE" 2>/dev/null \
    | sed 's/.*"amount":\([0-9.]*\).*/\1/' \
    | awk '{s+=$1} END {printf "%.2f", s}')
  echo "${total:-0.00}"
}

case "${1:-help}" in
  add)
    DESC="${2:?Usage: ledger.sh add \"description\" amount [pending|paid]}"
    AMOUNT="${3:?Missing amount}"
    STATUS="${4:-pending}"
    DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    ID=$(date +%s%N | cut -c1-13)
    echo "{\"id\":\"$ID\",\"date\":\"$DATE\",\"task\":\"$DESC\",\"amount\":$AMOUNT,\"status\":\"$STATUS\"}" >> "$LEDGER_FILE"
    echo "✅ Added: $DESC — \$$AMOUNT ($STATUS)"
    ;;

  balance)
    if [[ ! -f "$LEDGER_FILE" ]]; then echo "💰 No entries yet."; exit 0; fi
    PENDING=$(sum_amounts "pending")
    PAID=$(sum_amounts "paid")
    TOTAL=$(awk "BEGIN {printf \"%.2f\", $PENDING + $PAID}")
    echo "💰 Agent Ledger Balance"
    echo "━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Pending:  \$$PENDING"
    echo "  Paid:     \$$PAID"
    echo "  Total:    \$$TOTAL"
    WALLET=$(jq -r '.wallet // ""' "$CONFIG_FILE" 2>/dev/null)
    [[ -n "$WALLET" ]] && echo "  Wallet:   $WALLET"
    ;;

  list)
    if [[ ! -f "$LEDGER_FILE" ]]; then echo "No entries yet."; exit 0; fi
    FILTER="${2:-}"
    echo "📋 Task Ledger"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    local_n=0
    while IFS= read -r line; do
      local_n=$((local_n + 1))
      DATE=$(echo "$line" | sed 's/.*"date":"\([^"]*\)".*/\1/' | cut -c1-10)
      TASK=$(echo "$line" | sed 's/.*"task":"\([^"]*\)".*/\1/')
      AMT=$(echo "$line" | sed 's/.*"amount":\([0-9.]*\).*/\1/')
      STATUS=$(echo "$line" | sed 's/.*"status":"\([^"]*\)".*/\1/')
      ICON=$([[ "$STATUS" == "paid" ]] && echo "💚" || echo "🟡")
      if [[ -z "$FILTER" ]] || [[ "$STATUS" == "$FILTER" ]]; then
        printf " %s %-3s %-12s %-38s \$%s\n" "$ICON" "$local_n." "$DATE" "$TASK" "$AMT"
      fi
    done < "$LEDGER_FILE"
    ;;

  pay)
    LINE="${2:?Usage: ledger.sh pay <line_number>}"
    if [[ ! -f "$LEDGER_FILE" ]]; then echo "No entries."; exit 1; fi
    sed -i '' "${LINE}s/\"pending\"/\"paid\"/" "$LEDGER_FILE"
    echo "💚 Marked line $LINE as paid."
    ;;

  stats)
    if [[ ! -f "$LEDGER_FILE" ]]; then echo "No data yet."; exit 0; fi
    TOTAL_TASKS=$(wc -l < "$LEDGER_FILE" | tr -d ' ')
    PENDING_COUNT=$(grep -c '"pending"' "$LEDGER_FILE" 2>/dev/null || true)
    PENDING_COUNT="${PENDING_COUNT:-0}"
    PAID_COUNT=$(grep -c '"paid"' "$LEDGER_FILE" 2>/dev/null || true)
    PAID_COUNT="${PAID_COUNT:-0}"
    PENDING=$(sum_amounts "pending")
    PAID=$(sum_amounts "paid")
    TOTAL=$(awk "BEGIN {printf \"%.2f\", $PENDING + $PAID}")
    AVG=$(awk "BEGIN {printf \"%.2f\", ($PENDING + $PAID) / $TOTAL_TASKS}")
    echo "📊 Agent Stats"
    echo "━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Tasks:     $TOTAL_TASKS ($PAID_COUNT paid, $PENDING_COUNT pending)"
    echo "  Earned:    \$$TOTAL"
    echo "  Avg/task:  \$$AVG"
    echo "  Paid out:  \$$PAID"
    echo "  Owed:      \$$PENDING"
    ;;

  export)
    FORMAT="${2:-json}"
    if [[ ! -f "$LEDGER_FILE" ]]; then echo "No data."; exit 0; fi
    if [[ "$FORMAT" == "csv" ]]; then
      echo "date,task,amount,status"
      while IFS= read -r line; do
        DATE=$(echo "$line" | sed 's/.*"date":"\([^"]*\)".*/\1/')
        TASK=$(echo "$line" | sed 's/.*"task":"\([^"]*\)".*/\1/')
        AMT=$(echo "$line" | sed 's/.*"amount":\([0-9.]*\).*/\1/')
        STATUS=$(echo "$line" | sed 's/.*"status":"\([^"]*\)".*/\1/')
        echo "\"$DATE\",\"$TASK\",$AMT,\"$STATUS\""
      done < "$LEDGER_FILE"
    else
      cat "$LEDGER_FILE"
    fi
    ;;

  wallet)
    if [[ -n "${2:-}" ]]; then
      jq --arg w "$2" '.wallet = $w' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
      echo "💎 Wallet set: $2"
    else
      WALLET=$(jq -r '.wallet // "not set"' "$CONFIG_FILE" 2>/dev/null)
      echo "💎 Wallet: $WALLET"
    fi
    ;;

  help|*)
    echo "💰 Agent Ledger — Track AI agent earnings"
    echo ""
    echo "Usage: ledger.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  add \"task\" amount [status]  Log a task"
    echo "  balance                     Show balance"
    echo "  list [pending|paid]         List tasks"
    echo "  pay <line>                  Mark as paid"
    echo "  stats                       Summary stats"
    echo "  export [json|csv]           Export data"
    echo "  wallet [address]            Get/set wallet"
    ;;
esac
