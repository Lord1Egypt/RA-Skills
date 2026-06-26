---
name: crypto-daily-report
description: Generate and send cryptocurrency daily reports with market overview, fear & greed index, liquidation data, economic calendar, and news aggregation. Use when users need crypto market daily briefings, automated market updates, or scheduled crypto news delivery to Telegram/Discord channels. Triggers include "币圈日报", "crypto daily", "daily report", "market update", "跑个日报".
---

# Crypto Daily Report Skill

Generate comprehensive cryptocurrency daily reports and send to messaging channels.

## Features

- Market overview (BTC, ETH, SOL, BNB prices)
- Fear & Greed Index sentiment analysis
- 24h liquidation statistics
- Economic calendar (token unlocks, Fed decisions, CPI/GDP releases)
- Curated news from Cointelegraph and TokenInsight
- Automated scheduled delivery

## Quick Start

### Generate Report Now

When user requests a daily report, execute:

```bash
# 1. Get prices
onchainos market prices "1:0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee,501:So11111111111111111111111111111111111111112,56:0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

# 2. Get BTC price via search
web_search "BTC price today USD"

# 3. Get Fear & Greed Index
curl -s "https://api.alternative.me/fng/?limit=2"

# 4. Get liquidation data
web_search "crypto liquidation 24h today total amount"

# 5. Get news
web_fetch "https://cointelegraph.com/rss"
web_fetch "https://tokeninsight.com/rss/news"

# 6. Get calendar
web_fetch "https://incrypted.com/en/calendar/"
```

Then assemble and send using `message` tool.

### Setup Scheduled Delivery

For automated daily delivery at 8:00 AM (UTC+8):

```bash
cron add --name "crypto-daily-report" \
  --schedule "0 0 * * *" \
  --timezone "Asia/Shanghai" \
  --target "telegram:-1002009088194" \
  --command "generate-crypto-daily-report"
```

Or use the setup script:

```bash
./scripts/setup-cron.sh -1002009088194
```

## Report Format

```
📰 币圈日报
{Date} {Weekday}

💰 大盘速览
BTC: ${price}
ETH: ${price}
SOL: ${price}
BNB: ${price}

😨 市场情绪
恐慌贪婪指数: {value} {emoji} {classification}
昨天: {value} | 上周: {value} | 上月: {value}
💡 解读: {interpretation}

💥 爆仓数据 (24h)
数据来源: CoinGlass / Gate
总爆仓金额: ~${amount}M
1小时爆仓: ~${amount}M
主要币种: BTC、ETH、SOL、BNB
{alert_message}

📅 重要日历
{calendar_events}

🔥 热点新闻
{numbered_news_items}

⚠️ 免责声明
以上信息仅供参考，不构成投资建议。币圈有风险，投资需谨慎。
```

## Data Sources

| Data | Source | Method |
|------|--------|--------|
| ETH, SOL, BNB | onchainos CLI | Direct API |
| BTC | Web search | Brave Search |
| Fear & Greed | alternative.me | REST API |
| Liquidations | Search aggregation | Brave Search |
| News | Cointelegraph, TokenInsight | RSS feeds |
| Calendar | Incrypted | Web scraping |

## Interpretation Guide

### Fear & Greed Index
- 0-24: Extreme Fear 🔴 (Potential bottom)
- 25-49: Fear 🟠 (Cautious)
- 50-74: Greed 🟢 (Optimistic)
- 75-100: Extreme Greed 🔵 (Potential top)

### Calendar Event Icons
- 🔴 High impact (token unlocks, Fed decisions)
- 🟡 Medium impact (economic data releases)
- 📍 Events (conferences, summits)

## Scripts

- `scripts/generate-report.sh` - Generate single report
- `scripts/setup-cron.sh` - Setup automated delivery
- `scripts/test-send.sh` - Test send to channel

See [references/data-sources.md](references/data-sources.md) for detailed API documentation.
