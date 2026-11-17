## Description:

Use when tasks require all-in-one multimodal understanding or generation with Alibaba Cloud Model Studio Qwen Omni models, including image-plus-audio interaction, voice assistants, and realtime multimodal agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare and standardize Qwen Omni multimodal requests for image, audio, and text assistant workflows, including realtime agents and spoken responses grounded in visual input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated request payload includes a default instruction to answer in Chinese and a placeholder image URL.

Mitigation: Review and edit the generated payload before sending it to Alibaba Cloud Model Studio or using it in an agent workflow.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cinience/skills/aliyun-qwen-omni)
- [Qwen Omni documentation](https://help.aliyun.com/zh/model-studio/qwen-omni)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write request payload files under output/aliyun-qwen-omni when using the helper script.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
