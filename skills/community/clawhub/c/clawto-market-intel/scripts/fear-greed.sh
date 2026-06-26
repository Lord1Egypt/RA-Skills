#!/usr/bin/env bash
# Fear & Greed Index — dual-market sentiment snapshot (mobile-safe)
set -euo pipefail

round() { awk "BEGIN {printf \"%.1f\", $1}" 2>/dev/null || echo "$1"; }

# ── Fetch Crypto F&G ──
crypto_json=$(curl -sf --max-time 10 "https://api.alternative.me/fng/?limit=2" 2>/dev/null || echo '{}')
crypto_now=$(echo "$crypto_json" | jq -r '.data[0].value // "N/A"')
crypto_prev=$(echo "$crypto_json" | jq -r '.data[1].value // "N/A"')

# ── Fetch CNN F&G (美股) ──
cnn_json=$(curl -sf --max-time 10 \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Accept: application/json" \
  -H "Origin: https://edition.cnn.com" \
  "https://production.dataviz.cnn.io/index/fearandgreed/graphdata" 2>/dev/null || echo '{}')
cnn_now=$(echo "$cnn_json" | jq -r '.fear_and_greed.score // "N/A"')
cnn_week_raw=$(echo "$cnn_json" | jq -r '.fear_and_greed.previous_1_week // "N/A"')
cnn_month_raw=$(echo "$cnn_json" | jq -r '.fear_and_greed.previous_1_month // "N/A"')
cnn_year_raw=$(echo "$cnn_json" | jq -r '.fear_and_greed.previous_1_year // "N/A"')

cnn_week=$(round "$cnn_week_raw")
cnn_month=$(round "$cnn_month_raw")
cnn_year=$(round "$cnn_year_raw")

# ── Emoji & label ──
emoji_for() {
  local v=$1
  [[ "$v" == "N/A" ]] && { echo "?"; return; }
  local vi; vi=$(printf "%.0f" "$v" 2>/dev/null || echo 0)
  if   (( vi <= 25 )); then echo "😱"
  elif (( vi <= 45 )); then echo "😨"
  elif (( vi <= 55 )); then echo "😐"
  elif (( vi <= 75 )); then echo "😎"
  else echo "🤑"
  fi
}

label_cn() {
  local v=$1
  [[ "$v" == "N/A" ]] && { echo "N/A"; return; }
  local vi; vi=$(printf "%.0f" "$v" 2>/dev/null || echo 0)
  if   (( vi <= 25 )); then echo "极度恐惧"
  elif (( vi <= 45 )); then echo "恐惧"
  elif (( vi <= 55 )); then echo "中性"
  elif (( vi <= 75 )); then echo "贪婪"
  else echo "极度贪婪"
  fi
}

trend_arrow() {
  local now=$1 prev=$2
  [[ "$now" == "N/A" || "$prev" == "N/A" ]] && { echo ""; return; }
  local d; d=$(awk "BEGIN {printf \"%.1f\", $now - $prev}" 2>/dev/null || echo 0)
  if   (( $(awk "BEGIN {print ($d > 2)}") )); then echo "📈"
  elif (( $(awk "BEGIN {print ($d < -2)}") )); then echo "📉"
  else echo "➡️"
  fi
}

# ── 5-star rating ──
#  0-20: ★☆☆☆☆  21-40: ★★☆☆☆  41-55: ★★★☆☆  56-75: ★★★★☆  76-100: ★★★★★
stars() {
  local v=$1
  [[ "$v" == "N/A" ]] && { echo "☆☆☆☆☆"; return; }
  local vi; vi=$(printf "%.0f" "$v" 2>/dev/null || echo 0)
  if   (( vi <= 20 )); then echo "★☆☆☆☆"
  elif (( vi <= 40 )); then echo "★★☆☆☆"
  elif (( vi <= 55 )); then echo "★★★☆☆"
  elif (( vi <= 75 )); then echo "★★★★☆"
  else echo "★★★★★"
  fi
}

strategy() {
  local v=$1
  [[ "$v" == "N/A" ]] && { echo "-"; return; }
  local vi; vi=$(printf "%.0f" "$v" 2>/dev/null || echo 0)
  if   (( vi <= 25 )); then echo "📈 分批建仓机会区"
  elif (( vi <= 45 )); then echo "📈 观察布局"
  elif (( vi <= 55 )); then echo "😐 观望为主"
  elif (( vi <= 75 )); then echo "⚠️ 关注止盈"
  else echo "🚨 减仓/对冲信号"
  fi
}

# ── Compute ──
crypto_emoji=$(emoji_for "$crypto_now")
cnn_emoji=$(emoji_for "$cnn_now")
crypto_cn=$(label_cn "$crypto_now")
cnn_cn=$(label_cn "$cnn_now")
crypto_trend=$(trend_arrow "$crypto_now" "$crypto_prev")
crypto_stars=$(stars "$crypto_now")
cnn_stars=$(stars "$cnn_now")

# ── Divergence ──
divergence=""
if [[ "$crypto_now" != "N/A" && "$cnn_now" != "N/A" ]]; then
  c_int=$(printf "%.0f" "$crypto_now")
  n_int=$(printf "%.0f" "$cnn_now")
  gap=$(( n_int - c_int ))
  if   (( gap > 20 )); then
    divergence="⚠️ 美股贪婪 vs 加密恐惧，出现显著情绪分化 → 加密可能滞后补涨 / 或避险资金撤离加密"
  elif (( gap < -20 )); then
    divergence="⚠️ 加密贪婪 vs 美股恐惧，出现显著情绪分化 → 加密独立行情 / 或风险偏好极端分化"
  elif (( gap > 10 )); then
    divergence="📌 美股情绪略高于加密，轻微分化中"
  elif (( gap < -10 )); then
    divergence="📌 加密情绪略高于美股，轻微分化中"
  else
    divergence="✅ 两个市场情绪趋于一致"
  fi
fi

# ── Extreme zone alerts ──
alerts=""
if [[ "$crypto_now" != "N/A" ]]; then
  c_int=$(printf "%.0f" "$crypto_now")
  if (( c_int <= 15 )); then
    alerts+="🚨 加密极度恐惧(<15)：历史大底区域，巴菲特时刻！\n"
  elif (( c_int >= 85 )); then
    alerts+="🚨 加密极度贪婪(>85)：FOMO 顶峰，注意止盈！\n"
  fi
fi
if [[ "$cnn_now" != "N/A" ]]; then
  n_int=$(printf "%.0f" "$cnn_now")
  if (( n_int <= 15 )); then
    alerts+="🚨 美股极度恐惧(<15)：历史大底区域，关注抄底！\n"
  elif (( n_int >= 85 )); then
    alerts+="🚨 美股极度贪婪(>85)：盛极而衰，谨慎追高！\n"
  fi
fi

# ── Historical context ──
cnn_context=""
if [[ "$cnn_month_raw" != "N/A" && "$cnn_now" != "N/A" ]]; then
  m_int=$(printf "%.0f" "$cnn_month_raw")
  n_int=$(printf "%.0f" "$cnn_now")
  if   (( n_int - m_int > 40 )); then
    cnn_context="📖 1个月前还在极度恐惧(${cnn_month})，现已贪婪(${cnn_now}) → 暴力情绪修复"
  elif (( n_int - m_int > 20 )); then
    cnn_context="📖 1个月前(${cnn_month}) → 现在(${cnn_now})，情绪明显修复"
  elif (( m_int - n_int > 40 )); then
    cnn_context="📖 1个月前还在贪婪(${cnn_month})，现已跌入恐惧(${cnn_now}) → 恐慌蔓延"
  elif (( m_int - n_int > 20 )); then
    cnn_context="📖 1个月前(${cnn_month}) → 现在(${cnn_now})，情绪明显恶化"
  fi
fi

# ── Output ──
echo ""
echo "===== 恐慌贪婪指数 ====="
echo ""

echo "🪙 加密货币  ${crypto_emoji}  ${crypto_now}  →  ${crypto_cn}  ${crypto_trend}"
echo "   ${crypto_stars}"
if [[ "$crypto_now" != "N/A" && "$crypto_prev" != "N/A" ]]; then
  echo "   昨日: ${crypto_prev}"
fi
echo ""

echo "📊 美股 (CNN)  ${cnn_emoji}  ${cnn_now}  →  ${cnn_cn}"
echo "   ${cnn_stars}"
if [[ "$cnn_week" != "N/A" ]]; then
  echo "   1周前: ${cnn_week}  |  1月前: ${cnn_month}  |  1年前: ${cnn_year}"
fi
echo ""

[[ -n "$cnn_context" ]] && echo "${cnn_context}" && echo ""
[[ -n "$divergence" ]] && echo "${divergence}" && echo ""
[[ -n "$alerts" ]] && echo -e "${alerts}"

echo "── 策略参考 ──"
echo "  加密: $(strategy "$crypto_now")"
echo "  美股: $(strategy "$cnn_now")"
echo ""
echo "数据来源: CNN Fear & Greed + Alternative.me"
echo "⏰ $(TZ='Asia/Shanghai' date '+%Y-%m-%d %H:%M CST')"
echo ""
