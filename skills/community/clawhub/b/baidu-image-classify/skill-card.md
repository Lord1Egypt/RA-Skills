## Description:

Recognizes objects, products, and scenes in images using Baidu image-classification APIs and returns labels, product details, or scene tags with confidence scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maple-8899](https://clawhub.ai/user/maple-8899)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to classify supplied images, identify products, and detect scenes through Baidu image-recognition endpoints. It is useful when an agent needs concise labels, confidence scores, or product and scene metadata from user-provided images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user-provided images to Baidu Cloud for recognition.

Mitigation: Confirm that the image data is appropriate to share with Baidu Cloud before use and apply organization-approved data handling controls.

Risk: The examples can fetch arbitrary remote image URLs.

Mitigation: Restrict remote inputs to validated public HTTPS image URLs and enforce timeouts, size limits, and content checks.

Risk: The examples handle API credentials unsafely, including inline credential placeholders and access tokens in URLs.

Mitigation: Move credentials to protected configuration and avoid placing tokens in URLs where the API supports safer handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maple-8899/skills/baidu-image-classify)
- [Baidu advanced general image classification endpoint](https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general)
- [Baidu product recognition endpoint](https://aip.baidubce.com/rest/2.0/image-classify/v2/shopping)
- [Baidu scene recognition endpoint](https://aip.baidubce.com/rest/2.0/image-classify/v2/scene)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Guidance]

**Output Format:** [Markdown with Python examples and JSON result structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires image input via local path or URL; examples expect JPG, PNG, or BMP images under 4 MB.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
