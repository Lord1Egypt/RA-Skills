## Description:

代码执行工具专业版 guides agents through batch PTY code execution workflows, concurrent task orchestration, execution auditing, and CI/CD integration for development teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate batch and concurrent code execution tasks, audit runs, and integrate agent-driven development workflows into CI/CD. It is best suited to controlled development or CI environments where executable commands and credentials are reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad code-execution workflows can run commands across development workspaces or CI environments.

Mitigation: Use only in controlled development or CI environments, restrict working directories and command scope, and avoid privileged accounts.

Risk: Automatic confirmations and password forwarding can approve unsafe prompts or expose credentials.

Mitigation: Review and remove automatic response rules, pass credentials only through scoped environment variables when required, and inspect prompts before execution.

Risk: External packages and CLI dependencies may affect the trust boundary of the execution environment.

Mitigation: Verify package sources and versions before installation and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-runner-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code, shell command, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose executable commands and configuration changes that require user review before running.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
