#!/bin/bash
# estimate.sh — Quick API cost estimate with custom parameters
# Usage: ./estimate.sh <heartbeat_secs> <tasks_per_day> <avg_input_tokens> <avg_output_tokens> [provider]

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <heartbeat_seconds> <tasks_per_day> <avg_input_tokens> <avg_output_tokens> [provider]"
  echo ""
  echo "Example: $0 300 20 8000 2000 minimax"
  echo "Example: $0 600 50 4000 1000 openai"
  echo ""
  echo "Providers: openai (default), anthropic, minimax, lmstudio"
  exit 1
fi

HB_INTERVAL="${1}"
TASKS_PER_DAY="${2}"
AVG_INPUT="${3}"
AVG_OUTPUT="${4}"
PROVIDER="${5:-${API_COST_MODEL:-openai}}"

# Provider pricing (per 1M tokens)
case "$PROVIDER" in
  minimax)
    INPUT_PRICE=0.10
    OUTPUT_PRICE=0.10
    ;;
  anthropic|claude)
    INPUT_PRICE=3.00
    OUTPUT_PRICE=15.00
    ;;
  openai|gpt)
    INPUT_PRICE=2.50
    OUTPUT_PRICE=10.00
    ;;
  lmstudio|local)
    INPUT_PRICE=0.01
    OUTPUT_PRICE=0.01
    ;;
  *)
    INPUT_PRICE=2.50
    OUTPUT_PRICE=10.00
    ;;
esac

echo "============================================"
echo "   OpenClaw API Cost Estimate"
echo "============================================"
echo ""
echo "Parameters:"
echo "  Heartbeat interval:  ${HB_INTERVAL}s"
echo "  Tasks per day:       ${TASKS_PER_DAY}"
echo "  Avg input tokens:     ${AVG_INPUT}"
echo "  Avg output tokens:    ${AVG_OUTPUT}"
echo "  Provider:             $PROVIDER"
echo ""

# Heartbeat cost
API_CALLS_PER_DAY=$(echo "86400 / $HB_INTERVAL" | bc)
HB_INPUT_TOKENS=500
HB_OUTPUT_TOKENS=50
HB_COST_PER_CALL=$(echo "scale=8; (($HB_INPUT_TOKENS * $INPUT_PRICE) + ($HB_OUTPUT_TOKENS * $OUTPUT_PRICE)) / 1000000" | bc)
HB_COST_PER_DAY=$(echo "scale=8; $API_CALLS_PER_DAY * $HB_COST_PER_CALL" | bc)

# Task cost
TASK_INPUT_COST=$(echo "scale=8; ($AVG_INPUT * $INPUT_PRICE) / 1000000" | bc)
TASK_OUTPUT_COST=$(echo "scale=8; ($AVG_OUTPUT * $OUTPUT_PRICE) / 1000000" | bc)
TASK_COST=$(echo "scale=8; $TASK_INPUT_COST + $TASK_OUTPUT_COST" | bc)
TASK_COST_PER_DAY=$(echo "scale=8; $TASKS_PER_DAY * $TASK_COST" | bc)

# Totals
TOTAL_DAY=$(echo "scale=8; $HB_COST_PER_DAY + $TASK_COST_PER_DAY" | bc)
TOTAL_WEEK=$(echo "scale=8; $TOTAL_DAY * 7" | bc)
TOTAL_MONTH=$(echo "scale=8; $TOTAL_WEEK * 4.33" | bc)
TOTAL_YEAR=$(echo "scale=8; $TOTAL_DAY * 365" | bc)

echo "--- Cost Breakdown ---"
echo "  Heartbeat cost/day:  \$$(printf '%.4f' $HB_COST_PER_DAY)  ($API_CALLS_PER_DAY calls @ \$$(printf '%.6f' $HB_COST_PER_CALL))"
echo "  Task cost/day:       \$$(printf '%.4f' $TASK_COST_PER_DAY)  ($TASKS_PER_DAY tasks @ \$$(printf '%.5f' $TASK_COST))"
echo ""
echo "============================================"
echo "   TOTAL ESTIMATED SPEND"
echo "============================================"
echo "  Daily:    \$$(printf '%.4f' $TOTAL_DAY)"
echo "  Weekly:   \$$(printf '%.4f' $TOTAL_WEEK)"
echo "  Monthly:  \$$(printf '%.4f' $TOTAL_MONTH)"
echo "  Yearly:   \$$(printf '%.4f' $TOTAL_YEAR)"
echo "============================================"
echo ""

# Optimization suggestions
if [ "$HB_INTERVAL" -lt 300 ]; then
  SAVINGS=$(echo "scale=8; $HB_COST_PER_DAY * 0.7" | bc)
  echo "💡 Increase heartbeat to 1800s → save ~\$$(printf '%.4f' $SAVINGS)/day"
fi

# Provider comparison
if [ "$PROVIDER" = "openai" ]; then
  MINI_COST=$(echo "scale=8; $TOTAL_DAY * 0.05" | bc)
  echo "💡 Switch to MiniMax M2 → ~\$$(printf '%.4f' $MINI_COST)/day (95% cheaper)"
fi

echo ""
