## Description:

Extracts structured fields from general machine-printed invoice files using the Sugon-Scnet OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send local invoice images, PDFs, or supported archives to Scnet OCR and receive structured invoice fields for review or downstream automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice files may contain sensitive personal, banking, tax, or business data and are uploaded to an external OCR API.

Mitigation: Use the skill only with approval from the data owner and only where the Scnet OCR service is acceptable for the document sensitivity.

Risk: SCNET_API_BASE is configurable, so a changed endpoint could receive both invoice files and the API token.

Mitigation: Use the official Scnet endpoint unless the alternate endpoint is fully controlled and trusted.

Risk: The SCNET_API_KEY credential could be exposed if pasted into chat or stored with broad file permissions.

Mitigation: Provide the key through an environment variable or a local .env file with restricted permissions, and do not paste the key into conversations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/general-print-invoice-ocr)
- [Scnet website](https://www.scnet.cn)
- [Sugon-Scnet OCR API docs](references/api-docs.md)
- [Invoice fields summary](assets/templates/fields-summary.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON OCR results on stdout with plain-text setup and error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY; accepts GENERAL_MACHINE_INVOICE and a local file path.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
