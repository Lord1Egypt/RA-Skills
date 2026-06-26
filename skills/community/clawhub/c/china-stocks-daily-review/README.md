# 📊 china-stocks-daily-review · A股市场行情分析
# China A-Share Market Daily Analysis

> 每日A股盘前综述 / 盘中简评 / 盘后复盘，三层数据降级体系，适配微信移动端阅读。
> Daily pre-market briefing / intraday snapshot / post-market review for China A-shares, with a 3-tier data fallback system, optimized for WeChat mobile reading.

---

## 功能概览 · Features

本 Skill 支持三类报告的自动生成，根据用户输入或当前时间自动判断类型：
This Skill auto-generates three report types, determined by user input or current time:

| 报告类型 · Report Type | 自动触发时段 · Auto-trigger Window | 核心价值 · Core Value |
|---------|------------|---------|
| 🌅 盘前市场综述 · Pre-Market Briefing | 8:00–9:25 | 隔夜外盘映射 + 超预期消息筛选 + 三场景剧本推演 · Overnight global market mapping + surprise news filter + 3-scenario playbook |
| 🕛 盘中市场简评 · Intraday Snapshot | 9:30–15:00 | 盘前预判验证 + 主线延续性判断 + 下午策略修正 · Pre-market forecast validation + sector momentum check + afternoon strategy update |
| 📊 盘后复盘报告 · Post-Market Review | 15:00 后 · After 15:00 | 主线聚类复盘 + 情绪评级 + 明日策略展望 · Sector clustering recap + sentiment rating + next-day outlook |

---

## 数据架构：三层工具降级体系 · Data Architecture: 3-Tier Fallback

```
Tushare Pro 官方 API（第一优先 · Primary）
  ↓ 权限不足 / 网络异常 / 空数据 · Insufficient quota / network error / empty data
AKShare 开源库（第二优先 · Secondary，免费 · Free）
  ↓ 接口失效 / 空数据 · API failure / empty data
搜索引擎实时抓取（兜底 · Fallback，覆盖所有场景 · Covers all scenarios）
```

**核心原则 · Core Principle**：每个数据项独立降级，不因某一项失败放弃整个报告；数据缺失时留空标注，不臆想填充。
Each data item degrades independently — a single failure never aborts the full report. Missing data is left blank, never fabricated.

---

## 数据覆盖范围 · Data Coverage

**优先级 1（核心，必须完整 · P1 — Critical, must be complete）**
- 主要指数收盘 · Major index closing prices：上证 (SSE Composite) / 深证 (SZSE Component) / 创业板 (ChiNext) / 科创50 (STAR 50)
- 全市场成交额、涨跌家数 · Total market turnover & advance/decline count
- 涨停 / 跌停 / 炸板家数、连板梯队 · Limit-up / limit-down / broken limit-up counts & consecutive limit-up ladder
- 北向 / 南向资金净流入 · Northbound (mainland-bound) / Southbound (HK-bound) net capital flow

> 📌 **涨停 Limit-up**：A股个股单日最大涨幅限制（主板10%，科创板/创业板20%）。封在涨停价即"涨停"。
> A-share daily price limit (±10% main board, ±20% STAR/ChiNext). A stock "hitting limit-up" means it closes at the ceiling price.
>
> **炸板 Broken limit-up**：涨停后被大量卖单打开，反映情绪转弱。
> A limit-up that gets broken by heavy sell orders — a sign of weakening sentiment.
>
> **连板 Consecutive limit-ups**：连续多日涨停，连板梯队是当日持续涨停的股票序列。
> Stocks hitting limit-up on multiple consecutive days; the "ladder" ranks them by streak length.

**优先级 2（重要，尽力获取 · P2 — Important, best-effort）**
- 晚间超预期公告（业绩/重组/定增）· After-hours surprise announcements (earnings / M&A / private placement)
- 政策消息面（财联社快讯 + 搜索引擎）· Policy news (Cailianshe flash news + search engines)
- 行业板块资金流 + 涨幅排名 · Sector capital flow + performance ranking

**优先级 3（辅助，情绪指标 · P3 — Supplementary, sentiment indicators）**
- 涨停题材聚类热度 TOP8 · Top-8 limit-up themes by frequency
- 炸板率、涨跌比情绪评级 · Broken limit-up rate, advance/decline ratio sentiment rating

**优先级 4（外盘，时间允许时获取 · P4 — Overseas markets, time-permitting）**
- 隔夜美股三大指数 · Overnight US markets：道琼斯 (DJIA) / 纳指 (NASDAQ) / 标普500 (S&P 500)
- 中概股（纳斯达克中国金龙指数）· Chinese ADRs (Nasdaq Golden Dragon China Index)
- A50期指、人民币汇率 · FTSE China A50 futures, USD/CNY exchange rate

---

## Tushare Token 配置 · Tushare Token Setup

本 Skill 使用 Tushare Pro 官方 API 作为第一数据源，需要用户自有 Token（免费注册即可获得基础积分）。
This Skill uses the Tushare Pro API as its primary data source. A free account is sufficient for basic access.

**首次配置（仅需一次）· First-time Setup (one-time only)**：

```bash
# 1. 免费注册 / Register for free：https://tushare.pro/register?reg=666
# 2. 获取 Token / Get your Token：https://tushare.pro/user/token
# 3. 保存到本地 / Save locally（替换 YOUR_TOKEN / replace YOUR_TOKEN）：
python -c "from pathlib import Path; Path.home().joinpath('.tushare_token').write_text('YOUR_TOKEN')"
```

Token 保存于 `~/.tushare_token`，不写入代码，不上传任何云端。
Token is stored locally at `~/.tushare_token` — never committed to code or uploaded to any cloud.

**未配置 Token 时 · If Token is not configured**：自动降级至 AKShare，核心数据仍可正常获取。
Automatically falls back to AKShare; core data remains available.

---

## 自动推送：安装即生效 · Auto Push: Active After Installation

安装本 Skill 后，**每日自动推送默认开启**，无需额外配置。
After installation, **daily auto-push is enabled by default** — no extra setup needed.

| 时间 · Time | 报告 · Report | 说明 · Description |
|-----|-----|------|
| **08:55** | 🌅 盘前综述 · Pre-Market | 开盘前5分钟，外盘映射 + 今日策略 · 5 min before open: global market map + today's playbook |
| **11:35** | 🕛 盘中简评 · Intraday | 午间后5分钟，验证预判 + 下午推演 · 5 min after midday close: forecast check + afternoon strategy |
| **15:05** | 📊 盘后复盘 · Post-Market | 收盘后5分钟，全天复盘 + 明日展望 · 5 min after close: full-day recap + next-day outlook |

**推送目标 · Push Destination**：自动发送到用户绑定的消息端（微信 / WhatsApp 等）；未绑定则直接输出在对话窗口。
Reports are sent to the user's linked messaging channel (WeChat / WhatsApp etc.); if none is linked, output appears in the chat window.

**非交易日 · Non-trading days**：周末、节假日、临时休市日自动跳过，不生成不推送。
Weekends, public holidays, and unexpected market closures are automatically skipped.

**关闭方式 · How to disable**：在 WorkBuddy 自动化管理页暂停/删除对应任务，或直接告诉 WorkBuddy「关闭盘前自动推送」。
Pause or delete the tasks in WorkBuddy's Automation panel, or simply tell WorkBuddy: "关闭盘前自动推送" (disable pre-market auto-push).

### Automation 执行逻辑 · Automation Execution Logic

每个定时任务的 RRULE 及核心执行流程如下：
Each scheduled task's RRULE and core execution flow:

| 报告 · Report | RRULE | 执行流程 · Flow |
|---|---|---|
| 🌅 盘前综述 | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=8;BYMINUTE=55` | 交易日判断 → 三层降级取数（外盘/情绪/消息/连板/技术）→ 生成报告 → 保存 `report_YYYYMMDD_premarket.md` → 推送 |
| 🕛 盘中简评 | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=11;BYMINUTE=35` | 交易日判断 → 三层降级取数（指数/涨跌比/板块/连板）→ 读取盘前预判 → 生成报告 → 保存 `report_YYYYMMDD_intraday.md` → 推送 |
| 📊 盘后复盘 | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=15;BYMINUTE=5` | 交易日判断 → 三层降级取数（指数/情绪/资金/板块/连板）→ 读取盘前/盘中预判 → 生成报告 → 保存 `report_YYYYMMDD_postmarket.md` → 推送 |

**交易日判断 · Trade day check**：
```python
import akshare as ak
from datetime import date

def is_trade_day(check_date=None):
    if check_date is None:
        check_date = date.today()
    try:
        df = ak.tool_trade_date_hist_sina()
        return check_date.strftime('%Y-%m-%d') in set(df['trade_date'].astype(str))
    except Exception:
        return check_date.weekday() < 5  # 失败时以周一至周五兜底
```

**报告文件命名 · File naming**：

| 类型 · Type | 文件名 · Filename |
|---|---|
| 盘前 Pre-market | `report_YYYYMMDD_premarket.md` |
| 盘中 Intraday | `report_YYYYMMDD_intraday.md` |
| 盘后 Post-market | `report_YYYYMMDD_postmarket.md` |

---

## 报告输出格式 · Output Format

- **纯文字段落 + emoji 图标**，适配微信移动端 · Plain text paragraphs with emoji, optimized for WeChat mobile
- 不使用 Markdown 表格、`**加粗**`、`#标题`、`-列表` 等语法 · No Markdown tables, bold, headings, or bullet-list syntax
- 关键数字加粗标注，段落空行分隔 · Key figures highlighted, sections separated by blank lines
- 结论先行：每节第一句即为核心判断，数字支撑在后 · Conclusion-first structure: lead with the key takeaway, support with data

---

## 三类报告结构速览 · Report Structure Overview

### 🌅 盘前综述 · Pre-Market Briefing
```
一、隔夜外盘映射 · Overnight global market map (US / HK / A50 / FX → open sentiment)
二、昨日A股回顾 · Yesterday's A-share recap (indices / capital flow / sentiment / limit-up ladder)
三、核心消息面 · Key news (surprise events only; digested news excluded)
四、技术面关键点位 · Key technical levels (resistance / support / volume threshold)
五、今日策略 · Today's strategy (sector call + 3-scenario playbook: gap-up with volume / gap-up thin / gap-down >1%)
```

### 🕛 盘中简评 · Intraday Snapshot
```
一、上午盘面数据 · Morning session data (indices / turnover vs pre-market forecast)
二、主线验证与板块表现 · Sector momentum check (sustained / sector rotation "fan" switch)
三、连板情绪 · Limit-up sentiment (streak height vs yesterday)
四、下午策略推演 · Afternoon strategy (if A → then B conditional branches)
```

### 📊 盘后复盘 · Post-Market Review
```
一、指数全天表现 · Full-day index performance (volume + turnover)
二、市场情绪 · Market sentiment (A/D ratio / limit-up / broken rate / sentiment rating)
三、主线复盘 · Sector recap (ranked by strength, with driver classification)
四、今日小结与明日策略 · Summary & next-day strategy (offense / defense / key watchpoints)
```

---

## 情绪评级体系 · Sentiment Rating System

> A-share sentiment is gauged by three metrics: **advance/decline ratio** (涨跌比), **consecutive limit-up height** (连板高度), and **broken limit-up rate** (炸板率).

| 评级 · Rating | 涨跌比 · A/D Ratio | 连板高度 · Max Streak | 炸板率 · Broken Rate |
|-----|-------|---------|-------|
| 亢奋 · Euphoric | >8:1 | ≥6板 (days) | <15% |
| 偏热 · Warm | >5:1 | 4–5板 | <20% |
| 正常 · Neutral | 3–5:1 | 3板 | 20–30% |
| 偏冷 · Cool | 1–3:1 | ≤2板 | >30% |
| 低迷 · Depressed | <1:1 | — | >50% |

---

## 版本历史 · Changelog

| 版本 · Version | 日期 · Date | 主要更新 · Changes |
|-----|-----|---------|
| v1.2.0 | 2026-03-25 | 盘前/盘中模板全面升级：新增情绪评级+连板梯队+三场景剧本；盘中新增盘前预判对比+电风扇判断 · Full template upgrade: added sentiment rating, limit-up ladder, 3-scenario playbook; intraday now includes pre-market forecast comparison + sector rotation detection |
| v1.1.0 | 2026-03-25 | 新增财联社快讯数据源；新增盘中涨跌比取数；工具B搜索引擎冗余回退升级 · Added Cailianshe flash news; added intraday A/D ratio; upgraded search engine fallback |
| v1.0.0 | 2026-03-24 | 首版发布：三层漏斗体系 + 三类报告模板 + Tushare/AKShare 双源降级 · Initial release: 3-tier funnel system, 3 report templates, Tushare/AKShare dual-source fallback |

---

## 依赖环境 · Dependencies

```
Python >= 3.10
akshare >= 1.10.0   （pip install akshare）
tushare >= 1.2.89   （可选 optional，pip install tushare，需自有 Token · requires your own Token）
baostock            （可选 optional，pip install baostock，指数数据备用源 · fallback source for index data）
```

---

> ⚠️ 本 Skill 生成的报告仅供参考，不构成任何投资建议。市场有风险，投资须谨慎。
> Reports generated by this Skill are for informational purposes only and do not constitute investment advice. Invest at your own risk.
