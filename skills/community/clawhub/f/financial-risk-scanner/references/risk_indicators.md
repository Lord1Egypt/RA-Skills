# Risk Indicators Reference

Detailed detection logic, thresholds, and calculation methods for all 21 financial risk indicators.

## Table of Contents

1. [Asset Reality Risks](#asset-reality-risks)
2. [Profit Quality Risks](#profit-quality-risks)
3. [Related Party Risks](#related-party-risks)
4. [Capital Structure Risks](#capital-structure-risks)
5. [Audit & Governance Risks](#audit--governance-risks)
6. [Industry Comparison Methods](#industry-comparison-methods)
7. [Severity Scoring System](#severity-scoring-system)

---

## Asset Reality Risks

### 1. Cash-Debt Paradox (存贷双高)

**Detection Criteria**:
- Cash / Total Assets > 15%
- Interest-bearing Debt / Total Assets > 30%
- Both conditions met simultaneously for 2+ consecutive years

**Data Fields Required**:
- `monetary_cap` (货币资金)
- `total_assets` (总资产)
- `short_loan` (短期借款)
- `long_loan` (长期借款)
- `total_liab` (总负债)

**Calculation**:
```python
cash_ratio = monetary_cap / total_assets
debt_ratio = (short_loan + long_loan + bonds_payable) / total_assets
paradox_score = cash_ratio * debt_ratio  # Higher = more suspicious
```

**Red Flags**:
- Cash yields low interest income (< 1% return)
- High debt interest rate (> 5% cost)
- Cash/debt mismatch growing over time
- Cash position volatile despite stable operations

**Cross-validation**:
- Check interest income in income statement vs cash balance
- Review cash management practices in announcements
- Compare with industry cash/debt norms

---

### 2. Receivables Anomaly (应收账款畸高)

**Detection Criteria**:
- Receivables growth rate > Revenue growth rate × 1.5 for 3+ years
- Or: Receivables / Revenue > 30% and rising

**Data Fields Required**:
- `accounts_receiv` (应收账款)
- `revenue` (营业收入)
- `oper_cost` (营业成本)

**Calculation**:
```python
receivables_growth = (receivables_t - receivables_t-1) / receivables_t-1
revenue_growth = (revenue_t - revenue_t-1) / revenue_t-1
ratio = receivables_growth / revenue_growth
# Warning if ratio > 1.5 for 3+ years
```

**Red Flags**:
- Concentration in few large customers
- Aging analysis shows increasing overdue amounts
- Bad debt provision lower than industry average
- Customer quality deteriorating

**Cross-validation**:
- Review top 5 customers disclosure
- Check customer creditworthiness
- Analyze collection cycle changes

---

### 3. Inventory Anomaly (存货异常)

**Detection Criteria**:
- Inventory growth > COGS growth × 1.5 for 2+ years
- Or: Inventory turnover ratio declining significantly

**Data Fields Required**:
- `inventory` (存货)
- `oper_cost` (营业成本)
- `finished_goods` (产成品)
- `raw_material` (原材料)

**Calculation**:
```python
inventory_turnover = oper_cost / ((inventory_t + inventory_t-1) / 2)
# Compare with 5-year average and industry median
```

**Red Flags**:
- Inventory aging increasing
- Finished goods占比上升 (overproduction)
- Inventory provisioning declining
- Inventory quality concerns in notes

**Cross-validation**:
- Check inventory write-downs
- Review production vs sales balance
- Analyze inventory composition changes

---

### 4. Prepayments Surge (预付账款激增)

**Detection Criteria**:
- Prepayments / Total Assets > 5%
- Prepayments growth > 50% without business rationale

**Data Fields Required**:
- `adv_payment` (预付账款)
- `total_assets` (总资产)
- `top_prepay_suppliers` (前五大预付供应商)

**Red Flags**:
- Prepayments to unknown/new suppliers
- Prepayments unrelated to core business
- Long-standing prepayments not converted
- Supplier relationship suspicious

**Cross-validation**:
- Review supplier identity in notes
- Check prepayment aging analysis
- Analyze supplier business legitimacy

---

### 5. Other Receivables High (其他应收款高企)

**Detection Criteria**:
- Other receivables > Net Assets × 5%
- Or: Other receivables growing rapidly without explanation

**Data Fields Required**:
- `other_receiv` (其他应收款)
- `total_hldr_equity` (净资产)
- `other_receiv_detail` (其他应收明细)

**Red Flags**:
- Related party in other receivables
- Loans to shareholders/executives
- Advances to affiliates
- Suspicious counterparties

**Cross-validation**:
- Check related party disclosure
- Review purpose of advances
- Analyze recovery timeline

---

### 6. Construction Suspended (在建工程悬案)

**Detection Criteria**:
- Construction in Progress > Total Assets × 10%
- Or: Construction uncompleted for > 3 years
- Or: Construction completion ratio stagnating

**Data Fields Required**:
- `const_in_prog` (在建工程)
- `total_assets` (总资产)
- `const_proj_detail` (在建工程明细)
- `fixed_assets` (固定资产)

**Red Flags**:
- Projects delayed repeatedly
- Budget overrun significant
- Progress reporting inconsistent
- Cash diverted to construction

**Cross-validation**:
- Review project progress in notes
- Check capital expenditure vs budget
- Analyze project necessity and ROI

---

## Profit Quality Risks

### 7. Cash-Profit Divergence (净现比背离)

**Detection Criteria**:
- Net profit positive, but operating cash flow negative for 3+ consecutive years
- Or: Cash-Profit Ratio < 0.5 sustained

**Data Fields Required**:
- `net_profit` (净利润)
- `net_cash_flows_oper_act` (经营活动现金流净额)

**Calculation**:
```python
cash_profit_ratio = net_cash_flows_oper_act / net_profit
# Warning if ratio < 0.5 for 3+ years
```

**Red Flags**:
- Profit from non-operating activities high
- Revenue recognition timing manipulated
- Large accruals without cash backing
- Receivables/inventory accumulating

**Cross-validation**:
- Analyze working capital changes
- Check accrual quality
- Review revenue recognition policy

---

### 8. Gross Margin Anomaly (毛利率异常)

**Detection Criteria**:
- Gross margin > Industry median + 10 percentage points
- Or: Gross margin rising while industry declining
- Or: Gross margin persistently above 50% in competitive industry

**Data Fields Required**:
- `revenue` (营业收入)
- `oper_cost` (营业成本)
- Industry classification

**Calculation**:
```python
gross_margin = (revenue - oper_cost) / revenue
industry_gm = get_industry_median(industry_code, 'gross_margin')
anomaly_score = gross_margin - industry_gm
```

**Red Flags**:
- Cost accounting changed
- Transfer pricing manipulation
- Cost allocation suspicious
- Vertical integration claims unverifiable

**Cross-validation**:
- Compare with direct competitors
- Analyze cost structure changes
- Check pricing strategy consistency

---

### 9. Sales Expense Anomaly (销售费用率异常)

**Detection Criteria**:
- Sales expense ratio < Industry median × 0.5
- Or: Sales expense declining while revenue growing rapidly

**Data Fields Required**:
- `sell_exp` (销售费用)
- `revenue` (营业收入)

**Calculation**:
```python
sales_expense_ratio = sell_exp / revenue
industry_ratio = get_industry_median(industry_code, 'sales_expense_ratio')
anomaly = industry_ratio / sales_expense_ratio  # High = suspicious
```

**Red Flags**:
- Marketing investment minimal
- Sales channels suspicious
- Customer acquisition cost hidden
- Third-party sales arrangements

**Cross-validation**:
- Review sales organization structure
- Check marketing investment disclosure
- Analyze customer acquisition methods

---

### 10. Abnormal Non-recurring Items (异常非经常性损益)

**Detection Criteria**:
- Non-recurring items > Net profit × 30%
- Or: Company relies on non-recurring items to avoid loss

**Data Fields Required**:
- `net_profit` (净利润)
- `non_recurring_profit` (非经常性损益)
- `invest_income` (投资收益)
- `asset_disposal_income` (资产处置收益)

**Red Flags**:
- Asset sales before reporting deadline
- Government subsidies one-time
- Investment gains from questionable sources
- Fair value gains unrealized

**Cross-validation**:
- Review nature of non-recurring items
- Check recurring vs non-recurring breakdown
- Analyze sustainability of gains

---

### 11. Asset Impairment Bath (资产减值洗大澡)

**Detection Criteria**:
- Asset impairment > Net profit × 50% in single year
- Or: Large impairment followed by profit recovery
- Or: Impairment timing suspicious (new management, turn-around)

**Data Fields Required**:
- `impair_loss` (资产减值损失)
- `net_profit` (净利润)
- `impair_detail` (减值明细)

**Red Flags**:
- Impairment concentrates on acquired assets
- Impairment reverses later
- Impairment enables future profit gains
- New management writes off predecessor assets

**Cross-validation**:
- Compare impairment with acquisitions
- Review impairment methodology
- Check impairment reversal history

---

## Related Party Risks

### 12. Related Transaction High (关联交易占比高)

**Detection Criteria**:
- Related party purchases > Total purchases × 30%
- Or: Related party sales > Total sales × 30%

**Data Fields Required**:
- `related_purchase` (关联采购)
- `related_sales` (关联销售)
- `total_purchase` (总采购)
- `revenue` (营业收入)

**Red Flags**:
- Pricing not at arm's length
- Dependency on related parties
- Related party identity unclear
- Transactions circular

**Cross-validation**:
- Review related party disclosure
- Check pricing fairness
- Analyze transaction necessity

---

### 13. Related Fund Flows (关联方资金往来频繁)

**Detection Criteria**:
- Related party in other receivables/payables > 50%
- Or: Fund flows with related parties frequent

**Data Fields Required**:
- `other_receiv_related` (其他应收-关联方)
- `other_payable_related` (其他应付-关联方)
- `other_receiv` (其他应收款)
- `other_payable` (其他应付款)

**Red Flags**:
- Fund flows inconsistent with business
- Loans to/from related parties
- Guarantees for related parties
- Related party liquidity issues

**Cross-validation**:
- Review related party financial status
- Check fund flow purpose
- Analyze repayment history

---

### 14. Related Guarantees (关联担保过多)

**Detection Criteria**:
- External guarantees > Net assets × 50%
- Or: Guarantees for related parties excessive

**Data Fields Required**:
- `external_guarantee` (对外担保)
- `total_hldr_equity` (净资产)
- `guarantee_detail` (担保明细)

**Red Flags**:
- Guarantees for financially weak parties
- Guarantees not disclosed timely
- Guarantee chain formation
- Contingent liability risk high

**Cross-validation**:
- Review guarantee purpose
- Check guaranteed party status
- Analyze guarantee chain

---

## Capital Structure Risks

### 15. Goodwill High (商誉占比过高)

**Detection Criteria**:
- Goodwill > Net assets × 30%
- Or: Goodwill from recent acquisitions significant

**Data Fields Required**:
- `goodwill` (商誉)
- `total_hldr_equity` (净资产)
- `acquisition_history` (收购历史)

**Red Flags**:
- Acquisition premium excessive
- Acquired business underperforming
- Goodwill impairment risk high
- Multiple high-premium acquisitions

**Cross-validation**:
- Review acquisition rationale
- Check acquired business performance
- Analyze impairment testing

---

### 16. Debt Ratio High (资产负债率畸高)

**Detection Criteria**:
- Debt ratio > 70% and rising for 3+ years
- Or: Debt ratio > industry median + 20 percentage points

**Data Fields Required**:
- `total_liab` (总负债)
- `total_assets` (总资产)

**Calculation**:
```python
debt_ratio = total_liab / total_assets
# Warning if > 70% and rising
```

**Red Flags**:
- Short-term debt占比高
- Debt restructuring frequent
- Credit rating declining
- Financing cost rising

**Cross-validation**:
- Review debt structure
- Check refinancing ability
- Analyze debt maturity profile

---

### 17. Short-term Liquidity Pressure (短期偿债压力)

**Detection Criteria**:
- Short-term borrowing / Cash > 3×
- Or: Current ratio < 1.0 sustained

**Data Fields Required**:
- `short_loan` (短期借款)
- `monetary_cap` (货币资金)
- `current_assets` (流动资产)
- `current_liab` (流动负债)

**Calculation**:
```python
liquidity_pressure = short_loan / monetary_cap
current_ratio = current_assets / current_liab
```

**Red Flags**:
- Cash insufficient for short-term debt
- Working capital negative
- Bank credit tightening
- Supplier credit reducing

**Cross-validation**:
- Review bank relationships
- Check credit facility status
- Analyze cash flow adequacy

---

### 18. Dual Debt High (长短期借款双高)

**Detection Criteria**:
- Short-term borrowing > 30% of assets
- Long-term borrowing > 20% of assets
- Cash position strained

**Data Fields Required**:
- `short_loan` (短期借款)
- `long_loan` (长期借款)
- `monetary_cap` (货币资金)
- `total_assets` (总资产)

**Red Flags**:
- Financing dependency extreme
- No operational cash generation
- Debt growing faster than assets
- Interest coverage declining

**Cross-validation**:
- Review financing strategy
- Check operational cash flow
- Analyze debt servicing ability

---

## Audit & Governance Risks

### 19. Auditor Changes (频繁更换审计机构)

**Detection Criteria**:
- Auditor changed 2+ times in 5 years
- Or: Auditor changed after clean opinion expected

**Data Fields Required**:
- `auditor` (审计机构)
- `audit_opinion` (审计意见)
- `audit_fee` (审计费用)

**Red Flags**:
- Auditor disagreement disclosed
- Fee change significant
- Timing of change suspicious
- New auditor unknown firm

**Cross-validation**:
- Review auditor change announcement
- Check predecessor auditor status
- Analyze audit fee changes

---

### 20. Non-standard Audit Opinion (非标审计意见)

**Detection Criteria**:
- Audit opinion contains emphasis of matter
- Or: Qualified opinion / Adverse opinion / Disclaimer

**Data Fields Required**:
- `audit_opinion` (审计意见类型)
- `audit_emphasis` (强调事项)

**Opinion Types**:
- Standard unqualified: ✅ Clean
- Unqualified with emphasis: ⚠️ Concern
- Qualified: 🔴 Problem
- Adverse / Disclaimer: ❌ Severe

**Cross-validation**:
- Review emphasis matters
- Check management response
- Analyze subsequent events

---

### 21. Executive Departures (高管频繁离职)

**Detection Criteria**:
- CFO / Board Secretary changed 2+ times in 3 years
- Or: Key executives departed before critical events

**Data Fields Required**:
- `cfo_name` (财务总监)
- `secretary_name` (董秘)
- `executive_changes` (高管变动记录)

**Red Flags**:
- CFO departed before financial issues
- Secretary departed before disclosure issues
- Multiple executives departed together
- Departures unexplained

**Cross-validation**:
- Review departure announcements
- Check executive succession
- Analyze departure timing vs events

---

## Industry Comparison Methods

### Data Sources

1. **Industry Classification**: Use Tushare `index_classify(src='SW2021')` for Shenwan industry codes
2. **Peer Selection**: Companies in same industry code, similar size
3. **Industry Metrics**: Calculate median for each metric across peers

### Key Industry Metrics

| Metric | Method |
|--------|--------|
| Gross Margin | Industry median + 10pp threshold |
| Sales Expense Ratio | Industry median × 0.5 threshold |
| Debt Ratio | Industry median + 20pp threshold |
| Inventory Turnover | Compare with industry average |
| Receivables Turnover | Compare with industry average |

### Peer Selection Criteria

```python
# Same Shenwan industry (level 2)
# Similar revenue scale (±50%)
# Exclude ST companies
# At least 5 peers for comparison
```

---

## Severity Scoring System

### Scoring Logic

Each indicator scored 0-3:
- 0: No concern
- 1: Minor concern (threshold approaching)
- 2: Moderate concern (threshold met)
- 3: Critical concern (threshold exceeded significantly)

### Overall Severity

| Total Score | Severity | Symbol |
|------------|----------|--------|
| 0-5 | Low | 🟢 |
| 6-15 | Moderate | 🟡 |
| 16-30 | High | 🟠 |
| 31+ | Critical | 🔴 |

### Single Indicator Critical

If any single indicator scores 3 and has cross-validation evidence → **Critical** overall

### Trend Analysis Bonus

- Risk increasing over 3 years: +1 to severity
- Risk decreasing: -1 to severity
- First-time occurrence: Evaluate with caution

---

## Implementation Notes

### Data Fetching Strategy

```python
# Fetch 10+ years of annual data
start_date = (current_year - 12) * 10000 + 1231  # e.g., 20141231
end_date = current_year * 10000 + 1231

# Core tables
pro.balancesheet(ts_code, start_date, end_date, report_type='1')  # Annual
pro.income(ts_code, start_date, end_date, report_type='1')
pro.cashflow(ts_code, start_date, end_date, report_type='1')
pro.fina_indicator(ts_code, start_date, end_date)

# Supporting data
pro.stock_company(ts_code)  # Company info
pro.index_classify(src='SW2021')  # Industry
```

### Missing Data Handling

- Use most recent available year if historical missing
- Flag missing data as limitation in report
- Use quarterly data for recent trends if annual unavailable
- Industry comparison may use peers with available data

---

*Reference document for financial-risk-scanner skill. Do not modify thresholds without validation.*