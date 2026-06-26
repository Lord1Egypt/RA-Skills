## Description: <br>
Smart backup rotation and retention manager. Create backups, enforce flexible retention policies (grandfather-father-son), verify integrity, and clean up old backups automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and administrators use this skill to create timestamped backups, configure retention policies, rotate old backup files, run checksum checks, and schedule automated backup jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup rotation can delete files that match the selected backup directory, prefix, and retention policy. <br>
Mitigation: Run --dry-run and --list before real rotation, keep backups in a dedicated directory, and choose a narrow --name prefix. <br>
Risk: Checksum output confirms file bytes can be read, but it is not proof that a backup is restorable. <br>
Mitigation: Pair SHA256 verification with periodic restore tests for important backup sets. <br>
Risk: Cron mode can repeatedly create, rotate, and verify backups without interactive review. <br>
Mitigation: Review the JSON config, log cron output, and validate retention counts before enabling automated runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlooi504/backup-rotator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local filesystem paths and retention counts supplied by the user; no external API calls are described.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
