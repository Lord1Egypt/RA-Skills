## Description:

Automated setup and configuration of Feishu/Lark bots with OpenClaw, including agent creation, channel configuration, credential management, routing bindings, customizable roles, and WebSocket or webhook connection modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lcz5221-svg](https://clawhub.ai/user/lcz5221-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up multiple Feishu/Lark bots for OpenClaw with separate workspaces, memories, agent identities, and routing bindings. It supports teams that need role-specific bots for service, sales, HR, technical support, legal, finance, or similar internal workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup process handles Feishu credentials and writes them into OpenClaw configuration.

Mitigation: Protect and rotate credentials, restrict access to generated configuration files, and use only trusted bot configuration files.

Risk: The security review says user-supplied configuration has too much influence over shell commands, file paths, credentials, and open bot access policies.

Mitigation: Review before installing or running, avoid running the setup script as root, validate paths and configuration values, and fix the shell command, path validation, and backup handling issues before production use.

Risk: Default open direct-message and group policies can expose bots more broadly than intended.

Mitigation: Prefer allowlists or pairing policies where possible and review Feishu bot permissions before deployment.

## Reference(s):

- [Example configuration](references/example-config.json)
- [ClawHub skill page](https://clawhub.ai/lcz5221-svg/skills/feishu-duoge)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions and a Python setup script that creates agent files and updates OpenClaw Feishu account bindings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
