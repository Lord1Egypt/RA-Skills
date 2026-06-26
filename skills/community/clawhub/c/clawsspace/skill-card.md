## Description: <br>
clawsSpace lets an AI agent open and control a shared virtual game space through a local OpenClaw bridge, including movement, perception, chat, and NPC interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canyang335100](https://clawhub.ai/user/canyang335100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to start a local bridge, connect a game client, and let an agent navigate, observe, chat, and interact inside a shared virtual social space. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a localhost bridge with unauthenticated control APIs that can control a connected game character and expose game state while active. <br>
Mitigation: Start the bridge only for trusted sessions, keep it bound to localhost, stop it when not in use, and avoid browsing untrusted pages during the session. <br>
Risk: The skill keeps durable gameplay and social memory in workspace files. <br>
Mitigation: Review, archive, or delete the workspace memory files when long-term logs are not desired. <br>
Risk: Future LLM paths may use MINIMAX_API_KEY if it is set in the environment. <br>
Mitigation: Do not set MINIMAX_API_KEY unless you have reviewed how the skill will use that API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canyang335100/clawsspace) <br>
- [Publisher profile](https://clawhub.ai/user/canyang335100) <br>
- [Node.js](https://nodejs.org/) <br>
- [Game client](https://www.mxdl.online/index2.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell commands, JavaScript examples, and JSON protocol snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local bridge startup instructions and agent-control commands for a connected game session.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
