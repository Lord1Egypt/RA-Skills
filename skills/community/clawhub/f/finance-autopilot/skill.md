---
name: Finance Autopilot
description: A proactive personal finance manager for AI agents. Tracks income and expenses, monitors subscriptions and bills, detects unusual spending, builds monthly budget reports, reminds you of payment due dates, and helps you understand where your money goes every month. Designed for individuals and families who want financial clarity without using complex apps. No accounting knowledge required. Just forward your bills and receipts and talk naturally.
---

# Finance Autopilot

## Philosophy

Most people have a vague sense of their finances. They know roughly what comes in and roughly what goes out, but the details are fuzzy. Finance Autopilot eliminates that fuzziness. It turns your AI agent into a personal CFO that tracks every dollar, spots every problem, and gives you a clear picture of your financial life at any moment.

The core insight: financial stress is almost never caused by not earning enough. It is caused by not knowing exactly where the money goes. Clarity alone changes behavior.

---

## Trigger Map

| What you say | What happens |
|---|---|
| "How am I doing this month" | Monthly spending summary |
| "What bills are due" | Upcoming payment list |
| "I just spent X on Y" | Expense logged |
| "Forward a receipt or invoice" | Auto-parsed and categorized |
| "What did I spend on food this month" | Category breakdown |
| "Am I on track for my budget" | Budget vs actual report |
| "What subscriptions am I paying for" | Full subscription audit |
| "Help me save more" | Savings opportunity analysis |
| "What was my biggest expense last month" | Expense analysis |

---

## Module 1: Expense Tracking

Trigger: Forward any receipt, invoice, or billing email. Or say "I just spent X on Y."

**How it works**:
- The agent parses the amount, merchant, category, and date from any forwarded receipt or invoice
- Expenses are automatically categorized: Food, Transport, Housing, Utilities, Entertainment, Health, Shopping, Subscriptions, Business
- You can correct any categorization by saying "that was actually for work" or "put that under health"
- Cash expenses are logged when you say "I spent 50 on groceries just now"

**Smart categorization**:
- Learns your patterns over time
- Recognizes recurring merchants and auto-categorizes them
- Flags ambiguous expenses and asks for clarification once, then remembers

---

## Module 2: Monthly Budget Report

Trigger: "How am I doing this month", "Show me my budget", or automatically on the 1st of each month

**The report includes**:
- Total income received this month
- Total expenses by category with percentage of income
- Budget vs actual for each category you have set limits on
- Top 5 individual expenses this month
- Comparison to last month: what went up, what went down
- One clear observation about your biggest financial pattern this month

**Budget setting**:
- Say "my food budget is 5000 per month" to set any category limit
- The agent alerts you at 70% and 90% of any budget limit
- No spreadsheet or app required

---

## Module 3: Bill and Payment Calendar

Trigger: "What bills are due", "What do I need to pay this week", or every Monday morning automatically

**What the agent tracks**:
- All recurring bills: rent, utilities, insurance, loan payments
- Subscription renewals with exact amounts and dates
- One-time invoices you have forwarded
- Tax payment deadlines if you mention them

**Alert schedule**:
- Annual bills: reminded 30 days and 7 days before due
- Monthly bills: reminded 5 days before due
- Weekly bills: reminded 2 days before due
- Overdue payments: flagged immediately in morning briefing

**Never miss a payment again**:
- The agent surfaces due payments in your morning briefing automatically
- If you confirm payment, the item is marked paid and archived
- Unpaid items roll forward until resolved

---

## Module 4: Subscription Audit

Trigger: "What am I paying for", "Audit my subscriptions", "What can I cancel"

**What the audit produces**:
- Complete list of every subscription with amount and billing cycle
- Monthly equivalent cost for all annual subscriptions
- Total monthly subscription spend
- Subscriptions you have not mentioned using in the past 30 days flagged as potentially unused
- Duplicate services identified (two music apps, two cloud storage services)
- Estimated annual savings if flagged subscriptions are cancelled

**Price increase detection**:
- If a renewal amount is higher than the previous one, the agent flags it immediately
- Shows you the exact increase in dollars and percentage
- Suggests whether to cancel, negotiate, or accept

---

## Module 5: Unusual Spending Detection

Trigger: Automatic, runs after every expense is logged

**What triggers an alert**:
- A single purchase more than 3x your average for that category
- Total spending in any category exceeding your budget by 20% or more
- A charge from a merchant you have never used before above a threshold you set
- Two charges from the same merchant on the same day
- Any charge ending in unusual amounts that may indicate fraud patterns

**Alert format**:
- Surfaces in your next morning briefing or immediately if severe
- One sentence explanation of why it was flagged
- Asks you to confirm it is legitimate or investigate further

---

## Module 6: Savings Opportunity Analysis

Trigger: "Help me save more", "Where can I cut back", "I want to save X per month"

**How it works**:
- Reviews your last 3 months of tracked expenses
- Identifies the top 3 categories with the most variability month to month
- Suggests specific, realistic reductions based on your actual patterns
- Calculates exactly how much you would save annually from each suggestion
- Never suggests cutting things you spend consistently on — only targets irregular splurges

**Goal tracking**:
- Say "I want to save 10000 by December" and the agent calculates the monthly savings needed
- Tracks progress toward the goal every month
- Adjusts the target if your income or expenses change

---

## Module 7: Income Tracking

Trigger: "I got paid today", "I received a payment from X", forward any payment confirmation

**What is tracked**:
- Salary or regular income with expected vs actual amounts
- Freelance or irregular income logged separately
- Late payments flagged if expected income does not arrive within 3 days of expected date
- Year to date income summary available at any time

---

## Module 8: Annual Financial Review

Trigger: "How was my year financially", every January 1st automatically

**The review covers**:
- Total income for the year
- Total expenses by category for the year
- Net savings: income minus expenses
- Biggest single expense of the year
- Month with highest and lowest spending
- Subscription cost for the full year
- One honest assessment of the year's financial health
- 3 specific recommendations for the coming year based on patterns

---

## Who This Skill Is For

**Individuals** who want to know where their money goes without using complex budgeting apps.

**Families** managing shared expenses, bills, and household budgets across multiple income sources.

**Freelancers and self-employed people** who need to track irregular income and business expenses alongside personal finances.

**People with subscription overload** who have lost track of what they are paying for every month.

**Anyone who has tried budgeting apps** and stopped using them because manual data entry is too painful.

---

## What Makes This Different From Mint, YNAB, or Other Budgeting Apps

Budgeting apps require you to open the app, categorize transactions, review dashboards, and maintain the habit. Most people stop within 3 weeks.

Finance Autopilot requires nothing except forwarding receipts and speaking naturally. The agent comes to you every morning with what you need to know. You never have to open a dashboard or remember to check in.

---

## Privacy and Safety Boundaries

- The agent will never connect directly to your bank account unless you explicitly set up an integration
- The agent will never share your financial data with any external service
- All expense data stays within your agent's memory
- The agent will never make any payment or transfer on your behalf under any circumstances
- If you ask the agent to pay something, it will show you the details and ask you to make the payment yourself

---

## Setup

No technical setup required. Start by saying "my monthly income is X" and forward your first bill or receipt. The agent builds your financial picture from there.

Optional: tell the agent your budget limits for each category in the first conversation.
