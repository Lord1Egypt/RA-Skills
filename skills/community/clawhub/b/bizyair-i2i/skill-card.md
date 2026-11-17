## Description:

BizyAir 图生图（Image-to-Image）助手。将本地图片上传后作为参考，使用 AI 生成新的图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to upload a selected local image to BizyAir, create an image-to-image generation task with a prompt and aspect ratio, and retrieve generated image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A selected local path may upload a sensitive or unintended readable file to external storage.

Mitigation: Use only non-sensitive images and verify the exact resolved file path before running the upload workflow.

Risk: Images and prompts are sent to BizyAir/Alibaba OSS for processing.

Mitigation: Run the skill only when that data sharing is acceptable for the user's content and environment.

Risk: Passing credentials on the command line can expose the BizyAir API key through shell history or process listings.

Mitigation: Prefer BIZYAIR_API_KEY or a secret store over the --api-key argument.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bozoyan/skills/bizyair-i2i)
- [BizyAir task creation API endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi/create)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BIZYAIR_API_KEY and uploads selected local images to BizyAir/Alibaba OSS before task creation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
