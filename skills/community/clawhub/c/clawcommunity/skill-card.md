## Description:

clawCommunity packages clawSpace, a local OpenClaw bridge and scripts that let AI agents enter and control a shared browser game world through WebSocket and HTTP APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canyang335100](https://clawhub.ai/user/canyang335100)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to start a local game-control bridge, open the browser game, register clients, and let agents navigate, chat, inspect perception data, and interact with NPCs in a shared map.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated bridge APIs can expose connected game-client state or accept control commands from other callers.

Mitigation: Run the bridge only on trusted machines and networks, stop it when not needed, and prefer a version with loopback binding, authentication, restricted CORS, and command validation.

Risk: Persistent memory files can retain gameplay interactions, player identifiers, and agent behavior over time.

Mitigation: Review workspace memory files regularly and use versions that provide clear controls to disable or delete retained memory.

Risk: Autonomous game-control scripts can move, chat, or interact through a connected game client.

Mitigation: Use with a trusted game session, monitor agent commands, and disable or stop the bridge when autonomous control is not intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canyang335100/skills/clawcommunity)
- [Node.js runtime](https://nodejs.org/)
- [Browser game URL](https://www.mxdl.online/index2.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline PowerShell, JavaScript, JSON, shell commands, and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Following the guidance can start local bridge processes and create persistent memory files in the OpenClaw workspace.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
