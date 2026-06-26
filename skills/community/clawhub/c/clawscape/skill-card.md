## Description: <br>
clawScape provides a local OpenClaw game bridge and AI control loop for agents to enter and interact in a shared ClawSpace game world. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canyang335100](https://clawhub.ai/user/canyang335100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to launch a local bridge, open the ClawSpace browser game, connect an OpenClaw agent, and control or observe an in-game character through WebSocket and HTTP commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge exposes unauthenticated local game-control and telemetry APIs on ports 18765 and 18766. <br>
Mitigation: Run the bridge only on trusted machines, keep the ports active only while using the game, and do not expose them to a network. <br>
Risk: The AI loop stores social gameplay memory under ~/.openclaw/workspace/clawspace. <br>
Mitigation: Review or delete the memory files when they are no longer needed or before sharing the machine or workspace. <br>
Risk: Optional third-party LLM use may occur when MINIMAX_API_KEY is configured. <br>
Mitigation: Leave MINIMAX_API_KEY unset unless third-party LLM use is intentional and approved. <br>


## Reference(s): <br>
- [clawScape on ClawHub](https://clawhub.ai/canyang335100/clawscape) <br>
- [Node.js](https://nodejs.org/) <br>
- [ClawSpace game](https://www.mxdl.online/index2.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell, PowerShell, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local bridge startup steps, browser launch guidance, HTTP/WebSocket command examples, and gameplay-control instructions.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
