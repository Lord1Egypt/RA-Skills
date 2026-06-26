---
name: dailyfinance
description: "Daily financial news briefing — stock markets, crypto, macro economy, Fed/PBOC policy, earnings reports. Bilingual EN/CN visual dashboard. Morning push + evening recap."
keywords:
  - 今日财经
  - 财经新闻
  - 股市
  - 每日财经
  - 股票市场
  - 加密货币
  - 比特币
  - 宏观经济
  - 市场动态
  - 美联储
  - 财报
  - 投资资讯
  - A股
  - 港股
  - 纳斯达克
  - 道琼斯
  - daily finance
  - market news
  - stock market
  - crypto news
  - economic news
  - market update
  - Fed news
  - earnings
  - investment news
  - financial briefing
  - S&P 500
  - bitcoin
  - Nasdaq
  - Hang Seng
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# Daily Finance / 今日财经

Generate a comprehensive daily financial news briefing with market data and bilingual content.

## Workflow

1. **Search for market data and news** — Use `web_search` to gather:
   - `"stock market today S&P 500 Dow"` — major indices
   - `"bitcoin crypto market today"` — crypto highlights
   - `"financial news today economy"` — macro news
   - `"China stock market A shares today"` — China markets
2. **Curate** — Select: 2-3 market data points (US indices, crypto, China/HK), 4-5 top financial stories.
3. **Write summaries** — Each story: headline (EN + CN), 2-sentence summary, impact assessment (bullish/bearish/neutral with emoji 📈📉➡️).
4. **Generate the visual** — Create a single-file HTML artifact.

## Visual Design Requirements

Create a Bloomberg/Financial Times inspired dashboard:

- **Layout**: Dashboard-style. Top row = market ticker strip. Below = news cards in clean grid.
- **Typography**: Professional financial fonts (e.g., Roboto Slab for headlines, Source Sans Pro for body, Fira Code for numbers/data). Numbers should be in a monospace font for alignment.
- **Color scheme**: Professional financial palette — dark navy (#1a1a2e) or off-white with gold (#c9a54e) accents. Green (#22c55e) for gains, Red (#ef4444) for losses. Subtle, authoritative.
- **Market ticker**: Horizontal scrolling strip at top showing: S&P 500, Dow, Nasdaq, BTC, ETH, Shanghai Composite, Hang Seng — with price and % change (color-coded green/red).
- **News cards**: Clean, professional cards. Each has: category badge (Macro / Crypto / Equity / Policy / Earnings), headline, summary, impact tag (📈📉➡️).
- **Market overview section**: Simple mini-charts or bar indicators showing daily performance of major indices.
- **Interactive**: Ticker auto-scrolls. Cards expandable for bilingual detail.
- **Disclaimer**: Small text: "This is a news summary, not financial advice. 本内容仅为资讯摘要，不构成投资建议。"
- **Ad-ready zone**: `<div id="ad-slot-ticker">` below ticker. `<div id="ad-slot-mid">` mid-page. `<div id="ad-slot-bottom">` at footer.
- **Footer**: "Powered by ClawCode"

## Content Guidelines

- Data accuracy is critical — always note that data may be delayed
- Include both US and China/HK market coverage
- Crypto section should be proportionate (1-2 items, not dominating)
- Maintain neutral tone — no predictions or advice
- Note the source for each data point
- Always include the financial disclaimer

## Output

Save as `/mnt/user-data/outputs/daily-finance.html` and present to user.

---

## 推送管理

```bash
# 开启每日推送（早晚各一次）
node scripts/push-toggle.js on <userId>

# 自定义时间和渠道
node scripts/push-toggle.js on <userId> --morning 08:00 --evening 20:00 --channel feishu

# 关闭推送
node scripts/push-toggle.js off <userId>

# 查看推送状态
node scripts/push-toggle.js status <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`
