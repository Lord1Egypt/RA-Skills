---
name: a-share-dcf-valuation
description: DCF valuation modeling for A-share listed companies. Pass stock code to automatically fetch financial data, calculate WACC, run conservative/base/optimistic three-scenario DCF valuation, generate sensitivity analysis matrix, and output complete Markdown report (in Chinese). Applicable to any A-share listed company valuation analysis.
---

# A-share DCF Valuation Modeling

## Trigger Conditions

Use when user requests DCF (Discounted Cash Flow) valuation analysis for an A-share stock.

## Environment Requirements

### Required Environment Variables

| Variable | Description | How to Obtain |
|----------|-------------|---------------|
| `TUSHARE_TOKEN` | Tushare API token (mandatory) | Register at https://tushare.pro, get token from user center |
| `OPENCLAW_WORKSPACE` | Workspace root path (optional) | Defaults to `~/.openclaw/workspace` |

### Python Dependencies

| Package | Version | Purpose |
|---------|---------|--------|
| `tushare` | Latest | A-share financial data API |
| `pandas` | ≥1.0 | Data processing |
| `numpy` | ≥1.18 | Numerical calculations |
| `scipy` | ≥1.4 | Beta regression (stats module) |

### Setup Instructions

1. **Configure Tushare Token**:
   ```bash
   # Add to ~/.bashrc or ~/.bash_profile
   export TUSHARE_TOKEN="your_token_here"
   source ~/.bashrc
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install tushare pandas numpy scipy
   ```

3. **Verify Setup**:
   ```bash
   python3 -c "import tushare as ts; ts.set_token('$TUSHARE_TOKEN'); pro = ts.pro_api(); print(pro.stock_basic(ts_code='600519.SH'))"
   ```

### Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `未设置 TUSHARE_TOKEN 环境变量` | Token not configured | Add export to shell profile |
| `Tushare API 获取失败` | Invalid token or network issue | Verify token, check network |
| `No module named 'tushare'` | Package not installed | `pip install tushare` |
| `Beta 回归数据不足` | Stock newly listed | Use industry default Beta |

## Quick Start

```
User input: "对 贵州茅台 600519 做 DCF 估值"
→ Run: python3 scripts/a_share_dcf.py 600519.SH
→ Report saved to: reports/dcf_贵州茅台_YYYY-MM-DD.md
```

## Valuation Methodology

**Method**: Two-stage FCFF (Free Cash Flow to Firm) discount model

**Formulas**:
- FCFF = Operating Cash Flow - Capital Expenditure
- WACC = We×Re + Wd×Rd×(1-T)
- Terminal Value = FCFF_n × (1+g) / (WACC - g)
- Equity Value = EV - Net Debt
- Per-share Value = Equity Value / Total Shares

**Three-Scenario Assumptions**:

| Scenario | WACC | Growth Rate | Perpetual Growth |
|----------|------|-------------|------------------|
| Conservative | WACC + 3% (min 14%) | 50% of 3-year avg | 2% |
| Base | Calculated WACC | 80% of 3-year avg | 3% |
| Optimistic | WACC - 3% (min 7%) | 100% of 3-year avg | 4% |

### Scenario Assumption Rationale

**Conservative Scenario**: Higher WACC reflects elevated risk premium; reduced growth rate accounts for potential downside from competition, regulation, or macro headwinds. Suitable for risk-averse investors.

**Base Scenario**: Uses calculated WACC from company-specific beta and capital structure; growth rate anchored to historical average but tempered for maturity trajectory. Represents most likely outcome under normal conditions.

**Optimistic Scenario**: Lower WACC assumes favorable risk environment; full historical growth reflects best-case execution. Appropriate for growth-oriented analysis or upside case.

## Execution Steps

### 1. Determine Stock Code Format

Tushare uses `XXXXXX.SH` (Shanghai) or `XXXXXX.SZ` (Shenzhen) format:

```python
# Auto conversion
if code.startswith('6'): 
    ts_code = f"{code}.SH"
elif code.startswith(('0', '3')):
    ts_code = f"{code}.SZ"
```

### 2. Run Valuation Script

```bash
cd $OPENCLAW_WORKSPACE && python3 skills/a-share-dcf-valuation/scripts/a_share_dcf.py <TS_CODE> [公司名]
# Example: python3 skills/a-share-dcf-valuation/scripts/a_share_dcf.py 600519.SH 贵州茅台
```

**Note**: `$OPENCLAW_WORKSPACE` defaults to `~/.openclaw/workspace`. Use relative paths from workspace root for portability.

### 3. Check Output

- Terminal displays real-time progress and key metrics
- Markdown report saved to `reports/dcf_{公司名}_{日期}.md`
- Verify report contains all required sections

### 4. Report to User

First provide summary conclusion, then report path:

```
## DCF 估值完成 — {公司名}

| 场景 | DCF每股价值 | vs 当前股价 |
|------|------------|------------|
| 保守 | ¥XX.XX     | -XX.X%     |
| 中性 | ¥XX.XX     | -XX.X%     |
| 乐观 | ¥XX.XX     | -XX.X%     |

当前股价: ¥XXX.XX
完整报告: reports/dcf_{公司名}_{日期}.md
```

## Important Notes

### Data Source
- **Tushare** is the sole data source (requires TUSHARE_TOKEN environment variable)
- If Tushare fetch fails, inform user that data is unavailable; do not fabricate data

### Beta Calculation
- Use ~500 trading days (~2 years) regression against CSI 300 (000300.SH)
- If regression R² < 0.1 or insufficient data, use industry default Beta:
  - Tech/Semiconductor: 1.5
  - Consumer/Healthcare: 0.8
  - Financial/Banking: 1.0
  - Cyclical/Manufacturing: 1.2
  - Others: 1.2

### WACC Parameters (Dynamic Calculation)

The following parameters are **NOT hardcoded fixed values**. They are dynamically determined with explicit data sources and rationale:

#### 1. Risk-Free Rate (RF)

| Approach | Source | Value Range |
|----------|--------|-------------|
| **Primary** | China 10-year Treasury yield | 1.8% - 4.5% (historical) |
| **Reference** | 中债估值 | ~2.1% - 2.5% (2024-2025) |
| **Fallback** | Recent 10Y bond average | 2.25% (default) |

**Method**: Query public bond yield data; if unavailable, use recent reference value with explicit notation.

#### 2. Equity Risk Premium (ERP)

**Correct Terminology**: ERP (Equity Risk Premium), not MRP (Market Risk Premium).

| Source | ERP Estimate |
|--------|--------------|
| Damodaran (2024) | 6.5% for China |
| 中金/中信研报 | 5% - 8% |
| 程晓明等学术研究 | 6.0% - 7.5% |
| Historical calculation (A股20年平均收益率 - RF) | 5.5% - 7.0% |

**Industry Adjustment**:
- Tech/Semiconductor: +1.0% to 1.5%
- Financial: -1.0%
- Consumer/Healthcare: 0%

**Method**: Base ERP 6.5% + industry-specific risk adjustment.

#### 3. Debt Cost (Rd)

| Approach | Formula |
|----------|---------|
| **Primary** | LPR 1Y + Credit Spread |
| **LPR Reference** | 3.1% (2025 1-year LPR) |
| **Credit Spread** | 0.5% - 1.5% based on rating |

| Company Profile | Estimated Rd |
|-----------------|--------------|
| Low debt (<10%), strong credit | 3.6% (LPR + 0.5%) |
| Moderate debt (10-50%) | 4.0% (LPR + 0.9%) |
| High debt (>50%) | 5.0% (LPR + 1.9%) |

**Method**: Estimate based on company's debt ratio and implied credit quality.

#### 4. Tax Rate (Tax)

| Source | Rate |
|--------|------|
| **Primary** | Actual effective tax rate from financial statements |
| **High-tech enterprise** | 15% (qualified) |
| **General corporate** | 25% |

**High-tech Identification Criteria**:
1. Industry: 电子、半导体、计算机、通信、医药生物、医疗器械、新能源、电力设备
2. Gross margin > 30% (common indicator of tech companies)

**Method**: First attempt to extract actual tax rate from income statement; if unavailable, determine based on industry and gross margin characteristics.

### Special Cases
- **Financial stocks (banks/insurers/brokers)**: Standard DCF not applicable (FCFF meaningless), use PB-ROE or DDM model, inform user
- **Loss-making companies**: When FCFF is negative with no recovery signs, DCF not applicable, use alternative methods
- **ST/*ST stocks**: Alert user to delisting risk

### Report Quality
- All amounts in "亿元" (100 million yuan)
- Growth rates in percentage
- Two decimal places
- Annotate data source and timeliness
- Must include disclaimer

### Risk Disclosure (Dynamic Generation)

The "Risk Disclosure" section must be dynamically generated based on company and industry characteristics, NOT hardcoded. The script should:

1. **Industry-specific risks**: Map company's industry to relevant risk factors
2. **Company-specific risks**: Analyze financial data to identify company-level risks
3. **Model risks**: Always include DCF sensitivity to WACC and perpetual growth
4. **Macro risks**: General economic, interest rate, and policy risks

**Industry Risk Mapping**:

| Industry | Key Risk Factors |
|----------|------------------|
| 科技/半导体 | 技术迭代快、研发投入大、国际竞争、供应链风险 |
| 消费/食品饮料 | 品牌溢价风险、消费降级、渠道变革 |
| 医药/医疗 | 政策监管（集采）、研发失败、专利到期 |
| 金融/银行 | 利率周期、信用风险、监管趋严 |
| 周期/制造 | 经济周期敏感、产能过剩、环保政策 |
| 新能源/光伏 | 技术路线竞争、产能扩张过快、补贴退坡 |
| 房地产/建材 | 政策调控、去杠杆、销售疲软 |
| 互联网/传媒 | 用户增长放缓、监管趋严、变现模式受限 |
| 交通运输 | 油价波动、需求周期、基础设施投资 |
| 其他 | 行业竞争格局变化、政策不确定性 |

## Report Structure (Markdown, output in Chinese)

```markdown
# DCF 估值报告 — {公司名} ({TS_CODE})

> 估值日期 | 当前股价 | 总市值 | PE | PB

## 一、公司基本面概览
- 公司简介
- 历史财务数据表(7年)
- 关键财务指标(最新年报)

## 二、WACC 计算
- 参数表格(Rf, Beta, MRP, Re, Rd, Tax, We, Wd, WACC)

## 三、三场景 DCF 估值
- 场景假设表(含设定依据说明)
- 估值结果表

## 四、敏感性分析
- WACC × 永续增长率 矩阵

## 五、关键假设
- 列出核心假设

## 六、风险提示(Dynamic)
- 根据公司行业特性、财务状况动态生成针对性风险提示

## 七、结论
- 估值区间
- 与当前股价对比
- 简要分析

> 免责声明
```

## File Organization

All paths should be relative to the workspace root (`$OPENCLAW_WORKSPACE` or `~/.openclaw/workspace`):

- **Script**: `skills/a-share-dcf-valuation/scripts/a_share_dcf.py`
- **Report**: `reports/dcf_{公司名}_{YYYY-MM-DD}.md`

**Important**: Avoid absolute paths like `/home/laigen/` in the script. Use environment variable `$OPENCLAW_WORKSPACE` or relative paths for portability.
