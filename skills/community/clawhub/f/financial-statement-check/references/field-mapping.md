# 财报三表科目字段映射表

## 概述

本文档定义了三表（**资产负债表 / 利润表 / 纳税申报表**）关键科目的标准字段名及其常见措辞变体，用于指导大模型在OCR结果中准确识别和映射科目，并统一单位和币种。

## 三表识别关键词

### 资产负债表（Balance Sheet）
识别关键词（表头/标题中出现以下任一即可判定）：
- "资产负债表"、"合并资产负债表"、"母公司资产负债表"
- "Balance Sheet"、"Statement of Financial Position"
- 表中同时出现"资产"和"负债"分区

### 利润表（Income Statement）
识别关键词：
- "利润表"、"合并利润表"、"损益表"、"综合收益表"
- "Income Statement"、"Profit and Loss Statement"、"Statement of Comprehensive Income"
- 表中出现"营业收入"、"净利润"等损益类科目

### 纳税申报表（Tax Return）
识别关键词：
- "纳税申报表"、"增值税纳税申报表"、"企业所得税年度纳税申报表"、"企业所得税月（季）度预缴纳税申报表"
- "VAT Return"、"Corporate Income Tax Return"
- 表中出现"应税销售额"、"销项税额"、"进项税额"、"应纳税额"、"应纳税所得额"等科目

## 报告期与申报类型识别

### 报告期识别

在表头、落款或备注区识别以下信息：
- **时间窗口**：`起始日 ~ 截止日`，如"2024-01-01 ~ 2024-12-31"、"2024年1月1日至2024年12月31日"、"2024年度"
- **期末日**：如"2024年12月31日"、"截至2024年第三季度末"
- **税款所属期**：纳税申报表中的"税款所属期自 …… 至 ……"

### 自然年错位判定

- **无错位**：报告期起始日为 `XXXX-01-01`，截止日为 `XXXX-12-31` 或落在 `XXXX-03/06/09/12` 月末
- **错位**：报告期跨越自然年（如 2024-07-01 ~ 2025-06-30），或起止日期非月末/季末/年末

### 申报类型识别

依据"税款所属期"长度判定申报类型：

| 申报类型 | 判定依据 |
|---------|---------|
| 月度 | 税款所属期跨度为 1 个月（如 2024-05-01 ~ 2024-05-31） |
| 季度 | 税款所属期跨度为 3 个月（如 2024-Q1、2024-01-01 ~ 2024-03-31） |
| 年度 | 税款所属期跨度为 12 个月（如 2024-01-01 ~ 2024-12-31） |

## 资产负债表字段映射

### 资产类

| 标准字段名 | JSON Key | 常见措辞变体 |
|-----------|----------|-------------|
| 总资产 | total_assets | 资产合计、资产总计、资产总额、Total Assets |
| 流动资产 | current_assets | 流动资产合计、流动资产小计、Current Assets |
| 非流动资产 | non_current_assets | 非流动资产合计、非流动资产小计、Non-current Assets |
| 货币资金 | cash_and_equivalents | 货币资金、现金及现金等价物、银行存款、Cash and Cash Equivalents |
| 应收账款 | accounts_receivable | 应收账款、应收帐款、应收款项、Accounts Receivable |
| 应收票据 | notes_receivable | 应收票据、Notes Receivable |
| 预付款项 | prepayments | 预付款项、预付账款、Prepayments |
| 存货 | inventory | 存货、库存商品、Inventory、Inventories |
| 其他流动资产 | other_current_assets | 其他流动资产、Other Current Assets |
| 固定资产 | fixed_assets | 固定资产、固定资产净值、固定资产净额、Property Plant and Equipment |
| 在建工程 | construction_in_progress | 在建工程、Construction in Progress |
| 无形资产 | intangible_assets | 无形资产、Intangible Assets |
| 长期投资 | long_term_investments | 长期股权投资、长期投资、Long-term Investments |
| 商誉 | goodwill | 商誉、Goodwill |

### 负债类

| 标准字段名 | JSON Key | 常见措辞变体 |
|-----------|----------|-------------|
| 总负债 | total_liabilities | 负债合计、负债总计、负债总额、Total Liabilities |
| 流动负债 | current_liabilities | 流动负债合计、流动负债小计、Current Liabilities |
| 非流动负债 | non_current_liabilities | 非流动负债合计、非流动负债小计、Non-current Liabilities |
| 短期借款 | short_term_borrowings | 短期借款、短期贷款、Short-term Borrowings |
| 应付账款 | accounts_payable | 应付账款、应付帐款、Accounts Payable |
| 应付票据 | notes_payable | 应付票据、Notes Payable |
| 预收款项 | advance_receipts | 预收款项、预收账款、合同负债、Advance Receipts、Contract Liabilities |
| 应付职工薪酬 | employee_benefits_payable | 应付职工薪酬、应付工资、Employee Benefits Payable |
| 应交税费 | taxes_payable | 应交税费、应交税金、Taxes Payable |
| 长期借款 | long_term_borrowings | 长期借款、长期贷款、Long-term Borrowings |
| 应付债券 | bonds_payable | 应付债券、Bonds Payable |

### 所有者权益类

| 标准字段名 | JSON Key | 常见措辞变体 |
|-----------|----------|-------------|
| 所有者权益 | owners_equity | 所有者权益合计、股东权益合计、净资产、所有者权益（或股东权益）合计、Total Equity、Shareholders' Equity |
| 实收资本 | paid_in_capital | 实收资本、股本、实收资本（或股本）、Paid-in Capital、Share Capital |
| 资本公积 | capital_reserve | 资本公积、Capital Reserve |
| 盈余公积 | surplus_reserve | 盈余公积、Surplus Reserve |
| 未分配利润 | undistributed_profit | 未分配利润、留存收益、Retained Earnings、Undistributed Profit |
| 少数股东权益 | minority_interest | 少数股东权益、Minority Interest |

### 资产负债表 — **必填字段清单**（字段完整性校验用）

| 标准字段名 | JSON Key |
|-----------|----------|
| 总资产 | total_assets |
| 总负债 | total_liabilities |
| 所有者权益 | owners_equity |
| 货币资金 | cash_and_equivalents |
| 短期借款 | short_term_borrowings |
| 营业收入（如在报表中附列） | revenue |

> 📌 **说明**："营业收入"原则上在利润表中披露，资产负债表必填项里列示它，是为了兼容部分财报在资产负债表附注中给出的同口径营业收入，便于跨表核对。

## 利润表字段映射

| 标准字段名 | JSON Key | 常见措辞变体 |
|-----------|----------|-------------|
| 本期营业收入 | revenue | 营业收入、营业总收入、主营业务收入、本期金额、本期数、Revenue、Operating Revenue、Total Revenue |
| 上期营业收入 | revenue_last_period | 上期营业收入、上年同期营业收入、上期金额、上年同期数 |
| 营业成本 | operating_cost | 营业成本、营业总成本、主营业务成本、Cost of Revenue、Operating Cost |
| 毛利润 | gross_profit | 毛利润、毛利、营业毛利、Gross Profit（注：部分报表不直接列示，需计算：营业收入 - 营业成本）|
| 税金及附加 | taxes_and_surcharges | 税金及附加、营业税金及附加、Taxes and Surcharges |
| 销售费用 | selling_expenses | 销售费用、营销费用、Selling Expenses |
| 管理费用 | admin_expenses | 管理费用、Administrative Expenses |
| 财务费用 | financial_expenses | 财务费用、Financial Expenses |
| 研发费用 | rd_expenses | 研发费用、研究开发费用、R&D Expenses |
| 资产减值损失 | asset_impairment_loss | 资产减值损失、Asset Impairment Loss |
| 信用减值损失 | credit_impairment_loss | 信用减值损失、Credit Impairment Loss |
| 投资收益 | investment_income | 投资收益、Investment Income |
| 营业利润 | operating_profit | 营业利润、Operating Profit |
| 营业外收入 | non_operating_income | 营业外收入、Non-operating Income |
| 营业外支出 | non_operating_expenses | 营业外支出、Non-operating Expenses |
| 利润总额 | total_profit | 利润总额、税前利润、Profit Before Tax、Total Profit |
| 所得税费用 | income_tax_expense | 所得税费用、所得税、Income Tax Expense |
| 净利润 | net_profit | 净利润、税后利润、Net Profit、Net Income |
| 归属母公司净利润 | net_profit_to_parent | 归属于母公司所有者的净利润、归属于母公司股东的净利润、Net Profit Attributable to Parent |
| 会计折旧 | accounting_depreciation | 折旧、固定资产折旧（附注中披露）、会计准则下折旧费用 |
| 实际计提职工薪酬 | actual_employee_compensation | 应付职工薪酬本期计提数、职工薪酬（含工资、社保、福利费等实际计提数） |

### 利润表 — **必填字段清单**

| 标准字段名 | JSON Key |
|-----------|----------|
| 营业收入 | revenue |
| 营业利润 | operating_profit |
| 利润总额 | total_profit |
| 净利润 | net_profit |

## 纳税申报表字段映射

### 增值税纳税申报表

| 标准字段名 | JSON Key | 常见措辞变体 |
|-----------|----------|-------------|
| 应税销售额 | taxable_sales | 应税销售额、按适用税率计税销售额、一般项目应税销售额、简易计税应税销售额 |
| 销项税额 | output_tax | 销项税额、本期销项税额合计、Output VAT |
| 进项税额 | input_tax | 进项税额、本期进项税额合计、Input VAT |
| 应纳税额（增值税） | vat_payable | 应纳税额、本期应纳税额、增值税应纳税额 |
| 实缴增值税额 | vat_paid | 已纳税额、本期已缴税额、实缴增值税、入库税款 |

### 企业所得税纳税申报表

| 标准字段名 | JSON Key | 常见措辞变体 |
|-----------|----------|-------------|
| 营业收入（申报口径） | tax_revenue | 营业收入、一、营业收入、纳税人营业收入 |
| 利润总额（申报口径） | tax_total_profit | 利润总额、会计利润总额 |
| 纳税调增金额 | tax_adjustment_increase | 纳税调整增加额、加：纳税调整增加额、企业纳税调增金额 |
| 纳税调减金额 | tax_adjustment_decrease | 纳税调整减少额、减：纳税调整减少额 |
| 应纳税所得额 | taxable_income | 应纳税所得额、应纳所得税所得额 |
| 应纳所得税额 | income_tax_payable | 应纳所得税额、应纳企业所得税额、应纳税额 |
| 减免税额 | tax_reduction | 减免所得税额、减：减免所得税额 |
| 抵免税额 | tax_credit | 抵免所得税额、减：抵免所得税额 |
| 实缴企业所得税额 | income_tax_paid | 已预缴所得税额、实际已缴所得税额、本期实缴所得税额 |
| 税法折旧 | tax_depreciation | 税法折旧额、按税法规定计算的折旧额、折旧（税法口径） |
| 税表可扣除职工薪酬 | deductible_employee_compensation | 工资薪金支出税前扣除金额、职工薪酬税前扣除额、实际发生的合理的工资薪金支出 |

### 纳税申报表 — **必填字段清单**

| 标准字段名 | JSON Key |
|-----------|----------|
| 应税销售额 | taxable_sales |
| 销项税额 | output_tax |
| 进项税额 | input_tax |
| 应纳税额（增值税） | vat_payable |
| 营业收入（申报口径） | tax_revenue |
| 利润总额（申报口径） | tax_total_profit |
| 应纳税所得额 | taxable_income |
| 应纳所得税额 | income_tax_payable |

## 单位与币种统一规则（⭐强制）

### 1. 单位统一为"万元"

从表头、脚注或备注识别单位，统一转换为 **万元**（保留2位小数）：

| 原单位 | 换算系数（→万元） |
|-------|-----------------|
| 元 | ÷ 10000 |
| 千元 | ÷ 10 |
| 万元 | × 1（无需转换） |
| 百万元 | × 100 |
| 亿元 | × 10000 |

### 2. 币种一致性与汇率转换

**执行步骤**：

1. 识别三表各自标注的币种（CNY / USD / EUR / HKD / JPY / …）；通常在表头"金额单位：人民币元"或"Currency: USD"等位置。
2. **若三表币种一致**：按上述单位规则转换为"万元"即可，输出时在表头标注币种（例：`金额（万元，CNY）`）。
3. **若三表币种不一致**：
   - 以 CNY（人民币）为基准，对非 CNY 科目**按当前实时汇率**乘上汇率折算为 CNY 后，再转万元。
   - **在输出时标注币种**，例如：`金额（万元，已由USD按汇率1:7.15折算为CNY）`。
   - 汇率来源优先使用实时接口（如中国人民银行中间价 / 外汇牌价）。若无法获取实时数据，使用报告期最后一日的官方汇率，并在输出中注明。

### 3. 负数与千分位处理

- 括号表示：`(1,234.56)` → `-1234.56`
- 负号表示：`-1,234.56` → `-1234.56`
- 红字/红色标注视为负数
- 去除千分位分隔符：`1,234,567.89` → `1234567.89`

### 4. 空值处理

- "—"、"-"、"/"、空白 → `null`（未披露，**字段完整性校验时计为缺失**）
- "0"、"0.00" → `0`（披露为零，**视为已披露**）

### 5. 异常标注

- 若 OCR 未识别到某科目 或 映射失败，原始指标输出时该行金额栏标注 `⚠️ 异常（未识别/未匹配）` 而非留空。
