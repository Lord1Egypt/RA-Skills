## Description:

将编程任务委派给本地代码 CLI 执行，支持异步流程与单任务调试迭代。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to delegate coding, debugging, testing, and deployment-related tasks to a local code CLI while keeping the main agent responsive. It is intended for clearly scoped software tasks with an identifiable project directory and technical stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes broad local command execution for coding work.

Mitigation: Use it only in a dedicated project directory and review delegated commands before execution.

Risk: The skill documents automatic file-edit permission bypass behavior.

Mitigation: Avoid permission-bypass mode unless the repository and task are fully trusted.

Risk: Delegated work may expose project contents to the external CLI provider.

Mitigation: Do not run delegated tasks on repositories or paths containing secrets or sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-delegate-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline text and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include delegated CLI status, command output, implementation guidance, test results, and error-handling recommendations.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
