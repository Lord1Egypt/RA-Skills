## Description:

This skill supports image editing with Alibaba Cloud Model Studio Qwen Image Edit models for inpainting, replacement, style transfer, local edits, subject consistency, and request/response documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and document Alibaba Cloud Qwen Image Edit workflows for instruction-based image edits, local edits, inpainting, style transfer, and subject-consistency tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba Cloud credentials may be exposed through logs, source control, or shared environments.

Mitigation: Keep DASHSCOPE_API_KEY and Alibaba Cloud credential files out of logs and repositories, and use a clean virtual environment for installation.

Risk: Saved prompts, request payloads, and private image URLs may contain sensitive user or business data.

Mitigation: Retain output evidence only as long as needed, avoid storing sensitive prompts or private image URLs, and redact shared artifacts.

Risk: An unreviewed or floating dashscope dependency may introduce compatibility or supply-chain risk.

Mitigation: Use a pinned and reviewed dashscope version where possible before deploying the skill.

## Reference(s):

- [Alibaba Cloud Qwen Image Edit guide](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-qwen-image-edit)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create request and response evidence files under the configured output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
