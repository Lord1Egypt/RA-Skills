## Description:

查询技能 is an example ClawHub skill that demonstrates skill metadata, dependency declarations, installation commands, and API credential configuration.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[feifeifeichangmeilidejutu12138](https://clawhub.ai/user/feifeifeichangmeilidejutu12138)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors can use this example to understand how a ClawHub skill declares required environment variables, command-line dependencies, operating system support, installation steps, and default configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation steps include package-manager and sudo commands.

Mitigation: Review the install commands first and run privileged package installation only through a trusted admin workflow.

Risk: The skill declares API key configuration.

Mitigation: Use test or low-privilege credentials unless the package source and purpose have been verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feifeifeichangmeilidejutu12138/skills/find-2skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown skill metadata with installation commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review of package installation commands and low-privilege API credentials before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
