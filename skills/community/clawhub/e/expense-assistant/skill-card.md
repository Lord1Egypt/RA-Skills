## Description:

Expense Assistant helps users organize business entertainment and travel reimbursement materials by recognizing invoices and receipts, classifying expenses, generating reimbursement summaries, and preparing evidence filenames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esther-muye](https://clawhub.ai/user/esther-muye)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and finance-support agents use this skill to collect reimbursement evidence, separate business entertainment, travel, and transportation-subsidy documents, calculate reimbursement summaries, and prepare files for company reimbursement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial and reimbursement documents.

Mitigation: Use it only on intended reimbursement materials in a dedicated folder, and avoid mixing unrelated personal or business files into the working directory.

Risk: The included workflow can rename, move, and copy documents automatically.

Mitigation: Require a preview and explicit confirmation before file operations, sanitize generated filenames, and keep backups of original documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/esther-muye/skills/expense-assistant)
- [报销助手参考文档](references/数据结构.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown or plain text summaries with optional file operations and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rename, move, or copy reimbursement documents when the user authorizes file handling.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
