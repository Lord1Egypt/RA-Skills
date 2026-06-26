## Description: <br>
Backs up and restores OpenClaw configuration files before upgrades, machine transfers, recovery, or maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexjunanjing-2](https://clawhub.ai/user/alexjunanjing-2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create timestamped backups of OpenClaw configuration, workspace, skills, memory, tokens, and local data, then restore those files when moving systems or recovering from failure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may contain sensitive OpenClaw data such as tokens, memory, skills, and user data. <br>
Mitigation: Store generated backups in a private location and consider encrypting archives before transferring or retaining them. <br>
Risk: The shell backup script automatically deletes OpenClaw backup archives older than 15 days. <br>
Mitigation: Review, change, or disable the cleanup behavior unless that retention period matches operational requirements. <br>
Risk: Restore operations overwrite current OpenClaw configuration after user confirmation. <br>
Mitigation: Inspect the archive contents and keep the generated .bak copies until the restored OpenClaw gateway is verified. <br>


## Reference(s): <br>
- [OpenClaw Configuration Locations](references/config-locations.md) <br>
- [ClawHub skill page](https://clawhub.ai/alexjunanjing-2/backup-openclaw-config) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and file path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included scripts can create .tar.gz backup archives and .info metadata files, and can restore archived configuration after confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
