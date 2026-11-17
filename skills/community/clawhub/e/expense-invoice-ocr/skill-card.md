## Description:

Recognizes 19 common enterprise expense and invoice document types by uploading a user-approved local image or PDF to the Scnet remote OCR service and returning structured OCR results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Employees, finance operations teams, and agent developers use this skill to extract structured fields from local invoices, travel receipts, medical invoices, tax documents, and other expense paperwork after the user explicitly consents to upload the file to Scnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local invoices, receipts, travel documents, medical invoices, tax documents, and similar files may contain sensitive or regulated data and are uploaded to a third-party OCR service.

Mitigation: Use the skill only after explicit user consent for the specific file and only when the user or organization has approved sending that document to Scnet.

Risk: SCNET_API_BASE can be configured to send documents and the bearer token to an endpoint other than the documented Scnet service.

Mitigation: Keep SCNET_API_BASE set to the documented Scnet HTTPS endpoint unless the code is changed to enforce an approved allowlist.

Risk: The API key may be exposed if pasted into chat or shared in logs.

Mitigation: Store SCNET_API_KEY in the skill configuration or environment and avoid sharing the key in chat.

Risk: Automated or repeated calls could upload files without clear intent or exceed service rate limits.

Mitigation: Trigger only on an explicit request for a specific local file, require confirmation before upload, and process OCR requests serially.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/expense-invoice-ocr)
- [Scnet website](https://www.scnet.cn)
- [Scnet OCR API documentation summary](artifact/references/api-docs.md)
- [OCR field summary](artifact/assets/templates/fields-summary.md)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [JSON returned to stdout, with Markdown guidance and shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY; sends the selected local file and OCR type to a remote HTTPS OCR endpoint.]

## Skill Version(s):

1.0.8 (source: SKILL.md frontmatter, skill.yaml, ClawHub release metadata, CHANGELOG released 2026-08-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
