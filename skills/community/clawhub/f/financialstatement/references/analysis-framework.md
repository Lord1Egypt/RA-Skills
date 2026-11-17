# US Tech Giant Analyst — Deep Analysis Framework

Use this template as the exact output skeleton for every company analysis. Replace bracketed cues with sourced facts and a clear judgment. The HTML report is the primary deliverable; the markdown version mirrors the same sections for archival.

## Depth Rules

- Every section needs at least one concrete number AND one judgment. No summary-only sections.
- Build the HTML report self-contained (inline CSS/SVG, no CDN, no external JS).
- Include at least three charts: a market-share donut, a revenue-trend bar chart, and either a segment-mix stacked bar or a 52-week range bar.

## Report Template

```
# [公司名] ([TICKER]) 深度分析报告
数据日期：YYYY-MM-DD

## 0. 核心摘要 (Core Summary)
- 关键指标卡：营收、净利润、毛利率、市值、目标价、买入评级占比。
- 一句话结论：[核心判断：优势 + 主要隐忧]。
- 要点：5 条以内，每条带数字。

## 1. 商业模式 (Business Model)
- 营收结构：按业务板块拆（如 数据中心 92% / 游戏+边缘 8%），标注各板块占比与同比增速。
- 三层拆解：产品/系统/软件（或等价的三层）各贡献什么。
- 客户结构：前几大客户类型及占比（如 超大规模云 vs 企业）。
- 赚钱逻辑：高毛利 + 生态锁定 + 回购；近期结构性变化。
- 判断：[商业模式是否稳健、是否有新引擎。]

## 2. 市场占额 (Market Share)
- 赛道大盘：[赛道名] 全球规模与增速（如 全球半导体 ~$975B，2026E）。
- 份额：本公司约 X%（来源），并注明口径差异（含/不含自研芯片等）。
- 竞争对手：最近对手 [对手] 约 Y%，用表格列出 3-4 家。
- 判断：[份额趋势 + 是否被侵蚀 + 护城河信号。]

## 3. 发展前景 (Growth Prospects)
- 2-3 年主线：[如 AI 资本开支、推理迁移、主权 AI]。
- 跨年指引/订单可见性：[如有，如 下季指引、未完成订单]。
- 上行驱动 / 下行风险：各列 2-3 个，带具体数字。
- 判断：[增长确定性高/中/低 + 主要矛盾（需求 vs 供给）。]

## 4. 技术壁垒 (Technology Moat)
- 壁垒类型：规模效应 / 网络效应 / 专利 IP / 软硬一体 / 数据飞轮 / 供应链锁定。
- 证据：逐条给出，每条带数字（开发者数、产能锁定比例、研发投入等）。
- 判断：[壁垒可持续性与时间窗口。]

## 5. 财报表现 (Financial Reports)
- 最新季：营收 [X]（同比 +X%）、净利润 [X]、毛利率 [X]%、经营利润率 [X]%、FCF [X]。
- 对比预期：beat/miss 共识；连续超预期次数。
- 近 5 年：营收与净利趋势（图表或表格）。
- 资产负债表：现金、供给承诺/负债、回购分红、DSO 等。
- 判断：[财务健康度与可持续性。]

## 6. 股价走势 (Stock Price Trend)
- 近期表现：52 周区间 [低-高]、当前价、YTD 涨跌、市值。
- 催化/压制：[财报后走势、关键事件]。
- 共识：目标价均值 [X]（最高/最低），评级分布（买/持/卖占比）。
- 判断：[仅作背景，非投资建议。]

## 7. 估值对比 (Valuation vs Peers)
- 表格：本公司 + 3-4 家同行，列 远期P/E、PEG、P/S。
- 判断：[相对增长斜率，估值贵不贵、为什么。]

## 8. 主要风险 (Key Risks) — 风险矩阵
- 按"概率 × 影响"列 4-6 条，如：供给瓶颈、资本开支集中、出口管制、自研侵蚀、估值、地缘。

## 数据来源与日期 (Sources & Dates)
- [来源名称 + URL]（抓取日期）
```

## Source Checklist (prefer primary)

- SEC filings: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=[TICKER]
- Company investor relations: [ir.company.com] → Quarterly Results / SEC Filings
- Market share: IDC, Canalys, StatCounter, Gartner, Omdia, TrendForce, Jon Peddie Research, Silicon Analysts
- Valuation & estimates: Nasdaq, Reuters, Investing.com, analyst consensus aggregates
- News catalysts: Reuters, Bloomberg, CNBC, The Information (verify date)

## Chart Requirements (HTML, inline only)

1. Market-share donut — use CSS `conic-gradient` with a legend.
2. Revenue-trend bar chart — CSS flexbox bars or inline SVG; label each bar with value + YoY.
3. Segment-mix stacked bar OR 52-week range bar (with current-price marker).

No Chart.js / CDN. Everything must render offline.

## Worked Example (deep) — NVIDIA (NVDA), data as of the latest quarter

Fill the template above with live figures each run. Skeleton with real example numbers (verify and refresh at run time):

- 核心摘要: FY27 Q2 营收 $96.2B(+106%)、数据中心 $89.0B(+117%)、毛利率 75%、市值 ~$5.49T、目标价均值 $334.67、96% 买入。结论：需求远超供给、护城河牢固，但 HBM 瓶颈压毛利。
- 商业模式: 数据中心占 92.5%（超大规模云 $48.7B / AI云+企业 $40.3B）；芯片+系统+软件三层；"算力即收入"。
- 市场占额: IDC 约 81%；仅商用芯片口径 87.4%；计入自研 ASIC 75-80%；中国≈0%。对手 AMD 5-7%、Intel ~1%、自研 ASIC 12-18%。
- 发展前景: Q3 指引 $108B；首次 FY28 +70% 指引；云厂未完成订单 >$2T；hyperscaler capex 2026 $650-700B。风险：内存涨价压毛利至 71-72%。
- 技术壁垒: CUDA 500万+开发者；锁定 ~60% TSMC CoWoS；HBM4 锁供；Vera Rubin 3nm/3360亿晶体管。
- 财报: 近5年营收 FY22 $26.9B → FY26 $215.9B；净利 FY26 $120B；FCF $21.3B/季；供给承诺 $279B。
- 股价: 52周 $164.07-236.54，现 $217.55，YTD +10%；目标价均值 $334.67（高 $710.29/低 $180）。
- 估值: 远期 P/E 24-32x（行业均值 35.7x）；PEG 0.27-0.42；AMD 30-63x / Intel ~61x / Broadcom 31-41x / Qualcomm 15x。
- 风险: 内存供给(高·高)、AI capex 集中(高·中)、出口管制(中·高)、自研 ASIC(中)、估值(中)、台积电地缘(低·极高)。
- 来源: SEC 8-K、NVIDIA IR、IDC/Silicon Analysts/TrendForce、stockanalysis/Investing.com、券商研报聚合（填 URL 与日期）。
