## Description:

Recognizes bank drafts, checks, receipts, invoices, customs declarations, and other financial documents with Scnet OCR, returning structured key fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to submit local financial document images, PDFs, or supported archives to Scnet OCR and extract structured fields for downstream finance-document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial documents can be uploaded to a remote OCR service.

Mitigation: Install only where external processing by Scnet is approved, and avoid regulated or highly confidential documents unless that processing is authorized.

Risk: The configured API token can be sent to a configurable network endpoint.

Mitigation: Keep SCNET_API_BASE pinned to the documented HTTPS endpoint and use a limited Scnet API token.

Risk: Weak file and destination scoping can cause unintended document upload.

Mitigation: Confirm the exact local file path and OCR type before each upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/financial-bill-ocr)
- [Sugon-Scnet OCR API documentation summary](references/api-docs.md)
- [Recognized field summary](assets/templates/fields-summary.md)
- [Scnet service homepage](https://www.scnet.cn)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON printed to standard output, with errors returned as text messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ocrType and filePath; the selected local file is uploaded to Scnet's OCR service for recognition.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, skill.yaml, changelog released 2026-08-12, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
