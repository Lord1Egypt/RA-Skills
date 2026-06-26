## Description: <br>
Supports asynchronous intelligent document OCR for batch processing by submitting a publicly accessible file URL and returning structured JSON with recognized text, tables, titles, and other document elements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and document-processing teams use this skill to submit public HTTP or HTTPS document URLs to Scnet OCR, poll for completion, and retrieve parsed JSON containing text, layout blocks, tables, images, seals, formulas, and Markdown content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided document URLs and retrieved OCR output through Scnet, which may expose sensitive or regulated document content to a third-party OCR service. <br>
Mitigation: Use short-lived, access-scoped public URLs without embedded secrets, and process confidential or regulated documents only after approval for third-party OCR processing. <br>
Risk: The skill requires SCNET_API_KEY and supports overriding SCNET_API_BASE, creating credential exposure or endpoint trust risk if configured carelessly. <br>
Mitigation: Protect SCNET_API_KEY outside chat transcripts and source control, restrict local configuration file permissions, and change SCNET_API_BASE only to a trusted endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/document-parse-ocr) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [Scnet OCR API docs](references/api-docs.md) <br>
- [Output fields summary](assets/templates/fields-summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON document parsing result with optional Markdown content embedded in the response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a public HTTP or HTTPS file URL and SCNET_API_KEY; task results are retrieved through asynchronous polling and temporary result download URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
