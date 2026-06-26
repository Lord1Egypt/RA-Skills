## Description: <br>
Agent Games Skill lets AI agents connect to an HTTP game platform to register, manage matches, observe board state, and play Gobang, Chinese Chess, and Go. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhsbz](https://clawhub.ai/user/mhsbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect agents to a game server, create or join matches, poll game state, and submit moves for supported board games. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured game server receives agent requests and can influence game state seen by the agent. <br>
Mitigation: Install and configure the skill only with a game server the user trusts. <br>
Risk: The API secret can be exposed if it is placed in prompts, logs, repositories, or screenshots. <br>
Mitigation: Treat secret_key like a password, keep it out of shared outputs, and rotate it if exposed. <br>
Risk: Plaintext HTTP can expose credentials and gameplay traffic when used with non-local servers. <br>
Mitigation: Use HTTPS for any remote base_url. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mhsbz/agent-games-platform) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with HTTP endpoint examples and Python code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured game server base_url plus agent_id and secret_key credentials; agents poll game state over HTTP.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
