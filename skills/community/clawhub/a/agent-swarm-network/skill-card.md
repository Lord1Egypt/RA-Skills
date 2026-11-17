## Description:

Agent Swarm Network helps agents coordinate through inter-agent messaging, context snapshot and restore, event-driven collaboration, sub-agent routing, file transfer, and network diagnostics using Pilot Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarahmirrand001-oss](https://clawhub.ai/user/sarahmirrand001-oss)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to preserve context across sessions, coordinate multiple agents, publish collaboration events, route tasks, exchange files, and inspect Pilot network health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically saves and restores sensitive session context in plaintext under ~/.pilot/.

Mitigation: Secure ~/.pilot with restrictive permissions, avoid storing secrets in sessions that may be snapshotted, regularly clear old snapshots, and disable or closely control auto-restore and auto-snapshot behavior where possible.

Risk: The skill relies on a persistent network-capable Pilot daemon.

Mitigation: Install only when persistent agent memory and peer networking are intentional, pin and verify the Pilot Protocol build, and keep the registry local unless an external registry is deliberately configured.

Risk: Restored inbox content and received files can influence later agent behavior.

Mitigation: Treat restored inbox content and transferred files as untrusted input and review them before using their contents to drive decisions or commands.

## Reference(s):

- [Agent Swarm Network ClawHub listing](https://clawhub.ai/sarahmirrand001-oss/skills/agent-swarm-network)
- [Agent Swarm Network homepage](https://agent-swarm-network.vercel.app)
- [Pilot Protocol](https://github.com/TeoSlayer/pilotprotocol)
- [MCP skill manifest schema](https://spec.modelcontextprotocol.io/2025-03/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for pilotctl commands, local configuration, context snapshot files, event messages, file transfer paths, and diagnostics.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter, manifest.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
