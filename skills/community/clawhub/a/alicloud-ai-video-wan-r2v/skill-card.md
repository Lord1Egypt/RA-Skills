## Description:

Generates reference-based videos with Alibaba Cloud Model Studio Wan R2V models, including wan2.6-r2v-flash and wan2.6-r2v.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI video practitioners use this skill to prepare and run Alibaba Cloud Wan reference-to-video generation workflows from reference video or image material while preserving style across multi-shot outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can persist prompts, media references, task identifiers, polling snapshots, and generated outputs in the workspace.

Mitigation: Avoid highly sensitive prompts or private media URLs, review saved artifacts before sharing, and clean output directories when the evidence is no longer needed.

Risk: The skill installs the dashscope SDK without a pinned version.

Mitigation: Pin and review the dependency version before use in controlled or production environments.

Risk: Using the skill requires Alibaba Cloud credentials for video generation.

Mitigation: Use scoped credentials, keep DASHSCOPE_API_KEY out of checked-in files, and confirm users are authorized to submit the referenced media.

## Reference(s):

- [Wan Video-to-Video API Reference](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference)
- [Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/alicloud-ai-video-wan-r2v)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with shell commands and JSON request or response artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes request payloads, task outputs, polling snapshots, and generated video artifacts under the configured output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
