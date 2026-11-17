## Description:

Claw Crony installs and configures the Claw Crony A2A Gateway plugin for cross-server OpenClaw agent communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccccl8](https://clawhub.ai/user/ccccl8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install Claw Crony, configure Agent Cards, bearer tokens, peers, networking, TOOLS.md guidance, and verify A2A messaging between OpenClaw servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation steps can fetch and install plugin code and dependencies.

Mitigation: Review and pin the plugin source and dependencies before installation, and prefer a package-manager flow over curl-to-shell setup.

Risk: Gateway configuration can expose an A2A endpoint and bearer-token access to peers.

Mitigation: Bind the gateway to a trusted interface or encrypted overlay, restrict peer access, and verify connectivity before use.

Risk: Peer tokens may be placed in agent-visible TOOLS.md content.

Mitigation: Move peer tokens to a secret store and reference them at runtime instead of storing credentials in agent instructions.

Risk: Outbound A2A messages may send user content to another server or agent.

Mitigation: Require explicit user confirmation before sending content to a peer and avoid constructing shell commands from raw message text.

## Reference(s):

- [Claw Crony ClawHub release page](https://clawhub.ai/ccccl8/skills/claw-crony)
- [ccccl8 publisher profile](https://clawhub.ai/user/ccccl8)
- [TOOLS.md A2A Section Template](references/tools-md-template.md)
- [Claw Crony plugin repository mentioned in setup instructions](https://github.com/ccccl8/claw-crony.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and table snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include plugin installation commands, OpenClaw configuration commands, TOOLS.md content, and connectivity tests.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
