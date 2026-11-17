## Description:

Agent Mesh enables AI agents on different machines to exchange messages over the Decent Network peer-to-peer mesh without a third-party platform, server, or account registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xli](https://clawhub.ai/user/0xli)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Agent Mesh to connect agents across machines for peer-to-peer coordination without relying on a centralized chat service, webhook, or account system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent internet-connected peer-to-peer daemon use can increase network and local state exposure.

Mitigation: Install only in environments where persistent P2P messaging is acceptable, supervise the daemon, and review ~/.decent-peer permissions, logs, retention, allow.txt entries, watchdogs, and startup configuration.

Risk: Remote peer messages can be surfaced into an agent turn or control hook.

Mitigation: Treat all peer messages as untrusted, avoid the Claude Stop hook until message-body injection into hook reasons is addressed, and review messages before acting on them.

Risk: Unpinned dependencies can change the runtime behavior of the peer messaging stack.

Mitigation: Pin npm dependencies before operational use and verify the installed @decentnetwork/peer version meets the documented minimum.

Risk: Secrets sent through peer messages may be exposed through inbox files, logs, or downstream agent prompts.

Mitigation: Do not send secrets over the mesh and keep peer state and log files access-controlled.

## Reference(s):

- [Agent Mesh on ClawHub](https://clawhub.ai/0xli/skills/decent-agent-mesh)
- [Decent Network](https://decent.network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, AGENT_NAME, and a persistent peer daemon for message delivery.]

## Skill Version(s):

0.1.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
