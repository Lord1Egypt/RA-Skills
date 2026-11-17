## Description:

Claude代码运行器 helps agents invoke Claude Code through a PTY to perform code generation, review, refactoring, debugging, testing, deployment, and CI/CD-related programming tasks in non-TTY environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering teams, and automation workflows use this skill to delegate repository programming tasks such as code review, refactoring, bug fixing, feature implementation, and CI/CD integration to an agent running Claude Code through a PTY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to let an agent run commands and edit code through a PTY, which can affect repository contents and local execution state.

Mitigation: Use it in a disposable or least-privilege workspace, review proposed changes, and avoid granting broader filesystem or execution access than the task requires.

Risk: The security evidence notes broad execution/write authority and mentions root or sudo user switching without tight scoping or confirmation guidance.

Mitigation: Avoid sudo or root execution unless the environment is isolated and the command scope has been explicitly reviewed.

## Reference(s):

- [Claude代码运行器 ClawHub skill page](https://clawhub.ai/thcjp/skills/code-runner-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and text responses with inline code or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform file edits and command execution through the host agent environment.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
