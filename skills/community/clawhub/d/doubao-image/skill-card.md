## Description:

Generates images with the Volcengine Doubao image-generation API using custom prompts, size, model, and count parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanxing0724](https://clawhub.ai/user/wanxing0724)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to request images from the Volcengine Doubao API and save the generated image output locally. It supports prompt-driven generation with configurable image size, model, and image count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and API-key-authenticated image-generation requests are sent to Volcengine.

Mitigation: Install only if this external processing is acceptable, and do not include secrets, private data, or regulated content in prompts.

Risk: The skill automatically downloads external image content to a hard-coded local path with weak safeguards.

Mitigation: Review or change the script before use so downloads have timeouts, size and content checks, validated image hosts, and a user-chosen output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanxing0724/skills/doubao-image)
- [Volcengine console](https://console.volces.com/)
- [Volcengine image-generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration]

**Output Format:** [Terminal text with generated image URLs and local image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VOLCENGINE_IMAGE_API_KEY; generated images are downloaded to a local images directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
