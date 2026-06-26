# Family Bookkeeping Reporting

Use this file for consistent reporting output.

## Supported Report Types

- Monthly total expense
- Monthly total income
- Monthly net balance
- Yearly total expense
- Yearly total income
- Yearly net balance
- Breakdown by `一级类型`
- Breakdown by `二级类型`
- Breakdown by `记账人`
- Breakdown by `支付平台`

## Output Pattern

Lead with the answer first, then show the breakdown.

Suggested compact structure:
1. 时间范围
2. 总支出
3. 总收入
4. 结余
5. Top categories
6. Optional member or platform breakdown

## Query Interpretation Notes

- `这个月花了多少` → monthly expense total
- `这个月收入多少` → monthly income total
- `今年花在哪些地方最多` → yearly category ranking
- `看看老婆 3 月花了多少` → filter by member + month
- `查一下支付宝本月支出` → filter by platform + month + expense

## Handling Ambiguity

If the date range is ambiguous:
- Infer common phrases like `这个月`, `上个月`, `今年`, `去年`
- If still ambiguous, ask one concise clarifying question

If the user asks for a deletion or edit while phrasing it like a query, prioritize the explicit action request.
