## Description:

DeepVista CLI: Authentication, global flags, and security conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this shared reference to install and operate the DeepVista CLI, authenticate, choose profiles and global flags, and follow command safety conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run an update-check command when loaded, which can execute local CLI behavior without an explicit user request.

Mitigation: Remove the silent load-time check or require explicit user approval before running it. Use an isolated, non-privileged installation and a trusted, pinned package version.

Risk: DeepVista authentication uses local credentials and configurable profiles or API URLs.

Mitigation: Do not expose tokens, verify the active profile and API URL before use, and preview write or destructive operations with --dry-run where supported.

## Reference(s):

- [DeepVista CLI homepage](https://cli.deepvista.ai)
- [ClawHub skill page](https://clawhub.ai/jingconan/skills/deepvista-shared)
- [Publisher profile](https://clawhub.ai/user/jingconan)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI installation, authentication, profile, output, exit-code, and safety guidance.]

## Skill Version(s):

0.1.0-alpha.21 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
