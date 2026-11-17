## Description:

Route Alibaba Cloud Model Studio requests to the right local skill (Qwen Image, Qwen Image Edit, Wan Video, Wan R2V, Qwen TTS, Qwen ASR and advanced TTS variants).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route ambiguous Alibaba Cloud Model Studio requests to the appropriate local capability skill before generating, editing, transcribing, translating, retrieving, or understanding text, image, audio, video, and multimodal content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, audio, video, or documents may be sent to Alibaba Cloud when routed skills call Model Studio services.

Mitigation: Avoid submitting sensitive content unless the user is comfortable sending it to Alibaba Cloud under their account.

Risk: The skill installation guidance installs the dashscope SDK without pinning a package version.

Mitigation: Use a fresh virtual environment and review or pin the dashscope package version before deployment.

## Reference(s):

- [Official source list](references/sources.md)
- [DashScope async task API](https://dashscope.aliyuncs.com/api/v1/tasks/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route the agent to a more specific local Alibaba Cloud Model Studio skill and may save evidence files under output/alicloud-ai-entry-modelstudio/.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
