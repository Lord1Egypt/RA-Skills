## Description:

基于 Azure AI Foundry 构建持久化智能体，支持函数工具、托管工具、流式响应、结构化输出与会话线程管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation teams use this Chinese-language guide to configure Azure AI Foundry agents, add function or hosted tools, manage conversation threads, and produce example code or setup commands. It is not intended for deterministic critical decisions, medical diagnosis, or legal judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags broad activation scope and possible command execution during setup.

Mitigation: Install only for Azure AI Foundry Agent Framework work, review commands before execution, and avoid activating it for unrelated general chat or LLM tasks.

Risk: The skill guides Azure credential use, hosted tools, package installation, and cloud resources.

Mitigation: Review Azure credential scope, environment variables, package installs, and hosted tool configuration before following examples.

Risk: The artifact itself excludes deterministic critical decisions, medical diagnosis, and legal judgments.

Mitigation: Use the skill for development guidance and prototypes, and require qualified review for high-impact or regulated decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-agent-framework-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance for Azure AI Foundry Agent Framework setup and examples.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
