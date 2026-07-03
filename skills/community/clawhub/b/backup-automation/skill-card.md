## Description: <br>
Automated backup for OpenClaw instances. Backs up agents, skills, cron jobs, and memory. Supports local tar archives. Credentials, periodic scheduling, and git sync are OPT-IN only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzargona](https://clawhub.ai/user/jzargona) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to create, list, restore, and check local backups of agents, skills, cron configuration, memory, and core OpenClaw configuration. It is intended for local disaster recovery workflows, with credential backup, scheduled backup, and git sync enabled only when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore can overwrite files under the user's home directory. <br>
Mitigation: Inspect the selected archive first and restore only after confirming the backup is correct and overwrites are acceptable. <br>
Risk: Optional git sync can push workspace contents to a remote repository. <br>
Mitigation: Keep git sync disabled unless the repository, branch, and contents to be pushed have been reviewed. <br>
Risk: Optional credential backup can include tokens or API keys. <br>
Mitigation: Leave credential backup disabled unless secrets must be backed up, and restrict access to generated archives. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jzargona/skills/backup-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and local tar archive files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local backup archives under ~/backups; credential backup, periodic scheduling, and git sync are opt-in.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
