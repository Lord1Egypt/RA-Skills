## Description:

Team-wide peer-to-peer mesh for OpenClaw agents that lets agents ping teammates, send messages and wait for replies, broadcast to the team, and discover agent status through direct WebSocket calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams running OpenClaw agents on routable containers or pods use this skill to exchange direct agent-to-agent messages, check team agent availability, and broadcast updates without operating a central broker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable OpenClaw gateway tokens are shared among teammates and stored locally.

Mitigation: Store tokens outside the skill directory in a user-only file, keep them out of git, restrict file permissions, and rotate tokens if they may have been exposed.

Risk: Agent messages and tokens may cross plaintext WebSocket connections.

Mitigation: Use the mesh only on trusted private networks, prefer pinned installation, and rotate tokens if traffic may have crossed an untrusted network.

Risk: Dry-run output and operational logs may reveal sensitive message content.

Mitigation: Avoid logging dry-run previews or command output that contains sensitive prompts, replies, or routing details.

Risk: The optional IM fallback can hand messages to a user-provided external script.

Mitigation: Disable the fallback unless needed, and review the configured fallback script before allowing it to send messages.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai)
- [Team registry example](references/registry.json)
- [Token file example](references/tokens.example.json)
- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/agent-team-mesh)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses direct OpenClaw gateway calls and local configuration files; message size limits and dry-run behavior are part of the documented workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
