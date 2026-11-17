## Description:

Use CamScanner to add a tiled text watermark across an entire image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add repeated text watermarks such as confidential, draft, copyright, or custom notices to image files through CamScanner's image processing service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are uploaded to CamScanner's external service for processing.

Mitigation: Use the skill only for images appropriate for external processing, and avoid highly sensitive images unless CamScanner's privacy and retention terms have been reviewed and accepted.

Risk: RGBA PNG inputs with an alpha channel may fail in the upstream image processing service.

Mitigation: Convert affected PNG files to JPEG before uploading.

Risk: The download step returns JSON instead of the binary image if response_mode=raw is omitted.

Mitigation: Always include response_mode=raw on the download request.

Risk: A failed upload or watermark request can produce an empty or null file identifier.

Mitigation: Check each returned file_id before continuing to the next step.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/camscanner-ai/skills/camscanner-watermark-image)
- [CamScanner Publisher Profile](https://clawhub.ai/user/camscanner-ai)
- [CamScanner Website](https://www.camscanner.com)
- [CamScanner AI Tools API Base](https://ai-tools.camscanner.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown guidance with bash/curl commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for uploading an image, applying a tiled text watermark, and downloading the watermarked image.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
