## Description:

向日葵远程控制 provides agent tools for managing AweSun devices, starting remote sessions, running remote commands, forwarding ports, and controlling remote desktops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutecube](https://clawhub.ai/user/cutecube)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent manage authorized AweSun devices, open remote desktop, file, CMD, SSH, camera, and port-forwarding sessions, and perform desktop input, screenshots, command execution, and power actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control authorized remote devices, including desktop input, command execution, screenshots, shutdown, wake, device removal, and port forwarding.

Mitigation: Install only when remote device control is intended, and require human review before high-impact actions are executed.

Risk: The MCP API token is configured as plaintext environment data.

Mitigation: Keep the token out of shared workspaces and source control, and replace the placeholder only in a private local configuration.

Risk: The integration depends on a locally configured AweSun MCP server with broad access to remote sessions.

Mitigation: Use only a trusted AweSun MCP server, pin the MCP dependency before installation, and disconnect sessions when work is complete.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cutecube/skills/awesun-remote-control)
- [ClawHub publisher profile](https://clawhub.ai/user/cutecube)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-formatted tool results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool results may include device and session metadata, command output, port-forwarding status, or Base64 screenshot data from the configured AweSun MCP server.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
