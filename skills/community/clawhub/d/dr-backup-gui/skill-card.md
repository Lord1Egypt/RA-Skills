## Description: <br>
Dr Backup Gui is a disaster-recovery backup and migration GUI for configuring and running Velero, rclone, rsync, and Coriolis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenzhouzhao](https://clawhub.ai/user/chenzhouzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform operators, and system administrators use this skill to launch a local GUI for Kubernetes backup and restore, cloud storage synchronization, file synchronization, and cross-cloud VM migration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup, sync, restore, and migration commands can delete, overwrite, move, or modify real data and infrastructure resources. <br>
Mitigation: Install and run on a controlled admin workstation or virtual environment, review source, destination, SSH target, endpoint, and delete settings, and use dry-run or non-production testing before production use. <br>
Risk: Saved profiles and logs may contain sensitive connection details or operational context. <br>
Mitigation: Restrict permissions on ~/.dr_backup_gui and avoid committing profiles, logs, or saved connection data to shared repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenzhouzhao/dr-backup-gui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and GUI-generated command and log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local profiles, job records, and activity logs under ~/.dr_backup_gui.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
