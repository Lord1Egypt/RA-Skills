## Description: <br>
Automates restic backups for configured local paths and named Docker volumes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can initialize a restic repository and run incremental backups for local application paths and Docker volumes. Review the configured paths and volume names before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup script targets hardcoded local paths and Docker volumes that may contain private data. <br>
Mitigation: Review and edit the backup paths and Docker volume names before running backups, and run it only in environments where the selected data is intended to be backed up. <br>
Risk: The artifact has empty user-facing documentation and creates a restic key file in the repository path. <br>
Mitigation: Confirm the restic repository location, key-file storage, file permissions, and recovery process before use. <br>


## Reference(s): <br>
- [Auto Backup Manager on ClawHub](https://clawhub.ai/kingaiwork/auto-backup-manager) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON status output from a Python CLI, with operational behavior driven by restic, Docker, and local path configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires restic, Docker access for volume backups, and explicit review of local backup paths before execution.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
