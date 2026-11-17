# Finance Voucher Workbook Workflow

## Output Shape

Create a single `.xlsx` workbook containing:

- `信息汇总表`: source line-item invoice table.
- `发票基础信息`: invoice-level source table, including a total row when present.
- `进项税`: invoice-level input VAT checklist.
- `进项税 (有数量的)`: line-item-level input VAT table with quantity and unit price.
- Monthly voucher export sheet such as `202607`: import-ready voucher rows.
- `科目编码`: existing chart of accounts.
- `处理逻辑说明`: concise audit trail of source, month boundary, voucher rules, special tickets, and checks.
- `科目映射清单`: supplier/item-to-account mapping and rule sources.

Use the prior workbook's column order where available. Do not add decorative dashboard sheets.

## Source Tables

For `信息汇总表`, preserve columns like:

`序号 | 发票代码 | 发票号码 | 数电发票号码 | 销方识别号 | 销方名称 | 购方识别号 | 购买方名称 | 开票日期 | 税收分类编码 | 特定业务类型 | 货物或应税劳务名称 | 规格型号 | 单位 | 数量 | 单价 | 金额 | 税率 | 税额 | 价税合计 | 发票来源 | 发票票种 | 发票状态 | 是否正数发票 | 发票风险等级 | 开票人 | 备注`

For `发票基础信息`, preserve invoice-level columns like:

`序号 | 发票代码 | 发票号码 | 数电发票号码 | 销方识别号 | 销方名称 | 购方识别号 | 购买方名称 | 开票日期 | 金额 | 税额 | 价税合计 | 发票来源 | 发票票种 | 发票状态 | 是否正数发票 | 发票风险等级 | 开票人 | 备注`

Use `数电发票号码` as the primary invoice key when present. Otherwise use `发票代码 + 发票号码`.

## 进项税 Sheet

Generate one row per invoice.

Required columns:

`序号 | 勾选状态 | 发票来源 | 转内销证明编号 | 发票代码 | 发票号码 | 数电票号码 | 开票日期 | 销售方纳税人识别号 | 销售方纳税人名称 | 金额 | 税额 | 价税合计 | 票种 | 票种标签 | 发票状态`

Rules:

- `金额`, `税额`, and `价税合计` are invoice-level totals.
- `勾选状态` can be `已勾选` when source data is intended for checked input VAT processing.
- `所属月份` is usually the month after the invoice month, unless the user says otherwise.
- Store long invoice/taxpayer identifiers as text so Excel does not display scientific notation.

## 进项税 (有数量的) Sheet

Generate one row per source line item.

Rules:

- Do not merge same-invoice multi-line items.
- Preserve unit, quantity, unit price, amount, tax rate, tax amount, total, issuer, and remarks.
- Preserve electricity remarks because they often contain billing periods and meter details.
- If source contains quantity formulas or unit conversions, keep values unless the user asks to preserve formulas.

## Voucher Sheet

Use the prior voucher export column order:

`年份 | 月份 | 日 | 凭证类型 | 凭证编号 | 附单数 | 制单人 | 审核人 | 记账人 | 序号 | 科目编码 | 摘要 | 借方 | 贷方 | 外币金额 | 币种 | 汇率 | 数量 | 单价 | 结算类别 | 票号 | 结转标志 | 项目编码 | 客户编码 | 部门编码 | 人员编码 | 现金流量编码 | 合同编号`

Grouping:

- Group by invoice key.
- Voucher date normally equals `开票日期`.
- For a single-line ordinary purchase invoice, create three rows:
  1. debit material/expense account for pre-tax amount;
  2. debit input VAT account for tax amount;
  3. credit AP/bank account for tax-inclusive total.
- For one invoice with multiple line items, create one material/expense debit row per material account or line item, one tax row for total tax, and one credit row for invoice total.
- `借方` total must equal `贷方` total across the sheet.
- Keep `外币金额 = 0`, `币种 = RMB`, `汇率 = 0` unless the source explicitly requires foreign currency.

Personnel and numbering:

- Preserve the prior month's `制单人`, `审核人`, `记账人`, and `附单数` unless instructed otherwise.
- Continue voucher numbering from the prior workbook or the user-provided start.

## Account Mapping Rules

Never invent account codes. Use this priority:

1. Exact supplier and goods/service match in the prior month voucher sheet.
2. Exact supplier match in historical voucher sheet such as `24-26`.
3. Goods/service class match in historical vouchers.
4. Existing chart-of-accounts class match, documented as a finance-review assumption.

Document every mapping in `科目映射清单` with:

`供应商/场景 | 货物或服务 | 借方科目 | 借方口径 | 进项税科目 | 贷方科目 | 摘要生成口径 | 规则来源/说明`

Common mapping patterns from the reference case:

| Supplier / scenario | Goods or service | Debit account | Input tax account | Credit account | Summary pattern | Notes |
|---|---:|---:|---:|---|---|---|
| 东莞市钰瀚新材料科技有限公司 | 塑胶扣具 | 1403.002.028. | 2221.001.001. | 2202.050. | 购钰瀚商贸扣具 | Reuse June/history |
| 嘉兴市裕弘盛纺织品有限公司 | 过胶涤纶布 | 1403.002.002. | 2221.001.001. | 2202.018. | 购裕弘盛过胶涤纶布 | Reuse June/history |
| 东莞市源海盛五金制品有限公司 | 狗扣 | 1403.002.012. | 2221.001.001. | 2202.021. | 购源海盛狗扣 | Reuse June/history |
| 广东电网有限责任公司惠州惠阳供电局 | 电费 | 5101.001. | 2221.001.001. | 1002.002. | 付电费 | Special electricity handling |
| 灏洋外贸服务（惠州）有限公司 | 代理运费 | 6601.003. | 2221.001.001. | 2202.033. | 购运输费(灏洋外贸) | Freight/agent service |
| 惠州市联裕顺五金塑胶制品有限公司 | 胶袋 | 1403.002.029. | 1231.004. | 2202.039. | 购联裕顺胶袋 | Historical special tax account; flag for review |
| 昱冠拉链（惠州）有限公司 | 拉链/拉链头 | 1403.002.017./1403.002.018. | 2221.001.001. | 2202.011. | 购昱冠拉链 + item | Multi-line invoice split |
| 深圳市臻美达五金拉链有限公司 | 拉链/拉链头 | 1403.002.017./1403.002.018. | 2221.001.001. | 2202.022. | 购臻美达 + item | Multi-line invoice split |
| 东莞安姆科扣具有限公司 | D扣/日扣/梯扣 | 1403.002.028. | 2221.001.001. | 2202.020. | 购安姆科扣具 + item | Same invoice, same material class |
| 东莞市信耀五金塑胶制品有限公司 | 五金塑胶配件(胶轮) | 1403.002.028. | 2221.001.001. | 2202.019. | 购信耀胶轮 | Reuse June/history |
| 惠阳区新圩长布鸿益织带厂 | 魔术贴 | 1403.002.036. | 2221.001.001. | 2202.043. | 购鸿益魔术贴 | Reuse June/history |
| 深圳市辉鸿纺织有限公司 | 网布 | 1403.002.003. | 2221.001.001. | 2202.041. | 购辉鸿网布 | Reuse June/history |
| 惠州市惠阳嘉伟纸品有限公司 | 纸箱 | 1403.002.011. | 2221.001.001. | 2202.028. | 购嘉伟纸箱 | Reuse June/history |
| 东莞标信精密橡塑制品有限公司 | 塑胶扣具 | 1403.002.038. | 2221.001.001. | 2202.030. | 购东莞标信塑胶扣具 | Reuse June/history |
| 东莞市寮步广兴纺织品有限公司 | 尼龙布 | 1403.002.023. | 2221.001.001. | 2202.009. | 购寮步广兴尼龙布 | Reuse June/history |
| 惠州市联恒新材料有限公司 | 珍珠棉 | 1403.002.020. | 2221.001.001. | 2202.042. | 购联恒珍珠棉 | Reuse June/history |
| 惠阳区新圩华昌制线加工厂 | 织带 | 1403.002.037. | 2221.001.001. | 2202.027. | 购华昌织带 | Reuse June/history |

## Special Tickets

- Electricity: use the electricity-specific debit and bank/AP account from history; keep remarks.
- Freight/agent freight: use the transport expense account and AP account from history. If multiple freight invoices exist, generate separate voucher groups unless the prior template consolidates them.
- Red invoices: keep sign convention consistent with the source and prior template. If unclear, stop and ask.
- Foreign-currency settlement: do not infer from normal VAT purchase data. Ask for exchange rate, currency, settlement bank, and voucher pattern.
- One invoice with multiple line items: split material debit rows and aggregate tax/credit rows.
- One line item split across accounts: only split when prior template or user mapping proves the rule.

## Audit Sheet Content

`处理逻辑说明` should state:

- Source workbook and month boundary.
- Output sheets generated.
- Voucher grouping and numbering policy.
- Account mapping policy.
- Special-ticket handling.
- Verification performed.
- Remaining finance-review assumptions.

## Validation Checklist

Complete only when:

- `进项税` invoice totals equal source `发票基础信息` totals.
- `进项税 (有数量的)` line totals equal source `信息汇总表` totals.
- Voucher debit total equals credit total.
- Each invoice key appears in the voucher sheet unless excluded and documented.
- All account codes exist in `科目编码`.
- Long identifiers display as text, not scientific notation.
- No formula errors appear.
- Rendered key sheets are legible.
