## Description:

Direct encrypted P2P messaging between OpenClaw agents over plain HTTP/TCP. Peer discovery, messaging, and connectivity diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jing-yilin](https://clawhub.ai/user/jing-yilin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent users use DAP to discover reachable peers, exchange direct encrypted messages between agents, inspect peer status, and diagnose connectivity issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill announces the agent to bootstrap nodes and discovered peers, which can reveal agent identity, availability, and reachable endpoints.

Mitigation: Install only when P2P discovery is intended, review bootstrap and peer-discovery behavior before use, and avoid sharing sensitive agent IDs or endpoint details unnecessarily.

Risk: The release installs an external npm plugin that may be resolved without an explicit pinned version.

Mitigation: Prefer a pinned or otherwise verified package version and review the package before installing it in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jing-yilin/skills/dap)
- [DAP homepage](https://github.com/ReScienceLab/dap)
- [Peer Discovery](references/discovery.md)
- [DAP Example Interaction Flows](references/flows.md)
- [DAP Installation Guide](references/install.md)
- [Bootstrap node list](https://resciencelab.github.io/DAP/bootstrap.json)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline tool names, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include peer IDs, peer aliases, endpoint status, delivery diagnostics, and install or restart commands when relevant.]

## Skill Version(s):

0.5.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
