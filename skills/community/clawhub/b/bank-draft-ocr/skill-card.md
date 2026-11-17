## Description:

Recognizes bank draft documents and extracts structured fields such as issue date, payee, paying bank, and draft amount.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External developers and operations teams use this skill to submit authorized bank-draft images, PDFs, or archives to the Scnet OCR API and receive structured JSON containing recognized draft fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads potentially sensitive bank-draft documents to a configurable external OCR endpoint.

Mitigation: Use only documents approved for that endpoint, and confirm organizational approval before processing financial documents.

Risk: A modified SCNET_API_BASE could redirect document uploads and API credentials to an untrusted destination.

Mitigation: Keep config/.env permissions restricted, verify the endpoint before use, and avoid changing SCNET_API_BASE unless the destination is trusted.

Risk: The skill requires an API credential to call Scnet OCR.

Mitigation: Store SCNET_API_KEY in a protected environment or config file and do not paste credentials into chats or logs.

## Reference(s):

- [Sugon-Scnet OCR API Documentation](references/api-docs.md)
- [Bank Draft Field Summary](assets/templates/fields-summary.md)
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/skills/bank-draft-ocr)
- [Scnet Website](https://www.scnet.cn)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Structured JSON returned on standard output, with human-readable error text on failure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and accepts optional SCNET_API_BASE; uploads the provided document file to the configured OCR endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.yaml, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
