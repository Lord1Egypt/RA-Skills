#!/usr/bin/env bash
# CostClaw Token Usage Analyzer v0.2
# Zero-setup: reads your actual workspace and config, outputs prioritized savings
# Usage: ./analyze.sh [workspace_path] [text|json]
set -euo pipefail

WORKSPACE="${1:-$(pwd)}"
FORMAT="${2:-text}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Load pricing
source "$SCRIPT_DIR/pricing.env" 2>/dev/null || true

# --- Color codes (disabled for json) ---
if [ "$FORMAT" = "text" ]; then
  RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
  BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
else
  RED=''; GREEN=''; YELLOW=''; BLUE=''; CYAN=''; BOLD=''; NC=''
fi

# --- Detect default model from gateway config ---
detect_model() {
  local config_paths=(
    "$HOME/.openclaw/config.yaml"
    "$HOME/.openclaw/config.yml"
    "$HOME/.openclaw/openclaw.yaml"
    "$HOME/.openclaw/openclaw.yml"
  )
  for cfg in "${config_paths[@]}"; do
    if [ -f "$cfg" ]; then
      # Try to extract model from config
      local model
      model=$(grep -E '^\s*(model|default_model|primary):' "$cfg" 2>/dev/null | head -1 | sed 's/.*: *//' | tr -d '"' | tr -d "'")
      if [ -n "$model" ]; then
        echo "$model"
        return
      fi
    fi
  done
  # Fallback: check env or assume Sonnet
  echo "${OPENCLAW_MODEL:-anthropic/claude-sonnet-4-5}"
}

# --- Get pricing for model ---
get_input_price() {
  local model="$1"
  case "$model" in
    *opus*)   echo "${OPUS_INPUT:-15.00}" ;;
    *sonnet*) echo "${SONNET_INPUT:-3.00}" ;;
    *haiku*)  echo "${HAIKU_INPUT:-0.80}" ;;
    *gpt-4.1-mini*|*gpt-4o-mini*) echo "${GPT41MINI_INPUT:-0.40}" ;;
    *gpt-4.1*|*gpt-4o*) echo "${GPT41_INPUT:-2.00}" ;;
    *o3*)     echo "${O3_INPUT:-2.00}" ;;
    *o4-mini*) echo "${O4MINI_INPUT:-1.10}" ;;
    *gemini*2.5*pro*|*gemini*pro*) echo "${GEMINI25PRO_INPUT:-1.25}" ;;
    *gemini*flash*) echo "${GEMINI25FLASH_INPUT:-0.15}" ;;
    *)        echo "3.00" ;; # Sonnet-equivalent default
  esac
}

get_output_price() {
  local model="$1"
  case "$model" in
    *opus*)   echo "${OPUS_OUTPUT:-75.00}" ;;
    *sonnet*) echo "${SONNET_OUTPUT:-15.00}" ;;
    *haiku*)  echo "${HAIKU_OUTPUT:-4.00}" ;;
    *gpt-4.1-mini*|*gpt-4o-mini*) echo "${GPT41MINI_OUTPUT:-1.60}" ;;
    *gpt-4.1*|*gpt-4o*) echo "${GPT41_OUTPUT:-8.00}" ;;
    *o3*)     echo "${O3_OUTPUT:-8.00}" ;;
    *o4-mini*) echo "${O4MINI_OUTPUT:-4.40}" ;;
    *gemini*2.5*pro*|*gemini*pro*) echo "${GEMINI25PRO_OUTPUT:-10.00}" ;;
    *gemini*flash*) echo "${GEMINI25FLASH_OUTPUT:-0.60}" ;;
    *)        echo "15.00" ;; # Sonnet-equivalent default
  esac
}

get_model_tier() {
  local model="$1"
  case "$model" in
    *opus*)   echo "premium" ;;
    *sonnet*|*gpt-4.1|*gpt-4o|*o3*|*gemini*pro*) echo "standard" ;;
    *haiku*|*mini*|*flash*) echo "economy" ;;
    *)        echo "standard" ;;
  esac
}

# --- Calculation helpers ---
# Ensure bc output has leading zero (e.g., ".69" -> "0.69")
fix_bc() {
  local val
  val=$(bc)
  [[ "$val" == .* ]] && val="0${val}"
  [[ "$val" == -.* ]] && val="-0${val#-}"
  [ -z "$val" ] && val="0.00"
  echo "$val"
}

# monthly_input_cost(tokens_per_turn, turns_per_day, price_per_mtok)
monthly_input_cost() {
  echo "scale=2; $1 * $2 * 30 / 1000000 * $3" | fix_bc
}

# --- Main analysis ---
MODEL=$(detect_model)
INPUT_PRICE=$(get_input_price "$MODEL")
OUTPUT_PRICE=$(get_output_price "$MODEL")
MODEL_TIER=$(get_model_tier "$MODEL")
TURNS_PER_DAY=20  # Conservative estimate

# ═══════════════════════════════════════
# SECTION 1: Workspace Files
# ═══════════════════════════════════════
declare -a file_names=()
declare -a file_tokens=()
declare -a file_monthly=()
total_ws_tokens=0

if [ "$FORMAT" = "text" ]; then
  echo -e "${BOLD}${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
  echo -e "${BOLD}${BLUE}║         CostClaw Token Analyzer v0.2                  ║${NC}"
  echo -e "${BOLD}${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
  echo ""
  echo -e "${BOLD}${CYAN}📁 Workspace Files${NC} (injected every turn)"
  echo "────────────────────────────────────────────────────────"
fi

for f in "$WORKSPACE"/*.md; do
  [ -f "$f" ] || continue
  name=$(basename "$f")
  bytes=$(wc -c < "$f" | tr -d ' ')
  # ~4 chars per token for English markdown
  est_tokens=$((bytes / 4))
  total_ws_tokens=$((total_ws_tokens + est_tokens))
  
  # Monthly cost for this file
  mo_cost=$(echo "scale=2; $est_tokens * $TURNS_PER_DAY * 30 / 1000000 * $INPUT_PRICE" | fix_bc)
  
  file_names+=("$name")
  file_tokens+=("$est_tokens")
  file_monthly+=("$mo_cost")
  
  if [ "$FORMAT" = "text" ]; then
    if [ "$est_tokens" -gt 10000 ]; then
      flag="${RED}⚠ LARGE${NC}"
    elif [ "$est_tokens" -gt 5000 ]; then
      flag="${YELLOW}⚡ MEDIUM${NC}"
    elif [ "$est_tokens" -gt 2000 ]; then
      flag="${CYAN}• OK${NC}"
    else
      flag="${GREEN}✓ Small${NC}"
    fi
    printf "  %-28s %6d tok  \$%6s/mo  %b\n" "$name" "$est_tokens" "$mo_cost" "$flag"
  fi
done

if [ "$FORMAT" = "text" ]; then
  echo "────────────────────────────────────────────────────────"
  total_ws_monthly=$(echo "scale=2; $total_ws_tokens * $TURNS_PER_DAY * 30 / 1000000 * $INPUT_PRICE" | fix_bc)
  printf "  ${BOLD}%-28s %6d tok  \$%6s/mo${NC}\n" "TOTAL" "$total_ws_tokens" "$total_ws_monthly"
fi

# ═══════════════════════════════════════
# SECTION 2: Skills
# ═══════════════════════════════════════
skill_count=0
skill_total_tokens=0

if [ -d "$WORKSPACE/skills" ]; then
  for skill_dir in "$WORKSPACE/skills"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_count=$((skill_count + 1))
    # Skill descriptions in system prompt average ~350 tokens each
    skill_total_tokens=$((skill_total_tokens + 350))
  done
fi

# Also count system-installed skills
sys_skill_dir="/opt/homebrew/lib/node_modules/openclaw/skills"
sys_skill_count=0
if [ -d "$sys_skill_dir" ]; then
  for skill_dir in "$sys_skill_dir"/*/; do
    [ -d "$skill_dir" ] || continue
    sys_skill_count=$((sys_skill_count + 1))
    skill_total_tokens=$((skill_total_tokens + 350))
  done
fi

total_skill_count=$((skill_count + sys_skill_count))
skill_monthly=$(echo "scale=2; $skill_total_tokens * $TURNS_PER_DAY * 30 / 1000000 * $INPUT_PRICE" | fix_bc)

if [ "$FORMAT" = "text" ]; then
  echo ""
  echo -e "${BOLD}${CYAN}🔧 Skills${NC}"
  echo "────────────────────────────────────────────────────────"
  echo "  Workspace skills: $skill_count"
  echo "  System skills:    $sys_skill_count"
  echo "  Total:            $total_skill_count (~${skill_total_tokens} tok/turn, \$${skill_monthly}/mo)"
fi

# ═══════════════════════════════════════
# SECTION 3: Model & Pricing
# ═══════════════════════════════════════
if [ "$FORMAT" = "text" ]; then
  echo ""
  echo -e "${BOLD}${CYAN}⚙️  Model & Pricing${NC}"
  echo "────────────────────────────────────────────────────────"
  echo "  Detected model: $MODEL"
  echo "  Tier:           $MODEL_TIER"
  echo "  Input:          \$${INPUT_PRICE}/MTok"
  echo "  Output:         \$${OUTPUT_PRICE}/MTok"
fi

# ═══════════════════════════════════════
# SECTION 4: Cost Summary
# ═══════════════════════════════════════
total_input_tokens=$((total_ws_tokens + skill_total_tokens + 3000)) # +3K for system prompt
avg_output_tokens=2000

daily_input=$(echo "scale=2; $total_input_tokens * $TURNS_PER_DAY / 1000000 * $INPUT_PRICE" | fix_bc)
daily_output=$(echo "scale=2; $avg_output_tokens * $TURNS_PER_DAY / 1000000 * $OUTPUT_PRICE" | fix_bc)
daily_total=$(echo "scale=2; $daily_input + $daily_output" | fix_bc)
monthly_total=$(echo "scale=2; $daily_total * 30" | fix_bc)

if [ "$FORMAT" = "text" ]; then
  echo ""
  echo -e "${BOLD}${CYAN}💰 Cost Estimate${NC} (${TURNS_PER_DAY} turns/day)"
  echo "────────────────────────────────────────────────────────"
  echo "  Input per turn:     ~${total_input_tokens} tokens"
  echo "  Output per turn:    ~${avg_output_tokens} tokens"
  echo ""
  echo "  Daily input:        \$${daily_input}"
  echo "  Daily output:       \$${daily_output}"
  echo -e "  ${BOLD}Daily total:         \$${daily_total}${NC}"
  echo -e "  ${BOLD}${RED}Monthly estimate:    \$${monthly_total}${NC}"
fi

# ═══════════════════════════════════════
# SECTION 5: Ranked Recommendations
# ═══════════════════════════════════════
declare -a rec_descriptions=()
declare -a rec_savings=()
declare -a rec_actions=()

# Check for oversized workspace files (>5K tokens)
for i in "${!file_names[@]}"; do
  tokens="${file_tokens[$i]}"
  name="${file_names[$i]}"
  if [ "$tokens" -gt 10000 ]; then
    target=5000
    save_tokens=$((tokens - target))
    save_monthly=$(echo "scale=2; $save_tokens * $TURNS_PER_DAY * 30 / 1000000 * $INPUT_PRICE" | fix_bc)
    rec_descriptions+=("Trim ${name} from ${tokens} to ~${target} tokens")
    rec_savings+=("$save_monthly")
    rec_actions+=("Move rarely-used sections to memory/ files. Archive old content. Keep only what's needed every turn.")
  elif [ "$tokens" -gt 5000 ]; then
    target=3000
    save_tokens=$((tokens - target))
    save_monthly=$(echo "scale=2; $save_tokens * $TURNS_PER_DAY * 30 / 1000000 * $INPUT_PRICE" | fix_bc)
    rec_descriptions+=("Trim ${name} from ${tokens} to ~${target} tokens")
    rec_savings+=("$save_monthly")
    rec_actions+=("Move rarely-used sections to separate files loaded on-demand.")
  fi
done

# Check model tier — if premium, suggest routing
if [ "$MODEL_TIER" = "premium" ]; then
  # Estimate savings from routing heartbeats + simple tasks to Haiku
  # Assume 30% of turns are simple/heartbeat
  simple_turns=$((TURNS_PER_DAY * 30 / 100))
  opus_simple_cost=$(echo "scale=2; $simple_turns * $total_input_tokens / 1000000 * $INPUT_PRICE * 30" | fix_bc)
  haiku_simple_cost=$(echo "scale=2; $simple_turns * $total_input_tokens / 1000000 * ${HAIKU_INPUT:-0.80} * 30" | fix_bc)
  routing_save=$(echo "scale=2; $opus_simple_cost - $haiku_simple_cost" | fix_bc)
  rec_descriptions+=("Route simple tasks & heartbeats to Claude Haiku")
  rec_savings+=("$routing_save")
  rec_actions+=("Add model overrides in cron jobs: model=anthropic/claude-haiku-4. For heartbeats, configure a cheaper model in gateway config.")
fi

# Check skill count
if [ "$total_skill_count" -gt 15 ]; then
  excess=$((total_skill_count - 10))
  save_tokens=$((excess * 350))
  save_monthly=$(echo "scale=2; $save_tokens * $TURNS_PER_DAY * 30 / 1000000 * $INPUT_PRICE" | fix_bc)
  rec_descriptions+=("Reduce active skills from ${total_skill_count} to ~10")
  rec_savings+=("$save_monthly")
  rec_actions+=("Disable unused skills. Consider lazy loading: keep a skill index, load individual skills on-demand.")
fi

# Always recommend: heartbeat cache alignment (if not already mentioned)
# Estimate: saving 1 cache-write per day = significant
cache_write_savings=$(echo "scale=2; $total_input_tokens / 1000000 * ${OPUS_CACHE_WRITE:-18.75} * 30" | fix_bc 2>/dev/null || echo "1.00")
rec_descriptions+=("Align heartbeat to 55min (Anthropic cache TTL)")
rec_savings+=("$cache_write_savings")
rec_actions+=("Set heartbeat interval to 55 minutes. Keeps Anthropic's 1h prompt cache warm, paying cache-read rates instead of cache-write rates.")

# Always recommend: enable compaction
rec_descriptions+=("Enable aggressive context compaction")
rec_savings+=("2.00")
rec_actions+=("Set compaction.mode to 'aggressive' with maxTokens: 8000 in gateway config. Auto-trims long conversations.")

# Sort recommendations by savings (descending) — simple bubble sort
n=${#rec_descriptions[@]}
for ((i = 0; i < n; i++)); do
  for ((j = i + 1; j < n; j++)); do
    if (( $(echo "${rec_savings[$j]} > ${rec_savings[$i]}" | bc -l) )); then
      # Swap
      tmp="${rec_descriptions[$i]}"; rec_descriptions[$i]="${rec_descriptions[$j]}"; rec_descriptions[$j]="$tmp"
      tmp="${rec_savings[$i]}"; rec_savings[$i]="${rec_savings[$j]}"; rec_savings[$j]="$tmp"
      tmp="${rec_actions[$i]}"; rec_actions[$i]="${rec_actions[$j]}"; rec_actions[$j]="$tmp"
    fi
  done
done

# Calculate total potential savings
total_savings=0
for s in "${rec_savings[@]}"; do
  total_savings=$(echo "scale=2; $total_savings + $s" | fix_bc)
done
optimized_monthly=$(echo "scale=2; $monthly_total - $total_savings" | fix_bc)
# Floor at $0
if (( $(echo "$optimized_monthly < 0" | bc -l) )); then
  optimized_monthly="0.00"
fi
if (( $(echo "$monthly_total > 0" | bc -l) )); then
  pct_savings=$(echo "scale=0; $total_savings * 100 / $monthly_total" | fix_bc 2>/dev/null || echo "0")
else
  pct_savings=0
fi

if [ "$FORMAT" = "text" ]; then
  echo ""
  echo -e "${BOLD}${CYAN}📋 Recommendations${NC} (ranked by savings)"
  echo "════════════════════════════════════════════════════════"
  
  for i in "${!rec_descriptions[@]}"; do
    rank=$((i + 1))
    echo -e "  ${BOLD}${rank}. ${rec_descriptions[$i]}${NC}"
    echo -e "     ${GREEN}💵 Save ~\$${rec_savings[$i]}/month${NC}"
    echo "     → ${rec_actions[$i]}"
    echo ""
  done
  
  echo "════════════════════════════════════════════════════════"
  echo -e "  ${BOLD}Current monthly:     \$${monthly_total}${NC}"
  echo -e "  ${BOLD}${GREEN}Optimized monthly:   \$${optimized_monthly} (save ${pct_savings}%)${NC}"
  echo "════════════════════════════════════════════════════════"
fi

# ═══════════════════════════════════════
# JSON Output
# ═══════════════════════════════════════
if [ "$FORMAT" = "json" ]; then
  # Build JSON manually (no jq dependency)
  echo "{"
  echo "  \"analyzer_version\": \"0.2.0\","
  echo "  \"workspace\": \"$WORKSPACE\","
  echo "  \"model\": \"$MODEL\","
  echo "  \"model_tier\": \"$MODEL_TIER\","
  echo "  \"input_price_per_mtok\": $INPUT_PRICE,"
  echo "  \"output_price_per_mtok\": $OUTPUT_PRICE,"
  echo "  \"turns_per_day\": $TURNS_PER_DAY,"
  echo "  \"workspace_tokens\": $total_ws_tokens,"
  echo "  \"skill_tokens\": $skill_total_tokens,"
  echo "  \"total_input_tokens_per_turn\": $total_input_tokens,"
  echo "  \"daily_cost\": $daily_total,"
  echo "  \"monthly_cost\": $monthly_total,"
  echo "  \"optimized_monthly\": $optimized_monthly,"
  echo "  \"savings_percent\": $pct_savings,"
  echo "  \"files\": ["
  for i in "${!file_names[@]}"; do
    comma=""
    [ "$i" -lt $((${#file_names[@]} - 1)) ] && comma=","
    echo "    {\"name\": \"${file_names[$i]}\", \"tokens\": ${file_tokens[$i]}, \"monthly_cost\": ${file_monthly[$i]}}${comma}"
  done
  echo "  ],"
  echo "  \"recommendations\": ["
  for i in "${!rec_descriptions[@]}"; do
    comma=""
    [ "$i" -lt $((${#rec_descriptions[@]} - 1)) ] && comma=","
    # Escape quotes in description
    desc=$(echo "${rec_descriptions[$i]}" | sed 's/"/\\"/g')
    action=$(echo "${rec_actions[$i]}" | sed 's/"/\\"/g')
    echo "    {\"rank\": $((i+1)), \"description\": \"$desc\", \"monthly_savings\": ${rec_savings[$i]}, \"action\": \"$action\"}${comma}"
  done
  echo "  ]"
  echo "}"
fi
