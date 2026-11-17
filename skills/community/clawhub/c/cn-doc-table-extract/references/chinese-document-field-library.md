# Chinese Document Field Library / 中文文档抽取字段库

Canonical mapping used by `scripts/extract_tables.py` (header aliasing) and
`scripts/validate_fields.py` (required-field and format rules).

**How to read a row**: `中文原文 (pinyin-free Chinese original)` → `English key` →
accepted alias variants → expected value type → required for which profile.

**Value types**

| Type | Meaning | Examples |
|---|---|---|
| `date` | A calendar date | `2024-01-05`, `2024年1月5日` |
| `datetime` | Date + time | `2024-01-05 14:30:00` |
| `amount` | A monetary value, RMB assumed unless stated | `1,234.56`, `￥1234.56` |
| `amount_pct` | A rate or percentage | `13%`, `0.13` |
| `text` | Free text | `货款` |
| `id` | An identifier, digits and/or letters | `25377000000123456789` |
| `person` | A person or company name | `张三`, `示例制造有限公司` |
| `code` | A coded value | HS code `8471300000` |
| `enum` | One of a fixed set | `借` / `贷` |

**Normalization rules applied before matching** (the original string is always kept
in `raw`):

1. Trim whitespace and non-breaking spaces (U+00A0).
2. Convert full-width ASCII to half-width (U+FF01–U+FF5E → U+21–U+7E) and full-width
   space (U+3000) to a normal space.
3. Strip a trailing `：` / `:` / `:` from a header cell.
4. Remove all whitespace inside a candidate header before alias comparison.
5. Lowercase Latin text for alias comparison only.

---

## 1. 银行对账单 / 交易明细 — `bank_statement`

| 中文原文 | English key | Aliases accepted | Type | Required |
|---|---|---|---|---|
| 交易日期 | transaction_date | 交易日, 日期, 记账日期, 交易时间, 交易日, 交易日 | date | yes |
| 摘要 | summary | 摘要, 交易摘要, 摘要说明, 交易类型, 备注, 用途 | text | no |
| 借方发生额 | debit_amount | 借方发生额, 借方金额, 支出金额, 借方, 付出金额, 支出 | amount | no |
| 贷方发生额 | credit_amount | 贷方发生额, 贷方金额, 收入金额, 贷方, 收入, 存入金额, 收入金额 | amount | no |
| 发生额 | amount | 交易金额, 金额, 发生额, 交易额 | amount | no |
| 余额 | balance | 余额, 账户余额, 本方余额, 联方余额 | amount | no |
| 对方户名 | counterparty | 对方户名, 对方账户名称, 对方账户名, 交易对手, 对方单位名称, 收款人, 付款人 | person | no |
| 对方账号 | counterparty_account | 对方账号, 对方账户, 交易对手账号 | id | no |
| 本方账号 | account_no | 本方账号, 本方账户, 账号, 卡号, 账户账号 | id | no |
| 币种 | currency | 币种, 货币, 货币代码 | text | no |
| 凭证号 / 流水号 | transaction_no | 流水号, 交易流水号, 凭证号, 业务编号, 参考号, 回单编号 | id | no |

**Profile rules**

- At least one of `debit_amount` / `credit_amount` / `amount` must be present on a
  statement record; if none of the three is found, the statement is read as a balance
  listing and the run is flagged `no_amount_column`.
- `balance` should be monotonically consistent with the running amounts within each
  account. A break in the chain is a `warning` named `balance_chain_break` — bank
  systems legitimately insert a carried balance row, so the check reports the first
  break and does not claim the statement is wrong.
- Negative values in `debit_amount` or `credit_amount` are `warning`
  `unexpected_sign` (some banks show reversals as negative amounts).
- Cross-page statements often repeat the header row on every page; those repeated rows
  must be dropped and counted in `dropped_header_rows`.

---

## 2. 增值税发票 / 收据 — `vat_invoice`

| 中文原文 | English key | Aliases accepted | Type | Required |
|---|---|---|---|---|
| 发票代码 | invoice_code | 发票代码, 票据代码, 发票编码 | id | yes |
| 发票号码 | invoice_number | 发票号码, 票据号码, 发票号, 票据号, 发票流水号 | id | yes |
| 开票日期 | issue_date | 开票日期, 填开日期, 开具日期, 出发日期, 日期 | date | yes |
| 金额 | amount | 金额, 合计金额, 不含税金额, 税前金额, 货款金额, 小计 | amount | yes |
| 税额 | tax_amount | 税额, 合计税额, 增值税额, 税额合计, 增值税 | amount | yes |
| 价税合计 | total_amount | 价税合计, 价税合计金额, 价税总计, 合计金额(大写), 合计 | amount | yes |
| 销方名称 | seller | 销方名称, 销售方名称, 销售方, 销方, 收款方 | person | yes |
| 销方税号 | seller_tax_id | 销方纳税人识别号, 销售方纳税人识别号, 纳税人识别号, 税号, 统一社会信用代码 | id | no |
| 购方名称 | buyer | 购方名称, 购买方名称, 购买方, 购方, 付款方 | person | no |
| 购方税号 | buyer_tax_id | 购方纳税人识别号, 购买方纳税人识别号 | id | no |
| 开票人 | drawer | 开票人, 制单人, 复核人 | person | no |
| 备注 | remarks | 备注, 备注栏, 附加说明 | text | no |
| 项目名称 | item_name | 项目名称, 货物或应税劳务名称, 商品名称, 品名, 货物名称 | text | no |
| 数量 | quantity | 数量, 件数, 台数, 数量(单位) | amount | no |
| 单价 | unit_price | 单价, 单价(元), 成交单价 | amount | no |
| 税率 | tax_rate | 税率, 税率(%), 征收率 | amount_pct | no |

### 发票号码与发票代码长度规则

This is the most common false rejection, so the rule is stated explicitly:

| Document generation | 发票号码 invoice number | 发票代码 invoice code |
|---|---|---|
| 全电发票 / 数电票 (fully digital) | **20 digits** | often absent |
| 纸质增值税发票 (paper VAT invoice) | **8 digits** | **10 or 12 digits** |
| 增值税普通发票 2017 and earlier | 8 digits | 10 or 12 digits |

Acceptance rule in `validate_fields.py`:

- `invoice_number`: length ∈ {8, 20} → pass. Length ∈ {9, 10, 12} → `warning`
  `invoice_number_length_unusual` (these are more likely to be a code pasted into the
  wrong field). Any other length → `error` `invalid_invoice_number`.
- `invoice_code`: length ∈ {10, 12} → pass. Absent → allowed only when the document
  declares 全电发票. Present with another length → `warning`.
- Digits only. A value containing letters, spaces or `*` → `error`
  `invalid_invoice_number`.

### 价税合计 reconciliation

- If `amount`, `tax_amount` and `total_amount` are all present:
  `|amount + tax_amount - total_amount| <= tolerance` (default `0.01`) → pass.
  Otherwise → `error` `total_not_additive`.
- If only `amount` and `tax_amount` are present, and `tax_rate` is present:
  `|amount * tax_rate - tax_amount| <= max(0.01, amount * 0.005)` → else `warning`
  `tax_rate_inconsistent`.
- Never derive `total_amount` and write it back into the record as if the document
  printed it.

---

## 3. 保单 / 保险合同 — `insurance_policy`

| 中文原文 | English key | Aliases accepted | Type | Required |
|---|---|---|---|---|
| 保单号 | policy_no | 保单号, 保单号码, 保险单号, 合同号, 保单号/合同号, 保险合同号 | id | yes |
| 投保人 | policyholder | 投保人, 投保人名称, 投保人姓名, 客户名称, 投保单位 | person | yes |
| 被保人 | insured | 被保人, 被保险人, 被保险人名称, 受益人(when used as subject), 保险受益人 | person | yes |
| 保险标的 | subject | 保险标的, 标的, 保险标的名称, 承保标的 | text | no |
| 保险责任 | coverage | 保险责任, 保险责任范围, 承保范围 | text | no |
| 保额 | sum_insured | 保额, 保险金额, 保险金额(元), 保险金额（万元）, 责任限额, 累计责任限额 | amount | yes |
| 保费 | premium | 保费, 保险费, 保险费(元), 年保费, 保费合计, 期缴保费 | amount | yes |
| 缴费期 | payment_term | 缴费期, 缴费期间, 缴费期限, 交费期间, 保险期间, 保障期间, 保险期限 | text | yes |
| 生效日期 | effective_date | 生效日期, 保险起期, 起保日期, 生效日, 起始日期 | date | yes |
| 到期日期 | expiry_date | 到期日期, 保险止期, 终止日期, 终保日期, 失效日期 | date | no |
| 缴费方式 | payment_mode | 缴费方式, 交费方式, 支付方式, 交费年期 | enum | no |
| 币种 | currency | 币种, 货币 | text | no |
| 保险公司 | insurer | 保险公司, 承保公司, 保险人 | person | no |
| 业务员 / 代理人 | agent | 业务员, 代理人, 保险经纪人, 营销员 | person | no |

### 保单规则

- `保额` and `保费` must be > 0. A zero or negative value → `error`
  `non_positive_amount`.
- If the document states 保险金额 in 万元 (ten-thousand yuan units — the header literally
  reads 保险金额(万元)), the value must be multiplied by 10000 before comparison with a
  currency field. Record the unit in the raw string and in `notes`.
- If both `effective_date` and `expiry_date` are present and expiry ≤ effective →
  `error` `date_range_inverted`.
- `缴费期` with a `终身` / `趸缴` / `终身寿险` value and a `保费` of 0 is a normal
  configuration, not an error. Do not flag it.
- `被保险人` may legitimately be identical to `投保人`. Do not flag that as a
  duplicate-field issue.

---

## 4. 工资表 / 社保公积金表 — `payroll`

| 中文原文 | English key | Aliases accepted | Type | Required |
|---|---|---|---|---|
| 姓名 | name | 姓名, 员工姓名, 职工姓名, 人员姓名, 名字 | person | yes |
| 工号 | employee_no | 工号, 员工工号, 员工编号, 人员编号, 职工号, 序号 | id | yes |
| 身份证号 | id_no | 身份证号, 身份证号码, 公民身份号码, 证件号码, 身份证 | id | no |
| 部门 | department | 部门, 所属部门, 部门名称, 中心 | text | no |
| 岗位 | position | 岗位, 职位, 岗位名称, 职务 | text | no |
| 应发工资 | gross_pay | 应发工资, 应发合计, 工资总额, 应发金额, 应发工资合计 | amount | yes |
| 扣款合计 | deduction_total | 扣款合计, 扣款小计, 扣款总额, 各项扣款合计 | amount | no |
| 个人所得税 | income_tax | 个人所得税, 个税, 所得税, 代扣个税, 个人所得税(元) | amount | no |
| 社保个人 | social_insurance | 社保, 社保个人, 个人社保, 养老保险, 医疗保险个人, 社保(个人) | amount | no |
| 公积金个人 | housing_fund | 公积金, 住房公积金, 个人公积金, 公积金个人 | amount | no |
| 实发工资 | net_pay | 实发工资, 实发合计, 实发金额, 税后工资, 应发-扣款 | amount | yes |
| 银行账号 | bank_account | 银行账号, 银行卡号, 工资卡号, 账号 | id | no |
| 入职日期 | hire_date | 入职日期, 入职时间, 参加工作日期 | date | no |

### 工资表规则

- Payroll rows are personal data. Mask 身份证号 to the last 4 characters in any
  human-readable output, and say that you did it.
- Reconciliation: if `gross_pay`, `deduction_total` and `net_pay` are all present,
  `|gross_pay - deduction_total - net_pay| <= 0.01` → else `warning`
  `payroll_not_additive`. Rounding differences up to 0.05 are tolerated (common when
  cents are dropped per row) but still reported as `info`.
- `姓名` + `工号` must be unique across rows. A repeated pair → `error`
  `duplicate_employee_row`.
- `扣款合计` may itself be missing while its components are present. In that case sum
  the components (个税 + 社保 + 公积金 + 其他) and compare with `实发工资`; the
  reconstruction is written to `notes`, never into the field itself.

---

## 5. 物流运单 / 报关单 / 招投标明细 — `logistics`, `customs`

| 中文原文 | English key | Aliases accepted | Type | Required |
|---|---|---|---|---|
| 运单号 | waybill_no | 运单号, 运单号码, 货运单号, 物流单号, 提单号, 快递单号 | id | yes |
| 发货人 | shipper | 发货人, 发货方, 托运人, 寄件人, 卖方 | person | yes |
| 收货人 | consignee | 收货人, 收货方, 收货单位, 收件人, 买方 | person | yes |
| 品名 | goods_name | 品名, 货物名称, 商品名称, 物品名称, 货品名称 | text | yes |
| 件数 / 数量 | quantity | 件数, 数量, 箱数, 件量, 数量(件) | amount | yes |
| 毛重 | gross_weight | 毛重, 毛重(kg), 总重, 重量 | amount | no |
| 净重 | net_weight | 净重, 净重(kg), 净重量 | amount | no |
| 体积 | volume | 体积, 体积(m3), 材积 | amount | no |
| 运费 | freight | 运费, 运杂费, 物流费用, 运输费用 | amount | no |
| 起运地 | origin | 起运地, 发货地, 起运站 | text | no |
| 目的地 | destination | 目的地, 到达地, 目的站, 收货地 | text | no |
| 报关单号 | declaration_no | 报关单号, 海关单号, 进出口报关单号 | id | yes (customs) |
| 商品编号 | hs_code | 商品编号, HS编码, 商品编码, 海关编码, 税则号列 | code | yes (customs) |
| 单价 | unit_price | 单价, 单价(元), 成交单价, 申报单价 | amount | no |
| 数量 | quantity | 数量, 申报数量, 成交数量 | amount | yes |
| 金额 | amount | 金额, 总价, 申报金额, 成交金额, 人民币金额 | amount | yes |
| 币制 | currency | 币制, 币种, 货币代码 | text | yes (customs) |
| 成交方式 | trade_term | 成交方式, 贸易方式, 交货方式 | text | no |
| 原产地 | origin_country | 原产地, 原产国 | text | no |

### 物流/报关规则

- `毛重` ≥ `净重` when both are present. Otherwise → `warning` `weight_inverted`.
- `数量` × `单价` should equal `金额` within tolerance when all three are present →
  else `warning` `line_amount_mismatch`.
- `金额` in a customs declaration is usually a 币制 amount, not always RMB. Do not
  apply a tax-rate check to it.
- A 报关单号 is typically 18 characters with a customs prefix. Length outside 18 is a
  `warning`, not an error, because formats vary by customs district.

---

## 6. 通用明细表 — `generic`

For a document with no recognizable profile:

- The header row is used verbatim as the field name.
- The first column is also recorded as `key` if it looks like an identifier (all digits,
  or a `编号`/`代码` style header) — this gives the duplicate-row check something to
  key on.
- Only universal checks apply: parseable amounts, parseable dates, no identical
  duplicate rows, and traceability.

---

## 7. Amount parsing reference

`validate_fields.py` accepts all of the following and normalizes them to a float:

| Input | Normalized |
|---|---|
| `1234.56` | `1234.56` |
| `1,234.56` | `1234.56` |
| `12,345,678.90` | `12345678.90` |
| `￥1,234.56` | `1234.56` |
| `¥1,234.56` | `1234.56` |
| `RMB 1,234.56` | `1234.56` |
| `CNY1234.56` | `1234.56` |
| `人民币1,234.56元` | `1234.56` |
| `1,234.56 元` | `1234.56` |
| `１２３４．５６` (full-width) | `1234.56` |
| `1234.56-` (trailing minus) | `-1234.56` |
| `(1,234.56)` (accounting negative) | `-1234.56` |
| `1 234,56` (European spacing) | `1234.56` |

Rejected → `error` `invalid_amount`: `12.3.4`, `1,2,3`, `abc`, `12,34.5.6`, empty.

A bare `-` or `--` means "no amount" in many Chinese forms (合计/小计 rows, blank
cells). It is treated as *missing*, not as an error, and is excluded from sums.

---

## 8. Date parsing reference

| Input | Normalized |
|---|---|
| `2024-01-05` | `2024-01-05` |
| `2024/01/05` | `2024-01-05` |
| `2024.01.05` | `2024-01-05` |
| `2024年1月5日` | `2024-01-05` |
| `2024年01月05日` | `2024-01-05` |
| `20240105` | `2024-01-05` |
| `2024年1月` | `2024-01-01` (day defaults to 1, flagged `info` `date_day_defaulted`) |
| `2024-01-05 14:30:00` | `2024-01-05` (time kept in `raw`) |

Rejected → `error` `invalid_date`: `2024年2月30日`, `2024-13-01`, `01/02/2024`
(ambiguous day/month order), `2024-1-5-` , `待定`, `见附注`.

Ambiguous inputs keep `raw`, set the normalized value to `null`, and are listed under
`issues` with the rule `ambiguous_date`. They are **never** auto-resolved.
