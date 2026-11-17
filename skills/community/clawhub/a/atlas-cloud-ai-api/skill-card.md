## Description:

Atlas Cloud provides agent guidance, API examples, and scripts for generating images, generating videos, and calling OpenAI-compatible LLM chat models through Atlas Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihhhh](https://clawhub.ai/user/xixihhhh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to integrate Atlas Cloud image generation, video generation, model discovery, and OpenAI-compatible chat APIs into projects. It also provides runnable Python scripts and shell/API examples for listing models and saving generated media outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, chat messages, and uploaded media are sent to Atlas Cloud and may include sensitive project or personal data.

Mitigation: Use only data approved for Atlas Cloud processing, avoid secrets and regulated data, and review Atlas Cloud data handling before deployment.

Risk: Generated output downloads are based on URLs returned by remote services.

Mitigation: Download outputs into a controlled directory, inspect files before further use, and avoid automatically executing or trusting downloaded content.

Risk: MCP package behavior may change across releases.

Mitigation: Pin the MCP package version before use and review updates before upgrading.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xixihhhh/skills/atlas-cloud-ai-api)
- [Source Homepage](https://github.com/AtlasCloudAI/nano-banana-2-skill)
- [Image Generation Reference](references/image-gen.md)
- [Video Generation Reference](references/video-gen.md)
- [LLM Chat Reference](references/llm-chat.md)
- [Model Reference and Selection Guide](references/models.md)
- [Atlas Cloud Model List](https://console.atlascloud.ai/api/v1/models)
- [Atlas Cloud API Keys](https://www.atlascloud.ai/console/api-keys)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Python, TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY for Atlas Cloud API calls; bundled scripts may save generated image or video files returned by remote services.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
