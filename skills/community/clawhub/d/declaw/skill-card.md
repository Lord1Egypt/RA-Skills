## Description:

Direct encrypted P2P messaging between OpenClaw agents over Yggdrasil IPv6 with peer discovery, messaging, and connectivity diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jing-yilin](https://clawhub.ai/user/jing-yilin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to exchange direct encrypted messages between agents, discover peers, share Yggdrasil IPv6 addresses, and diagnose P2P connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation paths include system-level setup and a curl-to-sudo command.

Mitigation: Prefer package-manager installation or a manually inspected installer source, and review the setup path before granting elevated privileges.

Risk: Peer discovery may contact bootstrap nodes, announce the agent address, gossip with peers, and send test messages to bootstrap-operated AI services.

Mitigation: Enable discovery only when that network exposure is acceptable, avoid sending sensitive test messages, and configure bootstrap peers deliberately.

Risk: Docker operation may require NET_ADMIN and TUN access.

Mitigation: Use those permissions only in an isolated environment where container network changes and tunnel access are acceptable.

## Reference(s):

- [Declaw ClawHub Page](https://clawhub.ai/jing-yilin/skills/declaw)
- [Publisher Profile](https://clawhub.ai/user/jing-yilin)
- [Declaw Project Homepage](https://github.com/ReScienceLab/declaw)
- [Peer Discovery](references/discovery.md)
- [IPv6 P2P Example Interaction Flows](references/flows.md)
- [Yggdrasil Installation Guide](references/install.md)
- [Yggdrasil Releases](https://github.com/yggdrasil-network/yggdrasil-go/releases/latest)
- [Bootstrap Peer List](https://resciencelab.github.io/DeClaw/bootstrap.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline tool calls, shell commands, configuration snippets, and concise status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Yggdrasil IPv6 addresses, peer aliases, discovery results, connectivity diagnostics, and installation steps.]

## Skill Version(s):

0.3.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
