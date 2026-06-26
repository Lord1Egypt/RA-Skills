---
name: ar-collections-agent
description: Accounts Receivable (AR) collections workflow automation for accounting firms and finance teams. Use when you need to: (1) identify overdue invoices and aged AR buckets (30/60/90/120+ days), (2) draft escalating collection emails or call scripts, (3) generate AR aging reports and DSO calculations, (4) prioritize collection targets by balance and risk, (5) track payment promises and follow-up schedules, (6) calculate bad debt reserves or write-off recommendations, or (7) produce client-ready AR health dashboards. Works with QBO exports, CSV invoice data, or direct QBO API. NOT for: initiating legal action or filing liens (escalate to attorney), sending external emails without approval, accessing client QBO accounts without explicit write authorization, or PTIN-backed tax services.
---

# AR Collections Agent

Automate and systematize accounts receivable collections: aging analysis, prioritization, outreach drafts, DSO tracking, and bad debt analysis.

## Inputs Accepted

- QBO AR Aging Summary/Detail (CSV or PDF export)
- Invoice CSV: `invoice_id, customer, invoice_date, due_date, amount, amount_due, status`
- Direct QBO query results (via qbo-automation skill)
- Manually pasted invoice data

## Core Workflows

### 1. AR Aging Analysis

Bucket invoices into standard aging tiers:

| Bucket | Days Past Due |
|--------|--------------|
| Current | 0 |
| 1–30 | 1–30 |
| 31–60 | 31–60 |
| 61–90 | 61–90 |
| 91–120 | 91–120 |
| 120+ | 121+ |

Calculate per customer:
- Total AR balance
- Oldest invoice date
- % of balance in each bucket
- Days Sales Outstanding (DSO) = (AR Balance / Total Credit Sales) × Days in Period

Flag high-risk accounts: balance > $5k AND 60+ days past due, or any invoice 120+ days.

### 2. Prioritization Matrix

Score each overdue account (1–10):
- **Balance weight (40%):** Higher balance = higher score
- **Age weight (40%):** Older = higher score  
- **History weight (20%):** Prior payment promises broken = higher score

Output: ranked list, top 10 accounts to contact first.

### 3. Collection Outreach Drafts

Draft escalating messages based on aging tier. See `references/email-templates.md` for full templates.

**Tone ladder:**
- 1–30 days: Friendly reminder
- 31–60 days: Second notice, reference invoice
- 61–90 days: Firm request, payment plan offer
- 91–120 days: Final notice, escalation warning
- 120+ days: Collections/legal escalation notice

Always include: invoice numbers, amounts, due dates, payment link/instructions.

**Never send without Irfan's approval.** Draft only unless explicitly authorized.

### 4. DSO & KPI Dashboard

Calculate and report:
- **DSO** (overall and per customer segment)
- **Collection Effectiveness Index (CEI):** (Beginning AR + Credit Sales − Ending AR) / (Beginning AR + Credit Sales − Current AR) × 100
- **Bad Debt %:** Write-offs / Total Credit Sales × 100
- **% AR Current vs. Aged**

Output format: summary table + bullet insights for client presentation.

### 5. Bad Debt Reserve & Write-Off Analysis

Apply allowance method by aging bucket (customize per client):

| Bucket | Default Reserve % |
|--------|------------------|
| Current | 0.5% |
| 1–30 | 2% |
| 31–60 | 5% |
| 61–90 | 15% |
| 91–120 | 30% |
| 120+ | 50–100% |

Output: recommended reserve amount, GL journal entry draft, write-off candidates.

### 6. Payment Promise Tracker

When a customer commits to pay by a date:
1. Log: customer, amount, promise date, follow-up date (3 days before)
2. Flag broken promises for escalation tier bump
3. Output: follow-up schedule CSV or table

Save tracker state to `memory/ar-promise-tracker.md` if persistence requested.

## Output Formats

- **AR Aging Report:** Markdown table or CSV
- **Collection Priority List:** Ranked table with scores
- **Email Drafts:** Ready-to-send (with approval), parameterized per customer
- **DSO Dashboard:** Summary metrics + trend commentary
- **Bad Debt Schedule:** GL-ready journal entries
- **Follow-Up Schedule:** Date-indexed action list

## Reference Files

- `references/email-templates.md` — Full escalation email templates (all 5 tiers)
- `references/ar-kpi-formulas.md` — DSO, CEI, turnover ratio formulas with examples

## Guardrails

- **Read-only default:** Never modify QBO or send emails without explicit approval
- **No legal advice:** Flag 120+ day accounts for attorney review; do not draft demand letters
- **Client data isolation:** Never mix AR data across clients in the same analysis
- **Write-off authority:** Recommend only; write-off execution requires Irfan sign-off
- **PTIN boundary:** Bad debt tax deduction guidance requires PTIN-backed service; flag and refer
