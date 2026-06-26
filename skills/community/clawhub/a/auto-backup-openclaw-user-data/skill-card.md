## Description: <br>
Backs up OpenClaw user data with full or selective backup targets, scheduled execution, ZIP compression, logging, notifications, and retention cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjj345](https://clawhub.ai/user/hjj345) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to configure and run local backups of OpenClaw workspaces and memory, including scheduled backups, status checks, retention cleanup, and notification reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can receive broad local access to OpenClaw workspaces and memory. <br>
Mitigation: Configure partial backup targets before enabling automation and use a private backup directory. <br>
Risk: Backup archives can include sensitive local data such as keys, credentials, environment files, or memory content. <br>
Mitigation: Turn on sensitive-file exclusions, review selected targets, and confirm backup contents before relying on scheduled runs. <br>
Risk: External notifications and schedule templates can expose backup metadata or operational details. <br>
Mitigation: Review the HEARTBEAT and cron templates, disable notifications when not required, and restrict notification channels and recipients. <br>
Risk: ZIP encryption may not protect backups if the password is stored only in the skill's plaintext config file. <br>
Mitigation: Do not rely on ZIP encryption alone; protect the backup directory and manage encryption secrets outside plaintext skill configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hjj345/auto-backup-openclaw-user-data) <br>
- [README](README.md) <br>
- [Configuration schema](references/config-schema.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [HEARTBEAT prompt example](HEARTBEAT_prompt_example.md) <br>
- [Cron prompt example](cron_prompt_example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance and JSON-like command results with backup file paths, status details, logs, and notification content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create ZIP backup archives, local logs, retained backup lists, and external notification messages when configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
