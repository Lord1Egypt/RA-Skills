#!/bin/bash
# analyze.sh — Full OpenClaw API cost analysis
# Analyzes heartbeat, tools, model config, and generates a complete cost report

set -e

PROVIDER="${API_COST_MODEL:-minimax}"
REPORT_INTERVAL="${API_COST_INTERVAL:-weekly}"

echo "============================================"
echo "   OpenClaw API Cost Analyzer"
echo "   $(date '+%Y-%m-%d %H:%M UTC')"
echo "============================================"
echo ""

# Detect or estimate heartbeat interval
CONFIG_FILE="${HOME}/.openclaw/openclaw.json"
AGENT_CONFIG_DIR="${HOME}/.openclaw/agents"

HEARTBEAT_INTERVAL="${HEARTBEAT_INTERVAL:-auto}"

if [ "$HEARTBEAT_INTERVAL" = "auto" ]; then
  if [ -f "$CONFIG_FILE" ]; then
    HEARTBEAT_INTERVAL=$(python3 -c "
import json, sys, re
try:
    with open('$CONFIG_FILE', 'r') as f:
        cfg = json.load(f)
    # heartbeat is at cfg.agents.defaults.heartbeat.every
    hb = cfg.get('agents', {}).get('defaults', {}).get('heartbeat', {})
    if isinstance(hb, dict):
        every = hb.get('every', 'auto')
    elif isinstance(hb, str):
        every = hb
    else:
        every = 'auto'
    if every not in ('auto', None, '') and every is not None:
        m = re.match(r'(\d+)([smh])', str(every))
        if m:
            val, unit = int(m.group(1)), m.group(2)
            print(str(val * {'s': 1, 'm': 60, 'h': 3600}[unit]))
        else:
            print('auto')
    else:
        print('auto')
except:
    print('auto')
" 2>/dev/null || echo "auto")
  fi

  if [ "$HEARTBEAT_INTERVAL" = "auto" ]; then
    HEARTBEAT_INTERVAL=1800
    echo "⚠️  Could not detect heartbeat interval — using 30 min default"
  else
    echo "✓ Detected heartbeat: ${HEARTBEAT_INTERVAL}s"
  fi
else
  echo "✓ Using configured heartbeat: ${HEARTBEAT_INTERVAL}s"
fi

# Count tools/skills
TOOL_COUNT=0
SKILL_DIR="${HOME}/.openclaw/workspace/skills"
NPM_SKILL_DIR="${HOME}/.npm-global/lib/node_modules/openclaw/skills"

if [ -d "$SKILL_DIR" ]; then
  TOOL_COUNT=$((TOOL_COUNT + $(find "$SKILL_DIR" -name "*.sh" -o -name "*.js" -o -name "SKILL.md" 2>/dev/null | wc -l)))
fi

echo "✓ Skills/tools detected: $TOOL_COUNT"

# Count tools in openclaw config
if [ -f "$CONFIG_FILE" ]; then
  CONFIG_TOOLS=$(python3 -c "
import json, sys
try:
    with open('$CONFIG_FILE', 'r') as f:
        cfg = json.load(f)
    tools = cfg.get('tools', cfg.get('skills', cfg.get('plugins', [])))
    if isinstance(tools, list):
        print(len(tools))
    else:
        print(0)
except:
    print(0)
" 2>/dev/null || echo "0")
  echo "✓ Tools in config: $CONFIG_TOOLS"
fi

# Provider pricing
case "$PROVIDER" in
  minimax)
    INPUT_PRICE=0.10
    OUTPUT_PRICE=0.10
    MODEL_NAME="MiniMax M2"
    ;;
  anthropic)
    INPUT_PRICE=3.00
    OUTPUT_PRICE=15.00
    MODEL_NAME="Claude 3.5 Sonnet"
    ;;
  openai)
    INPUT_PRICE=2.50
    OUTPUT_PRICE=10.00
    MODEL_NAME="GPT-4o"
    ;;
  openai-mini)
    INPUT_PRICE=0.15
    OUTPUT_PRICE=0.60
    MODEL_NAME="GPT-4o-mini"
    ;;
  *)
    INPUT_PRICE=0.10
    OUTPUT_PRICE=0.10
    MODEL_NAME="MiniMax M2"
    ;;
esac

INPUT_PRICE_DISPLAY=$(printf '%.2f' "$INPUT_PRICE")
OUTPUT_PRICE_DISPLAY=$(printf '%.2f' "$OUTPUT_PRICE")

echo "✓ Model: $MODEL_NAME @ \$$INPUT_PRICE_DISPLAY/\$$OUTPUT_PRICE_DISPLAY per 1M tokens"
echo ""

# ---- CALCULATIONS ----

# Heartbeat costs
HB_CALLS_DAY=$(echo "86400 / $HEARTBEAT_INTERVAL" | bc)
HB_INPUT_TOKENS=500
HB_OUTPUT_TOKENS=50
HB_COST_CALL=$(echo "scale=8; (($HB_INPUT_TOKENS * $INPUT_PRICE) + ($HB_OUTPUT_TOKENS * $OUTPUT_PRICE)) / 1000000" | bc)
HB_COST_DAY=$(echo "scale=8; $HB_CALLS_DAY * $HB_COST_CALL" | bc)
HB_COST_WEEK=$(echo "scale=8; $HB_COST_DAY * 7" | bc)
HB_COST_MONTH=$(echo "scale=8; $HB_COST_WEEK * 4.33" | bc)

# Task costs (estimated)
TASKS_PER_DAY=20
AVG_INPUT=6000
AVG_OUTPUT=1500
TASK_COST=$(echo "scale=8; (($AVG_INPUT * $INPUT_PRICE) + ($AVG_OUTPUT * $OUTPUT_PRICE)) / 1000000" | bc)
TASK_COST_DAY=$(echo "scale=8; $TASKS_PER_DAY * $TASK_COST" | bc)
TASK_COST_WEEK=$(echo "scale=8; $TASK_COST_DAY * 7" | bc)
TASK_COST_MONTH=$(echo "scale=8; $TASK_COST_WEEK * 4.33" | bc)

# Tool overhead (each tool call adds ~200 tokens)
TOOL_OVERHEAD_CALLS=$(echo "$TOOL_COUNT * 3" | bc)
TOOL_OVERHEAD_DAY=$(echo "scale=8; $TOOL_CALLS_DAY * 200 * $INPUT_PRICE / 1000000" | bc)

TOTAL_DAY=$(echo "scale=8; $HB_COST_DAY + $TASK_COST_DAY" | bc)
TOTAL_WEEK=$(echo "scale=8; $TOTAL_DAY * 7" | bc)
TOTAL_MONTH=$(echo "scale=8; $TOTAL_WEEK * 4.33" | bc)
TOTAL_YEAR=$(echo "scale=8; $TOTAL_DAY * 365" | bc)

echo "============================================"
echo "   COST BREAKDOWN"
echo "============================================"
echo ""
echo "Heartbeat:"
echo "  $HB_CALLS_DAY calls/day × \$$(printf '%.6f' $HB_COST_CALL) = \$$(printf '%.4f' $HB_COST_DAY)/day"
echo ""
echo "Task execution:"
echo "  $TASKS_PER_DAY tasks/day × \$$(printf '%.5f' $TASK_COST) = \$$(printf '%.4f' $TASK_COST_DAY)/day"
echo ""
echo "============================================"
echo "   TOTAL ESTIMATED SPEND"
echo "============================================"
echo ""
printf "  %-10s  %s\n" "Daily:"    "\$$(printf '%.4f' $TOTAL_DAY)"
printf "  %-10s  %s\n" "Weekly:"   "\$$(printf '%.4f' $TOTAL_WEEK)"
printf "  %-10s  %s\n" "Monthly:"  "\$$(printf '%.4f' $TOTAL_MONTH)"
printf "  %-10s  %s\n" "Yearly:"   "\$$(printf '%.4f' $TOTAL_YEAR)"
echo ""
echo "============================================"
echo "   EFFICIENCY SCORE"
echo "============================================"

# Score heartbeat
if [ "$HEARTBEAT_INTERVAL" -le 60 ]; then
  HB_SCORE=10
  HB_RATING="🔴 Critical"
elif [ "$HEARTBEAT_INTERVAL" -le 300 ]; then
  HB_SCORE=40
  HB_RATING="🟡 High waste"
elif [ "$HEARTBEAT_INTERVAL" -le 900 ]; then
  HB_SCORE=75
  HB_RATING="🟢 Good"
else
  HB_SCORE=95
  HB_RATING="✅ Optimal"
fi

# Score model
case "$PROVIDER" in
  minimax)
    MODEL_SCORE=95
    MODEL_RATING="✅ Best price/performance"
    ;;
  openai-mini)
    MODEL_SCORE=70
    MODEL_RATING="🟡 Good, MiniMax cheaper"
    ;;
  anthropic)
    MODEL_SCORE=50
    MODEL_RATING="🟡 Premium — use for complex reasoning only"
    ;;
  openai)
    MODEL_SCORE=30
    MODEL_RATING="🔴 Expensive — consider MiniMax for volume"
    ;;
  *)
    MODEL_SCORE=60
    MODEL_RATING="🟡 Review pricing"
    ;;
esac

OVERALL_SCORE=$(( (HB_SCORE + MODEL_SCORE) / 2 ))

echo ""
printf "  %-20s  %d/100 — %s\n" "Heartbeat:" "$HB_SCORE" "$HB_RATING"
printf "  %-20s  %d/100 — %s\n" "Model choice:" "$MODEL_SCORE" "$MODEL_RATING"
echo "  --------------------------------"
printf "  %-20s  %d/100\n" "OVERALL:" "$OVERALL_SCORE"
echo ""

echo "============================================"
echo "   TOP 3 COST REDUCTION RECOMMENDATIONS"
echo "============================================"
echo ""

# Recommendation 1
if [ "$HB_SCORE" -lt 70 ]; then
  OPTIMAL_HB=1800
  CURRENT_HB_COST=$HB_COST_DAY
  OPTIMAL_HB_CALLS=$(echo "86400 / $OPTIMAL_HB" | bc)
  OPTIMAL_HB_COST=$(echo "scale=8; $OPTIMAL_HB_CALLS * $HB_COST_CALL" | bc)
  SAVINGS=$(echo "scale=4; ($CURRENT_HB_COST - $OPTIMAL_HB_COST) * 365" | bc)
  echo "1. 🔧 Increase heartbeat interval"
  echo "   Current: ${HEARTBEAT_INTERVAL}s → Recommended: ${OPTIMAL_HB}s"
  SAVINGS_FMT=$(printf "% .4f" "$SAVINGS")
  echo "   Estimated annual savings: ~\$ $SAVINGS_FMT"
  echo ""
fi

# Recommendation 2
if [ "$PROVIDER" = "openai" ] || [ "$PROVIDER" = "anthropic" ]; then
  OPENAI_MONTH=$TOTAL_MONTH
  MINI_COST=$(echo "scale=4; $OPENAI_MONTH * 0.05" | bc)
  echo "2. 💡 Switch to MiniMax M2"
  echo "   Current provider: $PROVIDER"
  echo "   Estimated monthly savings: ~\$$MINI_COST (95% reduction)"
  echo ""
fi

# Recommendation 3
if [ "$TOOL_COUNT" -gt 20 ]; then
  echo "3. ⚡ Audit active tools"
  echo "   $TOOL_COUNT tools detected — many may be unused"
  echo "   Disable unused tools to reduce overhead calls"
  echo ""
fi

# Default recommendations if none above apply
if [ "$HB_SCORE" -ge 70 ] && [ "$PROVIDER" = "minimax" ] && [ "$TOOL_COUNT" -le 20 ]; then
  echo "1. ✅ Configuration looks well-optimized"
  echo "   No major cost issues detected"
  echo "   Consider batching tasks for further savings"
  echo ""
fi

echo "============================================"
echo "   SAVINGS POTENTIAL SUMMARY"
echo "============================================"
echo ""

MAX_SAVINGS=$(echo "scale=4; $TOTAL_YEAR * 0.95" | bc)
CONSERVATIVE_SAVINGS=$(echo "scale=4; $TOTAL_YEAR * 0.50" | bc)

printf "  Conservative savings:  ~\$%s/year\n" "$CONSERVATIVE_SAVINGS"
printf "  Maximum potential:     ~\$%s/year\n" "$MAX_SAVINGS"
printf "  With current config:  ~\$%s/year\n" "$(printf '%.4f' $TOTAL_YEAR)"
echo ""
echo "============================================"
echo ""
echo "Run heartbeat_diagnosis.sh for heartbeat-only analysis"
echo "Run estimate.sh for custom parameter estimates"
echo "Example: HEARTBEAT_INTERVAL=300 ./estimate.sh 300 30 8000 2000 minimax"
echo ""
