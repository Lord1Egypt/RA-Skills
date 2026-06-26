---
name: report-generator
description: >
  Automated sales and performance report generator for retail store managers.
  Generates daily, weekly, and monthly reports from POS/ERP data.
  Highlights anomalies, tracks targets, and delivers reports via configured channels.
  Use when a store manager asks for: 今天的销售, 日报, 周报, 月报, 销售额,
  业绩怎么样, 完成率, 数据怎么样, daily report, sales summary, performance report,
  how did we do today, weekly summary, monthly review.
  Also triggers for scheduled automatic report delivery.
metadata:
  openclaw:
    emoji: 📊
---

# Report Generator

## Overview

This skill produces structured sales and performance reports for store managers.
Reports are data-first, anomaly-aware, and always include a recommended action.

**Depends on:** POS/ERP data connection configured in `report_config` (Step 05).
If no data source is connected: return empty report with setup guidance.

---

## Report Types

| Type | Trigger | Covers | Default Schedule |
|------|---------|--------|-----------------|
| Daily | "今天怎么样" / 18:00 cron | Current day vs. yesterday | Daily 18:00 |
| Weekly | "本周报告" / Monday 09:00 | Mon–Sun vs. prior week | Monday 09:00 |
| Monthly | "月报" / 1st of month | Full month vs. prior month | 1st @ 09:00 |
| On-demand | Any data question | Specified time range | — |

---

## Report Structure

Every report follows this 5-section format:

### Section 1: Headline Numbers
The top 3 KPIs the manager cares about most:
- Total revenue (实际 vs 目标, percentage completion)
- Transaction count
- Average transaction value

### Section 2: Product Performance
- Top 5 best-selling SKUs (by revenue)
- Any items with zero sales (flag if > 3 days)
- Low stock warnings (pull from inventory data if available)

### Section 3: Anomalies & Alerts
Auto-detect and flag:
- Revenue > 20% above/below yesterday → flag
- A category drops > 30% vs. prior period → flag
- Escalation rate spike → flag
- Unusual peak/valley in hourly distribution → note

### Section 4: Staff Performance (if data available)
- Transactions per staff member
- Average ticket per staff
- (Never names individuals negatively in customer-facing channels)

### Section 5: Recommended Actions
1–3 specific, actionable items the manager should do today/this week.
Examples: "补货SKU001（库存仅剩3件）", "关注女装区下午时段表现"

---

## Data Source Integration

Pull data from configured sources in `report_config`:

| Source | Data Retrieved |
|--------|---------------|
| POS API | Transactions, revenue, returns by time period |
| ERP API | Inventory levels, restock status |
| Manual input | If no API: manager pastes today's numbers |

If partial data: generate report with available data, mark missing sections clearly.

**Reference:** [data-connectors.md](references/data-connectors.md)

---

## Delivery

After generating, deliver via configured channel:
- `report_config.delivery_channel` (wecom / telegram / etc.)
- `report_config.recipients` (manager IDs)

Format for channel:
- WeCom: Use card format with emoji headers for scannability
- Text channels: Markdown tables

---

## On-Demand Queries

For ad-hoc questions like "上周卖得最好的是什么？":
1. Identify time range and metric from the question
2. Query data source
3. Use `scripts/generate_report.py --period custom --start X --end Y --metric top_products`
4. Present inline (no delivery to channel)

**Reference:** [metric-definitions.md](references/metric-definitions.md) — standard metric formulas.
