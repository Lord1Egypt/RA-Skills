#!/bin/bash
set -e

# 加密货币市场晨报生成脚本
SKILL_DIR=$(cd "$(dirname "$0")" && pwd)
JSON_OUTPUT=0

# 参数解析
if [ "$1" = "--json" ]; then
  JSON_OUTPUT=1
fi

# 检查依赖
if ! command -v curl &> /dev/null; then
  echo "错误：curl 未安装，请先安装 curl"
  exit 1
fi
if ! command -v jq &> /dev/null; then
  echo "错误：jq 未安装，请先安装 jq"
  exit 1
fi

# 1. 获取市场概览数据（来自CoinGecko公开API）
MARKET_DATA=$(curl -s "https://api.coingecko.com/api/v3/global")
TOTAL_MARKET_CAP=$(echo "$MARKET_DATA" | jq -r '.data.total_market_cap.usd | tostring | (. / 1e12 | . * 100 | round / 100 | tostring) + " 万亿美元"')
MARKET_CHANGE_24H=$(echo "$MARKET_DATA" | jq -r '.data.market_cap_change_percentage_24h.usd | . * 100 | round / 100 | tostring + " %"')
TOTAL_VOLUME_24H=$(echo "$MARKET_DATA" | jq -r '.data.total_volume.usd | tostring | (. / 1e9 | . * 100 | round / 100 | tostring) + " 千亿美元"')
BTC_DOMINANCE=$(echo "$MARKET_DATA" | jq -r '.data.market_cap_percentage.btc | . * 100 | round / 100 | tostring + " %"')

# 2. 获取重点资产数据
BTC_PRICE=$(echo "$MARKET_DATA" | jq -r '.data.active_cryptocurrencies')
ASSETS_DATA=$(curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,binancecoin&order=market_cap_desc&per_page=4&page=1&sparkline=false")
BTC_INFO=$(echo "$ASSETS_DATA" | jq -r '.[] | select(.id=="bitcoin") | "BTC: $" + (.current_price|tostring) + "，24h涨跌幅: " + (.price_change_percentage_24h|.*100|round/100|tostring) + " %"')
ETH_INFO=$(echo "$ASSETS_DATA" | jq -r '.[] | select(.id=="ethereum") | "ETH: $" + (.current_price|tostring) + "，24h涨跌幅: " + (.price_change_percentage_24h|.*100|round/100|tostring) + " %"')
SOL_INFO=$(echo "$ASSETS_DATA" | jq -r '.[] | select(.id=="solana") | "SOL: $" + (.current_price|tostring) + "，24h涨跌幅: " + (.price_change_percentage_24h|.*100|round/100|tostring) + " %"')
BNB_INFO=$(echo "$ASSETS_DATA" | jq -r '.[] | select(.id=="binancecoin") | "BNB: $" + (.current_price|tostring) + "，24h涨跌幅: " + (.price_change_percentage_24h|.*100|round/100|tostring) + " %"')

# 3. 获取最新新闻（来自CryptoPanic公开RSS）
NEWS_RSS=$(curl -s "https://cryptopanic.com/news/rss/")
REG_NEWS=$(echo "$NEWS_RSS" | grep -o '<title>[^<]*</title>' | sed 's/<title>//g' | sed 's/<\/title>//g' | grep -v "CryptoPanic" | head -3)
NEWS_SOURCES="CoinGecko API, CryptoPanic 公开新闻RSS"

# 4. 风险提示
RISK_TIPS="1. 加密货币市场24小时不间断交易，波动性极高，注意仓位控制；2. 全球监管政策仍存在不确定性，部分地区合规要求持续更新；3. 近期链上钓鱼攻击、智能合约漏洞事件仍有发生，注意资产安全；4. 本简报仅为信息汇总，不构成任何投资建议。"

# 输出处理
if [ $JSON_OUTPUT -eq 1 ]; then
  jq -n \
    --arg overview "当前加密货币总市值 $TOTAL_MARKET_CAP，24小时整体涨跌幅 $MARKET_CHANGE_24H，24小时总交易额 $TOTAL_VOLUME_24H，BTC市值占比 $BTC_DOMINANCE，市场整体活跃度处于正常区间。" \
    --arg assets "重点资产动态：$BTC_INFO；$ETH_INFO；$SOL_INFO；$BNB_INFO" \
    --arg macro "最新宏观/监管消息：$(echo "$REG_NEWS" | tr '\n' '；')" \
    --arg risk "$RISK_TIPS" \
    --arg sources "$NEWS_SOURCES" \
    '{
      "市场概览": $overview,
      "重点资产动态": $assets,
      "宏观/监管消息": $macro,
      "风险提示": $risk,
      "信息来源": $sources
    }'
else
  echo "# 📈 加密货币市场晨报 $(date +"%Y-%m-%d")"
  echo ""
  echo "## 1. 市场概览"
  echo "当前加密货币总市值 $TOTAL_MARKET_CAP，24小时整体涨跌幅 $MARKET_CHANGE_24H，24小时总交易额 $TOTAL_VOLUME_24H，BTC市值占比 $BTC_DOMINANCE，市场整体活跃度处于正常区间。"
  echo ""
  echo "## 2. 重点资产动态"
  echo "$BTC_INFO"
  echo "$ETH_INFO"
  echo "$SOL_INFO"
  echo "$BNB_INFO"
  echo ""
  echo "## 3. 宏观/监管消息"
  echo "$REG_NEWS" | sed '/^$/d'
  echo ""
  echo "## 4. 风险提示"
  echo "$RISK_TIPS"
  echo ""
  echo "## 5. 信息来源"
  echo "$NEWS_SOURCES"
fi
