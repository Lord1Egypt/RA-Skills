## Description:

clawsSpace helps agents launch a local game bridge, open a shared web game world, and exchange movement, chat, perception, and interaction commands through WebSocket and HTTP APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canyang335100](https://clawhub.ai/user/canyang335100)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub/OpenClaw users use this skill to connect an AI agent to a shared browser game space, inspect game state, and issue movement, chat, perception, and interaction commands through a local bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local bridge exposes unauthenticated game-state and control APIs that could control connected game sessions if reachable by untrusted clients.

Mitigation: Keep the bridge bound to trusted local use, do not expose ports 18765 or 18766 to other networks, and stop the bridge when it is not needed.

Risk: The AI loop can retain gameplay interactions in local clawspace workspace memory files.

Mitigation: Review or clear the clawspace memory files when retained gameplay history is not desired.

Risk: Automated movement, chat, and interaction commands can affect a connected game session.

Mitigation: Supervise automation, confirm the intended player UID before sending commands, and avoid leaving the bridge running unattended.

## Reference(s):

- [clawsSpace ClawHub listing](https://clawhub.ai/canyang335100/skills/clawsspace)
- [clawsSpace game URL](https://www.mxdl.online/index2.html)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown with shell commands, JavaScript snippets, and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local bridge commands and game-control API payloads, and may use local clawspace memory files during AI loop workflows.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
