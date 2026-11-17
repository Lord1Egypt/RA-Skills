## Description:

Recognizes and extracts core fields from birth medical certificate images, including newborn details, birth information, parent information, medical institution details, and certificate identifiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to extract structured JSON data from birth medical certificates through the Scnet OCR service when they are authorized to process the document. It is limited to birth medical certificate OCR and is not intended for generic OCR or other identity-document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth medical certificate images contain highly sensitive personal and medical data and leave the local machine for Scnet OCR processing.

Mitigation: Use the skill only for documents the user is authorized to process, confirm consent before upload, and delete local images or cached copies after extracting the result.

Risk: The OCR service destination is configurable through SCNET_API_BASE, which can send documents or credentials to an unintended endpoint if changed.

Mitigation: Keep the default Scnet API base unless the alternative endpoint is fully trusted and verified before use.

Risk: API credentials may be stored in a plaintext .env file.

Mitigation: Prefer environment variables or a secret store, restrict any .env file to the local owner, and never paste API keys into chat transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/birth-medical-cert-ocr)
- [Sugon-Scnet OCR API documentation](references/api-docs.md)
- [Birth certificate output fields](assets/templates/fields-summary.md)
- [Scnet service site](https://www.scnet.cn)
- [Scnet OCR endpoint](https://api.scnet.cn/api/llm/v1/ocr/recognize)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON emitted by a Python CLI after an OCR API call, with setup and usage guidance in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The OCR result is returned from the service data payload with confidence fields removed by the local script.]

## Skill Version(s):

1.0.5 (source: server release metadata, SKILL.md frontmatter, skill.yaml, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
