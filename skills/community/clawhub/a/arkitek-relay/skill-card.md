## Description:

Connect this agent to ArkiTek for secure remote chat via SSE. No tunnels, no open ports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raleighgardner16-source](https://clawhub.ai/user/raleighgardner16-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an OpenClaw agent to ArkiTek so users can chat with the agent remotely through an outbound relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote chat relay can deliver instructions from ArkiTek to the local agent.

Mitigation: Use the skill only with an agent environment approved for remote chat and limit the environment variables and filesystem access available to the relay.

Risk: The install path relies on an unpinned third-party npm package.

Mitigation: Prefer a pinned and reviewed package version before installation.

Risk: The relay is a long-running cloud messaging channel.

Mitigation: Stop the background process when remote access is no longer needed.

## Reference(s):

- [ArkiTek homepage](https://arkitekai.com)
- [ClawHub skill page](https://clawhub.ai/raleighgardner16-source/skills/arkitek-relay)
- [ClawHub publisher profile](https://clawhub.ai/user/raleighgardner16-source)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARKITEK_API_KEY and a Node.js/npx environment; the relay process stays active while remote chat is needed.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
