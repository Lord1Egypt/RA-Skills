## Description:

当需要查询阿里云日志（SLS）时使用此技能，支持 CLI 查询日志、分析数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeweis](https://clawhub.ai/user/jeweis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to configure Alibaba Cloud SLS CLI access, map project and logstore names, and generate bounded log queries or SQL analysis commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials may be exposed through command-line arguments, shell history, or persistent local CLI configuration.

Mitigation: Use least-privileged short-lived Aliyun credentials, prefer safer credential handling over command-line secrets, and review local configuration before execution.

Risk: Broad CLI instructions and SDK-to-CLI mappings could change cloud or local state if administrative operations are used.

Mitigation: Restrict use to read-only SLS log commands unless administrative operations are explicitly required and confirmed.

Risk: Project mapping updates can persist incorrect or sensitive project/logstore associations.

Mitigation: Require user confirmation before appending new project mappings and avoid storing secrets in the mapping file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeweis/skills/aliyun-log-query)
- [Project mapping reference](references/project_mapping.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should keep log query result sizes bounded with LIMIT and short time ranges.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
