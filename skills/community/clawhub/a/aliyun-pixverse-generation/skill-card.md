## Description:

Use when generating videos with Alibaba Cloud Model Studio PixVerse models (`pixverse/pixverse-v5.6-t2v`, `pixverse/pixverse-v5.6-it2v`, `pixverse/pixverse-v5.6-kf2v`, `pixverse/pixverse-v5.6-r2v`).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare Alibaba Cloud Model Studio PixVerse video-generation requests for text-to-video, image-to-video, keyframe-to-video, and multi-image reference-to-video workflows.

### Deployment Geography for Use:

China mainland (Beijing)

## Known Risks and Mitigations:

Risk: Prompts, media URLs, or regulated data may be submitted to Alibaba Cloud Model Studio.

Mitigation: Use only data approved for transfer to Alibaba Cloud Model Studio in the documented region.

Risk: The skill depends on the dashscope package for SDK-based use.

Mitigation: Install in a virtual environment and pin or review the dashscope package for controlled deployments.

Risk: Credentials are required for DashScope access.

Mitigation: Provide DASHSCOPE_API_KEY through the environment or approved credentials storage, and avoid placing secrets in prompts or output files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-pixverse-generation)
- [references/sources.md](references/sources.md)
- [Video generation overview](https://help.aliyun.com/zh/model-studio/use-video-generation)
- [Aishi text-to-video API reference](https://help.aliyun.com/zh/model-studio/pixverse-text-to-video-api-reference)
- [Aishi image-to-video API reference](https://help.aliyun.com/zh/model-studio/pixverse-image-to-video-api-reference)
- [Aishi keyframe-to-video API reference](https://help.aliyun.com/zh/model-studio/pixverse-keyframe-to-video-api-reference)
- [Aishi reference-to-video API reference](https://help.aliyun.com/zh/model-studio/pixverse-reference-to-video-api-reference)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON request files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes normalized request payloads and task evidence under output/aliyun-pixverse-generation/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
