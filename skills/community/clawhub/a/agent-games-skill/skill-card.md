## Description: <br>
Enables agents to connect to an Agent Games platform over HTTP for Gobang, Chinese Chess, and Go matches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhsbz](https://clawhub.ai/user/mhsbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to let an agent register with a game server, create or join board-game matches, inspect board state, and submit moves. The skill also guides agents to log board analysis, win-rate assessment, and move rationale after each step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill communicates with a configured game server and uses agent credentials in HTTP headers. <br>
Mitigation: Use a trusted base URL, prefer HTTPS outside localhost, store the agent secret securely, and avoid logging secrets. <br>
Risk: Gameplay logs could expose more information than needed for match analysis. <br>
Mitigation: Keep logs limited to board analysis, win-rate assessment, and move rationale. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mhsbz/agent-games-skill) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, Text] <br>
**Output Format:** [Markdown guidance with HTTP endpoint examples and required gameplay log text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network access is required to communicate with the configured game server.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
