## Description:

Generates import-ready Chinese finance voucher and bank statement workbooks from monthly input VAT invoice exports or bank detail exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khanabdullha258974-dot](https://clawhub.ai/user/khanabdullha258974-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Finance operators, accountants, and developers use this skill to convert Chinese invoice exports or bank statement exports into accounting-reviewable Excel workbooks with voucher rows, account mappings, tax tables, and audit notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workbook rows may contain accounting assumptions that affect import accuracy, especially account mappings, red invoices, foreign-currency cases, and bank-fee aggregation.

Mitigation: Review the generated workbook before importing it into an accounting system, with special attention to rows marked for finance review and the account-mapping or check sheets.

Risk: Bank statement totals or balance chains can be incomplete when source rows are hidden, missing, or require finance judgment.

Mitigation: Use the generated check sheet to compare visible totals, source totals, differences, and affected dates before authorizing any manual补回 or classification.

## Reference(s):

- [Finance Voucher Workbook Workflow](references/workflow.md)
- [Bank Statement Workbook Workflow](references/bank_statement.md)
- [ClawHub Release Page](https://clawhub.ai/khanabdullha258974-dot/skills/china-finance-voucher)

## Skill Output:

**Output Type(s):** [files, markdown, guidance]

**Output Format:** [Excel workbook files with concise Markdown assumptions, audit notes, and finance-review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workbooks should preserve source sheets, stable columns, typed numbers, balanced voucher rows, and audit or check sheets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
