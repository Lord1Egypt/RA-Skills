## Description:

Fapiao Clipper helps agents manage Chinese invoice workflows by scanning email and local folders, extracting invoice data with local PDF and OCR engines, validating invoices, and exporting reimbursement files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alan5168](https://clawhub.ai/user/alan5168)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, finance operators, and developers use this skill to collect, recognize, validate, query, and export Chinese fapiao records for reimbursement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials may be exposed or misused when email scanning is enabled.

Mitigation: Use a dedicated app password, keep configuration files private, and disable email scanning when it is not needed.

Risk: Automatic email-link following may download files from untrusted invoice links.

Mitigation: Disable automatic link following unless the mailbox sources are trusted, and review downloaded files before processing.

Risk: The Streamlit web UI may expose invoice data if published beyond a trusted local network.

Mitigation: Keep the UI local or behind authenticated private access, and do not expose it publicly without access controls.

Risk: Generated configuration, SQLite databases, and exports contain sensitive financial records.

Mitigation: Restrict filesystem permissions, protect backups, and handle exported Excel and PDF files as confidential business records.

## Reference(s):

- [Fapiao Clipper project homepage](https://github.com/Alan5168/fapiao-clipper)
- [Fapiao Clipper ClawHub page](https://clawhub.ai/alan5168/skills/fapiao-clipper)
- [Web UI preview](docs/web-ui-preview.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands; runtime outputs include SQLite records, Excel workbooks, and merged PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process email attachments, local invoice files, and exported financial records depending on configuration.]

## Skill Version(s):

1.5.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
