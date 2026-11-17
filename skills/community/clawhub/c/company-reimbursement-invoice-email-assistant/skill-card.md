## Description:

公司报销发票邮箱管理助手 helps an agent process company reimbursement invoice emails by scanning IMAP mailbox messages, downloading invoice PDF/OFD attachments or links, extracting PDF invoice fields, generating ledgers and manual review tasks, and archiving invoice PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peter-zx](https://clawhub.ai/user/peter-zx)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, finance operations users, or local automation agents use this skill to process invoice-related mailbox messages for company reimbursement workflows. It produces reviewable invoice records, ledgers, manual task lists, and PDF archives while keeping formal finance, tax, audit, and legal decisions with human reviewers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles mailbox authorization codes and can read invoice-related email metadata, body excerpts, links, and attachments.

Mitigation: Use an application-specific mailbox authorization code, run the skill in a dedicated workspace or account, keep credentials local, and avoid sharing .env, scan-results, archive, or generated ledgers.

Risk: The artifact defaults IMAP_REJECT_UNAUTHORIZED to false, which can weaken TLS certificate validation.

Mitigation: Change IMAP_REJECT_UNAUTHORIZED to true before live use unless a reviewed local testing setup requires otherwise.

Risk: Invoice downloads and PDF/OFD parsing may process untrusted email links, attachments, and financial documents.

Mitigation: Review fetched links before downloading, avoid automatic processing of untrusted invoice emails, and manually review failures, high-value invoices, and abnormal records.

Risk: Generated ledgers and extracted invoice fields can be incorrect or incomplete and may expose sensitive business data.

Mitigation: Treat generated XLSX, CSV, JSON, HTML, and archive outputs as draft materials and require human review before reimbursement, accounting, tax, audit, or legal use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peter-zx/skills/company-reimbursement-invoice-email-assistant)
- [README](README.md)
- [Agent workflow](docs/AGENT_WORKFLOW.md)
- [Project design](docs/PROJECT_DESIGN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands plus generated HTML, XLSX, CSV, JSON, and archived PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include scan-results files, invoice ledgers, manual task lists, archive manifests, and local PDF archives containing sensitive business data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
