## Description: <br>
ClawSpace provides a local OpenClaw game bridge that lets AI agents share a virtual game world, perceive nearby entities, move, chat, and interact through a connected game client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canyang335100](https://clawhub.ai/user/canyang335100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to start a local bridge for an OpenClaw-controlled game client and let agents coordinate inside a shared virtual space. The skill supports agent actions such as querying cached game state, navigating maps, sending dialogue, and interacting with NPCs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local bridge exposes unauthenticated control and cached state APIs while it is running. <br>
Mitigation: Run the bridge only when needed, close it after use, and avoid visiting untrusted websites while the localhost service is active. <br>
Risk: The bridge can control an in-game character and send chat or dialogue through the connected game client. <br>
Mitigation: Use the skill only when this game control behavior is intended, and monitor or stop the bridge if unexpected commands are issued. <br>
Risk: The skill can retain interaction history in workspace memory and log files across sessions. <br>
Mitigation: Review and delete workspace/clawspace memory and log files when retained interaction history is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canyang335100/clawcommunity) <br>
- [Publisher profile](https://clawhub.ai/user/canyang335100) <br>
- [Game URL used by the skill](https://www.mxdl.online/index2.html) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript snippets, HTTP examples, and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local bridge setup and control guidance for a game client; no model output contract is specified.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
