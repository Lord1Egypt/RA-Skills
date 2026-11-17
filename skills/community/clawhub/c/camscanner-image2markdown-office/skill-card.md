## Description:

Converts images such as PNG and JPG into structured Markdown using CamScanner's OCR and document parsing service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert screenshots, photos, and scanned documents into Markdown before analysis or response generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images may contain sensitive personal, financial, business, health, or source-code information and are sent to CamScanner servers for OCR.

Mitigation: Use the skill only when third-party OCR processing is intended; redact or crop sensitive regions before upload.

Risk: The skill can process image-bearing requests without a built-in explicit consent checkpoint.

Mitigation: Confirm that the user wants the image sent to CamScanner before running the upload and conversion commands.

Risk: The workflow depends on remote API responses and local curl and jq binaries.

Mitigation: Verify curl and jq are available, check each returned file_id before proceeding, and fail closed if upload or conversion returns null.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/camscanner-ai/skills/camscanner-image2markdown-office)
- [CamScanner homepage](https://www.camscanner.com)
- [CamScanner image conversion API base URL](https://ai-tools.camscanner.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline bash commands that call a remote OCR service and save a local .md result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; sends input images to CamScanner servers for processing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
