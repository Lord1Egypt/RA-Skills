## Description:

Use when code generation, repository understanding, or coding-agent tasks need Alibaba Cloud Model Studio Qwen Coder models (`qwen3-coder-next`, `qwen3-coder-plus` and related coder variants).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Qwen Coder requests for code generation, code review drafting, repository-level reasoning, patch planning, and tool-using software-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository summaries, prompts, or selected files may contain code or data that should not be sent to Alibaba Cloud Model Studio.

Mitigation: Use the skill only with code and context approved for that service, and pass only files relevant to the requested change.

Risk: Secrets could be included in prompts, repository summaries, or generated request payloads.

Mitigation: Remove secrets before preparing requests and avoid storing credentials in generated outputs.

Risk: Generated request files may persist sensitive task context under output/aliyun-qwen-coder/.

Mitigation: Review and clean the output directory when it may contain sensitive information.

Risk: Unpinned SDK dependencies can change behavior across installations.

Mitigation: Pin the dashscope SDK version in controlled environments when reproducibility matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-qwen-coder)
- [Artifact source references](references/sources.md)
- [Alibaba Cloud Model Studio Qwen Coder documentation](https://help.aliyun.com/zh/model-studio/qwen-coder)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [Alibaba Cloud Model Studio model list](https://help.aliyun.com/zh/model-studio/models)
- [Alibaba Cloud Model Studio Cline integration documentation](https://help.aliyun.com/zh/model-studio/cline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON request payload files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write normalized request payloads under output/aliyun-qwen-coder/requests/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
