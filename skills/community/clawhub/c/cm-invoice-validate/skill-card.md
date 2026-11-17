## Description:

当用户需要查验发票真伪时使用，支持从发票信息或发票文件调用 ClawMate 接口完成查验。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijianhu1](https://clawhub.ai/user/lijianhu1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to validate invoice authenticity by supplying invoice identifiers or approved local invoice files, then reviewing structured pass/fail results and invoice details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice data, invoice files, and the API key may be sent to network destinations selected through configurable inputs.

Mitigation: Use the default ClawMate endpoint, restrict who can set file paths or API URLs, and avoid --api-url and --file-base64 with real data unless the destination is trusted.

Risk: Saved Markdown reports can contain sensitive invoice fields.

Mitigation: Review generated report files before sharing and store them only in approved locations.

Risk: The documented update path downloads and unpacks a release without a verified checksum or signature.

Mitigation: Do not run update commands unless the publisher provides a verified checksum or signed release.

Risk: The published Python script may not run as-is because the security evidence reports a syntax issue at the SKILL_CODE assignment.

Mitigation: Validate the script in a test environment before using it for production invoice checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijianhu1/skills/cm-invoice-validate)
- [ClawMate Invoice Validate API](https://www.clawmate.net/server/test/Api/InvoiceValidate)
- [ClawMate API key page](https://www.clawmate.net/user)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, JSON]

**Output Format:** [Markdown with optional JSON API responses and saved Markdown batch reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include invoice validation status, invoice fields, error explanations, and batch summaries.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact version text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
