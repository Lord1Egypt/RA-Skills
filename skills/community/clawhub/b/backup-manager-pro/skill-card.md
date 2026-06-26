## Description: <br>
Manages local OpenClaw backups, retention cleanup, pre-change snapshots, and restore guidance for configuration and workspace files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reaperchen](https://clawhub.ai/user/reaperchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create scheduled and manual backups, preserve state before configuration changes, clean expired backup data, and restore from trusted local backup archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may contain sensitive OpenClaw data such as API keys, auth profiles, agent memory, identity files, skills, and extensions. <br>
Mitigation: Protect or encrypt the backup directory, restrict filesystem permissions, and restore only from backup archives you trust. <br>
Risk: Scheduled backup setup can modify the user's crontab and setup-cron-auto.sh installs jobs without an interactive confirmation step. <br>
Mitigation: Prefer the interactive cron setup, review the exact cron entries before installation, and keep a copy of the prior crontab so jobs can be removed or rolled back. <br>
Risk: Restore operations can overwrite current OpenClaw configuration and workspace files. <br>
Mitigation: Use the restore script's confirmation flow, keep the pre-restore safety backup, and verify restored files before restarting OpenClaw. <br>
Risk: Cleanup scripts delete expired backup directories and archives according to retention rules. <br>
Mitigation: Review retention settings before enabling scheduled cleanup and keep critical backups outside automated cleanup paths when long-term retention is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/reaperchen/backup-manager-pro) <br>
- [Backup Strategies](backup-strategies.md) <br>
- [Backup Scripts Reference](backup-scripts.md) <br>
- [Recovery Guide](recovery-guide.md) <br>
- [Memory Template](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command examples and Bash scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local backup and restore procedures for OpenClaw; scripts write tar.gz archives, log files, symlinks, and optional cron entries.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
