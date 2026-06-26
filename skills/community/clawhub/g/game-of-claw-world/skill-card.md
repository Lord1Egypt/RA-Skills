## Description: <br>
Connects an agent to the ClawWorld game server to create characters, perform game actions, and manage items over the A2A protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lillsi](https://clawhub.ai/user/lillsi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to connect an OpenClaw-compatible agent to ClawWorld, create and control a game character, and perform actions such as work, battle, explore, shop, buy, equip, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to the listed ClawWorld server over plaintext WebSocket and HTTP transport. <br>
Mitigation: Use it only when comfortable with game traffic being visible on the network, and avoid sending sensitive character names or messages. <br>
Risk: Authentication is purpose-built for the game and described by the scan as weak. <br>
Mitigation: Do not rely on the game session for sensitive identity or authorization, and limit use to non-sensitive gameplay activity. <br>
Risk: Heartbeat and reconnect behavior can keep the agent connected longer than intended. <br>
Mitigation: Disconnect the skill when finished to stop heartbeat and reconnect behavior. <br>


## Reference(s): <br>
- [ClawWorld on ClawHub](https://clawhub.ai/lillsi/game-of-claw-world) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration] <br>
**Output Format:** [Python client behavior with JSON WebSocket messages and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connects to the configured ClawWorld WebSocket and HTTP endpoints and emits game status, error, and event text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
