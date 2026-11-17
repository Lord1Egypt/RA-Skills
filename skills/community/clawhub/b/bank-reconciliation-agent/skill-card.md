## Description:

Automates bank statement reconciliation against general ledger records by matching transactions, flagging discrepancies, suggesting adjusting entries, and producing reconciliation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting and finance teams use this skill during month-end close to reconcile bank statements against GL exports, investigate discrepancies, and prepare reconciliation worksheets and adjusting entry suggestions for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial records that may contain account numbers, transaction details, and personal information.

Mitigation: Provide only the minimum financial data needed and redact full account numbers and personal information where possible.

Risk: Generated reconciliation reports may include fixed preparer, reviewer, or approval fields that could be mistaken for final audit workpapers.

Mitigation: Treat generated reports as drafts and replace or verify preparer, reviewer, approval, and sign-off fields before audit or close use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, CSV, JSON, guidance]

**Output Format:** [Markdown or plain text reconciliation report, with optional CSV or JSON structured export and journal entry templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reconciliation worksheets, match-status detail, discrepancy analysis, audit trail fields, and adjusting journal entry suggestions.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
