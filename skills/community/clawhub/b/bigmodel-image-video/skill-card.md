## Description:

BigModel Image Video Generator uses BigModel CogView and CogVideoX APIs to generate single or batch images and asynchronous videos from prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and external users use this skill to create visual content such as covers, social posts, product images, posters, and short videos through BigModel API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a real BigModel API key and may expose secrets if users store the key in committed or synced shell configuration files.

Mitigation: Store the API key in a secret manager or temporary environment variable and avoid committing shell files that contain credentials.

Risk: Changing the BigModel base URL could route prompts, image URLs, or credentials to an unintended service.

Mitigation: Keep the default BigModel endpoint and avoid user-controlled base_url values unless they have been reviewed.

Risk: Prompts and optional image URLs are sent to BigModel for image or video generation.

Mitigation: Avoid submitting sensitive or confidential prompt content or image URLs unless the BigModel service terms and data handling are acceptable for the use case.

## Reference(s):

- [BigModel Open Platform](https://open.bigmodel.cn/)
- [BigModel API Endpoint](https://open.bigmodel.cn/api)
- [ClawHub Skill Page](https://clawhub.ai/156554395/skills/bigmodel-image-video)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime calls return JSON containing generated image, video, task, and cover URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BIGMODEL_API_KEY environment variable and sends prompts, and optional image URLs for video generation, to BigModel.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
