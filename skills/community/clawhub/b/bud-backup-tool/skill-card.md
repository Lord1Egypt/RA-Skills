## Description: <br>
Backs up and restores OpenClaw configuration, skills, memory, credentials, and workspace files for recovery or migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stigg86](https://clawhub.ai/user/stigg86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create local backup archives, inspect backup status, restore an OpenClaw setup, and optionally push backups to private off-site storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles credentials and may push backup archives to a hardcoded GitHub repository. <br>
Mitigation: Inspect and change the GitHub destination before use; do not push credential-containing archives unless they are encrypted and stored in a private repository you control. <br>
Risk: Restore operations can overwrite current OpenClaw configuration and credentials. <br>
Mitigation: Test restores on a disposable OpenClaw profile first and confirm the intended backup archive before restoring to an active setup. <br>


## Reference(s): <br>
- [Bud Backup Tool on ClawHub](https://clawhub.ai/stigg86/bud-backup-tool) <br>
- [Project homepage](https://github.com/stigg86/backup-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Python CLI invocation patterns.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local tar.gz backup archives and may invoke git for optional remote backup workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
