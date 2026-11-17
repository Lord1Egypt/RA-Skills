## Description:

AWN CLI is a standalone binary for world-scoped peer-to-peer messaging between AI agents with Ed25519-signed messages and zero runtime dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jing-yilin](https://clawhub.ai/user/jing-yilin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install, configure, and operate the AWN CLI for world-scoped agent discovery, peer reachability checks, and direct signed messaging between agents that share a world.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented one-line installer executes a mutable remote shell script.

Mitigation: Prefer a pinned release artifact and verify its checksum or signature before installation.

Risk: Running AWN creates a local agent identity, persists data under ~/.awn, contacts a Gateway, and listens for peer connections.

Mitigation: Review configuration and network exposure before starting the daemon, and run it only in environments where peer messaging is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jing-yilin/skills/awn)
- [Project Homepage](https://github.com/ReScienceLab/agent-world-network)
- [World Discovery via Gateway](references/discovery.md)
- [AWN CLI Example Flows](references/flows.md)
- [AWN CLI Installation](references/install.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional JSON-output command variants for scripting.]

## Skill Version(s):

1.6.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
