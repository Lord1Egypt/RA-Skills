## Description:

Generate images & videos with AIsa. Gemini 3 Pro Image (image) + Qwen Wan 2.6 (video) via one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate images and videos through the AIsa API, including Gemini image generation and Wan 2.6 asynchronous video tasks with polling and optional local download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, referenced image URLs, task IDs, and generated-media requests are sent to AIsa using AISA_API_KEY.

Mitigation: Avoid submitting sensitive or private content and use an API key scoped appropriately for the task.

Risk: The download path writes generated media locally and provider-returned download URLs are not validated by the skill.

Mitigation: Review chosen output paths before running download commands and inspect provider-returned URLs before downloading files.

Risk: A chosen output path can be overwritten when the client saves generated media.

Mitigation: Use a fresh output filename or directory for each run when preserving existing files matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bowen-dotcom/skills/aisa-media-gen-skill)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [AIsa GenerateContent documentation](https://docs.aisa.one/reference/generatecontent)
- [AIsa video generation documentation](https://docs.aisa.one/reference/post_services-aigc-video-generation-video-synthesis)
- [AIsa task status documentation](https://docs.aisa.one/reference/get_services-aigc-tasks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses from the client script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated image or video files locally when output or download options are used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
