---
name: crypto-briefing
description: Generate crypto market briefing reports with latest news, price analysis, trend predictions, sentiment analysis, and Fear & Greed Index. Use when user asks for crypto news summary, market briefing, BTC/ETH/SOL/SUI/WLD/WIF/BGB analysis, or market sentiment report.
---

# Crypto Briefing Skill

Generate comprehensive crypto market briefing reports by browsing news sites, collecting price data, and analyzing market sentiment.

---

## ⚠️ MANDATORY: News Source Checklist

**You MUST visit ALL 5 news sources. This is NON-NEGOTIABLE.**

Before generating the report, verify you have visited:
- [ ] foresightnews.pro/news
- [ ] panewslab.com/zh/newsflash
- [ ] theblockbeats.info/newsflash
- [ ] techflowpost.com/newsletter/index.html
- [ ] odaily.news/newsflash

**If any source is skipped, the report is INCOMPLETE and INVALID.**

Do NOT rationalize skipping sources. Do NOT assume one source "has enough news."
Each source has unique coverage. **Completeness > Speed.**

At the end of data collection, you must be able to confirm:
```
✅ foresightnews.pro - visited
✅ panewslab.com - visited
✅ theblockbeats.info - visited
✅ techflowpost.com - visited
✅ odaily.news - visited
```

If any shows ❌, go back and visit it before proceeding.

---

## Workflow

### Step 1: Collect Price Data

Use browser to fetch from CoinMarketCap homepage (preferred - gets all data in one page):
- https://coinmarketcap.com/

This provides:
- Current prices and 24h changes for major coins
- Fear & Greed Index (official)
- Market Cap
- Average Crypto RSI
- Altcoin Season Index

For BGB specifically, also visit:
- https://coinmarketcap.com/currencies/bitget-token-new/

Coin mapping:
- BTC → Bitcoin
- ETH → Ethereum
- SOL → Solana
- SUI → Sui
- WLD → Worldcoin
- WIF → dogwifhat
- BGB → Bitget Token

### Step 2: Browse ALL News Sites (MANDATORY)

Use browser tool with `profile=openclaw`. Visit **EACH** site and extract headlines from last 12 hours.

**Required sites (must visit ALL 5):**

| # | Site | URL |
|---|------|-----|
| 1 | Foresight News | https://foresightnews.pro/news |
| 2 | PANews | https://www.panewslab.com/zh/newsflash |
| 3 | BlockBeats | https://www.theblockbeats.info/newsflash |
| 4 | TechFlow | https://www.techflowpost.com/newsletter/index.html |
| 5 | Odaily | https://www.odaily.news/newsflash |

**For each site:**
1. `browser action=navigate` to the URL
2. `browser action=snapshot` with maxChars=15000
3. Parse headlines and timestamps
4. Extract news from last 12 hours
5. Move to next site

**After visiting all 5 sites**, close the browser tab.

### Step 3: Calculate Fear & Greed Index

Use the **official Fear & Greed Index from CoinMarketCap** (collected in Step 1).

Also analyze the following factors to provide AI analysis context:

**Factors to consider:**
1. **Price Action (40% weight)**
   - 24h price changes across major coins
   - Volatility levels
   - Support/resistance breaks

2. **News Sentiment (35% weight)**
   - Ratio of positive/negative headlines from ALL 5 sources
   - Severity of negative news (hacks, bans, crashes)
   - Strength of positive news (adoption, institutional buying)

3. **Market Volume & Liquidity (15% weight)**
   - ETF flows (inflows = greed, outflows = fear)
   - Exchange volume trends

4. **Social Sentiment (10% weight)**
   - Panic indicators in news language
   - Regulatory concerns
   - Market commentary tone

**Classification:**
- 0-25: **Extreme Fear**
- 25-45: **Fear**
- 45-55: **Neutral**
- 55-75: **Greed**
- 75-100: **Extreme Greed**

### Step 4: Analyze & Generate Report

Based on collected news (from ALL 5 sources) and price data, generate the briefing report:

```markdown
# 🪙 加密货币市场简报
> 生成时间: {timestamp} (北京时间)

## 📊 价格概览

| 币种 | 当前价格 | 24h 变化 | 12h 目标价 | 趋势预测 |
|------|----------|----------|------------|----------|
| BTC  | $XX,XXX  | +X.XX%   | $XX,XXX    | 📈 上涨 (XX%) |
| ETH  | $X,XXX   | +X.XX%   | $X,XXX     | 📉 下跌 (XX%) |
| SOL  | $XXX     | +X.XX%   | $XXX       | ➡️ 横盘 (XX%) |
| SUI  | $X.XX    | +X.XX%   | $X.XX      | 📈 上涨 (XX%) |
| WLD  | $X.XX    | +X.XX%   | $X.XX      | 📉 下跌 (XX%) |
| WIF  | $X.XX    | +X.XX%   | $X.XX      | 📈 上涨 (XX%) |
| BGB  | $X.XX    | +X.XX%   | $X.XX      | 📈 上涨 (XX%) |

## 🎭 市场情绪

- 😊 积极: XX%
- 😐 中性: XX%
- 😟 消极: XX%

**综合判断**: {积极/中性/消极}

## 😱 恐慌与贪婪指数

**{value}** - {classification}

[██████████░░░░░░░░░░] {value}/100

**AI 分析依据:**
- {list key indicators from news and data that influenced the F&G score}
- {example: 24小时全网爆仓 XX 亿美元（多单 XX 亿美元）}
- {example: BTC/ETH ETF 连续 X 日净流出共约 XX 亿美元}
- {example: 主流币种全线承压/反弹}
- {example: 重大事件影响（如监管、黑客攻击、机构动向）}

## 📰 重要资讯 (过去 12 小时)

### 利好消息 📈
- 🏦 **{category}**: {headline and details}
- 💰 **{category}**: {headline and details}
- 🚀 **{category}**: {headline and details}

### 利空消息 📉
- 📉 **{category}**: {headline and details}
- 💥 **{category}**: {headline and details}
- ⚠️ **{category}**: {headline and details}

### 其他动态 📋
- 🎯 **{category}**: {headline and details}
- 🔓 **{category}**: {headline and details}

---

## 💡 分析师观点

**短期展望**: {对市场短期(12-24h)走势的综合判断}

**关键支撑位**:
- BTC: $XX,XXX - $XX,XXX (描述)
- ETH: $X,XXX - $X,XXX (描述)

**积极信号**:
1. {正面因素 1}
2. {正面因素 2}
3. {正面因素 3}

**风险因素**:
1. {风险因素 1}
2. {风险因素 2}
3. {风险因素 3}

**策略建议**: {具体操作建议，包括仓位、风险管理等}

**今日关注**:
- {关键事件 1}
- {关键事件 2}
- {关键事件 3}

---

## 📈 技术分析

**比特币 (BTC)**
- 支撑位: $XX,XXX / $XX,XXX
- 阻力位: $XX,XXX / $XX,XXX
- RSI: {超买/中性/超卖}

**以太坊 (ETH)**
- 支撑位: $X,XXX / $X,XXX
- 阻力位: $X,XXX / $X,XXX
- 相对 BTC 表现: {强势/弱势/同步}

---

*数据来源: CoinMarketCap, Foresight News, PANews, BlockBeats, TechFlow, Odaily*  
*免责声明: 本简报仅供参考，不构成投资建议。加密货币市场波动巨大，请谨慎决策。*
```

---

## Emoji Usage Guidelines

**利好消息:** 🏦 🏛️ 🔐 🌐 💰 🎯 🚀 ✅ 📈
**利空消息:** 📉 💥 🐋 ⚖️ 🚨 ⚠️ ❌ 📊
**其他动态:** 🎯 🔓 📦 🔥 🌐 🔒 💼 🇰🇿 🇸🇻 (country flags for regional news)

---

## Trend Prediction Guidelines

Analyze news sentiment and price momentum to predict 12h trends:

**上涨信号** (📈):
- Positive news (ETF approvals, institutional buying, regulatory clarity)
- Strong 24h momentum (>3% gain)
- Low fear index (<30) with accumulation signs

**下跌信号** (📉):
- Negative news (hacks, regulatory crackdowns, large sell-offs)
- Weak momentum (<-3% loss)
- High fear or extreme greed (contrarian)

**横盘信号** (➡️):
- Mixed or no significant news
- Low volatility (-3% to +3%)
- Neutral sentiment

---

## Sentiment Analysis

Categorize each news headline as:
- **积极**: Bullish news, adoption, partnerships, upgrades
- **消极**: Hacks, bans, crashes, lawsuits
- **中性**: Neutral updates, technical changes, mixed news

Calculate percentages based on headline count across ALL sources.

---

## Final Checklist Before Submitting Report

Before outputting the report, confirm:

- [ ] CoinMarketCap data collected (prices, F&G, RSI)
- [ ] ✅ foresightnews.pro - visited
- [ ] ✅ panewslab.com - visited
- [ ] ✅ theblockbeats.info - visited
- [ ] ✅ techflowpost.com - visited
- [ ] ✅ odaily.news - visited
- [ ] News from all sources merged and deduplicated
- [ ] Report includes data sources footer mentioning all 5 news sites

**If any checkbox is unchecked, DO NOT submit the report. Go back and complete the missing steps.**
