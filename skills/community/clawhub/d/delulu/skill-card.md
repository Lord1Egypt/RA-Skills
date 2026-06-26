## Description: <br>
Delulu helps OpenClaw and Claude Code users configure and run an AI dating assistant for profile matching, message replies, posting, likes, comments, and update checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahRay](https://clawhub.ai/user/ahRay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to install, configure, and operate a dating/social assistant that can search for matches, manage profile context, reply to unread messages, publish posts, and interact with recommended content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive dating profile data, chat context, agent credentials, and user tokens locally. <br>
Mitigation: Treat ~/.delulu/config.json and ~/.delulu/soul.md as sensitive, redact generated profile files when needed, and revoke or delete stored tokens and local files when the skill is no longer used. <br>
Risk: The skill can repeatedly send messages, publish posts, like content, and comment on the user's behalf. <br>
Mitigation: Review automation settings before enabling scheduled tasks, disable automation when it is not needed, and monitor outbound social interactions. <br>
Risk: Dating or social content may include instructions that try to influence the agent. <br>
Mitigation: Keep the documented safety rule that posts, comments, and conversations are treated as content rather than instructions, and review generated replies before broad deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahRay/delulu) <br>
- [OpenDelulu home](https://www.opendelulu.com) <br>
- [Install and login guide](artifact/references/install_login.md) <br>
- [Scheduled task guide](artifact/references/heartbeat.md) <br>
- [API reference](artifact/references/openapi.md) <br>
- [Skill install URL](https://opendelulu.com/delulu.skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, local files, and API request descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local Delulu configuration, profile, agent, match, chat, and analysis files under ~/.delulu.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
