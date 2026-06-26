---
name: fund-keeper
version: 2.6.0
description: Chinese mutual fund intelligent advisor with real-time valuation, buy/sell suggestions, profit tracking, SIP planning, OCR recognition, and stock-fund linkage. Supports offline mode and multi-source caching.
metadata:
  openclaw:
    emoji: "🐔"
    category: finance
    network:
      required: true
      domains:
        - "fundgz.1234567.com.cn"
        - "fund.eastmoney.com"
        - "hq.sinajs.cn"
        - "push2.eastmoney.com"
      reason: "Fetch real-time fund valuation, historical NAV, and gold prices from public financial data sources"
    requires:
      pip: ["akshare>=1.12", "pandas>=2.0", "requests>=2.28", "easyocr>=1.7"]
keywords:
  - fund
  - mutual fund
  - investment
  - buy/sell suggestion
  - fund valuation
  - profit tracking
  - SIP
  - OCR
  - stock-fund linkage
---

# Fund Keeper - Intelligent Fund Advisor

A comprehensive tool for Chinese mutual fund management with real-time valuation, buy/sell suggestions, and portfolio tracking.

## Quick Start

### 1. Install Dependencies

```bash
pip install akshare pandas requests
```

### 2. Create Fund List

Create your portfolio in `workspace/funds/my-funds.md`:

```markdown
# My Fund Portfolio

## Holdings

| Fund Code | Fund Name | Shares | Cost NAV | Notes |
|---------|---------|---------|---------|------|
| 000001  | HuaXia Growth | 10000 | 1.500 | SIP |
| 110011  | YiFangDa SME | 5000 | 2.300 | Long-term |
```

### 3. Commands

```bash
# View portfolio P&L
fund-keeper portfolio

# Get buy/sell suggestions
fund-keeper advice

# View config
fund-keeper config

# Modify config
fund-keeper config --set alert_threshold=2.0

# Reset config
fund-keeper config --reset

# Add fund from screenshot
fund-keeper add-from-image screenshot.png

# View market overview
fund-keeper market

# Set alert
fund-keeper alert --fund 000001 --price 1.800
```

## Core Features

### 1. Real-time Valuation

- Fetch real-time NAV estimates from public sources
- Compare with historical NAV, calculate daily change
- Support QDII funds (HK/US markets)

### 2. Buy/Sell Suggestions

Based on comprehensive analysis:
- **Valuation**: PE/PB historical percentile
- **Technical**: Moving averages, MACD, RSI
- **Market Sentiment**: Capital flow, news
- **Cost Basis**: Compare with your holding cost

Suggestion Levels:
- **Strong Sell**: Overvalued + technical top divergence
- **Consider Selling**: Overvalued or profit target reached
- **Hold**: Normal range
- **Consider Buying**: Undervalued or SIP opportunity
- **Strong Buy**: Significantly undervalued + technical bottom divergence

### 3. OCR Fund Recognition

Support screenshot recognition from:
- Alipay fund holdings
- Fund platform screenshots
- Bank app fund pages

Auto-extract:
- Fund code
- Fund name
- Shares held
- Amount

### 4. Smart Alerts

- NAV reaches target price
- Daily change exceeds threshold
- Market volatility
- SIP date reminders

## Fund Search

```bash
py fund_keeper.py search --name gold     # Search by name
py fund_keeper.py search --fund 000218   # View fund details
```

## Portfolio Management

```bash
# Edit fund
py fund_keeper.py edit --fund 000218    # Interactive edit
py fund_keeper.py edit --fund 000218 --field amount --value 10000

# Remove fund
py fund_keeper.py remove --fund 000218
```

### Editable Fields
- `name` - Fund name
- `amount` - Amount held
- `profit` - Take profit %
- `stop` - Stop loss %
- `day` - SIP day
- `note` - Notes

## Gold Investment Report

```bash
py fund_keeper.py gold
```

Includes:
- International gold price (AUTD)
- Gold fund (000218) real-time NAV
- Investment suggestions (buy/hold/sell)

## Profit Visualization

```bash
py fund_keeper.py stats           # Basic stats
py fund_keeper.py stats --chart   # With charts
py fund_keeper.py trend           # 7-day trend
```

## Data Sources & Caching

**Multi-source Support**:
- TTJJ (default, fastest)
- EastMoney
- Sina Finance (backup)

**Caching**:
- Auto-cache results (30 min valid)
- Offline mode: `--offline`

## Important Notes

**Investment Risk**
- This tool is for reference only, not investment advice
- Market risks exist, invest carefully
- Diversification recommended

**Data Delay**
- Mutual fund NAV updates once daily (evening)
- Real-time estimates are approximations
- QDII funds have T+2 delay

## Stock-Fund Linkage (v2.2)

Link with stock-analysis skill:

```bash
# Recommend funds by sector
python stock_fund_linkage.py --sector semiconductor

# Analyze fund holdings
python stock_fund_linkage.py --fund 000218
```

## Scheduled Tasks

```bash
# Daily 15:00 after market close
openclaw cron add --name "fund-check" --cron "0 15 * * 1-5" \
  --session isolated --message "Check fund valuation and generate report"

# Weekly report on Monday 8:00
openclaw cron add --name "fund-weekly" --cron "0 8 * * 1" \
  --session isolated --message "Generate weekly fund portfolio report"
```

## Related Files

- `funds/my-funds.md` - Portfolio list
- `funds/config.json` - Configuration
- `funds/history.md` - Transaction history
- `memory/fund-learnings.md` - Investment insights

---

*Long-term investing, rational decisions.* 🐔