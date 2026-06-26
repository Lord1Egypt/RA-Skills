# Metric Definitions

## Core Revenue Metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| 营业额 (Gross Revenue) | Sum of all transaction amounts | Include returns as negative |
| 净销售额 (Net Revenue) | Gross Revenue - Returns | Primary performance metric |
| 笔数 (Transaction Count) | Count of completed transactions | Exclude voided/cancelled |
| 客单价 (ATV) | Net Revenue / Transaction Count | Average transaction value |
| 退货率 (Return Rate) | Return Count / Transaction Count × 100% | Alert if > 10% |
| 目标完成率 (Target Completion) | Net Revenue / Daily Target × 100% | Requires target config |

## Time-Based Comparisons

| Comparison | Label | Formula |
|------------|-------|---------|
| DoD (Day over Day) | 昨日对比 | (Today - Yesterday) / Yesterday × 100% |
| WoW (Week over Week) | 上周对比 | (This week - Last week) / Last week × 100% |
| MoM (Month over Month) | 上月对比 | (This month - Last month) / Last month × 100% |
| YoY (Year over Year) | 去年同期对比 | (This period - Same period last year) / Last year × 100% |

## Anomaly Thresholds

| Metric | Alert Threshold | Direction |
|--------|----------------|-----------|
| Daily revenue vs. yesterday | > ±20% | Both |
| Category revenue vs. last week | > -30% | Down only |
| Return rate | > 10% | Up only |
| Zero-sale days for any SKU | > 3 consecutive days | Flag for review |
| ATV vs. last week | > ±15% | Both |

## Report Period Definitions

| Period Key | Start | End |
|------------|-------|-----|
| `today` | 00:00 today | Current time |
| `yesterday` | 00:00 yesterday | 23:59 yesterday |
| `this_week` | Monday 00:00 | Current time |
| `last_week` | Previous Monday 00:00 | Previous Sunday 23:59 |
| `this_month` | 1st of month 00:00 | Current time |
| `last_month` | 1st of last month | Last day of last month 23:59 |

## Display Formatting

| Value Type | Format |
|------------|--------|
| Revenue | ¥12,430（or ¥12.4k for > 10k） |
| Percentage | 83%（no decimals for display） |
| Delta positive | +¥1,200 ↑12% (green in rich clients) |
| Delta negative | -¥800 ↓8% (flag in report) |
| Target | 83% → "目标完成83%，距目标差¥2,570" |
