## Description:

CamScanner Erase Handwriting helps agents remove handwritten strokes, annotations, and signatures from document images while preserving printed content and layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to clean scans or photos of documents by sending a selected image to CamScanner for handwriting removal and saving the processed image locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected document images are sent to CamScanner's third-party service for processing.

Mitigation: Use only when third-party processing is acceptable; avoid highly sensitive medical, legal, financial, identity, or confidential business documents unless approved.

Risk: The processed image is saved to a local filesystem path selected by the user.

Mitigation: Review the destination path before execution and avoid overwriting important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/camscanner-ai/skills/camscanner-image-erase-handwriting)
- [CamScanner homepage](https://www.camscanner.com)
- [CamScanner AI tools API base URL](https://ai-tools.camscanner.com)

## Skill Output:

**Output Type(s):** [shell commands, guidance, files]

**Output Format:** [Markdown guidance with bash and JSON examples; processed output is a JPG image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; sends selected images to CamScanner's service and saves output locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
