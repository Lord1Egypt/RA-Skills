## Description:

Use when a task needs Alibaba Cloud Model Studio Qwen Deep Research models to plan multi-step investigation, run iterative web research, and produce structured reports with citations or evidence summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research teams use this skill to prepare Alibaba Cloud Qwen Deep Research requests, guide multi-step web investigations, and organize structured reports with citations or evidence summaries.

### Deployment Geography for Use:

China mainland (Beijing) region

## Known Risks and Mitigations:

Risk: Research prompts, attachments, request payloads, and report snapshots may contain sensitive information and are sent to Alibaba Cloud Model Studio or retained locally.

Mitigation: Use the skill only when this data handling fits policy; avoid secrets or confidential business data in prompts and review retained files under output/aliyun-qwen-deep-research/.

Risk: The skill depends on the dashscope SDK in the runtime environment.

Mitigation: Pin or review the dashscope dependency before production installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-qwen-deep-research)
- [Qwen-Deep-Research](https://help.aliyun.com/zh/model-studio/qwen-deep-research)
- [Qwen-Deep-Research snapshot updates](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [Model Studio model list](https://help.aliyun.com/zh/model-studio/models)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON request files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates normalized request payloads and stores request/report artifacts under output/aliyun-qwen-deep-research/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
