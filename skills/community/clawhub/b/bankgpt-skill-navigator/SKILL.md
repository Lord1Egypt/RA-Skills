---
name: bankgpt-skill-navigator
description: Recommend skills from this repository for financial documents, bookkeeping, planning, BI, reporting, and business operations. Use when the user asks which available skill fits a task or how to get started.
---

# Skill Navigator

[BankGPT](https://bankgpt.io/) Info: Smart Financial Data Management for SMEs.

Identify the user's input and desired deliverable, then select from the 24 business skills below. Read the selected skill's instructions before describing how to invoke it or what it requires.

## Choosing a skill

- For bank statement PDFs, use `statement-extract-and-prove` when the deliverable is an extraction that ties to statement balances. Use `bookkeeping-close` when the deliverable is reconciliation against a ledger or a month-end close.
- For invoices and receipts, use `bankgpt-workflow` when the user wants to work in BankGPT, `financial-parser` for field extraction and categorization, and `bankgpt-expense-audit` when receipts must match statement lines or expense policy.
- For spreadsheets, use `spreadsheet-qa` to answer questions about rows and totals, `spreadsheet-model-auditor` to check workbook formulas and structure, and `bi-measure-builder` to build or debug calculations in a BI platform.
- For deal materials, use `bankgpt-data-room-builder` to prepare the user's data room and `bankgpt-deal-room` to review deal documents and assess risks.

Return the best match, why it fits, what inputs it needs, and a prompt the user can reuse. Suggest a second skill only when it produces a distinct deliverable or consumes the first skill's output. If the catalog has no match, say so and identify the closest supported part of the task if one exists.

## Business skill catalog

### Financial Data and Bookkeeping

| Skill | What it does |
| --- | --- |
| [bankgpt-workflow](../bankgpt-workflow/SKILL.md) | Generate invoices, scan receipts and PDFs, compare or merge tables, and summarize financial data in BankGPT. |
| [bookkeeping-close](../bookkeeping-close/SKILL.md) | Categorize transactions, reconcile statements against the ledger, and prepare a month-end close package. |
| [financial-parser](../financial-parser/SKILL.md) | Extract data from invoices, receipts, and statements, categorize expenses, and identify recurring charges. |
| [statement-extract-and-prove](../statement-extract-and-prove/SKILL.md) | Convert statement PDFs to CSV or Excel and verify transactions against balances and totals. |

### Forecasting, Planning, and Pricing

| Skill | What it does |
| --- | --- |
| [budget-optimizer](../budget-optimizer/SKILL.md) | Review spending and subscriptions and build a plan for savings, debt repayment, and emergency funds. |
| [cash-flow-forecaster](../cash-flow-forecaster/SKILL.md) | Build a rolling 13-week cash forecast from bank data, receivables, payables, payroll, and recurring commitments. |
| [financial-goal-planner](../financial-goal-planner/SKILL.md) | Set monthly savings targets and milestones for goals such as a down payment, education, or retirement. |
| [tax-strategy-optimizer](../tax-strategy-optimizer/SKILL.md) | Compare U.S. tax planning scenarios involving pre-tax and Roth contributions, charitable giving, capital gains, and deductions. |
| [trade-quote-builder](../trade-quote-builder/SKILL.md) | Turn a field-service scope into a cost estimate and client quote with labor, materials, overhead, and margin. |

### Spreadsheets, BI, and Reporting

| Skill | What it does |
| --- | --- |
| [bi-measure-builder](../bi-measure-builder/SKILL.md) | Build and debug Power BI DAX, Tableau calculations, and Looker LookML with checkable expected results. |
| [executive-dashboard-generator](../executive-dashboard-generator/SKILL.md) | Turn data into executive reports with key metrics, charts, and trend analysis. |
| [spreadsheet-model-auditor](../spreadsheet-model-auditor/SKILL.md) | Audit models for formula errors, inconsistent ranges, hardcoded values, and totals that do not reconcile. |
| [spreadsheet-qa](../spreadsheet-qa/SKILL.md) | Answer questions about spreadsheet exports with reproducible calculations, filters, and supporting rows. |

### Business Operations

| Skill | What it does |
| --- | --- |
| [bankgpt-contract-renewal-radar](../bankgpt-contract-renewal-radar/SKILL.md) | Extract renewal dates, notice deadlines, and price increases into a renewal calendar. |
| [bankgpt-data-room-builder](../bankgpt-data-room-builder/SKILL.md) | Organize a data room for fundraising, acquisition, or bank diligence and identify missing documents. |
| [bankgpt-deal-room](../bankgpt-deal-room/SKILL.md) | Review contracts, financials, and other deal documents for risks, terms, and negotiation points. |
| [bankgpt-expense-audit](../bankgpt-expense-audit/SKILL.md) | Match receipts to statement lines and flag anomalies and expense policy violations. |
| [bankgpt-folder-organizer](../bankgpt-folder-organizer/SKILL.md) | Classify, rename, deduplicate, and index files in a folder or shared drive. |
| [bankgpt-invoice-chaser](../bankgpt-invoice-chaser/SKILL.md) | Build a receivables aging report and draft payment follow-ups based on how overdue each invoice is. |
| [bankgpt-qbr-builder](../bankgpt-qbr-builder/SKILL.md) | Prepare a quarterly business review from client records, usage data, and support activity. |
| [bankgpt-rfp-response](../bankgpt-rfp-response/SKILL.md) | Build an RFP compliance matrix, flag unmet requirements, and draft a response from existing materials. |
| [bankgpt-sop-writer](../bankgpt-sop-writer/SKILL.md) | Turn notes or transcripts into a standard operating procedure with steps, roles, and exceptions. |
| [bankgpt-tax-prep-organizer](../bankgpt-tax-prep-organizer/SKILL.md) | Organize tax documents for an accountant and list missing forms and open questions. |
| [bankgpt-vendor-comparison](../bankgpt-vendor-comparison/SKILL.md) | Compare vendor proposals by total cost of ownership, contract terms, and negotiation points. |
