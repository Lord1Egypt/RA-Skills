## Description:

Use CamScanner to remove watermarks, stamps, and translucent logos from PDF documents while preserving the underlying text, images, and original layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide PDF watermark removal through CamScanner's hosted API when they need a clean local output PDF for sharing, printing, OCR, or further processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected PDF files are sent to CamScanner's servers for processing.

Mitigation: Install and use only when users are comfortable with the service handling the selected PDFs.

Risk: Confidential, regulated, or third-party-owned documents may carry privacy, compliance, or permission concerns.

Mitigation: Avoid using the skill for those documents unless the user has permission and accepts CamScanner's data handling claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/camscanner-ai/skills/camscanner-pdf-remove-watermark)
- [CamScanner homepage](https://www.camscanner.com)
- [CamScanner AI tools API base](https://ai-tools.camscanner.com)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Files, Guidance]

**Output Format:** [Markdown with bash and JSON examples; the processed output is a PDF file or raw PDF byte stream.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; sends the selected PDF to CamScanner servers for processing.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version: 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
