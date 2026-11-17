## Description:

DocuClaw extracts structured data from invoices, receipts, contracts, scans, photos, and emails into human-readable Markdown files with YAML metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[astonysh](https://clawhub.ai/user/astonysh)

### License/Terms of Use:


## Use Case:

Developers, operators, and document-heavy teams use DocuClaw to process invoices, receipts, contracts, mail, and other records into local Markdown archives for querying, archival workflows, expense tracking, and contract review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles potentially sensitive invoices, receipts, contracts, scans, photos, and emails.

Mitigation: Review privacy requirements before use and restrict processing to approved local storage and approved model providers.

Risk: The skill claims local-only processing while also describing OpenAI Vision and calendar or accounting integrations.

Mitigation: Use only local models and disable external sync when documents must remain on local hardware.

Risk: Calendar and accounting integrations can share extracted document data with third-party services.

Mitigation: Treat each integration as an outbound data path and enable only the integrations approved for the document sensitivity level.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown and YAML metadata guidance for document extraction and archival workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local model use, OpenAI Vision use, and calendar or accounting sync paths depending on deployment configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
