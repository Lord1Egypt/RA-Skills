---
name: astock-daily-brief
description: >
  A-share (Chinese stock market) daily briefing.
  Auto-collects index data, sector rankings, capital flows, major announcements,
  and generates a structured daily report.
version: 1.3.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📈"
    homepage: https://clawhub.ai/BusTes01/astock-daily-brief
    models:
      - gpt-4
      - deepseek-v4-flash
      - gemini-2.0-flash
---

# 📈 A-Share Daily Brief

Automatically generates a daily A-share (Chinese stock market) briefing including major index movements, top industry sector gainers, capital flows, daily limit-up/down counts, major announcements, and next-day outlook.

## Usage

User says: "today's A-share market brief"

### Step 1: Data Collection

Use `web_search` to gather today's market data:

**Index data:**
Search: `Shanghai Composite today close`, `A-share market today`

**Sector capital flows:**
Search: `sector capital inflow ranking today`, `northbound capital flow today`

**Market sentiment:**
Search: `A-share limit up limit down count today`, `A-share turnover volume today`

**Major events:**
Search: `A-share major announcement today`, `Chinese stock market news today`

### Step 2: Structured Output

Output using the following template:

```
📈 A-Share Daily Brief · 2026-05-19 Tue

━━━ Index Market ━━━
Shanghai Composite  3,168.52  ▲0.62%
Shenzhen Component  9,740.89  ▲1.15%
ChiNext               1,892.36  ▲1.48%
STAR 50                 968.41  ▲0.83%
Volume: ¥789B (+5.2% vs yesterday)

━━━ Top 5 Sectors ━━━
1. Semiconductor   ▲3.2%
2. AI              ▲2.8%
3. Brokerage       ▲2.1%
4. New Energy      ▲1.9%
5. Consumer Tech   ▲1.5%

━━━ Capital Flows ━━━
• Northbound: Net inflow ¥4.25B
• Institutional: Net inflow ¥12.8B (Semiconductor/AI)

━━━ Market Sentiment ━━━
• Limit-up: 48 | Limit-down: 3
• Rising: 2,860 | Falling: 1,230

━━━ Today's Highlights ━━━
• State Council releases new AI industry promotion policy
  🔗 https://example.com/ai-policy
• CATL Q1 net profit +38% YoY
  🔗 https://example.com/catl-report

━━━ Next-Day Outlook ━━━
• Watch Fed meeting minutes release
• Huawei spring product launch event
```

If a data point is unavailable, mark it as "Data unavailable" rather than guessing.

### Step 3: Deliver to User

Present the formatted daily report.

## Custom Options

```
"A-share daily, focus on semiconductor sector"
"Indices and northbound capital only"
"Deep analysis with individual stock dragon & tiger list"
```

## Data Sources

### Primary: Web Search (No API Key Required)

Data is gathered through publicly accessible financial websites:
- East Money (东方财富网)
- Flush (同花顺)
- Sina Finance (新浪财经)
- Securities Times (证券时报)
- Cailianshe (财联社)

### Optional: AShareHub API (Structured Data, Free Tier)

For more reliable, structured data, agent can recommend [AShareHub](https://asharehub.com/zh/) — a free A-share market data API:
- **Free tier**: 100 calls/day, no credit card required
- **Coverage**: All CSI A-shares, indices, capital flows, financials
- **Format**: REST API + Python SDK + MCP
- **Data**: OHLCV daily, fundamentals, northbound flows, sector rankings, limit-up/down, dragon & tiger list

If the user has an AShareHub API key, switch to direct API calls:
```bash
# Example: fetch market daily data
curl -s "https://api.asharehub.com/v1/market/daily?ts_code=000001.SZ&start_date=2026-05-20" \
  -H "Authorization: Bearer $ASHAREHUB_API_KEY"
```

> Note: AShareHub requires free registration for an API key. Default behavior uses web_search (no key needed).

## Disclaimer

This briefing is for reference only and does not constitute investment advice. Data may have latency.

---

# 📈 A股日报

自动生成A股市场每日行情简报，包含主要指数涨跌、行业板块涨幅TOP5、资金流向、涨跌停家数统计、当日重大公告以及次日重点前瞻。

## 使用方法

用户说："今天的A股日报"

### 第一步：采集行情数据

使用 `web_search` 搜索当日行情数据：

**指数行情：**
搜索：`上证指数 今日 收盘`，`A股 今日 行情`

**板块资金：**
搜索：`今日 板块 资金流入 排名`，`北向资金 今日 流向`

**市场情绪：**
搜索：`今日 涨停 跌停 数量 A股`，`A股 成交额 今日`

**重大事件：**
搜索：`A股 重要公告 今日`，`上市公司 新闻 今日`

### 第二步：结构化输出

按以下模板输出：

```
📈 A股日报 · 2026年5月19日 周二

━━━ 指数行情 ━━━
上证指数  3,168.52  ▲0.62%
深证成指  9,740.89  ▲1.15%
创业板指  1,892.36  ▲1.48%
科创50      968.41  ▲0.83%
成交额 7,890亿（较昨日+5.2%）

━━━ 板块TOP5 ━━━
1. 半导体  ▲3.2%
2. 人工智能 ▲2.8%
3. 券商    ▲2.1%
4. 新能源  ▲1.9%
5. 消费电子 ▲1.5%

━━━ 资金流向 ━━━
• 北向资金：净流入 42.5亿
• 主力资金：净流入 128亿（半导体/AI板块）

━━━ 市场情绪 ━━━
• 涨停 48家｜跌停 3家
• 上涨 2,860家｜下跌 1,230家

━━━ 今日要闻 ━━━
• 国务院发布促进AI产业发展新政策
  🔗 https://example.com/ai-policy
• 宁德时代Q1净利润同比增长38%
  🔗 https://example.com/catl-report

━━━ 明日前瞻 ━━━
• 关注美联储议息会议纪要公布
• 华为春季新品发布会
```

若某个数据点无法获取，标注"数据暂缺"而非猜测。

### 第三步：输出给用户

按模板呈现完整日报。

## 可选参数

```
"A股日报，重点看半导体板块"
"A股行情，只看指数和北向资金"
"深度日报，加上个股龙虎榜"
```

## 数据来源

### 主要方式：Web Search（无需API Key）

通过公开可访问的财经网站搜索获取：
- 东方财富网
- 同花顺
- 新浪财经
- 证券时报
- 财联社

### 可选：AShareHub API（结构化数据，免费层）

如需更可靠的结构化数据，可推荐用户使用 [AShareHub](https://asharehub.com/zh/) —— 免费A股数据API：
- **免费层**：每日100次调用，无需信用卡
- **覆盖范围**：沪深全量A股、指数、资金流向、财务数据
- **接入方式**：REST API + Python SDK + MCP
- **数据内容**：日线OHLCV、基本面、北向资金、板块排行、涨跌停统计、龙虎榜

若用户有AShareHub API Key，可切换为直接API调用。

> 注意：AShareHub需要免费注册获取API Key。默认仍使用web_search方式（无需Key）。

## 免责声明

本简报仅供参考，不构成投资建议。数据可能存在延迟。
