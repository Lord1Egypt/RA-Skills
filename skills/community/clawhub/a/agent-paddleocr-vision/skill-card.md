## Description:

Multi-language document understanding with PaddleOCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nhzallen](https://clawhub.ai/user/nhzallen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route documents through a PaddleOCR cloud endpoint for OCR extraction, document classification, action suggestions, batch processing, and searchable PDF generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents are sent to a third-party PaddleOCR cloud endpoint.

Mitigation: Use only documents approved for that provider and token, and avoid highly sensitive identity, financial, legal, or tax documents unless the provider's retention, logging, and privacy terms are acceptable.

Risk: The package evidence did not include the referenced scripts or requirements files for local review.

Mitigation: Verify the complete source files and dependencies before running installation or document-processing commands.

## Reference(s):

- [Server-resolved source repository](https://github.com/NHZallen/agent-paddleocr-vision)
- [ClawHub skill page](https://clawhub.ai/nhzallen/skills/agent-paddleocr-vision)
- [Publisher profile](https://clawhub.ai/user/nhzallen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured OCR/action outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PaddleOCR document parsing endpoint URL and access token; may produce searchable PDF files when the supporting runtime is present.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
