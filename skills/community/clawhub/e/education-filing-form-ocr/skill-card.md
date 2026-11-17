## Description:

Recognizes online education certificate filing forms and extracts structured fields such as name, update date, enrollment date, ID number, institution, education category, and major.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to submit local image or PDF files of education certificate filing forms to the Scnet OCR service and receive structured JSON recognition results for downstream review or extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive education documents and an API token are sent to a configurable Scnet OCR endpoint.

Mitigation: Use the skill only when sending those documents to Scnet is acceptable, keep config/.env private, and change SCNET_API_BASE only to a fully trusted destination.

Risk: The skill depends on the external requests package and a remote OCR service.

Mitigation: Install dependencies in an isolated or pinned environment and review service behavior before processing sensitive records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/skills/education-filing-form-ocr)
- [Publisher Profile](https://clawhub.ai/user/scnet-sugon)
- [Sugon-Scnet OCR API Docs](artifact/references/api-docs.md)
- [Field Summary](artifact/assets/templates/fields-summary.md)
- [Scnet Website](https://www.scnet.cn)
- [Scnet OCR API Base](https://api.scnet.cn/api/llm/v1)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Structured JSON recognition results with text guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and accepts an ocrType plus local file path; API rate limit guidance recommends serial calls.]

## Skill Version(s):

1.0.0 (source: frontmatter and changelog, released 2025-05-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
