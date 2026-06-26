## Description: <br>
Auto Backup Pro helps an agent plan and operate scheduled backups for important files, including incremental backup, compression, encryption options, verification reports, and retry guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbo405](https://clawhub.ai/user/linbo405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to configure scheduled backup routines, review backup status, and restore previous backups for important work directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup and restore actions may copy, retain, or overwrite user data without enough visibility into scope or retention. <br>
Mitigation: Confirm source folders, destination, cloud use, retention count, and restore behavior before use; require explicit confirmation before restores and preserve newer files. <br>
Risk: Encrypted backup claims create key-management risk if keys are not handled clearly. <br>
Mitigation: Confirm how encryption keys are generated, stored, rotated, and recovered before enabling encrypted backups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linbo405/auto-backup-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and configuration snippets, with shell commands when needed for backup or restore operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include backup status, storage usage, backup history, verification results, and restore guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
