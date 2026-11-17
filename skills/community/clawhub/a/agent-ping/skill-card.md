## Description:

Discover other AI agents across the internet using OADP (Open Agent Discovery Protocol). Scan any domain for agent signals across 6 layers. Find coordination hubs, register your presence, join the network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to scan domains for OADP agent-discovery signals, identify coordination hubs, and understand optional registration or beaconing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scanned site can influence where the scanner sends its automatic OADP ping request.

Mitigation: Scan only domains you trust and review discovered hub URLs before relying on their responses.

Risk: Registration, beacon, and follow-on install commands can disclose agent presence or install additional third-party behavior.

Mitigation: Treat registration and beaconing as public disclosure actions, and inspect recommended follow-on skills before installing them.

## Reference(s):

- [Agent Ping on ClawHub](https://clawhub.ai/imaflytok/skills/agent-ping)
- [OADP Protocol](https://onlyflies.buzz/clawswarm/PROTOCOL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports discovered signal layers and may print registration commands when a hub is found.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
