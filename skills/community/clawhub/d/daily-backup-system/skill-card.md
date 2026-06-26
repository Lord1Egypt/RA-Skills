## Description: <br>
Automates daily compressed backups of OpenClaw configuration, workspaces, environment files, scripts, and related data with seven-day rotation and restore guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Harvnk](https://clawhub.ai/user/Harvnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan recurring OpenClaw backups, retain recent archives, and recover an environment after a server or workspace failure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring full backups may include API keys, private agent memory, environment files, and other sensitive operational data. <br>
Mitigation: Store backups only in a private location, encrypt archives, restrict file permissions, and rotate credentials if a backup is exposed. <br>
Risk: The release describes a daily_backup.sh workflow, but the script is not included in the artifact for review. <br>
Mitigation: Obtain and review the actual backup script before scheduling it, document how to disable the cron job, and test restore steps in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Harvnk/daily-backup-system) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes backup setup, cron scheduling, rotation, and restore instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
