## Description:

Generates product images in the style of high-performing reference images by calling the Flyelep image-generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce teams, creators, and agents use this skill to provide product assets, reference images, and generation settings, then receive generated product image URLs from Flyelep.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local images may be uploaded to permanent public URLs without a clear consent or deletion flow.

Mitigation: Use only images the user is comfortable sending to Flyelep and potentially exposing through permanent public URLs; avoid confidential, personal, regulated, unreleased, or proprietary images unless the user explicitly accepts that transfer and storage model.

Risk: The skill requires a Flyelep API key at runtime.

Mitigation: Provide the API key only for the current run and do not store it in skill files, examples, repositories, or persistent configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyelepai/skills/gen-hot-image)
- [Flyelep open platform](https://www.flyelep.cn/controlboard)
- [Flyelep hot image generation API](https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotImage)
- [Flyelep task result API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult)
- [Flyelep file upload API](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON payloads, shell commands, and generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous task flow; final outputs are public image URLs returned by Flyelep.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
