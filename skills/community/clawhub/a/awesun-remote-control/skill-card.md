## Description:

Guides an agent in using AweSun’s remote-control CLI to manage devices, connect sessions, operate remote desktops, transfer files, run commands, and configure port forwarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutecube](https://clawhub.ai/user/cutecube)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to carry out remote support and administration of AweSun devices, including desktop work, file handling, command execution, and connection setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers high-impact remote operations, including shell commands, file transfer or deletion, desktop input, and device power controls.

Mitigation: Verify the target and access authorization, review commands and file paths, confirm before destructive or disruptive actions, and disconnect sessions when finished.

Risk: The security review is benign with medium confidence and notes that one local reference could not be resolved; setup guidance also describes claiming a free service trial.

Mitigation: Review the account and connection guides, and decide whether the service-trial capability is wanted before following setup instructions.

## Reference(s):

- [AweSun Remote Control release](https://clawhub.ai/cutecube/skills/awesun-remote-control)
- [Publisher profile: cutecube](https://clawhub.ai/user/cutecube)
- [Account and service management guide](artifact/references/account-guide.md)
- [Connection guide](artifact/references/connection-guide.md)
- [Device management guide](artifact/references/device-guide.md)
- [Desktop control guide](artifact/references/desktop-guide.md)
- [File management and transfer guide](artifact/references/file-guide.md)
- [Port forwarding guide](artifact/references/port-forwarding-guide.md)
- [Remote command execution and SSH guide](artifact/references/remote-exec-guide.md)
- [UI element locator guide](artifact/references/ui-locator.md)
- [UI patterns reference](artifact/references/ui-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with CLI examples and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may control remote devices and transfer or modify remote data.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
