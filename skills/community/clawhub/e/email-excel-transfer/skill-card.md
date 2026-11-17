## Description:

Automates retrieving data from email attachments and transferring it into Excel spreadsheets, defaulting to copy-based file updates so originals remain unchanged.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomasz-pedzierski-infinity](https://clawhub.ai/user/tomasz-pedzierski-infinity)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operators use this skill when they need an agent to extract spreadsheet data from email attachments, preview planned changes, and write approved updates into Excel copies. It is suited for mailbox-to-spreadsheet transfer workflows where originals should remain unchanged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles private mailbox data and reusable email credentials.

Mitigation: Use a dedicated low-privilege mailbox or OAuth token, and do not store real app passwords in source files.

Risk: Weak message or sender selection could read unintended email content.

Mitigation: Require the user to choose the account, message, and sender before reading mail, and make sender checks exact.

Risk: Email attachments can create unsafe file-handling exposure.

Mitigation: Save attachments in a private temporary directory, enforce size and file-type limits, and keep copy-first dry-run behavior before writing changes.

## Reference(s):

- [Email Excel Transfer on ClawHub](https://clawhub.ai/tomasz-pedzierski-infinity/skills/email-excel-transfer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes copy-first handling, dry-run preview guidance, app-password setup guidance, sender allowlisting, and attachment filename sanitization.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
