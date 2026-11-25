---
name: bankgpt-skill-composer
description: Compose multi-step workflows using the 24 business skills in this repository. Use when a financial or operations task needs multiple skills with explicit inputs, outputs, and handoffs.
---

# Skill Composer Studio

[BankGPT](https://bankgpt.io/) Info: Smart Financial Data Management for SMEs.

Use the [business skill catalog](../bankgpt-skill-navigator/SKILL.md#business-skill-catalog) as the source of eligible steps and their categories. Open the instructions for each selected skill to confirm that the inputs, outputs, and host requirements match.

## Build the workflow

1. Identify the available inputs and final deliverable. Use one skill when it can complete the task.
2. Order the steps by dependency. For each step, give the skill name, input, output, and any transformation needed before the next step. Preserve source rows or document references when they are needed to verify a result.
3. Add a decision or validation gate where it changes the workflow. For example, pause a reconciliation handoff if an extracted statement fails its balance check and carry forward the mismatch details for review.
4. When the user requests execution, use the available tools within the authorized scope and report completed steps, outputs, and blockers. For a design request, return the workflow and the conditions needed to run it.

## Example combinations

| Goal | Workflow and handoff |
| --- | --- |
| Close the books from statement PDFs | `statement-extract-and-prove` produces verified transaction rows for `bookkeeping-close`. Supply the ledger or accounting export separately for reconciliation. |
| Build a leadership report from spreadsheet exports | `spreadsheet-qa` produces checked metrics and definitions for `executive-dashboard-generator`. Add `bi-measure-builder` when the metrics also need to run in Power BI, Tableau, or Looker. |
| Track overdue invoices and their cash impact | `bankgpt-invoice-chaser` produces an aging report and draft follow-ups. Pass the aging report and expected collection dates to `cash-flow-forecaster` along with bank balances and planned outflows. |
| Prepare expense records for an accountant | `bankgpt-expense-audit` produces matched expenses and exceptions. Pass the report, source documents, and unresolved items to `bankgpt-tax-prep-organizer` for the document package. |
