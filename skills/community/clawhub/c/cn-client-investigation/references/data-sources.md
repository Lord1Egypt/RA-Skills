# CN Data Sources — 按 tier 的详细调用指南

## T1 — 交易所 / 监管披露（必查，文本权威）

### 巨潮资讯网 cninfo.com.cn

- **用途**：上市公司招股书、年报、季报、重大公告的 PDF 原文
- **Search URL pattern**：`http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=<关键词>`
- **调用方式**：先 `brave-web-search "<公司名> 招股书 cninfo"` 拿 URL，再 `web_fetch` 下载 PDF，用 `pdf` skill / `markitdown` 提文本
- **审计要点**：优先取最近 1-2 年披露版本；注意"草案"（draft）与"正式版"（final）差异

### Tushare Pro（通过 aigroup-market-mcp）

支持的常用 tool 及用途：

| Tool | Purpose | 注意 |
|------|---------|------|
| `aigroup-market-mcp__basic_info` | 公司基础信息（上市日期、行业、注册地、代码） | 部分字段为空，需二次核对 |
| `aigroup-market-mcp__company_performance` | 季度/年度利润表、资产负债表 | 日期格式 YYYYMMDD；注意单季 vs TTM |
| `aigroup-market-mcp__stock_data` | 日线行情（开盘/收盘/成交量/换手） | 大批量需分页 |
| `aigroup-market-mcp__macro_econ` | 宏观指标（CPI/GDP/利率/汇率） | 可用于行业分析背景 |

Token 权限坑：Tushare 对各 api 有 points 要求，某些 api 可能 402 无权限。

### 上交所 / 深交所 / 港交所 官网

- SSE: `www.sse.com.cn` — 科创板和主板披露，重大事项通报
- SZSE: `www.szse.cn` — 创业板和主板
- HKEX: `www.hkex.com.hk` — 港股招股书（IPO prospectus）、年报

## T2 — 工商 / 法律 / 商业 数据库

### 天眼查（tianyancha.com）/ 企查查（qcc.com）

- 股权结构、对外投资、诉讼、专利、招投标
- 如果 `aigroup-tianyancha-mcp` MCP 已装，优先走它；否则 `brave-web-search` + `web_fetch` 公开页
- 未上市公司 / 独角兽（如摩尔线程、壁仞）主要靠这个

### 国家企业信用信息公示系统 gsxt.gov.cn

- 官方工商登记底档
- 适合查实际控制人穿透 / 分支机构 / 行政处罚

## T3 — 第三方数据服务

### Wind / 同花顺 / 东方财富

- 付费服务，本栈不直接调；agent 若遇到数据可用性 gap，可建议用户线下 Wind 查，报告里标 "数据来源 Wind（未直接抓取）"

### FMP / Finnhub（via aigroup-fmp-mcp / aigroup-finnhub-mcp）

- 主要覆盖港股 H 股、中概股 ADR、和海外 peers（NVDA/AMD/INTC）
- 对 A 股覆盖有限，慎用

## T4 — 公开财经媒体

按权威程度排序（仅做补充，不作主数据源）：

| 媒体 | 特点 |
|------|------|
| 财新 caixin.com | 调查深度高，付费墙部分可跳过 |
| 21 世纪经济报道 21jingji.com | 产业观察 |
| 中国证券报 zgjrjw.com | 证监会官媒口径 |
| 上海证券报 cnstock.com | 同上 |
| 财联社 cls.cn | 实时快讯，准确率中等 |
| 澎湃 thepaper.cn | 长文深度 |
| 第一财经 yicai.com | 宏观 |

## 数据 provenance 记录模板

每个报告建一个 `data-provenance.md` 放在 deliverable 目录，格式：

```markdown
# <Company> 数据溯源表

| 指标 | 数值 | 单位 | 期间 | T | 源 | URL / 工具 | 取数时间 | 交叉验证 |
|------|-----|------|------|---|----|-----------|----------|---------|
| 2024Q3 营业收入 | 5.2 | 亿RMB | 2024-07 至 2024-09 | T1 | 巨潮资讯 2024Q3 业绩快报 | http://... | 2026-04-18 | Tushare company_performance OK ±0.5% |
| 最新市值 | 825 | 亿RMB | 2026-04-17 | T1 | Tushare stock_data | aigroup-market-mcp__stock_data | 2026-04-18 | 东方财富网页 OK |
| 2024 研发费用 | 8.3 | 亿RMB | 2024 全年（估算） | T3 | 研报推算 | 分析师电话会议 2024-12 | 2026-04-18 | 单源估算 |
| 实际控制人 | 陈天石、陈云霁 | — | 最新 | T1 | 招股书 2020 | http://... | 2026-04-18 | 天眼查 OK |
```

所有报告内出现的**硬数字** MUST 有一行 provenance 条目。估算/单源数据必须在报告页脚标注。

## 数据表述规范（estimate / restatement / price-basis, MANDATORY）

以下三条针对 `analysis.md` + `data-provenance.md` 的写作规则由 `provenance_verify.py --strict`、`style_scan.py`、以及下游 `data-quality-audit` 的新规则（`restatement_aware` / `roe_definition_check` / `price_basis_check`）交叉强制。违反其中任一条都会在交付前被拦住。

### 规范 1：估算值必须显式标注

若 `analysis.md` 中某硬数字的书写形式包含估算标记 —— `~`、`约`、`大约`、`估算`、`粗估`、`推算`、`approximately`、`est.` —— 则 `data-provenance.md` 对应行的 `源` 字段**必须**以下列前缀/关键词之一开头：

- `[ESTIMATED]`：分析师粗估（例如按同行中位数推算）
- `[DERIVED]`：由其他硬数字算得（例如 `NI / Revenue`，但请注意这不是 ROE — 见规范 3）
- 中文 `估算` / `推算`（同义，可与 `[ESTIMATED]` 互换）

**反例（会被 `provenance_verify --strict` FAIL）**：
```markdown
# analysis.md
- ROE 2024：~22.9%
# data-provenance.md
| ROE_2024 | 22.9 | % | 2024 | T1 | Tushare Pro income_all | ... |
```

**正例**：
```markdown
# analysis.md
- ROE 2024：~22.9%
# data-provenance.md
| ROE_2024 | 22.9 | % | 2024 | T1 | [DERIVED] agent 推算 (NI/平均净资产) | ... |
```

### 规范 2：重述敏感字段必须标注 pre / post restatement + 版本

字段集合 `{EPS, 归母净利润, BPS, 毛利率, 净资产, 营业收入}` 容易因年度审计重述而出现**两个官方版本**（原始刊发版 vs 重述版）。写作时：

- **优先使用最新重述版**（Tushare Pro income_all 通常已更新为重述版；East Money 年报和招股书可能仍是原始版）
- 若 `analysis.md` 与引用源给出的值差 > 10%，`provenance` 行必须显式写出版本标识，例如：`2022年年报（原始版 2023-04 刊发）` 或 `2023年年报（2022重述版，XBRL v2）`
- 强烈推荐交叉核对**交易所 XBRL 最终版**（SSE / SZSE / HKEX 披露最新版本）

**反例**：EPS 2022 = 1.34 元（原始版）直接进 analysis.md 且不标版本，而东方财富年报已改为 1.11 元（重述版）——海天味业 2026-04-19 audit 即因此被 `restatement_aware` 规则定位 FAIL。

**正例**：
```markdown
# analysis.md
- EPS 2022（重述版）：1.11 元/股；原始刊发版为 1.34 元，因存货计提后重述。
# data-provenance.md
| EPS_2022_restated | 1.11 | 元/股 | 2022 | T1 | 东方财富 2023年报（2022重述版） | ... | 2026-04-19 | Tushare income_all OK |
```

### 规范 3：股价基准 + ROE 口径规范

- **股价 (`price_basis_check`)**：若同一公司股价跨源差异 > 3%，注明**取数基准**：T+0 收盘 / T-1 收盘 / 盘中最新 / 前复权 / 后复权 / 不复权。币种（RMB / HKD）必须标注。
- **ROE 口径 (`roe_definition_check`)**：ROE = `净利润 / 平均净资产`，**不是** `净利润 / 营收`（后者是净利率）。若 `provenance` 的 `源` 字段注明 `derived: NI / Revenue` 却用于 ROE，会被 `data-quality-audit` 直接判 FAIL。正确 derivation 示例：`[DERIVED] NI / ((期初净资产 + 期末净资产) / 2)`。
