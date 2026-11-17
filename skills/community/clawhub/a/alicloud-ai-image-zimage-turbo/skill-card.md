## Description:

Generate images with Alibaba Cloud Model Studio Z-Image Turbo (z-image-turbo) via DashScope multimodal-generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate text-to-image outputs with Alibaba Cloud Model Studio Z-Image Turbo through DashScope, including endpoint selection, image size, seed, and prompt extension settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted endpoint overrides could expose the DashScope API key to an arbitrary service.

Mitigation: Allow only the official DashScope Beijing or Singapore endpoints, and do not let untrusted users or prompts set base_url or DASHSCOPE_BASE_URL.

Risk: The helper downloads URLs returned by the generation response and writes to the requested output path.

Mitigation: Use trusted endpoints, save only to intended output locations, and rotate any key used with an untrusted endpoint.

## Reference(s):

- [Z-Image Turbo API Reference](references/api_reference.md)
- [Official Z-Image API sources](references/sources.md)
- [Alibaba Cloud Model Studio Z-Image API Reference](https://help.aliyun.com/zh/model-studio/z-image-api-reference)
- [Alibaba Cloud International Z-Image API Reference](https://www.alibabacloud.com/help/zh/model-studio/z-image-api-reference)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-image-zimage-turbo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls, files]

**Output Format:** [Markdown guidance with JSON request/response mappings, shell commands, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call DashScope, print normalized JSON responses, and save generated images under the configured output path.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
