#!/bin/bash
# heartbeat_diagnosis.sh — Diagnose heartbeat waste in OpenClaw configuration
# Finds the heartbeat interval and calculates wasted API calls per day/week/year

set -e

HEARTBEAT_INTERVAL="${HEARTBEAT_INTERVAL:-auto}"
CONFIG_FILE="${HOME}/.openclaw/openclaw.json"

# Detect heartbeat interval
detect_heartbeat() {
  if [ "$HEARTBEAT_INTERVAL" != "auto" ]; then
    echo "$HEARTBEAT_INTERVAL"
    return
  fi

  if [ -f "$CONFIG_FILE" ]; then
    # Try to extract heartbeat interval from openclaw.json
    # heartbeat is at cfg.agents.defaults.heartbeat.every
    INTERVAL=$(python3 -c "
import json, sys, re
try:
    with open('$CONFIG_FILE', 'r') as f:
        cfg = json.load(f)
    hb = cfg.get('agents', {}).get('defaults', {}).get('heartbeat', {})
    result = 'auto'
    if isinstance(hb, dict):
        every = hb.get('every', 'auto')
        if every not in ('auto', None, '') and every is not None:
            m = re.match(r'(\d+)([smh])', str(every))
            if m:
                val, unit = int(m.group(1)), m.group(2)
                result = str(val * {'s': 1, 'm': 60, 'h': 3600}[unit])
    elif isinstance(hb, (int, float)):
        result = str(int(hb))
    print(result)
except:
    print('auto')
" 2>/dev/null)
    if [ "$INTERVAL" != "auto" ] && [ -n "$INTERVAL" ]; then
      echo "$INTERVAL"
      return
    fi
  fi

  # Try agent config files
  AGENT_CONFIG="${HOME}/.openclaw/agents/*/agent.json"
  for conf in $AGENT_CONFIG; do
    if [ -f "$conf" ]; then
      INTERVAL=$(python3 -c "
import json, sys, re
try:
    with open('$conf', 'r') as f:
        cfg = json.load(f)
    hb = cfg.get('heartbeat', {})
    result = 'auto'
    if isinstance(hb, dict):
        every = hb.get('every', 'auto')
        if every not in ('auto', None, '') and every is not None:
            m = re.match(r'(\d+)([smh])', str(every))
            if m:
                val, unit = int(m.group(1)), m.group(2)
                result = str(val * {'s': 1, 'm': 60, 'h': 3600}[unit])
    elif isinstance(hb, (int, float)):
        result = str(int(hb))
    print(result)
except:
    print('auto')
" 2>/dev/null)
      if [ "$INTERVAL" != "auto" ] && [ -n "$INTERVAL" ]; then
        echo "$INTERVAL"
        return
      fi
    fi
  done

  # Check environment variable
  if [ -n "$HEARTBEAT_INTERVAL" ] && [ "$HEARTBEAT_INTERVAL" != "auto" ]; then
    echo "$HEARTBEAT_INTERVAL"
    return
  fi

  echo "auto"
}

echo "=========================================="
echo "   OpenClaw Heartbeat Cost Diagnosis"
echo "=========================================="
echo ""

INTERVAL=$(detect_heartbeat)

if [ "$INTERVAL" = "auto" ]; then
  echo "⚠️  Could not auto-detect heartbeat interval"
  echo "   Set HEARTBEAT_INTERVAL env var (seconds) or check config manually"
  INTERVAL=1800  # assume 30 min
  echo "   Using conservative default: 30 minutes"
else
  echo "✓ Detected heartbeat: ${INTERVAL}s"
fi

# Calculate waste scenarios
API_CALLS_PER_DAY=$(echo "86400 / $INTERVAL" | bc)
API_CALLS_PER_WEEK=$(echo "$API_CALLS_PER_DAY * 7" | bc)
API_CALLS_PER_YEAR=$(echo "$API_CALLS_PER_WEEK * 52" | bc)

# Estimate tokens per heartbeat call (minimal keep-alive)
HEARTBEAT_INPUT_TOKENS=500
HEARTBEAT_OUTPUT_TOKENS=50

# Provider pricing (per 1M tokens)
case "${API_COST_MODEL:-openai}" in
  minimax)
    INPUT_PRICE=0.10
    OUTPUT_PRICE=0.10
    ;;
  anthropic)
    INPUT_PRICE=3.00
    OUTPUT_PRICE=15.00
    ;;
  openai)
    INPUT_PRICE=2.50
    OUTPUT_PRICE=10.00
    ;;
  *)
    INPUT_PRICE=2.50
    OUTPUT_PRICE=10.00
    ;;
esac

# Calculate cost per heartbeat
COST_PER_CALL=$(echo "scale=8; (($HEARTBEAT_INPUT_TOKENS * $INPUT_PRICE) + ($HEARTBEAT_OUTPUT_TOKENS * $OUTPUT_PRICE)) / 1000000" | bc)

COST_PER_DAY=$(echo "scale=8; $API_CALLS_PER_DAY * $COST_PER_CALL" | bc)
COST_PER_WEEK=$(echo "scale=8; $COST_PER_DAY * 7" | bc)
COST_PER_MONTH=$(echo "scale=8; $COST_PER_WEEK * 4.33" | bc)
COST_PER_YEAR=$(echo "scale=8; $COST_PER_DAY * 365" | bc)

echo ""
echo "--- Heartbeat Frequency ---"
echo "  Calls per day:  $API_CALLS_PER_DAY"
echo "  Calls per week:  $API_CALLS_PER_WEEK"
echo "  Calls per year:  $API_CALLS_PER_YEAR"
echo ""
echo "--- Estimated Heartbeat Cost ---"
echo "  Cost per call:   \$$COST_PER_CALL"
echo "  Cost per day:    \$$(printf '%.4f' $COST_PER_DAY)"
echo "  Cost per week:   \$$(printf '%.2f' $COST_PER_WEEK)"
echo "  Cost per month:  \$$(printf '%.2f' $COST_PER_MONTH)"
echo "  Cost per year:   \$$(printf '%.2f' $COST_PER_YEAR)"
echo ""

# Efficiency scoring
if [ "$INTERVAL" -le 60 ]; then
  SCORE=10
  RATING="🔴 Critical"
  RECOMMENDATION="Increase to at least 300s (5 min)"
elif [ "$INTERVAL" -le 300 ]; then
  SCORE=40
  RATING="🟡 High"
  RECOMMENDATION="Increase to 600-1800s (10-30 min)"
elif [ "$INTERVAL" -le 900 ]; then
  SCORE=70
  RATING="🟢 Good"
  RECOMMENDATION="Consider 1800s if agent is mostly idle"
else
  SCORE=95
  RATING="✅ Optimal"
  RECOMMENDATION="Heartbeat interval is well configured"
fi

echo "--- Efficiency Score ---"
echo "  Score: $SCORE/100 — $RATING"
echo "  Recommendation: $RECOMMENDATION"
echo ""

# Waste calculation if suboptimal
if [ "$SCORE" -lt 70 ]; then
  OPTIMAL_INTERVAL=1800
  OPTIMAL_CALLS_PER_DAY=$(echo "86400 / $OPTIMAL_INTERVAL" | bc)
  WASTED_CALLS_PER_DAY=$((API_CALLS_PER_DAY - OPTIMAL_CALLS_PER_DAY))
  WASTED_COST_PER_DAY=$(echo "scale=8; $WASTED_CALLS_PER_DAY * $COST_PER_CALL" | bc)
  WASTED_COST_PER_YEAR=$(echo "scale=8; $WASTED_COST_PER_DAY * 365" | bc)

  echo "--- Waste Analysis ---"
  echo "  Wasted calls/day:  $WASTED_CALLS_PER_DAY"
  echo "  Wasted cost/day:   \$$(printf '%.4f' $WASTED_COST_PER_DAY)"
  echo "  Wasted cost/year:   \$$(printf '%.2f' $WASTED_COST_PER_YEAR)"
  echo ""
  echo "💡 Fix: Set heartbeat interval to ${OPTIMAL_INTERVAL}s in openclaw config"
fi

echo ""
echo "=========================================="
echo "  Run ./analyze.sh for full cost report"
echo "=========================================="
