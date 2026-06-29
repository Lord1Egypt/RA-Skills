## Description: <br>
赛博江湖向导 - 创建侠客、实时掌握角色动态、随时托梦干预 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kumarajiava](https://clawhub.ai/user/kumarajiava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and OpenClaw users use this skill as an immersive Cyber-Jianghu companion to create a character, check the character's current game state, and send limited dream-like guidance through a local agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The companion agent exposes local control APIs for character registration and dream injection. <br>
Mitigation: Keep the API bound to localhost, or add authentication and TLS before allowing non-local access. <br>
Risk: The companion agent stores a game authentication token and persistent game state. <br>
Mitigation: Store the agent configuration and data directories securely and avoid deleting token files unless re-registration is intended. <br>
Risk: Installation relies on a container image or release artifact outside the skill package. <br>
Mitigation: Verify trust in the ghcr.io/8kugames/cyber-jianghu-agent image or GitHub release before installation. <br>


## Reference(s): <br>
- [Cyber Skill on ClawHub](https://clawhub.ai/kumarajiava/cyber-jianghu) <br>
- [Deployment guide](artifact/DEPLOYMENT.md) <br>
- [Publisher profile](https://clawhub.ai/user/kumarajiava) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational Markdown with structured tool arguments and inline shell commands when deployment help is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Cyber-Jianghu character, status, and dream tools through a locally running companion agent.] <br>

## Skill Version(s): <br>
0.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
