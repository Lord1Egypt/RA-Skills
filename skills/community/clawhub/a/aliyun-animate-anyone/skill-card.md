## Description:

Use when generating dance or motion-transfer videos with Alibaba Cloud Model Studio AnimateAnyone (`animate-anyone-gen2`) using a detected character image and an action template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to prepare Alibaba Cloud Model Studio AnimateAnyone detect, action-template, and video-generation requests for dance or large-body motion transfer from source motion video to a target character image.

### Deployment Geography for Use:

China mainland (Beijing)

## Known Risks and Mitigations:

Risk: The skill requires an Alibaba DashScope API key.

Mitigation: Keep credentials out of source control and logs, and provide them through the environment or the documented local credentials file.

Risk: Input media must be available through public HTTP or HTTPS URLs.

Mitigation: Review source image and video URLs before use and avoid exposing private or sensitive media.

Risk: Generated request artifacts may contain task IDs, media URLs, or provider workflow details.

Mitigation: Review files under output/aliyun-animate-anyone before sharing or committing them.

## Reference(s):

- [Skill release page](https://clawhub.ai/cinience/skills/aliyun-animate-anyone)
- [references/sources.md](references/sources.md)
- [Video generation overview (AnimateAnyone)](https://help.aliyun.com/zh/model-studio/use-video-generation)
- [AnimateAnyone quick start](https://help.aliyun.com/zh/model-studio/animateanyone-quick-start/)
- [AnimateAnyone image detection API](https://help.aliyun.com/zh/model-studio/animate-anyone-detect-api)
- [AnimateAnyone action template API](https://help.aliyun.com/zh/model-studio/animate-anyone-template-api)
- [AnimateAnyone video generation API](https://help.aliyun.com/zh/model-studio/animateanyone-video-generation-api)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON request files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes normalized request payloads, detection outputs, template IDs, and task polling snapshots under output/aliyun-animate-anyone/.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
