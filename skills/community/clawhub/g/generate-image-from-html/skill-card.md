## Description:

Generate a PNG image from HTML content or a public URL using headless Chromium. Supports custom dimensions, retina quality, full-page screenshots, cookie consent handling, and dynamic parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to create screenshots or render HTML/CSS templates as PNG images for social cards, banners, certificates, thumbnails, and webpage previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML, CSS, dynamic parameters, or public webpage URLs sent for rendering may contain sensitive data or private endpoints.

Mitigation: Send only approved public content, remove secrets and personal data, and avoid internal URLs unless pdfapihub.com has been approved for that use.

Risk: Generated image files may remain available through the service for a retention period.

Mitigation: Avoid confidential rendering jobs when URL output is used and account for the documented automatic deletion window.

## Reference(s):

- [PDF API Hub documentation](https://pdfapihub.com/docs)
- [Generate Image API endpoint](https://pdfapihub.com/api/v1/generateImage)
- [ClawHub skill page](https://clawhub.ai/rishabhdugar/skills/generate-image-from-html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide API requests that return image URLs, base64 image data, or PNG image files.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
