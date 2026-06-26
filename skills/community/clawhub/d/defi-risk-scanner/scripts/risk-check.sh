#!/usr/bin/env bash
# DeFi Risk Scanner - Production Risk Check Script
# 用法: ./risk-check.sh <protocol_name|address> [chain]
# 示例: ./risk-check.sh aave ethereum
#       ./risk-check.sh 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9 ethereum
set -e

TARGET="${1:-}"
CHAIN="${2:-ethereum}"
OUTPUT=""

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
  echo ""
  echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}  🔍 DeFi Risk Scanner - 风险评估报告${NC}"
  echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
  echo "  目标: $TARGET"
  echo "  链:   $CHAIN"
  echo -e "${CYAN}───────────────────────────────────────────────────${NC}"
}

print_section() {
  echo ""
  echo -e "${YELLOW}▶ $1${NC}"
  echo "  ─────────────────────────────────"
}

score_for() {
  local condition=$1
  local score=$2
  if eval "$condition"; then
    echo "$score"
  else
    echo "0"
  fi
}

format_tvl() {
  local val=$1
  # Convert scientific notation to plain integer
  val=$(echo "$val" | awk '{printf "%.0f", $1}')
  if awk "BEGIN {exit !($val > 1000000000)}"; then
    awk "BEGIN {printf \"%.2fB\", $val/1000000000}"
  elif awk "BEGIN {exit !($val > 1000000)}"; then
    awk "BEGIN {printf \"%.2fM\", $val/1000000}"
  elif awk "BEGIN {exit !($val > 1000)}"; then
    awk "BEGIN {printf \"%.2fK\", $val/1000}"
  else
    echo "$val"
  fi
}

calculate_protocol_risk() {
  local tvl_usd="$1"
  local chains="$2"
  local symbol="$3"
  local name="$4"
  
  local score=50  # start neutral
  
  # TVL scoring (40 points max) - use awk for big number comparisons
  local tvl_pts=0
  if [[ -n "$tvl_usd" && "$tvl_usd" != "null" ]]; then
    if awk "BEGIN {exit !($tvl_usd > 1000000000)}"; then
      tvl_pts=40
    elif awk "BEGIN {exit !($tvl_usd > 100000000)}"; then
      tvl_pts=30
    elif awk "BEGIN {exit !($tvl_usd > 10000000)}"; then
      tvl_pts=20
    elif awk "BEGIN {exit !($tvl_usd > 1000000)}"; then
      tvl_pts=10
    else
      tvl_pts=5
    fi
  fi
  
  # Chain diversity (10 points max)
  local chain_count=$(echo "$chains" | jq 'length' 2>/dev/null || echo 0)
  local chain_pts=0
  if (( chain_count >= 5 )); then
    chain_pts=10
  elif (( chain_count >= 2 )); then
    chain_pts=6
  elif (( chain_count >= 1 )); then
    chain_pts=3
  fi
  
  # Name recognition bonus (10 points max)
  local name_pts=0
  case "${name,,}" in
    *aave*|*uniswap*|*curve*|*compound*|*maker*|*synthetix*) name_pts=10 ;;
    *lido*) name_pts=8 ;;
    *) name_pts=0 ;;
  esac
  
  # Symbol check
  if [[ -z "$symbol" || "$symbol" == "null" ]]; then
    name_pts=$((name_pts - 5))
    (( name_pts < 0 )) && name_pts=0
  fi
  
  local total=$((50 + tvl_pts + chain_pts + name_pts))
  (( total > 100 )) && total=100
  echo "$total"
}

calculate_token_risk() {
  local price_usd="$1"
  local market_cap="$2"
  local liquidity_usd="$3"
  local h24_vol="$4"
  local fdv="$5"
  
  local score=50
  
  # Market cap / FDV ratio (20 pts) - use awk
  local ratio=0
  if [[ -n "$market_cap" && "$market_cap" != "null" && -n "$fdv" && "$fdv" != "null" ]] && awk "BEGIN {exit !($fdv > 0)}"; then
    ratio=$(awk "BEGIN {printf \"%.4f\", $market_cap / $fdv}")
    if awk "BEGIN {exit !($ratio >= 0.8)}"; then
      score=$((score + 20))
    elif awk "BEGIN {exit !($ratio >= 0.5)}"; then
      score=$((score + 10))
    elif awk "BEGIN {exit !($ratio >= 0.2)}"; then
      score=$((score + 0))
    else
      score=$((score - 15))
    fi
  fi
  
  # Liquidity vs Market Cap (20 pts)
  if [[ -n "$liquidity_usd" && "$liquidity_usd" != "null" && -n "$market_cap" && "$market_cap" != "null" ]] && awk "BEGIN {exit !($market_cap > 0)}"; then
    local liq_ratio=$(awk "BEGIN {printf \"%.4f\", $liquidity_usd / $market_cap}")
    if awk "BEGIN {exit !($liq_ratio >= 0.1)}"; then
      score=$((score + 20))
    elif awk "BEGIN {exit !($liq_ratio >= 0.05)}"; then
      score=$((score + 10))
    elif awk "BEGIN {exit !($liq_ratio >= 0.01)}"; then
      score=$((score + 0))
    else
      score=$((score - 20))
    fi
  fi
  
  # 24h Volume / Liquidity ratio (10 pts)
  if [[ -n "$h24_vol" && "$h24_vol" != "null" && -n "$liquidity_usd" && "$liquidity_usd" != "null" ]] && awk "BEGIN {exit !($liquidity_usd > 0)}"; then
    local vol_ratio=$(awk "BEGIN {printf \"%.4f\", $h24_vol / $liquidity_usd}")
    if awk "BEGIN {exit !($vol_ratio >= 0.05)}"; then
      score=$((score + 10))
    elif awk "BEGIN {exit !($vol_ratio >= 0.01)}"; then
      score=$((score + 5))
    fi
  fi
  
  # FDV check
  if [[ -n "$fdv" && "$fdv" != "null" ]]; then
    if awk "BEGIN {exit !($fdv < 10000000)}"; then
      score=$((score - 5))
    fi
    if awk "BEGIN {exit !($fdv > 10000000000)}"; then
      score=$((score + 5))
    fi
  fi
  
  (( score < 0 )) && score=0
  (( score > 100 )) && score=100
  echo "$score"
}

get_risk_level() {
  local score=$1
  if (( score >= 80 )); then
    echo "🟢 低风险 | 安全"
  elif (( score >= 60 )); then
    echo "🟡 中低风险 | 可接受"
  elif (( score >= 40 )); then
    echo "🟠 中高风险 | 谨慎"
  elif (( score >= 20 )); then
    echo "🔴 高风险 | 警告"
  else
    echo "⚫ 极高风险 | 危险"
  fi
}

# ─── MAIN ───────────────────────────────────────────────────────
if [ -z "$TARGET" ]; then
  echo "用法: $0 <protocol_name|address> [chain]"
  echo "示例: $0 aave ethereum"
  echo "      $0 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9 ethereum"
  exit 1
fi

print_header

IS_ADDRESS=0
if [[ "$TARGET" =~ ^0x[a-fA-F0-9]{10,}$ ]]; then
  IS_ADDRESS=1
fi

# ══════════════════════════════════════════════════════
# MODE 1: Protocol Name (by DefiLlama)
# ══════════════════════════════════════════════════════
if [ "$IS_ADDRESS" -eq 0 ]; then
  
  print_section "📊 DefiLlama 链上数据"
  
  # Fetch protocol data
  LLAMA_DATA=$(curl -s --max-time 10 "https://api.llama.fi/protocol/$TARGET" 2>/dev/null)
  
  if echo "$LLAMA_DATA" | jq -e '.name' >/dev/null 2>&1; then
    NAME=$(echo "$LLAMA_DATA" | jq -r '.name')
    SYMBOL=$(echo "$LLAMA_DATA" | jq -r '.symbol // empty')
    DESCRIPTION=$(echo "$LLAMA_DATA" | jq -r '.description // empty' | cut -c1-100)
    URL=$(echo "$LLAMA_DATA" | jq -r '.url // empty')
    TWITTER=$(echo "$LLAMA_DATA" | jq -r '.twitter // empty')
    
    echo "  名称:         $NAME"
    [[ -n "$SYMBOL" ]] && echo "  符号:         $SYMBOL"
    [[ -n "$URL" ]] && echo "  官网:         $URL"
    [[ -n "$TWITTER" ]] && echo "  Twitter:      @$TWITTER"
    [[ -n "$DESCRIPTION" ]] && echo "  描述:         $DESCRIPTION..."
    
    # Calculate TVL from currentChainTvls (sum positive values only)
    CHAIN_TVLS=$(echo "$LLAMA_DATA" | jq -r '.currentChainTvls // {}')
    if [ -n "$CHAIN_TVLS" ] && [ "$CHAIN_TVLS" != "{}" ]; then
      # Sum all positive TVL values (exclude negative borrowed values)
      # jq may return scientific notation, convert to regular number
      TVL_SUM=$(echo "$CHAIN_TVLS" | jq 'map(select(. > 0)) | add' 2>/dev/null | awk '{printf "%.0f", $1}' || echo "0")
      TVL_DISPLAY=$(format_tvl "$TVL_SUM")
      echo "  TVL:          \$$TVL_DISPLAY USD"
    fi
    
    # Chain diversity
    CHAIN_COUNT=$(echo "$LLAMA_DATA" | jq '.chains | length' 2>/dev/null || echo 0)
    if (( CHAIN_COUNT > 0 )); then
      CHAIN_LIST=$(echo "$LLAMA_DATA" | jq -r '.chains | .[]' 2>/dev/null)
      echo "  覆盖链:       $CHAIN_LIST"
      echo "  链数量:       $CHAIN_COUNT"
    fi
    
    # Check for staking / pool2
    STAKE_TVL=$(echo "$CHAIN_TVLS" | jq '."staking" // ."Ethereum-staking" // 0' 2>/dev/null)
    POOL2_TVL=$(echo "$CHAIN_TVLS" | jq '."pool2" // ."Ethereum-pool2" // 0' 2>/dev/null)
    
    echo ""
    echo "  风险评分计算..."
    TOTAL_SCORE=$(calculate_protocol_risk "$TVL_SUM" "$CHAIN_LIST" "$SYMBOL" "$NAME")
    RISK_LEVEL=$(get_risk_level "$TOTAL_SCORE")
    echo "  ─────────────────────────────────"
    echo -e "  综合评分:     ${CYAN}$TOTAL_SCORE/100${NC} $RISK_LEVEL"
    echo "  ─────────────────────────────────"
    
    # Risk factors
    echo ""
    echo "  风险因子拆解:"
    
    # TVL analysis (use awk for big numbers)
    if awk "BEGIN {exit !(${TVL_SUM:-0} > 1000000000)}"; then
      echo -e "    ${GREEN}✅ TVL > \$1B — 高度可信${NC}"
    elif awk "BEGIN {exit !(${TVL_SUM:-0} > 100000000)}"; then
      echo -e "    ${GREEN}✅ TVL > \$100M — 良好${NC}"
    elif awk "BEGIN {exit !(${TVL_SUM:-0} > 10000000)}"; then
      echo -e "    ${YELLOW}⚠️  TVL 中等（\$10M-\$100M）${NC}"
    elif awk "BEGIN {exit !(${TVL_SUM:-0} > 0)}"; then
      echo -e "    ${YELLOW}⚠️  TVL 较低（<\$10M）— 流动性可能被操控${NC}"
    else
      echo -e "    ${RED}❌ TVL 未找到或为 0${NC}"
    fi
    
    # Chain diversity
    if (( CHAIN_COUNT >= 5 )); then
      echo -e "    ${GREEN}✅ 多链部署（$CHAIN_COUNT 条链）— 分散风险${NC}"
    elif (( CHAIN_COUNT >= 2 )); then
      echo -e "    ${YELLOW}⚠️  覆盖 $CHAIN_COUNT 条链${NC}"
    fi
    
    # Staking / pool2 analysis
    if awk "BEGIN {exit !(${STAKE_TVL:-0} > 100000000)}"; then
      echo -e "    ${GREEN}✅ 有质押池（\$$(format_tvl ${STAKE_TVL:-0})）${NC}"
    fi
    if awk "BEGIN {exit !(${POOL2_TVL:-0} > 100000)}"; then
      echo -e "    ${YELLOW}⚠️  有 Pool2（\$$(format_tvl ${POOL2_TVL:-0})）${NC}"
    fi
    
    # Name recognition
    case "${NAME,,}" in
      *aave*|*uniswap*|*curve*|*compound*|*maker*|*lido*|*synthetix*)
        echo -e "    ${GREEN}✅ 知名协议，长期运营${NC}"
        ;;
    esac
    
  else
    echo "  ❌ 未找到协议: $TARGET"
    echo "  提示: 尝试使用协议 slug (例如 'aave-v3' 而非 'Aave V3')"
    TOTAL_SCORE=20
    RISK_LEVEL=$(get_risk_level 20)
  fi

# ══════════════════════════════════════════════════════
# MODE 2: Token Address (by DexScreener)
# ══════════════════════════════════════════════════════
else
  
  print_section "📊 DexScreener 流动性数据"
  
  DEX_DATA=$(curl -s --max-time 10 "https://api.dexscreener.com/latest/dex/tokens/$TARGET" 2>/dev/null)
  
  if echo "$DEX_DATA" | jq -e '.pairs | length > 0' >/dev/null 2>&1; then
    # Get the pair with highest liquidity
    PAIR_DATA=$(echo "$DEX_DATA" | jq -r '.pairs | sort_by(.liquidity.usd // 0) | reverse | .[0]')
    
    TOKEN_NAME=$(echo "$PAIR_DATA" | jq -r '.baseToken.name // empty')
    TOKEN_SYMBOL=$(echo "$PAIR_DATA" | jq -r '.baseToken.symbol // empty')
    PRICE_USD=$(echo "$PAIR_DATA" | jq -r '.priceUsd // empty')
    MARKET_CAP=$(echo "$PAIR_DATA" | jq -r '.marketCap // empty')
    LIQUIDITY_USD=$(echo "$PAIR_DATA" | jq -r '.liquidity.usd // empty')
    H24_VOL=$(echo "$PAIR_DATA" | jq -r '.volume.h24 // empty')
    FDV=$(echo "$PAIR_DATA" | jq -r '.fdv // empty')
    CHAIN_ID=$(echo "$PAIR_DATA" | jq -r '.chainId // empty')
    DEX_ID=$(echo "$PAIR_DATA" | jq -r '.dexId // empty')
    PRICE_CHANGE_24H=$(echo "$PAIR_DATA" | jq -r '.priceChange.h24 // empty')
    
    echo "  代币名称:     $TOKEN_NAME"
    echo "  符号:         $TOKEN_SYMBOL"
    [[ -n "$PRICE_USD" && "$PRICE_USD" != "null" ]] && echo "  当前价格:     \$$PRICE_USD"
    [[ -n "$MARKET_CAP" && "$MARKET_CAP" != "null" ]] && echo "  市值:         \$$(format_tvl $MARKET_CAP) (FDV: \$$(format_tvl $FDV))"
    [[ -n "$LIQUIDITY_USD" && "$LIQUIDITY_USD" != "null" ]] && echo "  流动性:       \$$(format_tvl $LIQUIDITY_USD)"
    [[ -n "$H24_VOL" && "$H24_VOL" != "null" ]] && echo "  24h 交易量:   \$$(format_tvl $H24_VOL)"
    [[ -n "$PRICE_CHANGE_24H" && "$PRICE_CHANGE_24H" != "null" ]] && echo "  24h 涨跌:     ${PRICE_CHANGE_24H}%"
    echo "  链:           $CHAIN_ID"
    echo "  DEX:          $DEX_ID"
    
    # Count total pairs
    PAIR_COUNT=$(echo "$DEX_DATA" | jq -r '.pairs | length')
    echo "  发现交易对:   $PAIR_COUNT 个"
    
    echo ""
    echo "  风险评分计算..."
    TOTAL_SCORE=$(calculate_token_risk "$PRICE_USD" "$MARKET_CAP" "$LIQUIDITY_USD" "$H24_VOL" "$FDV")
    RISK_LEVEL=$(get_risk_level "$TOTAL_SCORE")
    echo "  ─────────────────────────────────"
    echo -e "  综合评分:     ${CYAN}$TOTAL_SCORE/100${NC} $RISK_LEVEL"
    echo "  ─────────────────────────────────"
    
    echo ""
    echo "  风险因子拆解:"
    
    # Liquidity check (use awk)
    if [[ -n "$LIQUIDITY_USD" && "$LIQUIDITY_USD" != "null" ]]; then
      if awk "BEGIN {exit !($LIQUIDITY_USD > 1000000)}"; then
        echo -e "    ${GREEN}✅ 流动性充足（>\$1M）${NC}"
      elif awk "BEGIN {exit !($LIQUIDITY_USD > 100000)}"; then
        echo -e "    ${YELLOW}⚠️  流动性中等（\$100K-\$1M）${NC}"
      elif awk "BEGIN {exit !($LIQUIDITY_USD > 0)}"; then
        echo -e "    ${RED}❌ 流动性极低（<\$100K）— 容易被操控${NC}"
      fi
    fi
    
    # Market Cap / FDV ratio
    if [[ -n "$MARKET_CAP" && "$MARKET_CAP" != "null" && -n "$FDV" && "$FDV" != "null" ]]; then
      RATIO=$(awk "BEGIN {printf \"%.4f\", $MARKET_CAP / $FDV}")
      if awk "BEGIN {exit !($RATIO >= 0.9)}"; then
        echo -e "    ${GREEN}✅ 市值/FDV 比 $RATIO — 流通量健康${NC}"
      elif awk "BEGIN {exit !($RATIO >= 0.5)}"; then
        echo -e "    ${YELLOW}⚠️  市值/FDV 比 $RATIO — 部分代币未释放${NC}"
      else
        echo -e "    ${RED}❌ 市值/FDV 比 $RATIO — 大量代币未解锁，风险高${NC}"
      fi
    fi
    
    # Market cap size
    if [[ -n "$MARKET_CAP" && "$MARKET_CAP" != "null" ]]; then
      if awk "BEGIN {exit !($MARKET_CAP > 1000000000)}"; then
        echo -e "    ${GREEN}✅ 市值 >\$1B — 主流代币${NC}"
      elif awk "BEGIN {exit !($MARKET_CAP > 100000000)}"; then
        echo -e "    ${GREEN}✅ 市值 >\$100M — 中型项目${NC}"
      elif awk "BEGIN {exit !($MARKET_CAP > 10000000)}"; then
        echo -e "    ${YELLOW}⚠️  市值中等 — 小型项目${NC}"
      elif awk "BEGIN {exit !($MARKET_CAP > 0)}"; then
        echo -e "    ${RED}❌ 市值 <\$10M — 微型代币，高风险${NC}"
      fi
    fi
    
    # Multiple pairs / DEXs
    if (( PAIR_COUNT >= 3 )); then
      echo -e "    ${GREEN}✅ 多交易所部署（$PAIR_COUNT 个交易对）${NC}"
    elif (( PAIR_COUNT == 1 )); then
      echo -e "    ${YELLOW}⚠️  仅 1 个交易对 — 集中风险${NC}"
    fi
    
  else
    echo "  ❌ 未找到代币: $TARGET"
    echo "  提示: 确认代币已在 DEX（如 Uniswap）上创建了流动性池"
    TOTAL_SCORE=15
    RISK_LEVEL=$(get_risk_level 15)
  fi
  
fi

# ══════════════════════════════════════════════════════
# Common: Audit & Safety Checks
# ══════════════════════════════════════════════════════
print_section "🔐 安全与审计建议"

if [ "$IS_ADDRESS" -eq 0 ]; then
  # For protocols - show audit recommendation
  echo "  审计检查 (手动验证):"
  echo "    • 在 https://immunefi.com/ 查找 Bug Bounty 项目"
  echo "    • 在 https://www.certik.com/ 查询审计报告"
  echo "    • 检查 https://twitter.com/${TWITTER:-} 官方账号"
  echo "    • 在 Etherscan 查看合约是否已验证源码"
fi

echo "  推荐验证步骤:"
echo "    1. 在 https://debank.com/ 查看钱包持仓分布"
echo "    2. 在 https://tokensniffer.com/ 分析代币合约风险"
echo "    3. 在 https://dilation.info/ 检查代币稀释风险"
echo "    4. 在 https://revoke.cash/ 检查授权风险"

# ══════════════════════════════════════════════════════
# Summary & Disclaimer
# ══════════════════════════════════════════════════════
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  综合风险评分: ${CYAN}$TOTAL_SCORE/100${NC} $RISK_LEVEL"
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"

if (( TOTAL_SCORE >= 80 )); then
  echo ""
  echo "  ✅ 结论: 该项目各项指标健康，可持续性良好"
  echo "  💡 建议: 可进行常规参与，建议持续监控"
elif (( TOTAL_SCORE >= 60 )); then
  echo ""
  echo "  ⚠️  结论: 存在少数关注点，建议深入尽调"
  echo "  💡 建议: 仔细阅读白皮书，关注合约审计和团队背景"
elif (( TOTAL_SCORE >= 40 )); then
  echo ""
  echo "  🔶 结论: 多个风险因子，需谨慎评估"
  echo "  💡 建议: 仅用可承受损失的资金参与，充分了解合约风险"
else
  echo ""
  echo "  🔴 结论: 重大风险，不建议参与"
  echo "  💡 建议: 远离此类项目，谨防Rug Pull"
fi

echo ""
echo -e "${YELLOW}⚠️  免责声明${NC}: 以上分析仅供参考，非财务建议。"
echo "  加密货币投资有极高风险，可能导致本金全损。"
echo " DYOR（Do Your Own Research）— 始终自行验证。"
echo ""
