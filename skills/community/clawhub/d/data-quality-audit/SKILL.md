---
name: data-quality-audit
description: "Independent cross-source audit of a completed CN banker deliverable. Use when the user asks to audit / double-check / 双核实 / 交叉验证 / 数据质量检查 / 审计 an existing deliverable directory. Re-fetches every hard number from the data-provenance.md table using an independent tier-2 source (Tushare vs 东方财富 vs 巨潮 vs FMP) and applies common-sense sanity rules (毛利率 in range / 收入增速 in range / 市值 = 股价 × 股本 / 毛利 = 营收 × 毛利率 / …). Emits an audit-report.md with PASS / FLAG / FAIL classification. This is a post-delivery QA step — the deliverable itself was already produced by customer-investigation / datapack-builder / ppt-deliverable."
---

# Data Quality Audit Skill

**独立交叉核实 CN banker 交付物的数据质量 — 找到看似合理实则错误的数字**

## Why this exists

现有三道 gate（`verify_intelligence` / `cn_typo_scan` / `provenance_verify`）保证：每个硬数字**有来源**、**无 escape typo**、**行文对得上溯源表**。

但它们不保证**数字本身对**。具体漏洞场景：

- Agent 抄错了 Tushare 返回值（小数点位移 / 单位换算错）
- data-provenance.md 注明"来源：巨潮 2024 年报"但根本没去拉取
- 单源数字没做 cross-check（Tushare 跟东方财富同期数据差 5% 以上）
- 内部一致性违反（说 "毛利率 98%"、说 "营收 100 亿 / 毛利 80 亿" → 实际毛利率 80% 自相矛盾）
- 市值 ≠ 股价 × 股本（股本数据过期）

本 skill 做的是**独立审计**：再走一遍数据源 + 对账 + 常识 check，给出审计报告。类似内审对已完成账目的二次核查。

## When to trigger

用户说：
- "audit ~/deliverables/xxx"
- "双核实一下 xxx 这份报告"
- "对 xxx 做数据质量检查"
- "交叉验证 xxx 的数字"
- "给 xxx 跑审计"

或者在 banker workflow 最后，user 要求"审计完成再交付"。

## Workflow

### Step 1 — Parse data-provenance.md

读 `<deliverable>/data-provenance.md`（standard schema：每行一条"指标 | 数值 | 单位 | 期间 | Tier | 源 | URL/工具 | 取数时间 | 交叉验证状态"）。可用 helper:

```bash
python3 ~/.openclaw/extensions/aigroup-lead-discovery-openclaw/skills/data-quality-audit/scripts/quality-audit.py \
    --parse-only \
    ~/deliverables/<company>/data-provenance.md
# stdout: JSON array of {metric, value, unit, period, tier, source, url_tool, fetched_at, status}
```

如果 provenance 文件格式不标准，回退到 regex 扫 analysis.md 的硬数字 + 第一次提到的 source。

### Step 2 — Independent re-fetch per hard number

对每条硬数字，调用**一个不同于 provenance 声明源的 MCP**重新 fetch：

| Provenance claims source | Audit must call |
|-------------------------|-----------------|
| Tushare / aigroup-market-mcp | 东方财富 web_fetch / FMP (港股) / 巨潮 PDF |
| 巨潮 / CNINFO | Tushare / 东方财富 web_fetch |
| FMP / Finnhub | Tushare / yfinance web_fetch |
| 天眼查 / 企查查 | 国家信用 gsxt.gov.cn web_fetch / 互查 |
| 财经媒体（财新 / 21 世纪 / 财联社） | 找原始官方披露（交易所 / 巨潮） |

**不要**用声明的同一源去"核实"——那不是核实，是回抄。

取不到第二源时 → 标 `FLAG (single-source-unverifiable)`，不算 FAIL。

### Step 3 — Diff & classify

对比 audit-fetched value vs provenance value:

| Diff | 分类 |
|------|------|
| `abs(diff) / value < 2%` | **PASS (exact)** |
| `abs(diff) / value ∈ [2%, 5%)` | **PASS (minor variance)** — 两源 reporting 习惯不同属正常 |
| `abs(diff) / value ∈ [5%, 15%)` | **FLAG (material variance)** — 需人工复核 |
| `abs(diff) / value ≥ 15%` 或符号反转 | **FAIL (material conflict)** — deliverable 不得原样交付 |
| 第二源不可获取 | **FLAG (single-source-unverifiable)** |
| 第二源 404 / 403 / 数据不存在 | **FLAG (second-source-unavailable)** |

### Step 4 — Common-sense sanity rules

把 parsed hard numbers 喂给 `scripts/common-sense-rules.yaml` 定义的规则集：

- **gross_margin_range**: 公司毛利率应该在 `[-20%, 95%]`（负毛利或超过 95% 需人工确认）
- **revenue_growth_range**: 营收同比增速应该在 `[-50%, +200%]`（业务剧震需 flag）
- **market_cap_price_shares**: 若同份交付物声明了市值 / 股价 / 股本，`abs(market_cap − price × shares_outstanding) / market_cap < 3%`
- **gross_profit_identity**: 若声明了营收 / 毛利 / 毛利率，`abs(gross_profit − revenue × gross_margin) / gross_profit < 3%`
- **net_margin_not_above_gross**: 净利率不得 > 毛利率（基本恒等式）
- **ocf_net_income_direction**: 经营现金流和净利同向（若一正一负，flag）
- **employee_market_cap_ratio**: 市值 / 员工数 应该在 `[50 万, 5 亿 RMB]` 这个大区间（否则数据可疑，但只 flag 不 fail）
- **dividend_payout_bound**: 分红率超过 100% 需人工确认（转增 / 资本公积送股可能误读）
- **roe_extreme**: ROE 超过 50% 或为负需核验（杠杆 + 特殊事件）
- **valuation_multiple_sanity**: P/E ≤ 200 且 EV/EBITDA ≤ 100
- **restatement_aware (NEW)**: 对重述敏感字段 `{EPS, 归母净利润, BPS, 毛利率, 净资产, 营业收入}`，若 primary 值与第二源交叉验证差异 > 10%，flag 为可能 pre-restatement vs post-restatement 混用 —— 推荐优先核对**交易所 XBRL 最终版**或**最新年报重述版本**（而非最早刊发的原始版本）。海天味业 2026-04-19 audit 正是被这条规则定位到 EPS 2022 1.34 元 (pre-restatement) vs 1.11 元 (post-restatement) 差 20.7% 的真实场景。
- **roe_definition_check (NEW)**: ROE 口径规范 —— 若 `provenance.md` 的 derivation 字段写作 "净利/营收" / "NI/Revenue" 而指标名是 ROE / 净资产收益率，判为 **fail**（这是净利率不是 ROE）。正确公式：ROE = 净利润 / 平均净资产。五粮液 2026-04-18 audit 的 ROE ~22% vs 年报 25.06% 差异即来自此错口径。
- **price_basis_check (NEW)**: 同一公司股价与第二源差异 > 3% → flag。常见原因：T+0 vs T-1 vs 最新实时报价 vs 币种 vs 复权/不复权。海天 2026-04-19 audit 的 37.68 元 vs 35.60 元 即价差基准不一致。

每条规则违反 → 单独产一条 FLAG 或 FAIL 条目。当前规则集总数 13（10 原有 + 3 新 restatement_aware / roe_definition_check / price_basis_check）。

### Step 5 — Emit audit-report.md

输出到 `<deliverable>/audit-report.md`，结构：

```markdown
# Audit Report — <Company> <ticker>

**Audit date:** 2026-04-18
**Target deliverable:** /Users/jackdong/deliverables/<company>/
**Auditor:** aigroup-lead-discovery-openclaw/data-quality-audit@0.3.0

## Overall verdict

OVERALL PASS  (12/14 PASS, 2 FLAG, 0 FAIL)

## Per-number cross-check

| Metric | MD value | Independent source | Independent value | Diff | Verdict |
|--------|---------|--------------------|-------------------|------|---------|
| 2024Q3 营收 | 1,088 亿元 | 东方财富 Choice | 1,086 亿元 | -0.2% | PASS (exact) |
| 2024-04-17 市值 | 20,150 亿元 | Tushare stock_data | 20,180 亿元 | +0.15% | PASS (exact) |
| 员工数 | 30,000 | 巨潮 2023 年报 | N/A | — | FLAG (second-source-unavailable) |
| ... |

## Common-sense rules

- ✅ gross_margin_range (88% ∈ [-20%, 95%])
- ✅ revenue_growth_range (+17% YoY ∈ [-50%, +200%])
- ❌ gross_profit_check: 声明营收 1088 × 毛利率 92% = 1001，但 MD 里毛利 980 → 差 2.1%（容差内，PASS）
- ⚠️ employee_mkt_ratio: 20150/3 = 6717 万/人（高端白酒本就如此，FLAG 非 FAIL）

## Action items

- [ ] Re-fetch 员工数: 尝试国家信用公示 gsxt.gov.cn
- [ ] 补充 2024 Q1 毛利率 source（当前单源）

## Raw audit data

JSON dump at `<deliverable>/audit-raw.json`.
```

### Step 6 — Return verdict to user

Agent 的 final message 必须包含：
- overall verdict（OVERALL PASS / OVERALL FLAG: N items / OVERALL FAIL: M items）
- path to `audit-report.md`
- path to `audit-raw.json`
- 前三条 action items（如有）

## What this skill does NOT do

- 不重新走 banker analysis workflow（那是 datapack-builder / dcf-model 的事）
- 不重新跑 verify_intelligence / cn_typo_scan / provenance_verify（那是 `validate-delivery.py` 的事）
- 不改 deliverable 本身 —— audit 只出报告；人工决定是否回炉改

## Pair with validate-delivery.py

建议顺序：
1. `validate-delivery.py` — 快速 gate（exit 0 方可考虑交付）
2. `data-quality-audit`（本 skill）— 深度审计（OVERALL PASS 方可 client-ship）

gate 通过不等于 audit 通过；反之亦然。两层都是必要的。
