## Description:

Builds and operates a Feishu invoice approval bot that checks invoice details, flags tax risks, and requests the uploader's confirmation before submitting an approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaorui](https://clawhub.ai/user/wuhaorui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance teams use this skill to set up and maintain a Feishu bot that extracts invoice details, checks buyer and tax information, and prepares expense approvals for the original uploader to confirm.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted invoice images may cause the extraction agent to access unrelated files in the generated project.

Mitigation: Process each invoice in an isolated directory containing only its image and the extraction schema.

Risk: Testing or misconfiguration could create real approvals unintentionally.

Mitigation: Keep dry-run enabled during testing and require the original uploader's confirmation before live submission.

Risk: Anyone visible to the bot may be able to send invoices when no sender allowlist is configured.

Mitigation: Set a non-empty sender allowlist before production use.

Risk: Invoice images, extracted data, credentials, and audit records may contain sensitive information.

Mitigation: Restrict access and retention for invoice files, extracted JSON, environment files, and the SQLite database.

## Reference(s):

- [Feishu Invoice Approval release](https://clawhub.ai/wuhaorui/skills/automate-feishu-invoice-approval)
- [Setup reference](artifact/references/setup.md)
- [Operations reference](artifact/references/operations.md)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown guidance, shell commands, and generated Python project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run testing and an uploader confirmation step before live approval submission.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
