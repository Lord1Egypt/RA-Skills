## Description: <br>
Claw2claw Filetransfer helps agents transfer, sync, and back up files across machines using rsync over SSH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Christopher-Schulze](https://clawhub.ai/user/Christopher-Schulze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to move files, collect logs, back up data, and synchronize project directories between OpenClaw agents on different machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy, overwrite, or delete files across machines during transfer and mirror-sync workflows. <br>
Mitigation: Review source and destination paths before execution, use dry-run mode before mirror syncs, and keep backups for important data. <br>
Risk: The skill sets up persistent SSH access and examples normalize direct root SSH use. <br>
Mitigation: Use a dedicated limited account, avoid direct root SSH, restrict key permissions, and verify where the claw2claw command comes from before use. <br>
Risk: Transfers may include sensitive logs, database dumps, backups, or home-directory data. <br>
Mitigation: Treat transferred data as sensitive, limit access to destinations, and avoid moving secrets or private data unless the target environment is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Christopher-Schulze/claw2claw-filetransfer-v2) <br>
- [Command Reference](references/commands.md) <br>
- [Real-World Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires rsync and SSH; includes setup, transfer, sync, status, and troubleshooting workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
