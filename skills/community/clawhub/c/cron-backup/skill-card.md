## Description: <br>
Set up scheduled automated backups with version tracking and cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfanmy](https://clawhub.ai/user/zfanmy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and technical users use this skill to create timestamped backups, configure cron schedules, trigger backups when version sources change, and clean up older backup archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install persistent cron jobs that continue running after setup. <br>
Mitigation: Inspect the generated crontab entry after setup and install only when local cron-based backup automation is intended. <br>
Risk: Command-string version sources and shell execution paths may run unintended commands if untrusted input is used. <br>
Mitigation: Use trusted absolute paths and avoid command-string version sources unless the command is fully reviewed. <br>
Risk: Cleanup operations may permanently delete old backup archives. <br>
Mitigation: Test cleanup against a dedicated backup directory and confirm retention settings before scheduling cleanup. <br>


## Reference(s): <br>
- [Cron Backup ClawHub Skill Page](https://clawhub.ai/zfanmy/cron-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose cron entries and local filesystem backup, cleanup, and listing commands.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
