# Family Bookkeeping Import Mapping

Use this file when importing exported statements from WeChat or Alipay.

## Import Policy

- Do not claim direct access to user accounts
- Expect the user to export a bill file first
- Normalize external files into the canonical ledger schema
- Deduplicate primarily by `流水号`
- If `流水号` is unavailable, fallback to `日期 + 金额 + 备注/交易对方 + 支付平台`

## Canonical Output Fields

- 日期
- 金额
- 记账人
- 一级类型
- 二级类型
- 备注
- 收支类型
- 支付平台
- 导入来源
- 流水号

## WeChat Mapping

Common source columns:
- 交易时间
- 交易类型
- 交易对方
- 商品
- 收/支
- 金额(元)
- 支付方式
- 当前状态
- 交易单号
- 商户单号
- 备注

Suggested mapping:
- `日期` ← `交易时间`
- `金额` ← `金额(元)`
- `收支类型` ← `收/支`
- `支付平台` ← `微信`
- `流水号` ← `交易单号`
- `导入来源` ← `微信账单`
- `备注` ← `商品 + 交易对方 + 原备注`（可拼接）

## Alipay Mapping

Observed real-world export pattern:
- Often delivered as a **password-protected ZIP**
- Actual statement file is commonly a **GB18030-encoded CSV**
- The file may contain a long descriptive preface before the real header row

Common source columns:
- 交易时间
- 交易分类
- 交易对方
- 对方账号
- 商品说明
- 收/支
- 金额
- 收/付款方式
- 交易状态
- 交易订单号
- 商家订单号
- 备注

Suggested mapping:
- `日期` ← `交易时间`
- `金额` ← `金额`
- `收支类型` ← `收/支`
- `支付平台` ← `支付宝`
- `流水号` ← `交易订单号`
- `导入来源` ← `支付宝账单`
- `备注` ← `商品说明 + 交易对方 + 原备注`（可拼接）

Special rule:
- Skip rows where `收/支 = 不计收支` by default, because they are usually neutral entries such as investment movements, balance transfers, or yield postings.

## Normalization Rules

- Keep `金额` as a positive decimal number
- Use `收支类型` to indicate direction
- Trim whitespace from all string values
- Keep empty optional values as empty strings instead of inventing content
- If no category can be inferred, use `其他 / 暂未分类`
- If a row looks like a header note, summary, or empty line, skip it

## Dedupe Rules

Priority:
1. `流水号`
2. `日期 + 金额 + 支付平台 + 备注`

Recommended behavior:
- Keep only one record per unique dedupe key during a single import batch
- When comparing against existing ledger rows, prefer `流水号` exact match
