## Description: <br>
Quick diagnosis and repair for Discord bot, Gateway, OAuth token, and legacy config issues. Checks connectivity, token expiration, and cleans up old Clawdis artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhillock](https://clawhub.ai/user/jhillock) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who maintain Clawdbot or Discord integrations use this skill to diagnose Gateway availability, Discord connection, OAuth token, npm dependency, and legacy Clawdis configuration problems and to get repair commands or guided fix steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The `discord-doctor` command implementation is not included in the artifact, so fix behavior depends on an external command. <br>
Mitigation: Verify and trust the installed command source before running it, and start with diagnostic mode before using `--fix`. <br>
Risk: Fix mode can make persistent local changes such as installing npm packages, restarting the gateway, removing launchd services, and moving legacy config directories. <br>
Mitigation: Back up relevant configuration and approve each package install, daemon restart, launchd change, and config migration deliberately. <br>
Risk: OAuth-related repair steps can affect local authentication state. <br>
Mitigation: Follow re-authentication steps intentionally and avoid unattended OAuth-related fixes. <br>


## Reference(s): <br>
- [Discord Doctor ClawHub release page](https://clawhub.ai/jhillock/discord-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local diagnostic and repair actions; fix mode can modify gateway state, install npm packages, remove launchd services, and back up legacy configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
