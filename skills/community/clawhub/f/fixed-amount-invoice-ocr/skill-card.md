## Description:

Recognizes fixed-amount invoices by sending a local image, PDF, or archive to the Sugon-Scnet OCR API and returning structured JSON fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to extract key fields from fixed-amount invoice files through the SCNet OCR service. It is suited for agents that need invoice OCR results as structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload any readable local file to the configured OCR endpoint.

Mitigation: Use it only with approved invoice files and do not submit unrelated or highly sensitive documents unless the organization approves that data flow.

Risk: The API credential is sent to a configurable remote endpoint.

Mitigation: Keep SCNET_API_BASE fixed to the trusted SCNet HTTPS endpoint and store SCNET_API_KEY in environment or local configuration rather than chat.

Risk: The security verdict is suspicious because remote upload behavior is broad for a file-based OCR skill.

Mitigation: Review the skill and scan results before deployment, and restrict operational use to the intended fixed-amount invoice OCR workflow.

## Reference(s):

- [Sugon-Scnet OCR API docs](references/api-docs.md)
- [Fixed-amount invoice fields](assets/templates/fields-summary.md)
- [SCNet website](https://www.scnet.cn)
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/fixed-amount-invoice-ocr)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The JSON contains OCR response data for the submitted invoice file; errors are emitted as human-readable command-line messages.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
