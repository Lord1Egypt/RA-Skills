---
name: chinese-bank-forex-rates
description: "Use when you need the latest bank forex rates from major Chinese banks by bank name and currency names. Supports 招商银行, 中国银行, 中国农业银行, 中国工商银行, 中国建设银行, and 交通银行, with aliases such as 农行, 工行, 建行, and 交行."
---

# Chinese Bank Forex Rates

Use this skill when you need the latest forex rates for a supported Chinese bank and one or more currencies.

## Inputs

- `bank`: bank name or alias
- `currencies`: one or more currency names or ISO codes

## Output

The script returns JSON with:

- `bankName`
- `updateTime` in ISO 8601 format when normalization is possible
- `rates`: list of objects with `currencyName`, `buyPrice`, and `sellPrice`

Prices are standardized to CNY per 100 units of foreign currency, rounded to two decimal places. If the preferred value and configured fallback are both empty, the field is returned as an empty string.

## Supported Banks

- 招商银行
- 中国银行
- 中国农业银行
- 中国工商银行
- 中国建设银行
- 交通银行

## Price Selection Rule

When a bank exposes explicit `现汇` and `现钞` columns, the implementation uses:

- `buyPrice`: prefer `现汇买入价`, then `现钞买入价`
- `sellPrice`: prefer `现汇卖出价`, then `现钞卖出价`

If a bank only publishes one buy and one sell price, the published pair is used directly.

## Invocation

From this skill directory:

```bash
node index.js --bank 中国银行 --currencies 美元,EUR
```