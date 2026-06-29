## Description: <br>
Backup helps agents create, schedule, rotate, and restore OpenClaw backups for configuration, credentials, workspace data, sessions, and scheduled tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate full OpenClaw backup archives, configure daily backup schedules, rotate older archives, and restore a previous OpenClaw state when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may contain API keys, auth profiles, Telegram sessions, workspace memory, user files, and scheduled tasks. <br>
Mitigation: Store archives privately, preferably encrypted, and limit access to trusted users and systems. <br>
Risk: Restoring an archive can replace newer OpenClaw configuration or reintroduce old credentials and cron jobs. <br>
Mitigation: Verify the backup source and contents, and make a separate copy of the current ~/.openclaw directory before restore. <br>


## Reference(s): <br>
- [Restore OpenClaw from Backup](references/restore.md) <br>
- [ClawHub Backup Skill](https://clawhub.ai/paudyyin/backup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference compressed OpenClaw backup archives named openclaw-YYYY-MM-DD_HHMM.tar.gz.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
