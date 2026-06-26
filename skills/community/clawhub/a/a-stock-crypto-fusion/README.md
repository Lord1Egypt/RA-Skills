# FusionAlpha A&Crypto Desk

> 双市场（A股 + Crypto）分析技能，输出可执行的结构化报告。本文档提供详细使用说明、数据源、模板、架构、思维导图、FAQ、免责声明。中文为主，附英文摘要。

---
[English Version readme](#full-english-version)
## 目录
1. [概览 / Overview](#概览--overview)
2. [适用场景与优势](#适用场景与优势)
3. [触发规则与语言策略](#触发规则与语言策略)
4. [输出类型与模板](#输出类型与模板)
5. [时间周期与指标范围](#时间周期与指标范围)
6. [数据源与字段](#数据源与字段)
7. [安装与使用步骤](#安装与使用步骤)
8. [可选新闻源 CryptoPanic Token](#可选新闻源-cryptopanic-token)
9. [技能架构与流程](#技能架构与流程)
10. [思维导图 / Mind Map](#思维导图--mind-map)
11. [评测与质量现状](#评测与质量现状)
12. [常见问题 FAQ](#常见问题-faq)
13. [故障排查与回退策略](#故障排查与回退策略)
14. [安全与合规注意事项](#安全与合规注意事项)
15. [免责声明 / Disclaimer](#免责声明--disclaimer)
16. [Changelog](#changelog)


---

## 概览 / Overview
- **技能名称**：FusionAlpha A&Crypto Desk
- **覆盖市场**：A股 + 加密（可单独或混合输出）
- **默认输出**：
  - 加密三维共振报告
  - A股深度分析报告
  - 早盘决策内参
- **核心特点**：多维数据、模板硬约束、证据清单、方向/胜率/回撤/盈亏比，自动识别用户语言（中文优先，否则英文）。
- **使用场景**：研究学习、策略草稿、日报/简报生成、AI Agent 演示；非投资建议。

---

## 适用场景与优势
- **双市场融合**：同一技能支持 A股 与 Crypto，亦可生成双市场并行的观点/简报。
- **数据丰富**：K线/指标、订单簿/交易流、衍生品、行业/主力资金流、涨停池、龙虎榜、财经早餐；主要公共接口免密钥。
- **结构化可执行**：模板固定，强制证据清单、末行格式、方向约束、盈亏比/胜率/回撤约束。
- **语言自适应**：根据用户输入自动选择中文或英文回复。
- **安全兜底**：数据缺失时降级提示，不臆造；新闻源需用户自备 token，未提供则标注“未提供新闻源 token”。

---

## 触发规则与语言策略
- 触发关键词（中文）：币/crypto 行情、A股个股/板块、早盘内参/早报、交易策略、入场、止损、目标、胜率、回撤、盘口、资金费率、持仓、龙虎榜、涨停池。
- Trigger (English): crypto/coin analysis, A-share/China stock analysis, dual-market view, morning briefing, trading plan, entry/stop/targets, win rate, drawdown, order book, funding, OI.
- 语言：检测用户语言；中文优先，否则英文回复。

---

## 输出类型与模板
### A) 加密三维共振报告（Crypto 3D Resonance）
```
标题：
总结（7-10句）：
1) 中观：市场周期诊断
2) 宏观：背景/关键区间/VPVR
3) 微观：CVD/大单流/吸收
交易策略与决策：
- 决策（做多/做空/观望）
- 共振等级（强一致/部分一致/冲突可用/数据不足）
- 核心逻辑
- 仓位建议
- 入场/止损/目标/盈亏比
风险管理：
- 主要风险
证据清单：
证据1: <字段路径>=<数值>
证据2: <字段路径>=<数值>
(不少于2条)
最后一行（必须是最终行）：
币名[方向][胜率：X%][最大回撤：Y%]
```

### B) A股深度分析报告（A-share Deep Dive）
```
标题：
投资要点总结：
1. 基本面分析
2. 技术面分析
3. 资金与筹码分析
4. 机构与情绪分析
5. 新闻与研报解读
6. 交易策略与风险提示
证据清单：
证据1: <字段路径>=<数值>
证据2: <字段路径>=<数值>
(不少于2条)
最后一行（必须是最终行）：
股票名称(股票代码)[操作方向][胜率：X%][最大回撤：Y%]
方向仅限：积极买入 / 逢低吸纳 / 保持观望。
```

### C) 早盘决策内参（Morning Brief）
```
交易内参 - [日期]
一、今日财经要闻
二、市场核心看板
三、今日核心攻击方向
四、潜在焦点个股池
五、交易纪律与风险提示
```

---

## 时间周期与指标范围
- **Crypto**：默认用 5m/15m/1h（由上游数据决定，可包含日线）。
- **A股**：日线技术指标 + 盘口买一卖一 + 资金/筹码/龙虎榜/研报。
- **早盘**：当日指数开盘、行业资金（即时/今日）、前一交易日涨停池（或当日备源）、机构龙虎榜、财经早餐。

---

## 数据源与字段
技能本身不直接拉数据；可用 `scripts/` 直接抓取 JSON（或由上游自备数据）。字段说明与已测列名见 `references/data_sources.md`。

公共接口（2026-03-11 烟测）：
- Crypto（ccxt binanceusdm）：ticker/ohlcv/orderbook/trades/funding/OI。
- A股（akshare）：
  - `stock_fund_flow_industry`（行业资金流）
  - `stock_zt_pool_previous_em` / `stock_zt_pool_em`（涨停池）
  - `stock_lhb_jgzz_sina` / `stock_lhb_jgmmtj_em`（机构龙虎榜）
  - `stock_info_cjzc_em` / `stock_info_global_em/ths/futu/sina`（财经早餐/全球快讯）
  - 指数/实时行情接口偶发断开：`stock_zh_a_spot_em`、`stock_zh_index_spot_em`，建议重试或用拆分/备用接口。
- 早盘内参：指数开盘、行业资金流、涨停池、机构龙虎榜、财经早餐（多源 fallback 已列出）。
- 新闻源：CryptoPanic（需用户提供 token）。

---

## 安装与使用步骤
前置：Python 3（建议 3.10+）。脚本会访问公共数据源；若网络/接口波动会返回部分字段，并在 `meta.errors` 里记录原因。

1) 放置技能目录：`~/.config/opencode/skills/fusionalpha-acrypto-desk/`

2) 安装依赖（二选一）：
   - 一键创建 venv 并安装：`python3 scripts/bootstrap.py`
   - 直接安装到当前 Python：`python3 -m pip install -r scripts/requirements.txt`

3) 抓取 JSON（stdout 纯 JSON，可直接重定向为文件）：
   - Crypto：`python3 scripts/fetch_crypto.py --symbol BTC/USDT > crypto.json`
   - A股：`python3 scripts/fetch_ashare.py --code 600519 > ashare.json`
   - 早盘：`python3 scripts/fetch_morning.py --date 20260311 > morning.json`
   - 可选新闻（CryptoPanic）：
     - `export CRYPTOPANIC_TOKEN=...` 然后 `python3 scripts/fetch_news.py --base BTC --limit 5 > news.json`

4) 喂给任意 AI（开箱即用方式）：
   - 若不是 OpenCode 环境：把 `SKILL.md` 作为系统指令/Developer 指令粘贴进对话开头。
   - 把第 3 步得到的 JSON 粘贴进用户消息，并明确要输出哪种模板（Crypto/A股/早盘）。

示例请求（Crypto）：
```
请严格按 SKILL.md 的“加密三维共振报告”模板输出。下面是 market_data JSON：
<把 crypto.json 内容粘贴到这里>
```

---

## 可选新闻源 CryptoPanic Token
- 仅当用户需要“加密新闻/资讯/情绪”时提示索要 token。
- 通过环境变量 `CRYPTOPANIC_TOKEN` 或上游参数传入；**不要在回复中回显或存储 token**。
- 未提供 token 时：新闻为空或注明“未提供新闻源 token”，其余分析正常输出。
- Developer 计划不要加 `size` 参数（会返回 api_error）。

---

## 技能架构与流程
1) **触发**：检测用户意图（行情/策略/早报/双市场）；语言检测。
2) **数据输入**：上游喂入 JSON（行情/指标/盘口/资金流/衍生品/龙虎榜/研报/新闻等）。
3) **模板选择**：根据意图选择 Crypto / A股 / 早盘模板；可双市场并行输出。
4) **约束执行**：
   - 证据清单 ≥2，字段路径+数值。
   - 末行格式固定；A股方向仅“积极买入/逢低吸纳/保持观望”；Crypto 盈亏比 <1.5 则观望。
   - 胜率分档：强≤85，部分≤60，冲突/数据不足≤50。
5) **输出**：按用户语言返回 Markdown（但保持标题/标签/末行精确一致，不包整体 code block）。

---

## 思维导图 / Mind Map (ASCII)
```
FusionAlpha A&Crypto Desk
├─ 触发
│  ├─ Crypto 行情/策略/入场/止损/目标/胜率/回撤
│  ├─ A股 个股/板块/龙虎榜/涨停池/早报
│  └─ 早盘决策内参
├─ 数据
│  ├─ Crypto: ticker/ohlcv/orderbook/trades/funding/OI
│  ├─ A股: 行业资金/涨停池/龙虎榜/研报/筹码/财经早餐
│  └─ 新闻: CryptoPanic (需 token)
├─ 模板
│  ├─ Crypto 3D 共振
│  ├─ A股深度分析
│  └─ 早盘内参
├─ 约束
│  ├─ 证据≥2、字段+数值
│  ├─ 末行格式固定
│  ├─ 胜率分档 强≤85/部分≤60/冲突≤50/不足≤50
│  └─ A股只做多；Crypto 盈亏比<1.5 则观望
└─ 输出
   ├─ 语言自适应（中文优先）
   └─ Markdown 可用，标题/标签/顺序不可改
```

---

## 评测与质量现状
- 结构化评测（iteration-3）：with-skill 通过率 100% vs baseline 39%，Δ +0.61。
- 三类用例：Crypto 三维共振、A股深度、早盘内参均通过模板与断言。
- 描述优化：当前为手工优化描述（未跑 run_loop，因环境缺少 `claude` CLI）。

---

## 常见问题 FAQ
1) **缺少数据可以用吗？**  
   可以，但输出会降级并提示缺数据；建议提供结构化 JSON。

2) **akshare 指数/spot 偶尔断开？**  
   已知 `stock_zh_a_spot_em`、`stock_zh_index_spot_em` 偶发远端断开；请重试或用拆分/备用接口。

3) **CryptoPanic 报错 api_error？**  
   Developer 计划不要加 `size`；需 `public=true`；token 由用户自备。

4) **输出语言能指定吗？**  
   自动检测；若需强制英文，可在请求中明确“用英文输出”。

5) **方向/胜率/盈亏比是否强制？**  
   是。A股仅多头方向；Crypto 盈亏比 <1.5 必须改为观望；胜率分档上限强≤85/部分≤60/冲突≤50/不足≤50。

6) **证据清单必须数值吗？**  
   至少两条，需包含字段路径与具体数值/枚举；避免泛化描述。

7) **能否混合输出双市场视角？**  
   可以，在同一请求中要求 A股 + Crypto 简报或策略对照。

---

## 故障排查与回退策略
- 接口 40x/50x：重试或换备源（见 `references/data_sources.md`）。
- 数据缺失：在输出中标注缺失项，保持模板完整，避免臆造。
- 新闻不可用：标注“未提供新闻源 token”或“新闻源调用失败”。
- 早盘脚本：部分源失败会自动降级；详情见输出里的 `meta.errors`。
- 语言/格式错乱：检查是否使用了正确触发语和模板；避免整体 code block 包裹。

---

## 安全与合规注意事项
- 不回显/存储任何密钥；CryptoPanic token 仅由用户提供并在调用端使用。
- 输出仅供研究学习，不构成投资、法律或财务建议。
- 使用本技能即视为同意免责声明。

---

## 免责声明 / Disclaimer
本技能仅用于研究、学习与探索 AI Agent 在市场分析场景的可能性，不构成任何投资、法律或财务建议。使用者需自行承担全部风险；作者、发布者对任何损失不承担责任。下载、安装或使用本技能即视为同意本免责声明。  
For research/learning only. No financial/legal advice. Use at your own risk. Authors/publishers bear no liability. Installing/using implies acceptance of this disclaimer.

---

## Changelog
- v1.0：完成三类输出模板、数据源文档、评测迭代至 iteration-3（with-skill 100% vs baseline 39%）。

---

## Full English Version

### Overview
- **Name**: FusionAlpha A&Crypto Desk
- **Markets**: A-share (China) + Crypto (can be separate or mixed)
- **Defaults**: Crypto 3D resonance report, A-share deep dive, Morning briefing
- **Features**: multi-source data, hard templates, evidence lists, direction/win-rate/drawdown/R:R constraints, auto language detection (Chinese preferred, else English)
- **Use**: research/learning, strategy drafts, briefs; **not** financial advice

### 1) Scenarios & Advantages
- Dual-market coverage; mixed or single-market outputs
- Rich data: OHLCV/indicators, order book/flow, derivatives, fund flows, limit-up pool, LHB, breakfast; mostly public/no key; optional CryptoPanic token
- Structured, executable templates; evidence lists; strict final-line formats; R:R/win-rate/direction constraints
- Language auto-detect (Chinese preferred, else English)

### 2) Triggers & Language
- Triggers (EN): crypto/coin analysis, A-share/China stock analysis, dual-market view, morning briefing, trading plan, entry/stop/targets, win rate, drawdown, order book, funding, OI.
- Triggers (CN): crypto/币、A股个股/板块、早报/内参、策略/入场/止损/目标/胜率/回撤、盘口/龙虎榜/涨停池。
- Language: detect user input; respond in same language (CN preferred, else EN).

### 3) Outputs & Templates
**A) Crypto 3D Resonance**
```
Title:
Summary (7-10 sentences):
1) Mid-term: market cycle
2) Macro: context/levels/VPVR
3) Micro: CVD/large flow/absorption
Trading decision:
- Decision (long/short/observe)
- Resonance level (strong/partial/conflict/insufficient)
- Core logic
- Positioning
- Entry/Stop/Targets/R:R
Risk mgmt: key risks
Evidence list (>=2): field path + value
Final line (must be last):
<Coin>[Direction][Win rate:X%][Max drawdown:Y%]
```

**B) A-share Deep Dive**
```
Title
Key takeaways
1. Fundamentals
2. Technicals
3. Fund & chips
4. Institution & sentiment
5. News & research
6. Strategy & risks
Evidence list (>=2)
Final line (must be last):
StockName(StockCode)[Direction][Win rate:X%][Max drawdown:Y%]
Direction only: buy / buy-the-dip / observe
```

**C) Morning Brief**
```
Daily Brief - [date]
1) Top news
2) Market dashboard
3) Attack directions
4) Watchlist
5) Discipline & risks
```

### 4) Timeframes
- Crypto: typically 5m/15m/1h (plus daily if provided)
- A-share: daily indicators + Level1 bid/ask + fund/chips/LHB/research
- Morning: today’s open, sector flows (即时/今日), prior-day limit-up pool (or same-day fallback), institutional LHB, breakfast

### 5) Data & Fields
- The skill itself does **not** fetch data at inference time. Use `scripts/` to fetch JSON (or provide your own upstream JSON). See `references/data_sources.md`.
- Public sources tested (2026-03-11):
  - Crypto via ccxt binanceusdm: ticker/ohlcv/orderbook/trades/funding/OI
  - A-share via akshare: `stock_fund_flow_industry`, `stock_zt_pool_previous_em`/`stock_zt_pool_em`, `stock_lhb_jgzz_sina`/`stock_lhb_jgmmtj_em`, `stock_info_cjzc_em`, `stock_info_global_em/ths/futu/sina`; spot/index may occasionally disconnect (retry/fallback)
  - Morning brief: index, sector flow, limit-up pool, LHB, breakfast (multi-source fallbacks)
  - News: CryptoPanic (user token)

### 6) Install & Use
Prereqs: Python 3 (3.10+ recommended). Scripts call public data sources; intermittent failures return partial fields and are recorded in `meta.errors`.

1. Place skill at `~/.config/opencode/skills/fusionalpha-acrypto-desk/`

2. Install deps (choose one):
   - Bootstrap a local venv + install: `python3 scripts/bootstrap.py`
   - Install into current Python: `python3 -m pip install -r scripts/requirements.txt`

3. Fetch JSON (stdout is JSON-only; you can redirect to files):
   - Crypto: `python3 scripts/fetch_crypto.py --symbol BTC/USDT > crypto.json`
   - A-share: `python3 scripts/fetch_ashare.py --code 600519 > ashare.json`
   - Morning: `python3 scripts/fetch_morning.py --date 20260311 > morning.json`
   - Optional news (CryptoPanic):
     - `export CRYPTOPANIC_TOKEN=...` then `python3 scripts/fetch_news.py --base BTC --limit 5 > news.json`

4. Use with any LLM:
   - If you are not using OpenCode: paste `SKILL.md` into your system/developer instructions.
   - Paste the JSON from step 3 and explicitly request one of the templates (Crypto/A-share/Morning).

Example prompt (Crypto):
```
Follow the exact “Crypto Three-Dimension Resonance Report” template in SKILL.md.
Here is the market_data JSON:
<paste crypto.json here>
```

### 7) Constraints
- Evidence list >=2, with field path + value
- Exact headings/order; fixed final-line formats
- Win-rate brackets: strong≤85, partial≤60, conflict/insufficient≤50
- Crypto: R:R ≥1.5 else observe
- A-share: long-only (buy / buy-the-dip / observe)
- Markdown allowed, but keep headings/labels intact; do not wrap whole output in a code block

### 8) FAQs
- Missing data? Output degrades gracefully and notes missing fields.
- Akshare spot/index flaky? Retry or use split/fallback interfaces.
- CryptoPanic api_error? Omit `size` on Developer plan; use `public=true`; user must provide token.
- Language? Auto; force English by asking explicitly.
- Strictness? Yes—directions constrained, evidence required, final-line fixed.

### 9) Troubleshooting
- HTTP 40x/50x: retry or switch to fallbacks (see references/data_sources.md)
- No news token: leave news empty or note “no news token provided”
- Morning script: partial failures are recorded in `meta.errors`
- Format drift: ensure correct template headings/labels; keep final line last

### 10) Safety & Compliance
- Never echo/store keys. CryptoPanic token only used if user supplies it.
- Research/learning only; not financial advice.
- Using the skill means accepting the disclaimer.

### 11) Disclaimer (English)
For research/learning only. No financial/legal advice. Use at your own risk. Authors/publishers bear no liability. Installing/using implies acceptance of this disclaimer.

### 12) Changelog
- v1.0: templates, data references, eval iteration-3 (with-skill 100% vs baseline 39%).
