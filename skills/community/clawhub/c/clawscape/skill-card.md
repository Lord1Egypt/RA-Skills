## Description:

clawScape helps an agent start and use a local OpenClaw bridge to open the clawSpace game world, receive perception data, and send movement, chat, interaction, and AI-loop commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canyang335100](https://clawhub.ai/user/canyang335100)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to connect an OpenClaw agent to the clawSpace browser game through a local bridge, inspect world state, and automate movement, dialogue, NPC interaction, and memory-backed AI loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local game-control bridge with unauthenticated controls that other local clients or websites could abuse while it is running.

Mitigation: Run it only on a trusted machine, stop it when not in use, avoid browsing untrusted sites while it is active, and prefer a version that adds authentication, removes wildcard CORS, binds services explicitly to loopback, and validates command types and body sizes.

Risk: The AI loop can persist character memory and gameplay history in workspace files.

Mitigation: Keep the workspace on a trusted machine and use versions or procedures that let users inspect and clear saved memory.

Risk: Bridge commands can move the game character, send dialogue, and interact with NPCs on behalf of the user.

Mitigation: Review intended commands before execution, confirm the target player UID, and avoid running multiple control scripts against the same bridge.

## Reference(s):

- [clawScape ClawHub page](https://clawhub.ai/canyang335100/skills/clawscape)
- [Node.js](https://nodejs.org/)
- [clawSpace game](https://www.mxdl.online/index2.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command, JSON, JavaScript, and PowerShell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local HTTP and WebSocket commands for ports 18765 and 18766 plus notes about OpenClaw workspace memory files.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
