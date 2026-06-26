---
name: financial-report-analyzer
description: |
  EN: Extract, normalize and analyze key metrics from corporate financial reports (10-K, 10-Q, A-share annual/interim reports, IFRS/GAAP/CAS PDFs). Produces side-by-side YoY/QoQ comparisons, ratio analysis (ROE/ROA/gross margin/debt ratio/cash conversion cycle), and red-flag detection (earnings management signals, related-party tx anomalies, goodwill risk). Use when user uploads or names a financial report and asks "解读 / 分析 / 拆解 / 找风险点 / 对比同行 / extract financials".
  中文：从企业财报（10-K、10-Q、A股年报半年报、IFRS/GAAP/CAS PDF）中抽取并归一化关键指标，输出同比/环比对比、关键比率分析（ROE/ROA/毛利率/资产负债率/现金转换周期），以及红旗信号检测（盈余管理迹象、关联交易异常、商誉风险）。当用户上传或提及财报并要求"解读/分析/拆解/找风险点/同行对比"时触发。
version: 1.0.0
metadata:
  openclaw:
    emoji: "📊"
    homepage: https://github.com/openclaw-skills/financial-report-analyzer
    requires:
      bins:
        - python3
    envVars:
      - name: FINREPORT_ACCOUNTING_STANDARD
        required: false
        description: Default accounting standard hint when not auto-detectable. One of `CAS|IFRS|US-GAAP`.
      - name: FINREPORT_PEER_DB
        required: false
        description: Optional path to a custom peer-company benchmark database (CSV/Parquet).
---

# Financial Report Analyzer · 财报智能解读

> Pull every metric that matters from a 200-page annual report in under 60 seconds, with traceable line-item provenance, peer benchmarking, and red-flag detection.
>
> 60 秒从 200 页年报抽出全部关键指标，每个数字可溯源到原文，附同行对标与风险信号识别。

---

## 🎯 When to Use · 何时使用

**Trigger keywords (中文):** 分析财报、解读年报、半年报解读、利润表分析、资产负债表、现金流量表、ROE 分析、毛利率、商誉风险、关联交易、同行对比、行业对标、财报对比、招股说明书

**Trigger keywords (EN):** parse 10-K, analyze annual report, extract financials, ratio analysis, peer comparison, red flag detection, earnings quality

**Supported inputs:**
- PDF（A 股年报/半年报、招股书、Form 10-K/10-Q/20-F、IFRS annual reports）
- XBRL / iXBRL
- Excel 财务摘要（巨潮、东方财富、Wind 导出格式）
- 纯文本财务披露

**Do NOT use when:**
- User asks for stock price prediction or investment advice (this skill is descriptive analysis only)
- Input is a single number or one-line text
- Input is non-financial content

---

## 📋 Output Sections · 输出结构

The skill always produces a 5-section report:

| 段落 / Section | 内容 / Content |
|---|---|
| 1. 摘要 Executive Summary | 主营业务、规模、增长、盈利能力 5 行总结 |
| 2. 三表关键指标 Three-Statement KPIs | Revenue / Net Income / EBITDA / Total Assets / Equity / OCF |
| 3. 比率分析 Ratio Analysis | 盈利能力 / 偿债能力 / 营运能力 / 现金质量 / 杜邦分解 |
| 4. 红旗检测 Red Flags | 应收账款增速 vs 营收、商誉占净资产、关联交易、审计意见 |
| 5. 同行对标 Peer Benchmark | 行业中位数、分位数、相对排名 |

---

## 🔄 Analysis Protocol · 分析流程

### Step 1: Document ingestion · 文档摄入

```bash
python3 scripts/ingest.py --input <pdf-or-xbrl> --out /tmp/raw_extract.json
```

- Auto-detect report type (10-K / 年报 / 半年报 / 招股书)
- Identify reporting period and accounting standard
- Extract text + tables with layout preservation (uses bundled `pdfplumber`)

### Step 2: Table normalization · 报表归一化

`scripts/normalize_statements.py` maps raw line items to a standardized chart of accounts (`knowledge/coa_master.csv`), handling:
- 中文/英文双语科目名
- CAS ↔ IFRS ↔ US-GAAP 科目对照
- 单位归一（元/千元/百万元/亿元 → 元）
- 期间对齐（年度/季度/累计）

### Step 3: KPI & ratio computation · 指标计算

```bash
python3 scripts/compute_ratios.py --input normalized.json --out ratios.json
```

Computes 40+ standard ratios documented in `knowledge/ratio_definitions.md`, with formulas matching CFA Institute conventions and CSRC disclosure requirements.

### Step 4: Red-flag detection · 红旗扫描

`scripts/detect_red_flags.py` runs 18 heuristic checks, including:
- 应收账款增速显著高于营收增速 (Receivables growth >> Revenue growth)
- 经营性现金流持续低于净利润 (OCF/NI < 0.5 for 3+ years)
- 商誉/净资产 > 30%
- 关联方交易占营收 > 20%
- 审计意见非"标准无保留"
- 频繁更换会计师事务所
- 存货周转率突降
- 期间费用大幅波动
- 应付账款异常下降
- 在建工程长期挂账
- 其他应收款异常增长
- 大额非经常性损益占比
- 短期借款激增
- 商誉减值历史
- 大股东质押比例
- 控股股东净利润占比异常
- 利息覆盖倍数 < 1.5
- Z-score < 1.8

Each flag is documented with severity (🟢🟡🔴), evidence span, and recommended follow-up question.

### Step 5: Peer benchmarking · 同行对标

If `FINREPORT_PEER_DB` is set (or built-in industry medians available), produces percentile ranks. Otherwise outputs absolute values with industry context notes.

### Step 6: Report rendering · 报告渲染

```bash
python3 scripts/render_report.py --analysis ratios.json --flags flags.json --format md|json|html
```

For web channels with `web-prism-artifact` available, the skill automatically emits a structured artifact for inline rendering.

---

## 📤 Output Format · 输出格式

JSON structure:

```json
{
  "company": { "name": "...", "ticker": "...", "industry": "..." },
  "period": { "fiscal_year": 2024, "reporting_basis": "CAS" },
  "executive_summary": "...",
  "kpis": { "revenue": {...}, "net_income": {...}, ... },
  "ratios": { "roe": {...}, "gross_margin": {...}, ... },
  "red_flags": [ { "code": "RF03", "severity": "🟡", "title": "...", "evidence": "...", "page": 47 } ],
  "peer_benchmark": { "industry": "...", "rankings": {...} },
  "provenance": { /* page+line offset for every number */ }
}
```

For human consumption, `--format md` produces a Markdown report with embedded tables and red-flag callouts.

---

## ⚠️ Safety & Compliance · 安全合规

1. **Descriptive only, not predictive** — never output buy/sell/hold recommendations or stock price targets.
2. **Source attribution** — every number includes `{page, table, row}` pointing back to the source document.
3. **No silent imputation** — missing data is explicitly reported, never extrapolated.
4. **Red flags are signals, not verdicts** — output always frames flags as "warrant further investigation," not "company is fraudulent."
5. **Audit log** — full extraction log saved to `<output>.audit.log` for compliance.

> 本技能仅做描述性分析，绝不输出买卖评级或股价预测；所有数字可溯源；缺失数据明确标注不做估算；红旗信号仅作为"需进一步核查"的提示，不作定性结论。

---

## 🚀 Usage Examples · 使用示例

### Example 1: Single annual report analysis

```bash
python3 scripts/run_pipeline.py --input 600519_2024_annual.pdf --output report.json
python3 scripts/render_report.py --input report.json --format md > 茅台2024分析.md
```

### Example 2: YoY comparison

```bash
python3 scripts/compare_periods.py \
  --current 2024_annual.pdf \
  --prior 2023_annual.pdf \
  --output yoy_comparison.md
```

### Example 3: Peer benchmark (white-liquor industry)

```bash
python3 scripts/peer_benchmark.py \
  --target 600519_2024_annual.pdf \
  --peers 000858,000568,000799 \
  --output peer_report.md
```

### Example 4: Red-flag scan only (fast mode)

```bash
python3 scripts/run_pipeline.py --input report.pdf --mode red-flag-only --output flags.json
```

---

## 🧪 Testing · 测试

```bash
cd tests && python3 -m pytest -v
```

Test fixtures include:
- 10 real anonymized A-share annual reports (5 industries)
- 3 Form 10-K samples
- Edge cases: restated financials, going-concern qualifications, mid-year auditor change

---

## 📚 References · 参考资料

- CSRC《公开发行证券的公司信息披露内容与格式准则第 2 号》
- IFRS Standards: https://www.ifrs.org/issued-standards/
- US GAAP: https://asc.fasb.org/
- Beneish M-Score, Altman Z-Score original papers
- CFA Institute Financial Statement Analysis curriculum

## 🏷️ Tags · 标签

`finance` `accounting` `10-K` `annual-report` `ratio-analysis` `red-flag` `IFRS` `GAAP` `CAS` `财报` `年报` `财务分析`
