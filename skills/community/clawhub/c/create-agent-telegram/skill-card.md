## Description: <br>
Creates a new OpenClaw agent and binds it to a Telegram bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangzhiyu](https://clawhub.ai/user/liangzhiyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create an OpenClaw agent workspace, configure a Telegram bot account, bind the bot to the agent, and verify gateway status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify an OpenClaw team workspace and configuration. <br>
Mitigation: Review the generated configuration changes before applying them and keep a backup of openclaw.json. <br>
Risk: Telegram bot tokens are secrets and may grant access to the configured bot. <br>
Mitigation: Store bot tokens securely, avoid sharing them in logs or chat, and rotate tokens if they are exposed. <br>
Risk: Gateway restarts or related activation steps may interrupt active service. <br>
Mitigation: Schedule restarts and activation steps during an acceptable maintenance window. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes placeholder values for bot name, bot token, and agent ID; users should review commands before applying them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
