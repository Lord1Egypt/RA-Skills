---
name: chairman-daily-brief
description: >-
  Exclusive morning and evening briefing skill for listed company chairmen. 
  Provides daily briefings from an executive decision-making perspective,
  covering stock price movements, industry policy updates, competitor intelligence,
  capital market sentiment, and regulatory announcement alerts. 
  Morning briefings focus on pre-market outlook and risk warnings;
  evening briefings emphasize post-market review and next-day strategies.
  Data aggregated from multiple QVeris sources.
env:
  - QVERIS_API_KEY
requirements:
  env_vars:
    - QVERIS_API_KEY
credentials:
  required:
    - QVERIS_API_KEY
  primary: QVERIS_API_KEY
  scope: read-only
  endpoint: https://qveris.ai/api/v1
runtime:
  language: nodejs
  node: ">=18"
install:
  mechanism: local-skill-execution
  external_installer: false
  package_manager_required: false
persistence:
  writes_within_skill_dir:
    - config/companies.json
    - config/watchlist.json
    - .evolution/tool-evolution.json
  writes_outside_skill_dir: false
security:
  full_content_file_url:
    enabled: true
    allowed_hosts:
      - qveris.ai
    protocol: https
network:
  outbound_hosts:
    - qveris.ai
metadata:
  openclaw:
    requires:
      env: ["QVERIS_API_KEY"]
    primaryEnv: "QVERIS_API_KEY"
    homepage: https://qveris.ai
auto_invoke: true
source: https://qveris.ai
examples:
  - "Generate morning report: focus on 600519.SS Moutai"
  - "Chairman evening report: generate closing briefing for 0700.HK Tencent"
  - "Morning brief: BYD and new energy vehicle industry"
  - "Generate morning report, focus on competitor CATL"
  - "Evening report: summarize today's dynamics of three listed companies I follow"
---

# Chairman Daily Brief

A daily market briefing system designed for listed company chairmen, providing executive-level market intelligence from a strategic decision-making perspective.

## Core Value Proposition

Unlike ordinary investor market watching, this skill operates from a **chairman's decision-making perspective**:

- **Stock Movements → Impact Analysis**: Not just watching ups and downs, but analyzing impacts on financing, M&A, and shareholder relations
- **Industry Policy → Strategic Opportunities**: Capturing business opportunities or risks from regulatory changes in real-time
- **Competitors → Benchmarking Analysis**: Assessing how major competitor moves affect your company
- **Market Sentiment → Capital Strategy**: Timing suggestions for corporate capital operations based on investor sentiment
- **Announcement Alerts → Compliance Warnings**: Regulatory announcements and major event reminders

## Morning vs Evening Briefings

### Morning Brief — 7:00-9:00 AM (Pre-Market)

**Objective**: Equip the chairman with a complete picture before market open, preparing for the day ahead

**Content Modules**:
1. **Overnight Global Markets**: Impact of US stocks, Hong Kong stocks, and A50 futures on today's opening
2. **Macro Policy Express**: Industry policies and regulatory developments released overnight
3. **Company Pre-Market Outlook**: Pre-market price expectations, key levels today, potential volatility factors
4. **Industry Radar**: Major developments from other companies in the industry, sector index performance
5. **Competitive Intelligence**: Latest developments from major competitors and response recommendations
6. **Risk Alerts**: Potential risk points to monitor
7. **Today's Focus**: Schedule reminders for meetings, announcements, investor activities

### Evening Brief — 3:30-6:00 PM (Post-Market)

**Objective**: Review today's performance and plan tomorrow's strategy

**Content Modules**:
1. **Market Close Overview**: Market trends, sector performance, company stock performance
2. **Trading Analysis**: Trading volume, capital flow, Dragon Tiger List (if applicable)
3. **Today's Announcements**: Summary of important announcements from the company and competitors
4. **Media Monitoring**: Media coverage, analyst opinions, social media sentiment
5. **Institutional Activity**: Research report rating changes, target price adjustments, block trades
6. **Policy Interpretation**: Impact analysis of policies released today on the company
7. **Tomorrow's Strategy Recommendations**: Response strategies based on today's market conditions

## Data Sources

Multi-source data aggregated via QVeris:

- **Market Data**: THS iFinD, Alpha Vantage, Yahoo Finance
- **Financial News**: Caidazi News, THS Finance, East Money
- **Research Reports**: Caidazi Reports, Analyst Ratings
- **Policy Announcements**: Exchange announcements, CSRC releases, industry associations
- **Social Media**: X/Twitter sentiment, Xueqiu discussion heat
- **Macro Data**: Economic data, industry statistics

## Usage

### Generate Morning Report

```bash
# Single company morning report
node scripts/chairman_daily.mjs morning --symbol 600519.SS --company "Kweichow Moutai"

# Multi-company morning report (portfolio view)
node scripts/chairman_daily.mjs morning --watchlist holdings

# With industry focus
node scripts/chairman_daily.mjs morning --symbol 002594.SZ --industry "New Energy Vehicles"
```

### Generate Evening Report

```bash
# Single company evening report
node scripts/chairman_daily.mjs evening --symbol 0700.HK --company "Tencent Holdings"

# Full review (with competitor analysis)
node scripts/chairman_daily.mjs evening --symbol 000858.SZ --competitors 000568.SZ,000596.SZ

# Summary mode (key information only)
node scripts/chairman_daily.mjs evening --symbol AAPL --format summary
```

### Manage Watchlist

```bash
# Add company to watchlist
node scripts/chairman_daily.mjs watch --action add --symbol 600519.SS --company "Kweichow Moutai" --role self

# Add competitor
node scripts/chairman_daily.mjs watch --action add --symbol 002594.SZ --company "BYD" --role competitor --peer-group "New Energy Vehicles"

# View watchlist
node scripts/chairman_daily.mjs watch --action list

# Remove from watchlist
node scripts/chairman_daily.mjs watch --action remove --symbol 600519.SS
```

### OpenClaw Cron Job Setup

```bash
# Morning briefing schedule (weekdays 8:00 AM)
openclaw cron add \
  --name "Chairman Morning Brief" \
  --cron "0 8 * * 1-5" \
  --tz Asia/Shanghai \
  --session isolated \
  --message "Run chairman-daily-brief to generate morning report: node scripts/chairman_daily.mjs morning --watchlist holdings" \
  --channel feishu \
  --to <chat-id>

# Evening briefing schedule (weekdays 3:35 PM)
openclaw cron add \
  --name "Chairman Evening Brief" \
  --cron "35 15 * * 1-5" \
  --tz Asia/Shanghai \
  --session isolated \
  --message "Run chairman-daily-brief to generate evening report: node scripts/chairman_daily.mjs evening --watchlist holdings" \
  --channel feishu \
  --to <chat-id>
```

## Output Format

### Morning Report Example

```markdown
# 📊 Chairman Morning Brief — Kweichow Moutai (600519.SH)
📅 March 4, 2026 Tuesday 08:00

---

## 🌍 Overnight Global Markets
| Market | Close | Change | A-Share Impact |
|--------|-------|--------|----------------|
| Dow Jones | 43,850 | +0.5% | Positive |
| NASDAQ | 18,920 | +1.2% | Positive |
| Hang Seng | 23,450 | -0.3% | Slightly Negative |
| A50 Futures | 13,280 | +0.4% | Positive Opening Expected |

**Commentary**: US tech stocks rebounded strongly, boosting sentiment for A-share growth stocks. A50 futures rose slightly, indicating a stable opening for Moutai today.

---

## 📰 Macro Policy Express
🔔 **New Baijiu Industry Regulations** — State Administration for Market Regulation released draft "Baijiu Labeling and Identification Management Measures", imposing stricter requirements on marketing communications for high-end baijiu.
- **Impact Assessment**: Neutral to slightly negative, may affect marketing investments in the short term
- **Response Recommendation**: Review advertising compliance in advance, prepare investor communication talking points

---

## 📈 Company Pre-Market Outlook
| Indicator | Value | Expectation |
|-----------|-------|-------------|
| Previous Close | 1,580 CNY | - |
| Pre-Market Sentiment | Neutral | Slightly higher opening expected |
| Key Resistance | 1,600 CNY | Breakthrough requires volume |
| Key Support | 1,550 CNY | Strong support |

**Today's Focus Points**:
- Any institutional research report releases
- Northbound capital flow
- Dealer channel sales data rumors

---

## 🏭 Industry Radar
| Company | Development | Impact |
|---------|-------------|--------|
| Wuliangye | Released annual report preview, net profit +12% | Industry prosperity confirmed |
| Luzhou Laojiao | Announced 5% price increase | Industry pricing power solidified |

---

## 🎯 Competitive Intelligence
**Wuliangye (000858.SZ)** — Annual report exceeded expectations
- **Key Points**: Q4 revenue accelerated, high-end product mix improved
- **Impact on Moutai**: Intensified industry competition, need to monitor own market share
- **Recommendation**: Accelerate direct sales channel development, improve consumer reach efficiency

---

## ⚠️ Risk Alerts
1. **Policy Risk**: Baijiu industry regulations tightening, monitor subsequent detailed rules
2. **Valuation Risk**: Current PE 28x, above historical average, requires continued earnings growth support
3. **Foreign Outflow**: Northbound capital net selling for 3 consecutive days, monitor sustainability

---

## 📅 Today's Focus
- 09:30 National Bureau of Statistics releases February CPI data
- 10:00 Company IR quarterly communication meeting
- 14:00 Industry association symposium (Chairman attending)

---
*Data Sources: QVeris | THS iFinD, Caidazi, THS Finance*
```

### Evening Report Example

```markdown
# 🌙 Chairman Evening Report — Tencent Holdings (0700.HK)
📅 March 4, 2026 Tuesday 18:00

---

## 📊 Market Close Overview
| Indicator | Value | Change |
|-----------|-------|--------|
| Close Price | 485.00 HKD | +2.5% |
| Volume | 12.5M shares | +15% volume |
| Turnover | 6.06B HKD | - |
| Market Cap | 4.62T HKD | - |

**Market Comparison**: Hang Seng +0.8%, Tencent outperformed by 1.7 percentage points

---

## 💰 Trading Analysis
- **Capital Flow**: Northbound net buy 850M HKD
- **Main Force**: Large order net inflow 520M HKD
- **Dragon Tiger List**: Not listed

---

## 📢 Today's Announcements
**Company Announcements**:
- No major announcements

**Industry Announcements**:
- NetEase released Q4 earnings, gaming business exceeded expectations
- Regulator released new batch of game license approvals

---

## 📰 Media Monitoring
**Media Coverage**:
- Bloomberg: Tencent accelerates AI business layout, competing with OpenAI
- Caixin: WeChat Video Channel commercialization accelerates, ad revenue expectations raised

**Analyst Views**:
- Goldman Sachs: Maintains "Buy" rating, target price 520 HKD (+7%)
- Morgan Stanley: Upgrades to "Overweight", optimistic on cloud business turnaround

**Social Media Sentiment**: Positive (72% positive, 18% neutral, 10% negative)

---

## 🏦 Institutional Activity
| Institution | Rating Change | Target Price | Commentary |
|-------------|---------------|--------------|------------|
| Goldman Sachs | Maintain Buy | 520 HKD | AI business catalyst |
| Morgan Stanley | Upgrade to Overweight | 510 HKD | Cloud business turnaround |
| UBS | Maintain Neutral | 480 HKD | Fair valuation |

**Block Trades**: No block trades today

---

## 📋 Policy Interpretation
**Game License Approval Normalization**
- **Policy Content**: New batch of game licenses released today, Tencent approved for 2 titles
- **Impact Analysis**: Industry policy environment continues to improve, positive for gaming business growth
- **Strategic Significance**: Paves the way for subsequent new game launches

---

## 🎯 Tomorrow's Strategy Recommendations
**Based on today's market, recommend focusing on**:

1. **Investor Communication**: Utilize today's stock price rise window to communicate with institutional investors at appropriate times
2. **Buyback Pace**: If stock price pulls back below 480, consider accelerating buyback pace
3. **M&A Timing**: Positive market sentiment, can monitor potential M&A targets
4. **Risk Hedging**: Recommend moderate derivatives allocation to hedge short-term volatility

**Key Level Monitoring**:
- Break 490 → Opens upside to 520
- Fall below 475 → Triggers technical adjustment

---
*Data Sources: QVeris | THS iFinD, Caidazi, X Sentiment*
```

## Tool Chain Routing

This skill defines data acquisition priority routing via `references/tool-chains.json`:

```json
{
  "morning_brief": {
    "market_overview": ["ths_ifind.global_market", "alpha_vantage.market_status"],
    "policy_news": ["caidazi.news.query", "caidazi.report.query"],
    "company_quote": ["ths_ifind.real_time_quotation"],
    "industry_data": ["ths_ifind.industry_index", "caidazi.sector_analysis"],
    "sentiment": ["qveris_social.x_domain_hot_topics"]
  },
  "evening_brief": {
    "company_quote": ["ths_ifind.real_time_quotation", "ths_ifind.history_quotation"],
    "announcements": ["caidazi.news.query", "exchange_announcements"],
    "research": ["caidazi.report.query", "alpha_news_sentiment"],
    "fund_flow": ["ths_ifind.capital_flow", "ths_ifind.dragon_tiger"]
  }
}
```

## Security & Privacy

- Only uses `QVERIS_API_KEY`, does not store other credentials
- Only calls `qveris.ai` API
- Local persistence limited to configuration files within skill directory
- Research reports are for reference only and do not constitute investment advice

## Changelog

- v1.0.0: Initial version, supports basic morning/evening briefing functions
- v1.1.0: Added competitor analysis module
- v1.2.0: Added policy interpretation and risk alert modules
- v1.3.0: Full English localization
