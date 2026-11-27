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
| Close the books from statement PDFs | [statement-extract-and-prove](https://clawhub.ai/bankgpt/skills/statement-extract-and-prove) produces a verified transaction CSV and statement balances for [bookkeeping-close](https://clawhub.ai/bankgpt/skills/bookkeeping-close). Supply the ledger or accounting export for reconciliation. |
| Build a 13-week cash forecast from statement PDFs | [statement-extract-and-prove](https://clawhub.ai/bankgpt/skills/statement-extract-and-prove) produces verified bank transaction history for [cash-flow-forecaster](https://clawhub.ai/bankgpt/skills/cash-flow-forecaster). Supply current account balances, open receivables and payables, and scheduled outflows. |
| Build a household budget from statements and receipts | [financial-parser](https://clawhub.ai/bankgpt/skills/financial-parser) extracts and categorizes spending. Remove duplicate entries where receipts match statement transactions, then pass monthly category totals and take-home income to [budget-optimizer](https://clawhub.ai/bankgpt/skills/budget-optimizer). |
| Turn a household budget into a savings plan | [budget-optimizer](https://clawhub.ai/bankgpt/skills/budget-optimizer) identifies possible monthly savings. Pass the amount the user can commit each month, current savings, and target amount to [financial-goal-planner](https://clawhub.ai/bankgpt/skills/financial-goal-planner) to estimate a timeline. |
