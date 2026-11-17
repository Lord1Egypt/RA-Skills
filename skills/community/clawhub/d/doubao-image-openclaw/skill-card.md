## Description:

Generates images from text prompts using Volcengine's Doubao image generation API, with configurable model, image size, output count, and URL-only output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanxing0724](https://clawhub.ai/user/wanxing0724)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to request Doubao image generation from an agent workflow, optionally choosing model, dimensions, number of images, and whether to save files or return only image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Volcengine's Doubao API and may include sensitive content if users enter it.

Mitigation: Avoid prompts containing secrets, credentials, regulated personal data, or other confidential information.

Risk: The skill reads VOLCENGINE_IMAGE_API_KEY from the environment.

Mitigation: Provide the API key only in trusted runtime environments and rotate it if exposure is suspected.

Risk: Downloaded image URLs are saved without validating redirects, file type, or download size.

Mitigation: Prefer the default workspace output directory and treat downloaded images as untrusted files until reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wanxing0724/skills/doubao-image-openclaw)
- [Volcengine Console](https://console.volces.com/)
- [Volcengine Doubao Image Generation API Endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Text, Files]

**Output Format:** [Console text with URL or file path markers, plus downloaded JPEG image files when URL-only mode is not used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VOLCENGINE_IMAGE_API_KEY. DOUBAO_IMAGE_OUTPUT_DIR can override the default workspace image output directory.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
