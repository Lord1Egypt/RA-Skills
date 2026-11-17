## Description:

Routes Alibaba Cloud Model Studio requests to the appropriate local skill for Qwen text, code, research, image, video, audio, search, and multimodal tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this entry skill to route broad Alibaba Cloud Model Studio requests to a matching local sub-skill and receive focused guidance for text, code, research, image, video, audio, search, or multimodal work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broadly triggered entry skill may perform authenticated Alibaba Cloud Model Studio API operations, not only route requests.

Mitigation: Confirm the intended capability and operation scope before use, review the selected target sub-skill, and run a minimal read-only connectivity check before any broader operation.

Risk: Authenticated calls require DASHSCOPE_API_KEY and may expose or overuse privileges if the key is too broad.

Mitigation: Use a narrowly scoped key where possible, keep it in environment or credential storage, and avoid elevated installs.

Risk: Unpinned installation of the dashscope dependency can reduce reproducibility.

Mitigation: Pin the dashscope dependency version when reproducible installation behavior is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-modelstudio-entry)
- [Official source list](references/sources.md)
- [Alibaba Cloud Model Studio models](https://help.aliyun.com/zh/model-studio/models)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [Alibaba Cloud Model Studio OpenAI-compatible API](https://help.aliyun.com/zh/model-studio/openai-compatible)
- [DashScope task API](https://dashscope.aliyuncs.com/api/v1/tasks/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route users to local Alibaba Cloud sub-skills and summarize saved evidence paths for reproducibility.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
