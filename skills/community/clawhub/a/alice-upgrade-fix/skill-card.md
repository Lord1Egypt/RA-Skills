## Description: <br>
Helps agents guide OpenClaw 2026.4.x upgrades, configuration backups, post-upgrade checks, permission repair, plugin cleanup, and rollback steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoyoyosan](https://clawhub.ai/user/yoyoyosan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw installations use this skill to upgrade OpenClaw, preserve key local configuration files, check gateway health, repair common post-upgrade issues, and recover from backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The post-upgrade fix can broaden the local OpenClaw tool permission profile to full access. <br>
Mitigation: Review the permission change before running the fix, inspect configuration diffs afterward, and only keep full access if it matches the user's intended security posture. <br>
Risk: Cleanup commands may remove OpenClaw plugin runtime directories. <br>
Mitigation: Preview deletion targets first and keep a fresh backup before running cleanup or post-upgrade repair commands. <br>
Risk: Upgrade and repair scripts modify local OpenClaw configuration and restart the gateway. <br>
Mitigation: Run the scripts in a maintenance window, confirm backups exist, and validate gateway health after the restart. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yoyoyosan/alice-upgrade-fix) <br>
- [Publisher profile](https://clawhub.ai/user/yoyoyosan) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run bundled maintenance scripts that modify local OpenClaw configuration and plugin directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
