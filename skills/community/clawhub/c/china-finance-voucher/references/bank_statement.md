# Bank Statement Workbook Workflow

## Scope

Use this branch when the source is a monthly bank detail export, especially an `账户明细` workbook for the agricultural bank account used in the July 2026 case.

The goal is to produce a finance-ready workbook that matches the prior manual template, not a generic statement dump.

## Output Shape

Preserve the statement-style sheet as the main sheet, and add a `处理校验` sheet with:

- row counts
- income / expense totals
- fee aggregation summary
- balance continuity check
- rows that still depend on finance judgment

Do not add decorative sheets.

## Core Rules

1. Preserve the source row order for all non-fee rows.
2. Treat `费用外收` as the only automatically aggregated bank-fee class unless the user provides another grouping rule.
3. Group visible `费用外收` rows by transaction date.
4. Use the last visible fee row of the day for the output balance and counterparty fields.
5. Set the summary to `付手续费{n}单`, where `n` is the number of fee rows that day.
6. Keep non-fee summaries aligned to the prior manual template or historical finance judgment.
7. Do not invent accounting classifications when the manual template left a row blank.
8. Keep account numbers and other long identifiers as text, not scientific notation.
9. Keep balances continuous against the source statement when the source rows allow it.
10. Do not infer missing fee rows or fill missing statement rows by default.

## Exception Policy

If the visible detail rows do not reconcile to the source total row, or the balance chain has gaps:

- Do not automatically create inferred `费用外收` rows.
- Do not alter source totals to force a match.
- Record the issue in `处理校验` with visible totals, source totals, differences, and affected dates/rows.
- Mark the workbook as requiring finance review.
- 只有在用户明确授权，或手工模板能够证明缺失行和金额时，才允许补回缺失费用行。

如果用户授权补回，必须单独记录为 `用户授权补回/手工模板补回`，并说明笔数、金额、影响日期和依据。

## Manual-Template Behavior

Match the prior month style as closely as possible:

- `A` column: date extracted from `交易时间`
- `B` column: original `交易时间`
- `C` column: finance summary
- `D:F`: income, expense, balance
- `G:I`: counterparty account, name, bank
- `J`: bank memo / category

When the historical template uses a fixed summary such as `个人所得税`, `印花税`, `付社保费`, `退税`, `往来款`, `捐款`, or `付6月员工工资`, reuse that convention.

If the source has only dates and no transaction times, match non-fee rows to the manual template using date, income/expense amount, balance, counterparty account/name/bank, and bank memo. Do not depend on transaction time for summary reuse.

## Validation

Before delivery:

- reconcile raw income / expense totals
- verify the output row count after fee aggregation
- confirm fee rows are grouped by date only
- confirm the source balance chain still holds, or list each unexplained gap
- compare visible detail totals to source total rows when a total row exists
- check for clipped columns or scientific notation on identifiers

If a row requires finance judgment that cannot be derived from the bank file alone, surface it in `处理校验` rather than guessing.
