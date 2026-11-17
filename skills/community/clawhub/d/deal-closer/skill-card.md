## Description:

成交加速器 / Deal Closer is a Chinese-language CRM assistant for deal management, email signal extraction, pipeline analytics, follow-up drafting, sales learning, CRM relationship graphs, and IMAP/SMTP email workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjing5024064](https://clawhub.ai/user/hanjing5024064)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and sales operators use this skill to manage opportunities, scan mailbox signals, draft follow-up emails, log meetings, analyze pipeline health, and maintain CRM relationship context in Chinese-language workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read mailbox content and CRM records.

Mitigation: Install only where this access is acceptable, use least-privilege mailbox credentials or app passwords, and keep DC_DATA_DIR private.

Risk: The skill can draft and send outbound email.

Mitigation: Review every outbound email manually before sending.

Risk: Broad inbox scans or raw exports can expose sensitive sales or customer data.

Mitigation: Avoid broad scans and exports on sensitive accounts unless the data scope has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanjing5024064/skills/deal-closer)
- [Email service setup guide](artifact/references/email-setup-guide.md)
- [Sales pipeline report templates](artifact/references/pipeline-templates.md)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Azure Portal](https://portal.azure.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese-language Markdown and text responses with suggested Python shell commands, JSON command data, Mermaid snippets, and email draft content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON/CSV CRM records and email-related data under DC_DATA_DIR when the suggested commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
