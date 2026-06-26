---
name: bill-manager
description: Manage daily bills, expenses, and recurring payments with tracking, reminders, and analysis. Use when the user asks about bill management, expense tracking, payment reminders, recurring payments, spending analysis, or wants to organize personal or household bills. This skill provides personal finance management assistance.
version: v1.0.0
tags: expense-tracking, bill-management, personal-finance
---

# Daily Bill Manager

## Usage Scenarios

### Scenario 1: Record a Daily Expense
**User input:** "I spent ¥50 on lunch today and ¥200 on groceries"
**Expected output:** The skill provides a structured recording template, categorizes the expenses (Food), and confirms the log with date, amount, and category.

### Scenario 2: Generate a Monthly Spending Analysis
**User input:** "Show me my spending breakdown for this month"
**Expected output:** The skill generates a monthly expense analysis including fixed/variable expense ratios, category breakdowns, trend comparison vs last month, and identifies abnormal expenses.

### Scenario 3: Set Up a Payment Reminder
**User input:** "Remind me about my rent payment of ¥5000 due on the 1st of each month"
**Expected output:** The skill provides a reminder schedule entry with 3-5 days advance notice, priority level (High for rent), and suggests the best reminder method.
### Scenario 4: 水电气网费每个月乱七八糟的
**User input:** "家里的水电气网费还有物业费每个月都是家里人谁想起谁交，经常忘交被罚款，有没有办法统一管理？"
**Expected output:** 提供家庭账单统一管理方案：1）汇总所有账单（水、电、燃气、宽带、物业、租房/房贷、车位等）及缴费周期和金额；2）建议使用支付宝'生活缴费'功能或微信的'生活缴费'统一管理可线上支付的账单；3）设置日历提醒（iOS日历/飞书日历/微信提醒）在每个账单到期前3天通知。推荐使用鲨鱼记账的账单管理功能或随手记。

## Overview

This skill helps users manage daily bills, track expenses, and organize recurring payments. It provides a systematic approach to personal and household financial management, including bill tracking, payment reminders, expense categorization, and spending analysis.

## When to Use This Skill

- Tracking monthly bills and recurring payments
- Setting up payment reminders
- Categorizing and analyzing expenses
- Managing household budgets
- Recording daily expenditures
- Planning for upcoming payments
- Reviewing spending patterns

## Limitations

- Provides **organizational guidance and templates only**
- Does not connect to actual bank accounts or payment systems
- Does not make actual payments
- Requires manual data entry
- Not a substitute for professional financial advice

## Bill Categories

### 1. Fixed Monthly Bills

| Category | Examples | Typical Due Date |
|----------|----------|------------------|
| Housing | Rent, mortgage, property fees | Monthly fixed |
| Utilities | Electricity, water, gas | Monthly variable |
| Communications | Phone, internet, TV | Monthly fixed |
| Insurance | Health, life, property | Monthly/quarterly/annual |
| Subscriptions | Streaming, software, memberships | Monthly/annual |

### 2. Variable Expenses

| Category | Examples | Tracking Method |
|----------|----------|-----------------|
| Food | Groceries, dining out | Daily recording |
| Transportation | Fuel, public transit, parking | Per use |
| Shopping | Clothing, electronics, household | Per purchase |
| Entertainment | Movies, events, hobbies | Per activity |
| Healthcare | Medical visits, pharmacy | Per visit |
| Education | Tuition, courses, books | Per term |

### 3. Periodic/Annual Bills

| Category | Examples | Frequency |
|----------|----------|-----------|
| Vehicle | Insurance, registration, maintenance | Annual/semi-annual |
| Home | Property tax, HOA fees | Annual/quarterly |
| Professional | Licenses, certifications | Annual |
| Gifts/Holidays | Holiday spending, gifts | Annual/events |

## Workflow

1. **Setup categories** — Define bill categories based on personal situation
2. **Record bills** — Log each bill with amount, due date, and category
3. **Set reminders** — Configure alerts for upcoming due dates
4. **Track payments** — Mark bills as paid and record payment method
5. **Review regularly** — Analyze spending patterns monthly/quarterly
6. **Optimize** — Identify savings opportunities and adjust budget

## Bill Recording Template

### Basic Bill Record

```
Bill Record

Bill Name: [Name]
Category: [Fixed/Variable/Periodic]
Amount: $[Amount]
Frequency: [Monthly/Quarterly/Annual/One-time]
Due Date: [Day X of month/Specific date]
Payment Method: [Auto-debit/Manual/Cash]
Payee: [Recipient]

Notes: [Additional info]
```

### Monthly Bill Summary

```
Monthly Bill Summary - [Month Year]

[Fixed Expenses]
1. [Item 1]: $[Amount] Status: [Paid/Pending]
2. [Item 2]: $[Amount] Status: [Paid/Pending]
...
Fixed Expenses Total: $[Amount]

[Variable Expenses]
1. [Category 1]: $[Amount]
2. [Category 2]: $[Amount]
...
Variable Expenses Total: $[Amount]

[Total Monthly Expenses]
$[Amount]

[Budget Comparison]
Budget: $[Amount]
Actual: $[Amount]
Difference: $[Amount] [Over/Under]
```

## Reminder Setup

### Reminder Schedule

| Bill Type | Reminder Timing | Method |
|-----------|-----------------|--------|
| Fixed monthly | 3-5 days before due | Calendar/Note |
| Variable expenses | Weekly review | Checklist |
| Annual bills | 1 month before | Calendar alert |
| Credit cards | 7-10 days before due | Calendar/Note |

### Priority Levels

- **High**: Housing, utilities, insurance (essential services)
- **Medium**: Subscriptions, memberships
- **Low**: Discretionary spending

## Expense Analysis

### Monthly Analysis Framework

```
Monthly Expense Analysis - [Month Year]

I. Expense Structure
Fixed expenses ratio: [X]%
Variable expenses ratio: [Y]%
Savings rate: [Z]%

II. Category Analysis
1. Housing: $[Amount] ([X]%)
2. Food: $[Amount] ([X]%)
3. Transportation: $[Amount] ([X]%)
4. Communications: $[Amount] ([X]%)
5. Others: $[Amount] ([X]%)

III. Trend Comparison
vs. last month: [Increase/Decrease] $[Amount]/[X]%
vs. same month last year: [Increase/Decrease] $[Amount]/[X]%

IV. Abnormal Expenses
[List items that exceeded budget or were unusual]

V. Next Month Budget Recommendations
[Recommendations based on analysis]
```

### Annual Review Framework

```
Annual Bill Review - [Year]

I. Annual Total Expenses: $[Amount]
II. Monthly Average: $[Amount]

III. Annual Category Summary
[Annual totals and ratios by category]

IV. Large Expense Records
[Items exceeding $X]

V. Subscription Service Audit
[List all subscriptions and annual costs]

VI. Annual Financial Goal Achievement
[Savings goals, debt repayment, etc.]

VII. Next Year Budget Planning
[Next year's budget based on current year data]
```

## Usage

### Basic Recording
```
"Record an expense"
"Log today's bill"
"Help me track my spending"
```

### Bill Management
```
"Manage monthly bills"
"Set up bill reminders"
"View pending bills"
```

### Analysis
```
"Analyze this month's expenses"
"View spending statistics"
"Bill analysis report"
```

### Budget Planning
```
"Create next month's budget"
"Budget planning advice"
"How to save money"
```

## Output Format

The skill provides:
- **Recording templates** for different bill types
- **Reminder schedules** customized to bill cycles
- **Analysis reports** showing spending patterns
- **Budget recommendations** based on historical data
- **Optimization suggestions** for cost savings

## Best Practices

### Recording Habits

1. **Daily recording** — Log expenses daily while memory is fresh
2. **Keep receipts** — Save receipts for reference and verification
3. **Use categories consistently** — Maintain consistent categorization
4. **Note details** — Record what, when, where, and why
5. **Review weekly** — Check for missing entries weekly

### Budget Management

1. **Set realistic budgets** — Based on historical spending
2. **Build emergency fund** — 3-6 months expenses
3. **Track subscriptions** — Regularly audit recurring charges
4. **Plan for irregular bills** — Set aside monthly for annual bills
5. **Review and adjust** — Monthly budget reviews

### Cost Optimization

1. **Negotiate bills** — Contact providers for better rates
2. **Bundle services** — Combine for discounts
3. **Cancel unused subscriptions** — Regular audits
4. **Use autopay discounts** — Where available
5. **Time purchases** — Take advantage of sales

## Bill Management Checklist

### Daily
- [ ] Record day's expenses
- [ ] Check for receipts to log

### Weekly
- [ ] Review week's spending
- [ ] Update bill tracking
- [ ] Check upcoming due dates

### Monthly
- [ ] Pay all bills due
- [ ] Review monthly spending
- [ ] Compare to budget
- [ ] Plan next month's budget
- [ ] Check subscription services

### Quarterly
- [ ] Review spending trends
- [ ] Adjust budget categories
- [ ] Evaluate savings progress
- [ ] Check insurance rates

### Annually
- [ ] Complete annual spending review
- [ ] Plan next year's budget
- [ ] Audit all subscriptions
- [ ] Review insurance policies
- [ ] Set annual financial goals

## References

For detailed templates and tracking methods:
- [references/bill-templates.md](references/bill-templates.md) — Bill recording templates
- [references/expense-categories.md](references/expense-categories.md) — Expense categorization guide
- [references/budget-planning.md](references/budget-planning.md) — Budget planning frameworks

## Privacy Note

Bill information is processed for management purposes only. No financial data is stored or transmitted to third parties. Users maintain full control over their data.

## Disclaimer

This tool provides personal finance organization assistance only. It does not constitute financial advice. For investment decisions, debt management strategies, or complex financial planning, consult a qualified financial advisor.
