## Description: <br>
Backs up an OpenClaw system, including configuration, memory, selected user files, and system metadata, then uploads the archive to a configured cloud remote. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jaskies](https://clawhub.ai/user/Jaskies) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw environments use this skill to configure and run full-system backups to cloud storage. It is appropriate only where broad local and system data collection and upload are explicitly authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup can collect sensitive local, user, and system data and upload it to the configured Google Drive remote. <br>
Mitigation: Review and narrow the backup paths, add secret exclusions, encrypt the archive, and confirm the rclone destination before running. <br>
Risk: Recurring execution can repeatedly export broad system snapshots without additional review. <br>
Mitigation: Avoid cron scheduling unless recurring uploads are intentionally required and monitored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jaskies/backup-full-system-jaskies) <br>
- [Publisher profile](https://clawhub.ai/user/Jaskies) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands and a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, creates compressed tar.gz backup archives and uploads them with rclone.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
