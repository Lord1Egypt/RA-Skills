## Description: <br>
Adds and manages multiple Feishu bot accounts for OpenClaw, with account-level or group-chat routing to selected agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TwistedCz](https://clawhub.ai/user/TwistedCz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add Feishu bot accounts, bind them to agents, and choose account-level or group-chat routing without manually editing every configuration entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes OpenClaw Feishu bot configuration and restarts the gateway, which can affect message routing or short-term availability. <br>
Mitigation: Review the App ID, account ID, routing mode, agent binding, DM policy, and chat ID before execution; use the created configuration backup to restore if needed. <br>
Risk: Feishu app secrets are stored in local OpenClaw configuration and backup files. <br>
Mitigation: Protect ~/.openclaw/openclaw.json and ~/.openclaw/backups, limit access to those files, and avoid sharing logs or backups that may contain secrets. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with command examples and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local OpenClaw Feishu configuration, create backups, and restart the gateway when executed.] <br>

## Skill Version(s): <br>
0.0.1 (source: package.json and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
