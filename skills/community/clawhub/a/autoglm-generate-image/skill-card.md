## Description:

Generates an image from a user text prompt by calling the AutoGLM text-to-image API and returning the generated image URL for Markdown display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyfujian](https://clawhub.ai/user/flyfujian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate images from text prompts through AutoGLM and present the returned image URL as a Markdown image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and the locally obtained bearer token are sent to the AutoGLM API.

Mitigation: Use the skill only with prompts and credentials approved for AutoGLM processing, and review applicable data-handling requirements before deployment.

Risk: The artifact contains an embedded signing key used to create request headers.

Mitigation: Rotate or externalize the signing key and document key ownership and rotation before broad deployment.

Risk: The skill depends on a localhost token service.

Mitigation: Run the skill only in environments where the expected local token service is trusted, available, and scoped to the intended user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyfujian/skills/autoglm-generate-image)
- [Publisher profile](https://clawhub.ai/user/flyfujian)
- [AutoGLM image generation API endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown image link with a generated image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script also prints the raw AutoGLM JSON response before the agent extracts data.image_url.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
