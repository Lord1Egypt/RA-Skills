## Description:

clawSpace lets an agent start and use a local OpenClaw game bridge to control a browser-game character and read shared game-world state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canyang335100](https://clawhub.ai/user/canyang335100)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use clawSpace to let an agent launch the OpenClaw bridge, connect to the game, send movement, chat, and NPC interaction commands, and inspect map, player, NPC, and transport-point state through local APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge exposes unauthenticated game-control and game-state APIs.

Mitigation: Run it only on trusted machines and networks, restrict access to the local session, and stop the bridge when the game-control task is complete.

Risk: The dependency set includes a vulnerable ws package according to the authoritative security guidance.

Mitigation: Update or remove the vulnerable ws dependency before regular use.

Risk: Workspace memory or logs may retain game-world state, player identifiers, or session activity.

Mitigation: Clear workspace memory and logs when this state should not persist after use.

## Reference(s):

- [clawSpace on ClawHub](https://clawhub.ai/canyang335100/skills/clawspace)
- [Node.js](https://nodejs.org/)
- [clawSpace game URL](https://www.mxdl.online/index2.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript snippets, and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start local bridge services and send commands to browser-game sessions.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
