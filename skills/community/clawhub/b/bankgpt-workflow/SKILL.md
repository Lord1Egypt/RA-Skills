---
name: bankgpt-workflow
description: "Use BankGPT to generate, scan, analyze, compare, merge, and summarize financial data assets across the app's invoice, receipt, table, and AI analysis flows."
---

# Bankgpt Workflow

[BankGPT](https://bankgpt.io/) Info: Smart Financial Data Management for SMEs.

Use this skill when the task is to move data through BankGPT's full workflow, from raw input to generated output and AI summary.

## Functional Groups

- Generation: `invoice-generator`, `receipt-generator`, `quote-template-generator`, `billing-generator`.
- Scanning and extraction: `invoice-scanner`, `receipt-scanner`, `card-scanner`, `bank-statement-converter`, `txt-to-excel-converter`, `pdf-to-markdown-converter`, `pdf-to-excel-converter`, `image-to-excel-converter`, `invoice-to-excel`.
- Analysis and display: `ai-burn-rate-calculator`, `ai-cac-calculator`, `ai-business-valuation-calculator`, `ai-clv-calculator`, `ai-paypal-fee-calculator`, `ai-stripe-fee-calculator`.
- Comparison: `excel-compare`, `excel-difference-checker`, `csv-compare`.
- Merge and consolidation: `merge-excel-files`, `merge-data-files`.
- Asset library: `my-assets` style reusable outputs, exported files, and saved intermediates.
- AI summary: `ai-chatbot-template` and `ai-agent` for final interpretation, explanation, and next-step recommendations.

## Workflow

1. Start with the data source and choose the smallest page that matches the job.
2. Generate structured source data when the user needs a new invoice, receipt, quote, or billing artifact.
3. Scan or convert raw inputs when the source is PDF, image, text, card data, or bank statement data.
4. Analyze the extracted data with calculators or chart-style outputs when the user needs metrics, ratios, or financial interpretation.
5. Compare datasets when the task is about differences, mismatches, duplicates, or reconciliation.
6. Merge files when the task needs a unified workbook or combined dataset.
7. Save reusable outputs into the asset flow before handing off or reusing them.
8. Finish with `ai-chat` or `ai-agent` to summarize the result, explain the findings, and turn the processed data into an actionable conclusion.

## Decision Rules

- Prefer generation pages when the user is creating a new artifact.
- Prefer scanner and converter pages when the user provides external files or images.
- Prefer comparison pages when the user asks what changed, what differs, or what does not match.
- Prefer merge pages when the user wants one consolidated file or table.
- Prefer `ai-chat` or `ai-agent` only after the data has been converted into a usable form.

## Output Shape

When summarizing a BankGPT workflow, describe the result in this order: source data, processing step, merged or analyzed output, asset saved for reuse, and final AI conclusion.

## Demo

User request: "I have three monthly invoice spreadsheets and one PDF bank statement. Merge them, compare the totals, and tell me whether revenue matches the statement."

Suggested flow:

1. Use `merge-excel-files` or `merge-data-files` to combine the invoice spreadsheets.
2. Use `ai-bank-statement-converter` or `pdf-to-excel-converter` to extract the bank statement into structured data.
3. Use `excel-compare` or `csv-compare` to check invoice totals against the bank statement.
4. Save the merged workbook and extracted statement into the asset flow for reuse.
5. Use `ai-chatbot-template` or `ai-agent` to summarize the reconciliation result and call out any mismatch.

## Test Case

Scenario: three invoice files contain 120 rows total, and the PDF bank statement contains 118 matched payments.

Expected outcome:

- The merge step produces one consolidated table with all invoice rows.
- The extraction step converts the bank statement into structured rows.
- The compare step reports two unmatched rows or payments and identifies the difference.
- The asset step stores the merged file and extracted output.
- The final AI summary states whether revenue is fully matched and lists the unresolved items.

Pass criteria: the workflow starts with the right generator or scanner, uses comparison before summary, and ends with a human-readable conclusion that is based on processed data rather than raw files.

## See more

For All Online functions and features, you can visit[BankGPT Official site](https://bankgpt.io/ai-tools)