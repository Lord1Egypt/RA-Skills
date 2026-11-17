## Description:

Perform bank reconciliation between bank statements and general ledger files, including bank statement PDF ingestion, structured Excel extraction, amount-threshold matching, ID/key matching, semantic description matching, and reconciliation workbook generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipmunkrpa](https://clawhub.ai/user/chipmunkrpa)

### License/Terms of Use:

MIT-0

## Use Case:

Accountants, finance teams, and agents supporting reconciliation workflows use this skill to compare bank statement rows with general ledger transactions, identify matched and unmatched items, and produce a reviewable Excel reconciliation workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads bank statement and general ledger files that may contain sensitive financial data and writes reconciliation workbooks containing that data.

Mitigation: Use trusted input files, choose a private output folder, and review access controls before sharing generated workbooks.

Risk: PDF input creates a companion extracted workbook beside the source PDF, which may duplicate sensitive transaction data.

Mitigation: Store PDF inputs in a private working directory and remove the extracted workbook when it is no longer needed.

Risk: Unsupported or unusually formatted PDFs, especially scanned-image statements, may produce incomplete extraction results.

Mitigation: Use digital text-based PDFs or validated Excel inputs, and have a finance reviewer inspect the Summary, Recon Results, Unreconciled Bank, and Unreconciled GL tabs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Analysis]

**Output Format:** [Excel workbook plus a concise text or Markdown reconciliation summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an additional extracted Excel workbook beside a PDF bank statement input.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
