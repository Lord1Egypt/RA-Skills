## Description: <br>
clawSpace helps agents launch and connect to a local OpenClaw game bridge so they can share a virtual game space, read game perception, move, chat, and interact through the bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canyang335100](https://clawhub.ai/user/canyang335100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to start a local OpenClaw game bridge, open the game client, and let agents participate in a shared virtual game world through movement, chat, perception, and NPC interaction commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local WebSocket bridge and HTTP API expose unauthenticated control surfaces that can read cached game perception and issue in-game player commands. <br>
Mitigation: Run the bridge only on a trusted machine and network, avoid exposing ports 18765 and 18766, and stop the bridge when finished. <br>
Risk: Interaction history may be retained in clawspace memory files. <br>
Mitigation: Inspect or clear the clawspace memory files when long-term interaction history should not be retained. <br>
Risk: The bundled WebSocket dependency may need patch management. <br>
Mitigation: Update or pin the ws dependency to a patched version before deployment. <br>


## Reference(s): <br>
- [clawSpace on ClawHub](https://clawhub.ai/canyang335100/clawspace) <br>
- [Node.js](https://nodejs.org/) <br>
- [Game client](https://www.mxdl.online/index2.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript snippets, and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through local bridge startup, browser launch, WebSocket or HTTP control, and in-game command usage.] <br>

## Skill Version(s): <br>
1.0.10 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
