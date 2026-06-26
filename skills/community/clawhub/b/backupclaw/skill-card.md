## Description: <br>
Backup Claw helps agents back up and restore OpenClaw configuration files, excluding the workspace directory, with date-stamped backups, change detection, changelog logging, and restore-by-date support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyingtimes](https://clawhub.ai/user/flyingtimes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preserve local OpenClaw configuration, detect changes before creating a new backup, and restore a known backup date after configuration loss or unwanted changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill copies OpenClaw configuration files that may contain sensitive local settings or credentials. <br>
Mitigation: Use a private backup directory with appropriate filesystem permissions and avoid shared or synced destinations unless they are trusted. <br>
Risk: Restoring a backup can overwrite current OpenClaw configuration. <br>
Mitigation: Confirm restores only from backup dates the user recognizes, and preserve the workspace exclusion behavior during restore. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyingtimes/backupclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, file paths, and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create date-stamped local backup directories, update ~/.openclaw/backup.json, and append changelog.md when the backup or restore workflow is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
